from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ArgumentSpec:
    name: str
    help: str


@dataclass(frozen=True, slots=True)
class CommandSpec:
    name: str
    aliases: tuple[str, ...]
    help: str
    arguments: tuple[ArgumentSpec, ...] = ()


COMMAND_SPECS: tuple[CommandSpec, ...] = (
    CommandSpec(
        name="list-collections",
        aliases=("lc",),
        help="List all collections stored in the local Chroma database.",
    ),
    CommandSpec(
        name="create-collection",
        aliases=("cc",),
        help="Create a collection in the local Chroma database.",
        arguments=(ArgumentSpec("collection", "Name of the collection to create."),),
    ),
    CommandSpec(
        name="delete-collection",
        aliases=("dc",),
        help="Delete a collection from the local Chroma database.",
        arguments=(ArgumentSpec("collection", "Name of the collection to delete."),),
    ),
    CommandSpec(
        name="count",
        aliases=("co",),
        help="Count records in a collection from the local Chroma database.",
        arguments=(ArgumentSpec("collection", "Name of the collection to count."),),
    ),
    CommandSpec(
        name="add-data",
        aliases=("ad",),
        help="Chunk, embed, and add a file to a collection in the local Chroma database.",
        arguments=(
            ArgumentSpec("collection", "Name of the target collection."),
            ArgumentSpec(
                "file", "Path to the file to chunk and add to the collection."
            ),
        ),
    ),
    CommandSpec(
        name="query",
        aliases=("q",),
        help="Query a collection with the provided text.",
        arguments=(
            ArgumentSpec("collection", "Name of the target collection."),
            ArgumentSpec("query_text", "The text to query."),
        ),
    ),
)


def _add_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    command: CommandSpec,
) -> None:
    subparser = subparsers.add_parser(
        command.name,
        aliases=list(command.aliases),
        help=command.help,
        description=command.help,
    )

    for argument in command.arguments:
        subparser.add_argument(argument.name, help=argument.help)

    subparser.set_defaults(command=command.name)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect local Chroma collections.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in COMMAND_SPECS:
        _add_command(subparsers, command)

    return parser
