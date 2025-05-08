from pathlib import Path

import click
from pyioc3 import Container
from pyioc3.autowire import AutoWireContainerBuilder

from dfadapter.host_configuration import LocalHostConfigurationOpts
from dflib.service.config_set_service import ConfigSetService

from .decorators import catch_dferror
from .variant import Variant


@click.group()
@click.option(
    "--rcfile",
    type=Path,
    default=Path("~/.config/dfctl/dfctlrc"),
    show_default="~/.config/dfctl/dfctlrc",
    help="Optional path to the dfctlrc file.",
)
@click.option(
    "--set",
    type=Variant,
    default=[],
    multiple=True,
    help='Optional configuration override. Example: "MySection:MyKey=MyValue"',
)
@click.pass_context
def dfctl(ctx: click.Context, rcfile: Path, set: list[Variant]) -> None:
    """Yet another dotfiles management tool."""

    mods = [
        "dfadapter",
        "dflib",
    ]

    opts = LocalHostConfigurationOpts(rcfile=rcfile, overrides=[o.as_override() for o in set])

    _ = ctx.ensure_object(dict)
    ctx.obj["container"] = (
        AutoWireContainerBuilder(mods).bind_constant(LocalHostConfigurationOpts, opts).build()
    )


@dfctl.group("config-set")
@click.pass_context
def config_set(ctx: click.Context) -> None:
    container: Container = ctx.obj["container"]
    ctx.obj["srv"] = container.get(ConfigSetService)


@config_set.command("create")
@click.argument("config_set_name")
@click.pass_context
@catch_dferror
def config_set_create(ctx: click.Context, config_set_name: str) -> None:
    """Create a new configuration set."""
    srv: ConfigSetService = ctx.obj["srv"]
    srv.create(config_set_name)


@config_set.command("add-file")
@click.argument("config_set_name")
@click.argument("file", type=Path)
@click.pass_context
@catch_dferror
def config_set_add_file(ctx: click.Context, config_set_name: str, file: Path) -> None:
    """Create a new configuration set."""
    srv: ConfigSetService = ctx.obj["srv"]
    _ = srv.add_files(config_set_name, {str(file): file.read_bytes()})


if __name__ == "__main__":
    dfctl()
