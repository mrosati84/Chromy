from __future__ import annotations

from argparse import Namespace
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Generic, TypeVar, assert_never

from chromadb.errors import InternalError, NotFoundError

from chromy.command_inputs import (
    AddDataInput,
    CommandInput,
    CountCollectionInput,
    CreateCollectionInput,
    DeleteCollectionInput,
    DeleteRecordsInput,
    ListCollectionsInput,
    QueryInput,
)
from chromy.handlers.add_data import handle_add_data
from chromy.handlers.count_collection import handle_count_collection
from chromy.handlers.create_collection import handle_create_collection
from chromy.handlers.delete_collection import (
    handle_delete_collection,
    handle_delete_records,
)
from chromy.handlers.list_collections import handle_list_collections
from chromy.handlers.query import handle_query

CommandT = TypeVar("CommandT", bound=CommandInput)
CollectionCommandT = TypeVar(
    "CollectionCommandT",
    DeleteCollectionInput,
    CountCollectionInput,
    AddDataInput,
    QueryInput,
    DeleteRecordsInput,
)
CommandHandler = Callable[[CommandT], int]
ErrorMessageBuilder = Callable[[CommandT, Exception], str]


@dataclass(frozen=True, slots=True)
class CliErrorHandler(Generic[CommandT]):
    exception_type: type[Exception]
    message: ErrorMessageBuilder[CommandT]


def build_command_input(args: Namespace) -> CommandInput:
    command = str(args.command)

    match command:
        case "list-collections":
            return ListCollectionsInput()
        case "create-collection":
            return CreateCollectionInput(collection=str(args.collection))
        case "delete-collection":
            return DeleteCollectionInput(collection=str(args.collection))
        case "count":
            return CountCollectionInput(collection=str(args.collection))
        case "add-data":
            return AddDataInput(collection=str(args.collection), file=str(args.file))
        case "query":
            return QueryInput(
                collection=str(args.collection),
                query_text=str(args.query_text),
            )
        case "delete":
            return DeleteRecordsInput(
                collection=str(args.collection),
                where=str(args.where),
            )
        case _:
            raise ValueError(f"Unknown command: {command}")


def execute_command(args: Namespace) -> int:
    command_input = build_command_input(args)

    match command_input:
        case ListCollectionsInput():
            return _run_command(command_input, handle_list_collections)
        case CreateCollectionInput():
            return _run_command(
                command_input,
                handle_create_collection,
                (
                    CliErrorHandler(
                        exception_type=InternalError,
                        message=_collection_already_exists_message,
                    ),
                ),
            )
        case DeleteCollectionInput():
            return _run_command(
                command_input,
                handle_delete_collection,
                (_collection_not_found_handler(DeleteCollectionInput),),
            )
        case CountCollectionInput():
            return _run_command(
                command_input,
                handle_count_collection,
                (_collection_not_found_handler(CountCollectionInput),),
            )
        case AddDataInput():
            return _run_command(
                command_input,
                handle_add_data,
                (
                    _collection_not_found_handler(AddDataInput),
                    CliErrorHandler(
                        exception_type=FileNotFoundError,
                        message=_file_not_found_message,
                    ),
                ),
            )
        case QueryInput():
            return _run_command(
                command_input,
                handle_query,
                (_collection_not_found_handler(QueryInput),),
            )
        case DeleteRecordsInput():
            return _run_command(
                command_input,
                handle_delete_records,
                (
                    _collection_not_found_handler(DeleteRecordsInput),
                    CliErrorHandler(
                        exception_type=ValueError,
                        message=_exception_message,
                    ),
                ),
            )

    assert_never(command_input)


def _run_command(
    command_input: CommandT,
    handler: CommandHandler[CommandT],
    error_handlers: Sequence[CliErrorHandler[CommandT]] = (),
) -> int:
    try:
        return handler(command_input)
    except Exception as exc:
        for error_handler in error_handlers:
            if isinstance(exc, error_handler.exception_type):
                print(error_handler.message(command_input, exc))
                return 1
        raise


def _collection_already_exists_message(
    command: CreateCollectionInput,
    _: Exception,
) -> str:
    return f"Collection '{command.collection}' already exists."


def _collection_not_found_handler(
    _: type[CollectionCommandT],
) -> CliErrorHandler[CollectionCommandT]:
    return CliErrorHandler(
        exception_type=NotFoundError,
        message=_collection_not_found_message,
    )


def _collection_not_found_message(command: CollectionCommandT, _: Exception) -> str:
    return f"Collection '{command.collection}' does not exist."


def _file_not_found_message(command: AddDataInput, _: Exception) -> str:
    return f"The file {command.file} was not found."


def _exception_message(_: DeleteRecordsInput, exc: Exception) -> str:
    return str(exc)
