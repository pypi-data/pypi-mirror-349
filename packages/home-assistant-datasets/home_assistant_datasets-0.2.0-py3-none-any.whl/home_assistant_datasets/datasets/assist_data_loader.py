"""Module for reading 'assist' dataset file records.

The Assist dataset format was originally based on the home assistant intents
test format, but modified to perform more fine grained setup and testing of
entity states. This is better than just expecting a tool call since it can
deal with fuzzy actions that result in the same outcome.

An individual record contains sentences to scrape the model with. Each sentence
is expanded into it's own `EvalTask`.
"""

from collections.abc import Generator
import datetime
from dataclasses import dataclass, field
import logging
import pathlib
from slugify import slugify
from typing import Any

from mashumaro.mixins.yaml import DataClassYAMLMixin
from mashumaro.config import BaseConfig
from mashumaro.exceptions import MissingField

from home_assistant_datasets.entity_state import EntityState
from home_assistant_datasets.yaml_loaders import yaml_decode

from .dataset_card import DatasetCard

__all__ = [
    "Record",
    "Action",
    "read_record",
]

_LOGGER = logging.getLogger(__name__)


@dataclass(kw_only=True, frozen=True)
class ToolCall(DataClassYAMLMixin):
    """Represents an expected tool call."""

    tool_name: str
    """The name of the tool to call."""

    tool_args: dict[str, Any] | None = None
    """Arguments to the tool call."""

    class Config(BaseConfig):
        code_generation_options = ["TO_DICT_ADD_OMIT_NONE_FLAG"]
        forbid_extra_keys = True
        sort_keys = False
        omit_none = True


@dataclass(kw_only=True, frozen=True)
class Action(DataClassYAMLMixin):
    """An individual data item action."""

    sentences: list[str]
    """Sentences spoken."""

    setup: dict[str, EntityState] = field(default_factory=dict)
    """Initial entity states to override keyed by entity_id."""

    expect_changes: dict[str, EntityState] | None = None
    """The device states to assert on, keyed by entity_id."""

    ignore_changes: dict[str, list[str]] | None = None
    """The device state or attribute changes to ignored, keyed by entity_id."""

    expect_response: str | list[str] | None = None
    """Expect the agent to respond with this substring.

    When specified as a list, the response may match any valid substring in the last.
    """

    expect_tool_call: ToolCall | None = None
    """Expect the specified tool call to occur, independent of the outcome."""

    context_device: str | None = None
    """Synthetic home device id for the current context of the request."""

    context_now: datetime.datetime | None = None
    """The current time to use during tests."""

    class Config(BaseConfig):
        code_generation_options = ["TO_DICT_ADD_OMIT_NONE_FLAG"]
        forbid_extra_keys = False
        sort_keys = False
        omit_none = True
        omit_default = True


@dataclass(kw_only=True, frozen=True)
class RecordSource(DataClassYAMLMixin):
    """Information about the Record file source."""

    record_id: str
    """A unique identifier of this record within the dataset."""

    record_path: pathlib.Path
    """File path for this dataset record."""


@dataclass(kw_only=True)
class Record(DataClassYAMLMixin):
    """Represents an item in the dataset used to configure evaluation."""

    category: str | list[str]
    """Category used to describe the evaluation task when reporting"""

    tests: list[Action] | None = field(default_factory=list)
    """The set of tasks to evaluate."""

    record_source: RecordSource | None = None
    """Information about the filesystem source for this record.

    Attribute is set at runtime after being loaded.
    """

    @property
    def categories(self) -> list[str]:
        """Labels used for slicing model predictions."""
        if isinstance(self.category, list):
            return self.category
        return [self.category]

    class Config(BaseConfig):
        code_generation_options = ["TO_DICT_ADD_OMIT_NONE_FLAG"]
        sort_keys = True
        omit_none = True


def _make_slug(text: str) -> str:
    """Shorthand slugify command"""
    return slugify(text, separator="_")


def read_record_sources(dataset_card: DatasetCard) -> Generator[RecordSource]:
    """Generate the list of dataset files for the given path."""

    def unique_record_id(filename: pathlib.Path) -> str:
        """Convert the filename to a unique id withint he dataset."""
        assert dataset_card.path is not None
        relative_path = filename.relative_to(dataset_card.dataset_path)
        stem = str(relative_path)[:-5]  # No .yaml suffix
        return _make_slug(stem)

    for filename in dataset_card.dataset_files:
        yield RecordSource(record_id=unique_record_id(filename), record_path=filename)


def read_record(filename: pathlib.Path) -> Record:
    """Read the dataset record"""
    try:
        return yaml_decode(filename.open(), Record)
    except MissingField as err:
        raise ValueError(f"Dataset record invalid {filename}: {err}") from err


def read_dataset_records(
    dataset_card: DatasetCard, categories: set[str] | None = None
) -> Generator[Record]:
    """Generate the list of dataset records for the given path."""

    for record_source in read_record_sources(dataset_card):
        assert record_source.record_path is not None
        record = read_record(record_source.record_path)
        if categories and not any(
            category in categories for category in record.categories
        ):
            _LOGGER.debug(
                "Skipping record with category %s (not in %s)",
                record.category,
                categories,
            )
            continue
        record.record_source = record_source
        yield record
