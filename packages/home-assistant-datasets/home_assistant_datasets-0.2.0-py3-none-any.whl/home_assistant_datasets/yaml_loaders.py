"""Initialize the yaml_loaders extensions."""

import logging
import enum
from pathlib import Path
from typing import Any, TypeVar, Type

import yaml
from mashumaro.codecs.yaml import YAMLDecoder

from . import secrets

_LOGGER = logging.getLogger(__name__)

T = TypeVar("T")

_DEFAULT_LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


class FastSafeLoader(_DEFAULT_LOADER):  # type: ignore
    """The fastest available safe loader, either C or Python.

    This exists to support capturing the stream file name in the same way as the
    python yaml loader in order to support !include tags.
    """

    def __init__(self, stream: Any) -> None:
        """Initialize a safe line loader."""
        self.stream = stream

        # Set name in same way as the Python loader does in yaml.reader.__init__
        if isinstance(stream, str):
            self.name = "<unicode string>"
        elif isinstance(stream, bytes):
            self.name = "<byte string>"
        else:
            self.name = getattr(stream, "name", "<file>")

        super().__init__(stream)


def _default_decoder(stream: Any) -> Any:
    """Decode a YAML document using the custom tag constructors."""
    return yaml.load(stream, Loader=FastSafeLoader)


def yaml_decode(stream: Any, shape_type: Type[T] | Any) -> T:
    """Decode a YAML document using the custom tag constructors.

    This function is comparable to the mashumaro.codecs.yaml.yaml_decode function,
    but accepts a stream rather than content string in order to implement
    custom tags based on the current filename.
    """
    return YAMLDecoder(shape_type, pre_decoder_func=_default_decoder).decode(stream)  # type: ignore[no-any-return]


def _include_file(loader: yaml.SafeLoader, node: yaml.nodes.ScalarNode) -> Path:
    path = Path(node.value)
    if not path.is_absolute():
        loader_path = Path(loader.name)
        if not loader_path.exists():
            raise FileNotFoundError(
                f"Could not determine yaml file path from '{loader_path}'"
            )
        path = loader_path.parent / path

    if not path.exists():
        raise FileNotFoundError(f"File '{path}' does not exist {str(node.start_mark)}")

    if not path.is_file():
        raise FileNotFoundError(f"File '{path}' is not a file {str(node.start_mark)}")
    return path


def _include_tag_constructor(
    loader: yaml.SafeLoader, node: yaml.nodes.ScalarNode
) -> Any:
    """Load a file from the filesystem."""
    path = _include_file(loader, node)
    with path.open() as include_file:
        return yaml.load(include_file, Loader=FastSafeLoader)


def _include_text_tag_constructor(
    loader: yaml.SafeLoader, node: yaml.nodes.ScalarNode
) -> Any:
    """Load a text file from the filesystem."""
    path = _include_file(loader, node)
    return path.read_text()


_missing_secrets: set[str] = set({})


def _get_secret_constructor(
    loader: yaml.SafeLoader, node: yaml.nodes.ScalarNode
) -> Any:
    """Load a file from the filesystem."""
    secret_name = node.value
    try:
        return secrets.get_secret(secret_name)
    except KeyError as err:
        if secret_name not in _missing_secrets:
            _LOGGER.warning("Unable to load secret, proceeding anyway: %s", err)
        _missing_secrets.add(secret_name)
        return None


def configure_encoders() -> None:
    """Configure pyyaml with some formatting options specific to our eval records."""

    # Skip any output for unknown tags
    yaml.emitter.Emitter.prepare_tag = lambda self, tag: ""  # type: ignore[method-assign]

    # Make automation dumps look a little nicer in the output reports
    def str_presenter(dumper, data):  # type: ignore[no-untyped-def]
        """configures yaml for dumping multiline strings
        Ref: https://stackoverflow.com/questions/8640959/how-can-i-control-what-scalar-form-pyyaml-uses-for-my-data
        """
        if data.count("\n") > 0:  # check for multiline string
            return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
        return dumper.represent_scalar("tag:yaml.org,2002:str", data)

    yaml.add_representer(str, str_presenter)
    yaml.representer.SafeRepresenter.add_representer(str, str_presenter)
    yaml.SafeDumper.add_multi_representer(
        enum.StrEnum,
        yaml.representer.SafeRepresenter.represent_str,
    )


# Register the custom tag constructors.
FastSafeLoader.add_constructor("!include", _include_tag_constructor)
FastSafeLoader.add_constructor("!include_text", _include_text_tag_constructor)
FastSafeLoader.add_constructor("!secret", _get_secret_constructor)
