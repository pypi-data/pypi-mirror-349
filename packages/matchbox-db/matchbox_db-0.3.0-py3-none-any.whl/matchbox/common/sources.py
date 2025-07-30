"""Classes and functions for working with data sources in Matchbox."""

import re
import textwrap
from abc import ABC, abstractmethod
from copy import deepcopy
from functools import wraps
from pathlib import Path
from typing import (
    Any,
    Callable,
    Iterator,
    Literal,
    ParamSpec,
    Self,
    TypeVar,
    Union,
)

import polars as pl
from polars import DataFrame as PolarsDataFrame
from pyarrow import Table as ArrowTable
from pydantic import (
    AnyUrl,
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)
from sqlalchemy import Engine
from sqlalchemy.exc import OperationalError

from matchbox.common.db import (
    QueryReturnType,
    ReturnTypeStr,
    clean_uri,
    sql_to_df,
    validate_sql_for_data_extraction,
)
from matchbox.common.dtos import DataTypes, SourceResolutionName
from matchbox.common.exceptions import (
    MatchboxSourceCredentialsError,
)
from matchbox.common.hash import (
    HASH_FUNC,
    HashMethod,
    hash_rows,
)

T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R")


LocationType = Union["RelationalDBLocation"]
"""Type for Location class. Currently only supports RelationalDBLocation."""

LocationTypeStr = Union[Literal["rdbms"]]
"""String literal type for Location class. Currently only supports "rdbms"."""


def requires_credentials(method: Callable[..., T]) -> Callable[..., T]:
    """Decorator that checks if credentials are set before executing a method.

    A helper method for Location subclasses.

    Raises:
        MatchboxSourceCredentialsError: If the credentials are not set.
    """

    @wraps(method)
    def wrapper(self: "Location", *args, **kwargs) -> T:
        if self.credentials is None:
            raise MatchboxSourceCredentialsError
        return method(self, *args, **kwargs)

    return wrapper


class Location(ABC, BaseModel):
    """A location for a data source."""

    type: LocationTypeStr
    uri: AnyUrl
    credentials: Any | None = Field(exclude=True, default=None)

    def __eq__(self, other: Any) -> bool:
        """Custom equality which ignores credentials."""
        return (self.type, self.uri) == (
            other.type,
            other.uri,
        )

    def __hash__(self) -> int:
        """Custom hash which ignores credentials."""
        return hash((self.type, self.uri))

    def __deepcopy__(self, memo=None):
        """Create a deep copy of the Location object."""
        if memo is None:
            memo = {}

        obj_copy = type(self)(
            type=deepcopy(self.type, memo),
            uri=deepcopy(self.uri, memo),
        )

        # Both objects should share the same credentials
        if self.credentials is not None:
            obj_copy.credentials = self.credentials

        return obj_copy

    @abstractmethod
    def add_credentials(self, credentials: Any) -> None:
        """Adds credentials to the location."""
        ...

    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the data location.

        Raises:
            AttributeError: If the credentials are not set.
        """
        ...

    @abstractmethod
    def validate_extract_transform(self, extract_transform: str) -> bool:
        """Validate SQL ET logic against this location's query language.

        Raises:
            MatchboxSourceExtractTransformError: If the ET logic is invalid.
        """
        ...

    @abstractmethod
    def execute(
        self,
        extract_transform: str,
        batch_size: int,
        rename: dict[str, str] | Callable | None = None,
        return_batches: bool = False,
        return_type: ReturnTypeStr = "polars",
    ) -> Iterator[QueryReturnType] | QueryReturnType:
        """Execute ET logic against location and return batches.

        Args:
            extract_transform: The ET logic to execute.
            batch_size: The size of the batches to return.
            rename: Renaming to apply after the ET logic is executed.

                * If a dictionary is provided, it will be used to rename the columns.
                * If a callable is provided, it will take the old name as input and
                    return the new name.
            return_batches: If True, return an iterator of batches.
            return_type: The type of data to return. Defaults to "polars".

        Raises:
            AttributeError: If the credentials are not set.
        """
        ...


class RelationalDBLocation(Location):
    """A location for a relational database."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    type: Literal["rdbms"] = "rdbms"
    uri: AnyUrl
    credentials: Engine | None = Field(
        exclude=True,
        default=None,
        description=(
            "The credentials for a relational database are a SQLAlchemy Engine."
        ),
    )

    @field_validator("uri", mode="after")
    @classmethod
    def validate_uri(cls, value: AnyUrl) -> AnyUrl:
        """Ensure no credentials, query params, or fragments are in the URI."""
        return clean_uri(value)

    def _validate_engine(self, credentials: Engine) -> None:
        """Validate an engine matches the URI.

        Raises:
            ValueError: If the Engine and URI do not match.
        """
        uri = clean_uri(str(credentials.url))

        if any(
            [
                uri.scheme != self.uri.scheme,
                uri.host != self.uri.host,
                uri.port != self.uri.port,
                uri.path != self.uri.path,
            ]
        ):
            raise ValueError(
                "The Engine location URI does not match the location model URI. \n"
                f"Scheme: {uri.scheme}, {self.uri.scheme} \n"
                f"Host: {uri.host}, {self.uri.host} \n"
                f"Port: {uri.port}, {self.uri.port} \n"
                f"Path: {uri.path}, {self.uri.path} \n"
            )

    def add_credentials(self, credentials: Engine) -> None:  # noqa: D102
        self._validate_engine(credentials)
        self.credentials = credentials

    @requires_credentials
    def connect(self) -> bool:  # noqa: D102
        try:
            _ = sql_to_df(stmt="select 1", connection=self.credentials)
            return True
        except OperationalError:
            return False

    def validate_extract_transform(self, extract_transform: str) -> bool:  # noqa: D102
        # We are NOT attempting a full sanitisation of the SQL statement
        # Validation is done purely to stop accidental mistakes, not malicious actors
        # Users should only run indexing using SourceConfigs they trust and have read,
        # using least privilege credentials
        return validate_sql_for_data_extraction(extract_transform)

    @requires_credentials
    def execute(  # noqa: D102
        self,
        extract_transform: str,
        batch_size: int,
        rename: dict[str, str] | Callable | None = None,
        return_batches: bool = True,
        return_type: ReturnTypeStr = "polars",
    ) -> Iterator[QueryReturnType] | QueryReturnType:
        return sql_to_df(
            stmt=extract_transform,
            connection=self.credentials,
            rename=rename,
            batch_size=batch_size,
            return_batches=return_batches,
            return_type=return_type,
        )

    @classmethod
    def from_engine(cls, engine: Engine) -> "RelationalDBLocation":
        """Create a RelationalDBLocation from a SQLAlchemy Engine."""
        cleaned_url = engine.url.set(
            username=None,
            password=None,
            query={},
        )
        location = cls(uri=str(cleaned_url))
        location.add_credentials(engine)
        return location


class SourceField(BaseModel):
    """A field in a source that can be indexed in the Matchbox database."""

    model_config = ConfigDict(frozen=True)

    name: str = Field(
        description=(
            "The name of the field in the source after the "
            "extract/transform logic has been applied."
        )
    )
    type: DataTypes = Field(
        description="The cached field type. Used to ensure a stable hash.",
    )


class SourceConfig(BaseModel):
    """Configuration of a source that can, or has been, indexed in the backend.

    SourceConfigs are used to configure source resolutions. They are foundational
    processes on top of which linking and deduplication models can build new
    resolutions.
    """

    model_config = ConfigDict(frozen=True)

    location: LocationType = Field(
        discriminator="type",
        description=(
            "The location of the source. Used to run the extract/tansform logic."
        ),
    )
    name: SourceResolutionName = Field(
        description=(
            "A unique, human-readable name of the source resolution this "
            "object configures."
        )
    )
    extract_transform: str = Field(
        description=(
            "Logic to extract and transform data from the source. "
            "Language is location dependent."
        )
    )
    # Fields can to be set at creation, or initialised with `.default_columns()`
    key_field: SourceField = Field(
        description=textwrap.dedent("""
            The key field. This is the source's key for unique
            entities, such as a primary key in a relational database.

            Keys must ALWAYS be a string.

            For example, if the source describes companies, it may have used
            a Companies House number as its key.

            This key is ALWAYS correct. It should be something generated and
            owned by the source being indexed.
            
            For example, your organisation's CRM ID is a key field within the CRM.
            
            A CRM ID entered by hand in another dataset shouldn't be used 
            as a key field.
        """),
    )
    index_fields: tuple[SourceField, ...] = Field(
        default=None,
        description=textwrap.dedent(
            """
            The fields to index in this source, after the extract/transform logic 
            has been applied. 

            This is usually set manually, and should map onto the columns that the
            extract/transform logic returns.
            """
        ),
    )

    @property
    def prefix(self) -> str:
        """Get the prefix for the source."""
        return self.name + "_"

    @property
    def qualified_key(self) -> str:
        """Get the qualified key for the source."""
        return self.qualify_field(self.key_field.name)

    @property
    def qualified_fields(self) -> list[str]:
        """Get the qualified fields for the source."""
        return [self.qualify_field(field.name) for field in self.index_fields]

    def qualify_field(self, field: str) -> str:
        """Qualify a field name with the source name.

        Args:
            field: The field name to qualify.

        Returns:
            The qualified field name.
        """
        return self.prefix + field

    def _detect_fields(
        self, location: Location, extract_transform: str
    ) -> tuple[SourceField, ...]:
        """A helper method to detect the fields from the extract/transform logic.

        Return all detected fields as SourceFields.
        """
        df: pl.DataFrame = next(
            location.execute(extract_transform=extract_transform, batch_size=100)
        )

        return tuple(
            SourceField(
                name=col.name,
                type=DataTypes.from_dtype(col.dtype),
            )
            for col in df.iter_columns()
        )

    @field_validator("name", mode="after")
    @classmethod
    def validate_name(cls, value: str) -> str:
        """Ensure the name is a valid source resolution name.

        Raises:
            ValueError: If the name is not a valid source resolution name.
        """
        if not re.match(r"^[a-z0-9_]+$", value):
            raise ValueError(
                "Source resolution names must be alphanumeric and underscore only. "
            )
        return value

    @model_validator(mode="after")
    def validate_key_field(self) -> Self:
        """Ensure that the key field is a string and not in the index fields."""
        if self.key_field in self.index_fields:
            raise ValueError("Key field must not be in the index fields. ")

        if self.key_field.type != DataTypes.STRING:
            raise ValueError("Key field must be a string. ")

        return self

    @model_validator(mode="after")
    def validate_location_et_fields(self) -> "SourceConfig":
        """Ensure that the location, extract_transform, and fields are aligned."""
        if self.location.credentials is None:
            # We can't validate
            return self

        fields = self._detect_fields(
            location=self.location, extract_transform=self.extract_transform
        )

        if set(self.index_fields + (self.key_field,)) != set(fields):
            raise ValueError(
                "The index fields or key field do not match the "
                "extract/transform logic. "
                "Please check the index fields, key field and logic. \n"
                f"Declared index fields: {self.index_fields} \n"
                f"Declared key field: {self.key_field} \n"
                f"Fields from logic: {tuple(fields)} \n"
            )

        return self

    @classmethod
    def from_location(
        cls, location: Location, extract_transform: str
    ) -> "SourceConfig":
        """Create a SourceConfig from a Location.

        A convenience method to create a SourceConfig from minimal options.

        * Assumes a column aliasesed as "id" is the key field
        * Autodetects datatypes from a small sample
        * Uses the location's URI host and truncated ETL hash as the resolution name

        Args:
            location: The location of the source.
            extract_transform: The logic to extract and transform data from the source.

        Returns:
            A SourceConfig object with the location set.
        """
        # Detect fields
        fields: tuple[SourceField, ...] = cls._detect_fields(
            cls,
            location=location,
            extract_transform=extract_transform,
        )
        index_fields: tuple[SourceField] = tuple(
            field for field in fields if field.name != "id"
        )
        if len(index_fields) != len(fields) - 1:
            raise ValueError(
                "The extract/transform logic must return a column "
                "aliased as 'id' to be used as the key field."
            )

        # Create name
        et_hash = HASH_FUNC(extract_transform.encode("utf-8")).hexdigest()[:6]
        default_name: str | None = (
            location.uri.host or Path(location.uri.path).stem or None
        )
        if default_name is None:
            raise ValueError(
                "Could not detect a default name for the source. "
                "Please create the source manually."
            )

        return cls(
            name=default_name + "_" + et_hash,
            location=location,
            extract_transform=extract_transform,
            key_field=SourceField(name="id", type=DataTypes.STRING),
            index_fields=index_fields,
        )

    def set_credentials(self, credentials: Any) -> None:
        """Set the credentials for the location.

        Args:
            credentials: The credentials to set.
        """
        self.location.add_credentials(credentials)
        self.validate_location_et_fields()

    def query(
        self,
        qualify_names: bool = False,
        return_batches: bool = False,
        batch_size: int | None = None,
        return_type: ReturnTypeStr = "polars",
    ) -> Iterator[QueryReturnType] | QueryReturnType:
        """Applies the extract/transform logic to the source and returns the results.

        Args:
            qualify_names: If True, qualify the names of the columns with the
                source name.
            return_batches:
                * If True, return an iterator that yields each batch separately
                * If False, return a single Table with all results
            batch_size: Indicate the size of each batch when processing data in batches.
            return_type: The type of data to return. Defaults to "polars".

        Returns:
            The requested data in the specified format.

                * If return_batches is False: a single table
                * If return_batches is True: an iterator of tables
        """
        _rename: Callable | None = None
        if qualify_names:

            def _rename(c: str) -> str:
                return self.name + "_" + c

        return self.location.execute(
            extract_transform=self.extract_transform,
            rename=_rename,
            batch_size=batch_size,
            return_batches=return_batches,
            return_type=return_type,
        )

    def hash_data(self, batch_size: int | None = None) -> ArrowTable:
        """Retrieve and hash a dataset from its warehouse, ready to be inserted.

        Hashes the index fields defined in the source based on the
        extract/transform logic.

        Does not hash the key field.

        Args:
            batch_size: If set, process data in batches internally. Indicates the
                size of each batch.

        Returns:
            A PyArrow Table containing source keys and their hashes.
        """
        key_field: str = self.key_field.name
        index_fields: list[str] = [field.name for field in self.index_fields]

        def _process_batch(batch: PolarsDataFrame) -> PolarsDataFrame:
            """Process a single batch of data using Polars.

            Args:
                batch: Polars DataFrame containing the data

            Returns:
                Polars DataFrame with hash and keys columns

            Raises:
                ValueError: If any keys values are null
            """
            batch: pl.DataFrame = batch.rename({key_field: "keys"})

            if batch["keys"].is_null().any():
                raise ValueError("keys column contains null values")

            row_hashes: pl.Series = hash_rows(
                df=batch,
                columns=list(sorted(index_fields)),
                method=HashMethod.SHA256,
            )

            result = batch.with_columns(row_hashes.alias("hash")).select(
                ["hash", "keys"]
            )

            return result

        if bool(batch_size):
            # Process in batches
            all_results: list[pl.DataFrame] = []
            for batch in self.query(
                return_batches=True,
                batch_size=batch_size,
                return_type="polars",
            ):
                batch_result = _process_batch(batch)
                all_results.append(batch_result)

            processed_df = pl.concat(all_results)

        else:
            # Non-batched processing
            processed_df = _process_batch(self.query())

        return processed_df.group_by("hash").agg(pl.col("keys")).to_arrow()


class Match(BaseModel):
    """A match between primary keys in the Matchbox database."""

    cluster: int | None
    source: SourceResolutionName
    source_id: set[str] = Field(default_factory=set)
    target: SourceResolutionName
    target_id: set[str] = Field(default_factory=set)

    @model_validator(mode="after")
    def found_or_none(self) -> "Match":
        """Ensure that a match has sources and a cluster if target was found."""
        if self.target_id and not (self.source_id and self.cluster):
            raise ValueError(
                "A match must have sources and a cluster if target was found."
            )
        if self.cluster and not self.source_id:
            raise ValueError("A match must have source if cluster is set.")
        return self
