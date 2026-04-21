from __future__ import annotations

from argparse import Namespace
from collections.abc import Callable
from dataclasses import dataclass

from chromadb.errors import InternalError, NotFoundError

from handlers.add_data import handle_add_data
from handlers.count_collection import handle_count_collection
from handlers.create_collection import handle_create_collection
from handlers.delete_collection import (
    handle_delete_collection,
    handle_delete_records,
)
from handlers.list_collections import handle_list_collections
from handlers.query import handle_query


CommandHandler = Callable[[Namespace], int]
ErrorMessageBuilder = Callable[[Namespace], str]


@dataclass(frozen=True, slots=True)
class CliErrorHandler:
    exception_type: type[BaseException]
    message: ErrorMessageBuilder


@dataclass(frozen=True, slots=True)
class CommandConfig:
    handler: CommandHandler
    error_handlers: tuple[CliErrorHandler, ...] = ()


COMMANDS: dict[str, CommandConfig] = {
    "list-collections": CommandConfig(handler=handle_list_collections),
    "create-collection": CommandConfig(
        handler=handle_create_collection,
        error_handlers=(
            CliErrorHandler(
                exception_type=InternalError,
                message=lambda args: f"Collection '{args.collection}' already exists.",
            ),
        ),
    ),
    "delete-collection": CommandConfig(
        handler=handle_delete_collection,
        error_handlers=(
            CliErrorHandler(
                exception_type=NotFoundError,
                message=lambda args: f"Collection '{args.collection}' does not exist.",
            ),
        ),
    ),
    "count": CommandConfig(
        handler=handle_count_collection,
        error_handlers=(
            CliErrorHandler(
                exception_type=NotFoundError,
                message=lambda args: f"Collection '{args.collection}' does not exist.",
            ),
        ),
    ),
    "add-data": CommandConfig(
        handler=handle_add_data,
        error_handlers=(
            CliErrorHandler(
                exception_type=NotFoundError,
                message=lambda args: f"Collection '{args.collection}' does not exist.",
            ),
            CliErrorHandler(
                exception_type=FileNotFoundError,
                message=lambda args: f"The file {args.file} was not found.",
            ),
        ),
    ),
    "query": CommandConfig(
        handler=handle_query,
        error_handlers=(
            CliErrorHandler(
                exception_type=NotFoundError,
                message=lambda args: f"Collection '{args.collection}' does not exist.",
            ),
        ),
    ),
    "delete": CommandConfig(
        handler=handle_delete_records,
        error_handlers=(
            CliErrorHandler(
                exception_type=NotFoundError,
                message=lambda args: f"Collection '{args.collection}' does not exist.",
            ),
            CliErrorHandler(
                exception_type=ValueError,
                message=lambda args: str(args.error_message),
            ),
        ),
    ),
}


def execute_command(args: Namespace) -> int:
    command = COMMANDS[args.command]
    args.error_message = "An unexpected value was provided."

    try:
        return command.handler(args)
    except BaseException as exc:
        for error_handler in command.error_handlers:
            if isinstance(exc, error_handler.exception_type):
                print(error_handler.message(args))
                return 1
        raise
