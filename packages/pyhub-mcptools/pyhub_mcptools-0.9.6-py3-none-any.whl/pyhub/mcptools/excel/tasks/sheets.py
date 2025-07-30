from pathlib import Path

import xlwings as xw
from pydantic import Field

from pyhub.mcptools.core.celery import celery_task
from pyhub.mcptools.excel.decorators import macos_excel_request_permission
from pyhub.mcptools.excel.types import ExcelCellType, ExcelExpandMode, ExcelGetValueType
from pyhub.mcptools.excel.utils import (
    convert_to_csv,
    csv_loads,
    fix_data,
    get_range,
    get_sheet,
    json_dumps,
    json_loads,
    normalize_text,
)
from pyhub.mcptools.fs.utils import validate_path


@celery_task(queue="xlwings")
@macos_excel_request_permission
def get_opened_workbooks() -> str:
    """Get a list of all open workbooks and their sheets in Excel

    Returns:
        str: JSON string containing:
            - books: List of open workbooks
                - name: Workbook name
                - fullname: Full path of workbook
                - sheets: List of sheets in workbook
                    - name: Sheet name
                    - index: Sheet index
                    - range: Used range address (e.g. "$A$1:$E$665")
                    - count: Total number of cells in used range
                    - shape: Tuple of (rows, columns) in used range
                    - active: Whether this is the active sheet
                - active: Whether this is the active workbook
    """

    return json_dumps(
        {
            "books": [
                {
                    "name": normalize_text(book.name),
                    "fullname": normalize_text(book.fullname),
                    "sheets": [
                        {
                            "name": normalize_text(sheet.name),
                            "index": sheet.index,
                            "range": sheet.used_range.get_address(),  # "$A$1:$E$665"
                            "count": sheet.used_range.count,  # 3325 (total number of cells)
                            "shape": sheet.used_range.shape,  # (655, 5)
                            "active": sheet == xw.sheets.active,
                            "table_names": [table.name for table in sheet.tables],
                        }
                        for sheet in book.sheets
                    ],
                    "active": book == xw.books.active,
                }
                for book in xw.books
            ]
        }
    )


@celery_task(queue="xlwings")
@macos_excel_request_permission
def find_data_ranges(
    book_name: str = Field(
        default="",
        description="Name of workbook to use. Optional.",
        examples=["Sales.xlsx", "Report2023.xlsx"],
    ),
    sheet_name: str = Field(
        default="",
        description="Name of sheet to use. Optional.",
        examples=["Sheet1", "Sales2023"],
    ),
) -> str:
    """Detects and returns all distinct data block ranges in an Excel worksheet.

    Scans worksheet to find contiguous blocks of non-empty cells.
    Uses active workbook/sheet if not specified.

    Detection Rules:
        - Finds contiguous non-empty cell blocks
        - Uses Excel's table expansion
        - Empty cells act as block boundaries
        - Merges overlapping/adjacent blocks

    Returns:
        str: JSON list of range addresses (e.g., ["A1:I11", "K1:P11"])
    """

    sheet = get_sheet(book_name=book_name, sheet_name=sheet_name)

    data_ranges = []
    visited = set()

    used = sheet.used_range
    start_row = used.row
    start_col = used.column
    n_rows = used.rows.count
    n_cols = used.columns.count

    # 전체 데이터를 메모리로 한 번에 가져옴 (2D 리스트)
    data_grid = used.value

    # 엑셀 한 셀일 경우, data_grid 값은 단일 값이므로 보정
    if not isinstance(data_grid, list):
        data_grid = [[data_grid]]
    elif isinstance(data_grid[0], (str, int, float, type(None))):
        data_grid = [data_grid]

    for r in range(n_rows):
        for c in range(n_cols):
            abs_row = start_row + r
            abs_col = start_col + c
            addr = (abs_row, abs_col)

            if addr in visited:
                continue

            # 데이터 시작 부분에 대해서 범위 좌표 계산
            val = data_grid[r][c]
            if val is not None and str(val).strip() != "":
                cell = sheet.range((abs_row, abs_col))
                block = cell.expand("table")

                top = block.row
                left = block.column
                bottom = top + block.rows.count - 1
                right = left + block.columns.count - 1

                for rr in range(top, bottom + 1):
                    for cc in range(left, right + 1):
                        visited.add((rr, cc))

                data_ranges.append(block.address)

    return json_dumps(data_ranges)


@celery_task(queue="xlwings")
@macos_excel_request_permission
def get_special_cells_address(
    sheet_range: str = Field(
        default="",
        description="""Excel range to get data. If not specified, uses the entire used range of the sheet.
            Important: When using expand_mode, specify ONLY the starting cell (e.g., 'A1' not 'A1:B10')
            as the range will be automatically expanded.""",
        examples=["A1", "Sheet1!A1", "A1:C10"],
    ),
    book_name: str = Field(
        default="",
        description="Name of workbook to use. Optional.",
        examples=["Sales.xlsx", "Report2023.xlsx"],
    ),
    sheet_name: str = Field(
        default="",
        description="Name of sheet to use. Optional.",
        examples=["Sheet1", "Sales2023"],
    ),
    expand_mode: str = Field(
        default=ExcelExpandMode.get_none_value(),
        description=ExcelExpandMode.get_description("Mode for automatically expanding the selection range"),
    ),
    cell_type_filter: int = Field(
        default=ExcelCellType.get_none_value(),
        description=ExcelCellType.get_description(),
    ),
) -> str:
    """Get the address of special cells in an Excel worksheet based on specified criteria.

    Returns:
        str: Address of the special cells range.

    Note:
        Windows-only feature.
    """

    range_ = get_range(
        sheet_range=sheet_range,
        book_name=book_name,
        sheet_name=sheet_name,
        expand_mode=expand_mode,
    )

    if cell_type_filter:
        return range_.api.SpecialCells(cell_type_filter).Address

    return range_.get_address()


@celery_task(queue="xlwings")
@macos_excel_request_permission
def get_values(
    sheet_range: str = Field(
        description="""Excel range to get data. If not specified, uses the entire used range of the sheet.
            Important: When using expand_mode, specify ONLY the starting cell (e.g., 'A1' not 'A1:B10')
            as the range will be automatically expanded.""",
        examples=["A1", "Sheet1!A1", "A1:C10"],
    ),
    book_name: str = Field(
        default="",
        description="Name of workbook to use. Optional.",
        examples=["Sales.xlsx", "Report2023.xlsx"],
    ),
    sheet_name: str = Field(
        default="",
        description="Name of sheet to use. Optional.",
        examples=["Sheet1", "Sales2023"],
    ),
    expand_mode: str = Field(
        default=ExcelExpandMode.get_none_value(),
        description=ExcelExpandMode.get_description("Mode for automatically expanding the selection range"),
    ),
    value_type: str = Field(
        default=ExcelGetValueType.get_none_value(),
        description=ExcelGetValueType.get_description(),
    ),
) -> str:
    """Get data from Excel workbook.

    Retrieves data from a specified Excel range. By default uses the active workbook and sheet
    if no specific book_name or sheet_name is provided.

    Important:
        When using expand_mode, specify ONLY the starting cell (e.g., 'A1') in sheet_range.
        The range will be automatically expanded based on the specified expand_mode.

    Returns:
        str: csv format
    """

    range_ = get_range(
        sheet_range=sheet_range,
        book_name=book_name,
        sheet_name=sheet_name,
        expand_mode=expand_mode,
    )

    if value_type == ExcelGetValueType.FORMULA2:
        data = range_.formula2
    else:
        data = range_.value

    if data is None:
        return ""

    # Convert single value to 2D list format
    if not isinstance(data, list):
        data = [[data]]
    elif data and not isinstance(data[0], list):
        data = [data]

    return convert_to_csv(data)


@celery_task(queue="xlwings")
@macos_excel_request_permission
def set_values(
    sheet_range: str = Field(
        description="Excel range where to write the data",
        examples=["A1", "B2:B10"],
    ),
    values: str = Field(
        description="CSV string. Values containing commas must be enclosed in double quotes (e.g. 'a,\"b,c\",d')",
    ),
    csv_abs_path: str = Field(
        default="",
        description="""Absolute path to the CSV file to read.
            If specified, this will override any value provided in the 'values' parameter.
            Either 'csv_abs_path' or 'values' must be provided, but not both.""",
        examples=["/path/to/data.csv"],
    ),
    book_name: str = Field(
        default="",
        description="Name of workbook to use. Optional.",
        examples=["Sales.xlsx", "Report2023.xlsx"],
    ),
    sheet_name: str = Field(
        default="",
        description="Name of sheet to use. Optional.",
        examples=["Sheet1", "Sales2023"],
    ),
) -> str:
    """Write data to a specified range in an Excel workbook.

    Performance Tips:
        - When setting values to multiple consecutive cells, it's more efficient to use a single call
          with a range (e.g. "A1:B10") rather than making multiple calls for individual cells.
        - For large datasets, using CSV format with range notation is significantly faster than
          making separate calls for each cell.

    Returns:
        str: Success message indicating values were set.

    Examples:
        >>> func(sheet_range="A1", values="v1,v2,v3\\nv4,v5,v6")  # grid using CSV
        >>> func(sheet_range="A1:B3", values="1,2\\n3,4\\n5,6")  # faster than 6 separate calls
        >>> func(sheet_range="Sheet1!A1:C2", values="[[1,2,3],[4,5,6]]")  # using JSON array
        >>> func(csv_abs_path="/path/to/data.csv", sheet_range="A1")  # import from CSV file
    """

    range_ = get_range(sheet_range=sheet_range, book_name=book_name, sheet_name=sheet_name)

    if csv_abs_path:
        csv_path: Path = validate_path(csv_abs_path)
        with csv_path.open("rt", encoding="utf-8") as f:
            values = csv_loads(f.read())

    if values is not None:
        if values.strip().startswith(("[", "{")):
            data = json_loads(values)
        else:
            data = csv_loads(values)
    else:
        raise ValueError("Either csv_abs_path or values must be provided.")

    range_.value = fix_data(sheet_range, data)

    return f"Successfully set values to {range_.address}."


@celery_task(queue="xlwings")
@macos_excel_request_permission
def set_styles(
    styles: str = Field(
        description="""Styles to apply. Supports two input formats:

1. Single-range format:
   - Specify one range and style options separated by semicolons.
     e.g. "A1:B2;background_color=255,255,0;bold=true"
   - Range specifiers can be:
     • "A1:B2"
     • "Sheet1!A1:C3"
     • "Book.xlsx!Sheet1!A1"

2. Multi-range CSV format (pipe-separated):
   - The first line is a header with exactly these columns:
     book_name, sheet_name, sheet_range, expand_mode,
     background_color, font_color, bold, italic
   - Each following line defines styles for one cell range.
   - Example:
     book_name|sheet_name|sheet_range|expand_mode|background_color|font_color|bold|italic
     Sales.xlsx|Sheet1|A1:B2||255,255,0|255,0,0|true|false
        """,
        examples=[
            # 단일 범위 포맷
            "A1:B2;background_color=255,255,0;bold=true",
            "Sheet1!A1:C5;font_color=255,0,0;italic=true",
            "Sales.xlsx!Sheet1!A1;background_color=0,255,0",
            # 멀티 범위 포맷 (CSV)
            """book_name|sheet_name|sheet_range|expand_mode|background_color|font_color|bold|italic
Sales.xlsx|Sheet1|A1:B2||255,255,0|255,0,0|true|false""",
        ],
    ),
) -> str:
    """
    Apply styles to specified ranges in an Excel workbook.

    Supports two input formats:

    1. Single-range format:
       "<sheet_range>;<option1>=<value>;<option2>=<value>;..."
       - Applies to one continuous range.

    2. Multi-range CSV format (pipe-separated):
       - Header row must include exactly these columns:
         book_name, sheet_name, sheet_range, expand_mode,
         background_color, font_color, bold, italic
       - Each subsequent row applies its styles to the given sheet_range.

    Parameters:
        styles (str): Style instructions in one of the two formats.

    Returns:
        str: Comma-separated addresses of ranges where styles were applied.
    """

    def make_tuple(rgb_code: str) -> tuple[int, int, int] | None:
        if not rgb_code:
            return None
        r, g, b = tuple(map(int, rgb_code.split(",")))
        return r, g, b

    def apply_styles(range_obj: xw.Range, style_dict: dict) -> None:
        if style_dict.get("background_color"):
            range_obj.color = make_tuple(style_dict["background_color"])
        if style_dict.get("font_color"):
            range_obj.font.color = make_tuple(style_dict["font_color"])
        if "bold" in style_dict:
            range_obj.font.bold = str(style_dict["bold"]).lower() == "true"
        if "italic" in style_dict:
            range_obj.font.italic = str(style_dict["italic"]).lower() == "true"

    def parse_single_style(style_str: str) -> tuple[str, str, str, dict]:
        """Parse single-range format: sheet_range;[options]"""
        parts = style_str.split(";")
        _range_spec = parts[0]

        _options = {}
        for part in parts[1:]:
            if "=" in part:
                key, value = part.split("=", 1)
                _options[key.strip()] = value.strip()

        range_parts = _range_spec.split("!")
        if len(range_parts) == 1:
            return "", "", range_parts[0], _options
        elif len(range_parts) == 2:
            return "", range_parts[0], range_parts[1], _options
        else:
            return range_parts[0], range_parts[1], range_parts[2], _options

    selected_ranges: list[xw.Range] = []

    if "|" in styles and "sheet_range|" in styles.lower():
        lines = [line.strip() for line in styles.strip().split("\n")]
        header = [col.lower().strip() for col in lines[0].split("|")]

        for line in lines[1:]:
            if not line:
                continue

            values = line.split("|")

            if len(values) < len(header):
                raise ValueError(f"Invalid CSV format. Expected {len(header)} columns, got {len(values)}.")

            row_data = dict(zip(header, values, strict=False))

            excel_range = get_range(
                sheet_range=row_data.get("sheet_range"),
                book_name=row_data.get("book_name", ""),
                sheet_name=row_data.get("sheet_name", ""),
                expand_mode=row_data.get("expand_mode", ""),
            )
            apply_styles(excel_range, row_data)
            selected_ranges.append(excel_range)
    else:
        book_name, sheet_name, range_spec, options = parse_single_style(styles)
        excel_range = get_range(
            sheet_range=range_spec,
            book_name=book_name,
            sheet_name=sheet_name,
            expand_mode=options.get("expand_mode", ""),
        )
        apply_styles(excel_range, options)
        selected_ranges.append(excel_range)

    addresses = ",".join(r.get_address() for r in selected_ranges)
    return f"Successfully set styles to {addresses}."


@celery_task(queue="xlwings")
@macos_excel_request_permission
def autofit(
    sheet_range: str = Field(
        description="Excel range to autofit",
        examples=["A1:D10", "A:E"],
    ),
    book_name: str = Field(
        default="",
        description="Name of workbook to use. Optional.",
        examples=["Sales.xlsx", "Report2023.xlsx"],
    ),
    sheet_name: str = Field(
        default="",
        description="Name of sheet to use. Optional.",
        examples=["Sheet1", "Sales2023"],
    ),
    expand_mode: str = Field(
        default=ExcelExpandMode.get_none_value(),
        description=ExcelExpandMode.get_description(
            "Mode for automatically expanding the selection range. "
            "All expand modes only work in the right/down direction"
        ),
    ),
) -> str:
    """Automatically adjusts column widths to fit the content in the specified Excel range.

    Returns:
        None

    Examples:
        >>> func("A1:D10")  # Autofit specific range
        >>> func("A:E")  # Autofit entire columns A through E
        >>> func("A:A", book_name="Sales.xlsx", sheet_name="Q1")  # Specific sheet
        >>> func("A1", expand_mode="table")  # Autofit table data
    """

    range_ = get_range(
        sheet_range=sheet_range,
        book_name=book_name,
        sheet_name=sheet_name,
        expand_mode=expand_mode,
    )
    range_.autofit()

    return "Successfully autofit."


@celery_task(queue="xlwings")
@macos_excel_request_permission
def set_formula(
    sheet_range: str = Field(
        description="Excel range where to apply the formula",
        examples=["A1", "B2:B10", "Sheet1!C1:C10"],
    ),
    formula: str = Field(
        description="Excel formula to set. Must start with '=' and follow Excel formula syntax.",
        examples=["=SUM(B1:B10)", "=A1*B1", "=VLOOKUP(A1, Sheet2!A:B, 2, FALSE)"],
    ),
    book_name: str = Field(
        default="",
        description="Name of workbook to use. Optional.",
        examples=["Sales.xlsx", "Report2023.xlsx"],
    ),
    sheet_name: str = Field(
        default="",
        description="Name of sheet to use. Optional.",
        examples=["Sheet1", "Sales2023"],
    ),
) -> str:
    """Set a formula in a specified range of an Excel workbook.

    Applies an Excel formula to the specified range using Excel's formula2 property,
    which supports modern Excel features and dynamic arrays. The formula will be
    evaluated by Excel after being set.

    Formula Behavior:
        - Must start with "=" and follow Excel formula syntax
        - Cell references are automatically adjusted for multiple cells
        - Supports array formulas (CSE formulas)
        - Uses modern dynamic array features via formula2 property

    Returns:
        None

    Examples:
        >>> func("A1", "=SUM(B1:B10)")  # Basic sum formula
        >>> func("C1:C10", "=A1*B1")  # Multiply columns
        >>> func("D1", "=VLOOKUP(A1, Sheet2!A:B, 2, FALSE)")  # Lookup
        >>> func("Sheet1!E1", "=AVERAGE(A1:D1)", book_name="Sales.xlsx")  # Average
    """

    range_ = get_range(sheet_range=sheet_range, book_name=book_name, sheet_name=sheet_name)
    range_.formula2 = formula

    return "Successfully set formula."


@celery_task(queue="xlwings")
@macos_excel_request_permission
def add_sheet(
    name: str = Field(
        default="",
        description="Name of the new sheet. Optional.",
        examples=["Sales2024", "Summary", "Data"],
    ),
    book_name: str = Field(
        default="",
        description="Name of workbook to add sheet to. Optional.",
        examples=["Sales.xlsx", "Report2023.xlsx"],
    ),
    at_start: bool = Field(
        default=False,
        description="If True, adds the sheet at the beginning of the workbook.",
    ),
    at_end: bool = Field(
        default=False,
        description="If True, adds the sheet at the end of the workbook.",
    ),
    before_sheet_name: str = Field(
        default="",
        description="Name of the sheet before which to insert the new sheet. Optional.",
        examples=["Sheet1", "Summary"],
    ),
    after_sheet_name: str = Field(
        default="",
        description="Name of the sheet after which to insert the new sheet. Optional.",
        examples=["Sheet1", "Summary"],
    ),
) -> str:
    """Add a new sheet to an Excel workbook.

    Creates a new worksheet in the specified workbook with options for positioning.
    Uses the active workbook by default if no book_name is provided.

    Position Priority Order:
        1. at_start: Places sheet at the beginning
        2. at_end: Places sheet at the end
        3. before_sheet_name: Places sheet before specified sheet
        4. after_sheet_name: Places sheet after specified sheet

    Returns:
        str: Success message indicating sheet creation

    Examples:
        >>> func("Sales2024")  # Add with specific name
        >>> func(at_end=True)  # Add at end with default name
        >>> func("Summary", book_name="Report.xlsx")  # Add to specific workbook
        >>> func("Data", before_sheet_name="Sheet2")  # Add before existing sheet
    """
    before_sheet = None
    after_sheet = None

    if book_name:
        book = xw.books[book_name]
    else:
        book = xw.books.active

    if at_start:
        before_sheet = book.sheets[0]
    elif at_end:
        after_sheet = book.sheets[-1]
    elif before_sheet_name:
        before_sheet = book.sheets[before_sheet_name]
    elif after_sheet_name:
        after_sheet = book.sheets[after_sheet_name]

    book.sheets.add(
        name=name or None,  # 빈 문자열일 경우 None으로 지정하여 디폴트 값으로 동작
        before=before_sheet,
        after=after_sheet,
    )

    return f"Successfully added a new sheet{' named ' + name if name else ''}."
