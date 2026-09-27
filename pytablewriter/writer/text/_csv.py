import copy
from collections.abc import Sequence
from typing import Any

import dataproperty
import typepy
from dataproperty import DataProperty, LineBreakHandling
from typepy import Typecode

from .._common import HEADER_ROW
from ._text_writer import TextTableWriter


class CsvTableWriter(TextTableWriter):
    """
    A table writer class for character separated values format.
    The default separated character is a comma (``","``).

        :Example:
            :ref:`example-csv-table-writer`
    """

    FORMAT_NAME = "csv"

    @property
    def format_name(self) -> str:
        return self.FORMAT_NAME

    @property
    def support_split_write(self) -> bool:
        return True

    @property
    def margin(self) -> int:
        return self._margin

    @margin.setter
    def margin(self, value: int) -> None:
        # margin setting must be ignored
        return

    @property
    def _quoting_flags(self) -> dict[Typecode, bool]:
        # logical quoting flags: used to determine which values should be
        # quoted in outputs, and passed to pytablereader in from_csv method
        return self.__logical_quoting_flags

    @_quoting_flags.setter
    def _quoting_flags(self, value: dict[Typecode, bool]) -> None:
        self.__logical_quoting_flags = value

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self._set_chars("")
        self.indent_string = ""
        self.column_delimiter = kwargs.get("column_delimiter", ",")
        self._margin = 0

        self.is_padding = False
        self.is_formatting_float = False
        self.is_write_header_separator_row = False

        self._quoting_flags[Typecode.NULL_STRING] = False

        # disable dataproperty-level quoting to apply RFC 4180 compliant
        # quoting/escaping at the writer level instead
        self._dp_extractor.quoting_flags = copy.deepcopy(dataproperty.NOT_QUOTING_FLAGS)

        # keep line breaks as-is: they can be preserved within quoted fields
        self.update_preprocessor(line_break_handling=LineBreakHandling.NOP)

    def _write_header(self) -> None:
        if typepy.is_empty_sequence(self.headers):
            return

        super()._write_header()

    def _write_row(self, row: int, values: Sequence[str]) -> None:
        if row == HEADER_ROW:
            values = [self._escape_csv_item(value, is_quote=True) for value in values]

        super()._write_row(row, values)

    def _write_value_row(
        self, row: int, values: Sequence[str], value_dp_list: Sequence[DataProperty]
    ) -> None:
        values = [
            self._escape_csv_item(
                value, is_quote=self._quoting_flags.get(value_dp.typecode, False)
            )
            for value, value_dp in zip(values, value_dp_list)
        ]

        super()._write_value_row(row, values, value_dp_list)

    def _escape_csv_item(self, value: str, is_quote: bool) -> str:
        if not is_quote:
            # quote values that include special characters even if the value
            # type is not a quoting target (RFC 4180)
            is_quote = any(char in value for char in (self.column_delimiter, '"', "\n", "\r"))

        if not is_quote:
            return value

        return '"{:s}"'.format(value.replace('"', '""'))

    def _get_opening_row_items(self) -> list[str]:
        return []

    def _get_value_row_separator_items(self) -> list[str]:
        return []

    def _get_closing_row_items(self) -> list[str]:
        return []
