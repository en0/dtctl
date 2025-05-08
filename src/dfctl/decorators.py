from functools import wraps
from typing import Any, Callable

import click

from dflib.error import DFError


def catch_dferror(func: Callable[..., Any | None]) -> Callable[..., Any | None]:

    @wraps(func)
    def wrapper(*args: list[Any], **kwargs: dict[str, Any]) -> Any | None:
        try:
            return func(*args, **kwargs)
        except DFError as ex:
            click.echo(ex)
            return None

    return wrapper
