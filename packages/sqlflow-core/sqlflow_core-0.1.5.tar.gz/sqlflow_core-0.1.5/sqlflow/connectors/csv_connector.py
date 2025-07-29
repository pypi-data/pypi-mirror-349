"""CSV connector for SQLFlow."""

import csv
import os
from typing import Any, Dict, Iterator, List, Optional

import pyarrow.csv as csv_arrow

from sqlflow.connectors.base import (
    ConnectionTestResult,
    Connector,
    ConnectorState,
    Schema,
)
from sqlflow.connectors.data_chunk import DataChunk
from sqlflow.connectors.registry import register_connector
from sqlflow.core.errors import ConnectorError


@register_connector("CSV")
class CSVConnector(Connector):
    """Connector for CSV files."""

    def __init__(self):
        """Initialize a CSVConnector."""
        super().__init__()
        self.path: Optional[str] = None
        self.delimiter: str = ","
        self.has_header: bool = True
        self.quote_char: str = '"'
        self.encoding: str = "utf-8"

    def configure(self, params: Dict[str, Any]) -> None:
        """Configure the connector with parameters.

        Args:
            params: Configuration parameters

        Raises:
            ConnectorError: If configuration fails
        """
        try:
            self.path = params.get("path")
            if not self.path:
                raise ValueError("Path is required")

            self.delimiter = params.get("delimiter", ",")
            self.has_header = params.get("has_header", True)
            self.quote_char = params.get("quote_char", '"')
            self.encoding = params.get("encoding", "utf-8")

            self.state = ConnectorState.CONFIGURED
        except Exception as e:
            self.state = ConnectorState.ERROR
            raise ConnectorError(self.name or "CSV", f"Configuration failed: {str(e)}")

    def test_connection(self) -> ConnectionTestResult:
        """Test if the CSV file exists and is readable.

        Returns:
            Result of the connection test
        """
        self.validate_state(ConnectorState.CONFIGURED)

        try:
            if not self.path:
                return ConnectionTestResult(False, "Path not configured")

            if not os.path.exists(self.path):
                self.state = ConnectorState.ERROR
                return ConnectionTestResult(False, f"File not found: {self.path}")

            with open(self.path, "r", encoding=self.encoding) as f:
                f.read(1)

            self.state = ConnectorState.READY
            return ConnectionTestResult(True)
        except Exception as e:
            self.state = ConnectorState.ERROR
            return ConnectionTestResult(False, str(e))

    def discover(self) -> List[str]:
        """Discover available objects in the data source.

        For CSV, this returns a single object representing the file.

        Returns:
            List with a single object name

        Raises:
            ConnectorError: If discovery fails
        """
        self.validate_state(ConnectorState.CONFIGURED)

        try:
            if not self.path:
                raise ValueError("Path not configured")

            if not os.path.exists(self.path):
                raise ValueError(f"File not found: {self.path}")

            base_name = os.path.basename(self.path)
            name, _ = os.path.splitext(base_name)

            return [name]
        except Exception as e:
            self.state = ConnectorState.ERROR
            raise ConnectorError(self.name or "CSV", f"Discovery failed: {str(e)}")

    def get_schema(self, object_name: str) -> Schema:
        """Get schema for the CSV file.

        Args:
            object_name: Name of the object (ignored for CSV)

        Returns:
            Schema for the CSV file

        Raises:
            ConnectorError: If schema retrieval fails
        """
        self.validate_state(ConnectorState.CONFIGURED)

        try:
            if not self.path:
                raise ValueError("Path not configured")

            if not os.path.exists(self.path):
                raise ValueError(f"File not found: {self.path}")

            if self.has_header:
                with open(self.path, "r", encoding=self.encoding) as f:
                    reader = csv.reader(
                        f, delimiter=self.delimiter, quotechar=self.quote_char
                    )
                    header_row = next(reader)

                read_options = csv_arrow.ReadOptions(
                    skip_rows=1, encoding=self.encoding
                )
                parse_options = csv_arrow.ParseOptions(
                    delimiter=self.delimiter, quote_char=self.quote_char
                )
                convert_options = csv_arrow.ConvertOptions()

                table = csv_arrow.read_csv(
                    self.path,
                    read_options=read_options,
                    parse_options=parse_options,
                    convert_options=convert_options,
                )

                import pyarrow as pa

                fields = [
                    pa.field(name, dtype)
                    for name, dtype in zip(header_row, table.schema.types)
                ]
                schema = pa.schema(fields)

                table = pa.Table.from_arrays(table.columns, schema=schema)
            else:
                read_options = csv_arrow.ReadOptions(
                    skip_rows=0, encoding=self.encoding
                )
                parse_options = csv_arrow.ParseOptions(
                    delimiter=self.delimiter, quote_char=self.quote_char
                )
                convert_options = csv_arrow.ConvertOptions()

                table = csv_arrow.read_csv(
                    self.path,
                    read_options=read_options,
                    parse_options=parse_options,
                    convert_options=convert_options,
                )

            self.state = ConnectorState.READY
            return Schema(table.schema)
        except Exception as e:
            self.state = ConnectorState.ERROR
            raise ConnectorError(
                self.name or "CSV", f"Schema retrieval failed: {str(e)}"
            )

    def read(
        self,
        object_name: str,
        columns: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
        batch_size: int = 10000,
    ) -> Iterator[DataChunk]:
        """Read data from the CSV file in chunks.

        Args:
            object_name: Name of the object (ignored for CSV)
            columns: Optional list of columns to read
            filters: Optional filters to apply (not supported for CSV)
            batch_size: Number of rows per batch

        Yields:
            DataChunk objects

        Raises:
            ConnectorError: If reading fails
        """
        self.validate_state(ConnectorState.CONFIGURED)

        try:
            if not self.path:
                raise ValueError("Path not configured")

            if not os.path.exists(self.path):
                raise ValueError(f"File not found: {self.path}")

            if filters:
                import logging

                logging.warning("Filters are not supported for CSV and will be ignored")

            import pandas as pd

            df = pd.read_csv(
                self.path,
                sep=self.delimiter,
                header=0 if self.has_header else None,
                quotechar=self.quote_char,
                encoding=self.encoding,
                dtype=None,  # Allow pandas to automatically infer data types
            )

            if columns:
                df = df[columns]

            import pyarrow as pa

            table = pa.Table.from_pandas(df)

            yield DataChunk(table)

            self.state = ConnectorState.READY
        except Exception as e:
            self.state = ConnectorState.ERROR
            raise ConnectorError(self.name or "CSV", f"Reading failed: {str(e)}")

    def write(
        self, object_name: str, data_chunk: DataChunk, mode: str = "append"
    ) -> None:
        """Write data to a CSV file.

        Args:
            object_name: Name of the object (used to create filename if path not set)
            data_chunk: Data to write
            mode: Write mode (append or overwrite)

        Raises:
            ConnectorError: If writing fails
        """
        self.validate_state(ConnectorState.CONFIGURED)

        try:
            write_path = self.path
            if not write_path:
                write_path = f"{object_name}.csv"

            directory = os.path.dirname(os.path.abspath(write_path))
            if directory:
                os.makedirs(directory, exist_ok=True)

            # Get DataFrame from DataChunk
            df = data_chunk.pandas_df

            file_exists = os.path.exists(write_path) and os.path.getsize(write_path) > 0
            file_mode = "a" if mode == "append" and file_exists else "w"
            write_header = file_mode == "w" or not file_exists

            df.to_csv(
                write_path,
                mode=file_mode,
                header=write_header,
                index=False,
                sep=self.delimiter,
                quoting=csv.QUOTE_MINIMAL,
                quotechar=self.quote_char,
                encoding=self.encoding,
            )

            self.state = ConnectorState.READY
        except Exception as e:
            self.state = ConnectorState.ERROR
            raise ConnectorError(self.name or "CSV", f"Writing failed: {str(e)}")
