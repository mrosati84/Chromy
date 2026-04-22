from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ListCollectionsInput:
    pass


@dataclass(frozen=True, slots=True)
class CreateCollectionInput:
    collection: str


@dataclass(frozen=True, slots=True)
class DeleteCollectionInput:
    collection: str


@dataclass(frozen=True, slots=True)
class CountCollectionInput:
    collection: str


@dataclass(frozen=True, slots=True)
class AddDataInput:
    collection: str
    file: str


@dataclass(frozen=True, slots=True)
class QueryInput:
    collection: str
    query_text: str


@dataclass(frozen=True, slots=True)
class DeleteRecordsInput:
    collection: str
    where: str


CommandInput = (
    ListCollectionsInput
    | CreateCollectionInput
    | DeleteCollectionInput
    | CountCollectionInput
    | AddDataInput
    | QueryInput
    | DeleteRecordsInput
)
