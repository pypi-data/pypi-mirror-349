import argparse
import traceback
from pathlib import Path
from rbt.v1alpha1.admin import export_import_pb2_grpc
from reboot.admin import export_import_client
from reboot.aio.external import ExternalContext
from reboot.cli import terminal
from reboot.cli.rc import ArgumentParser, add_common_channel_args


def register_export_and_import(parser: ArgumentParser):

    def _add_common_args(subcommand):
        add_common_channel_args(subcommand)

        # Should be able to use 'rbt task' with 'rbt dev run' without an admin
        # secret.
        subcommand.add_argument(
            '--admin-bearer-token',
            type=str,
            help=(
                "the admin secret to use for authentication; defaults to the "
                "appropriate value for `dev`, but must be set explicitly in "
                "production"
            ),
            default='dev',  # Could be anything.
        )

    _add_common_args(parser.subcommand('export'))
    parser.subcommand('export').add_argument(
        '--directory',
        type=str,
        help="a directory to export data to, as JSON-lines files",
        required=True,
    )

    _add_common_args(parser.subcommand('import'))
    parser.subcommand('import').add_argument(
        '--directory',
        type=str,
        help="a directory to import data from, as JSON-lines files",
        required=True,
    )


def _export_import_stub(
    args: argparse.Namespace
) -> export_import_pb2_grpc.ExportImportStub:
    context = ExternalContext(
        name="reboot-cli",
        bearer_token=args.admin_bearer_token,
        url=args.application_url,
    )
    return export_import_pb2_grpc.ExportImportStub(
        context.legacy_grpc_channel()
    )


async def do_export(args: argparse.Namespace) -> int:
    """Implementation of the 'export' subcommand."""

    dest_dir = Path(args.directory)
    if dest_dir.is_dir() and any(dest_dir.iterdir()):
        terminal.fail(f"Destination directory `{dest_dir}` must be empty.\n\n")

    export_import = _export_import_stub(args)
    try:
        await export_import_client.do_export(
            export_import, dest_dir, admin_token=args.admin_bearer_token
        )
    except Exception as e:
        terminal.fail(
            f"Failed to export: {e}\n\nPlease report this issue to the maintainers."
        )

    terminal.info(f"Exported to: `{dest_dir}`")
    return 0


async def do_import(args: argparse.Namespace) -> int:
    """Implementation of the 'import' subcommand."""

    src_dir = Path(args.directory)
    if not src_dir.is_dir() or not any(src_dir.iterdir()):
        terminal.fail(f"Source directory `{src_dir}` must be non-empty.\n\n")

    export_import = _export_import_stub(args)
    try:
        await export_import_client.do_import(
            export_import, src_dir, admin_token=args.admin_bearer_token
        )
    except BaseException as e:
        traceback.print_exc()
        terminal.fail(
            f"Failed to import: {type(e)}: {e}\n\nPlease report this issue to the maintainers."
        )

    terminal.info(f"Imported from: `{src_dir}`")
    return 0
