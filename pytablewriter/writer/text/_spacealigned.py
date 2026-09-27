import copy
from typing import Any

import dataproperty
from dataproperty import LineBreakHandling

from ._csv import CsvTableWriter


class SpaceAlignedTableWriter(CsvTableWriter):
    """
    A table writer class for space-separated values (SSV) format.

        :Example:
            :ref:`example-space-aligned-table-writer`

    .. py:method:: write_table

        |write_table| with SSV format.

        :Example:
            :ref:`example-space-aligned-table-writer`
    """

    FORMAT_NAME = "space_aligned"

    @property
    def format_name(self) -> str:
        return self.FORMAT_NAME

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.column_delimiter = "  "
        self.char_cross_point = "  "

        self.is_padding = True
        self.is_formatting_float = kwargs.get("is_formatting_float", True)

        self._quoting_flags = copy.deepcopy(dataproperty.NOT_QUOTING_FLAGS)

        # replace line breaks with spaces to keep rows in a single line
        self.update_preprocessor(line_break_handling=LineBreakHandling.REPLACE)

    def _escape_csv_item(self, value: str, is_quote: bool) -> str:
        # do not quote/escape values for space-aligned format
        return value
