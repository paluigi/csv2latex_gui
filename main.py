"""CSV/Excel to LaTeX Converter - A Flet application."""

import flet
from flet import (
    Page,
    Text,
    Column,
    Container,
    Row,
    Button,
    Icons,
    FilePicker,
    FilePickerFileType,
    TextField,
    Checkbox,
    Dropdown,
    dropdown,
    SnackBar,
    Card,
    OutlinedButton,
    TextButton,
    Switch,
    Divider,
)
import pandas as pd
from pathlib import Path

try:
    from csv2latex_gui import __version__
except ImportError:
    __version__ = "0.2.0"


class Application:
    """Main application class for CSV/Excel to LaTeX converter."""

    def __init__(self):
        self.page: Page = None
        self.df: pd.DataFrame = None
        self.file_path: str = None
        self.latex_output: str = ""

        # UI control references
        self.file_picker: FilePicker = None
        self.file_name_text: Text = None
        self.column_container: Container = None
        self.output_field: TextField = None
        self.column_checkboxes: dict[str, Checkbox] = {}
        self.decimal_dropdowns: dict[str, Dropdown] = {}
        self.generate_button: Button = None
        self.copy_button: Button = None

    async def main(self, page: Page):
        """Main entry point for Flet application."""
        self.page = page

        # Configure page
        self.page.title = "CSV/Excel to LaTeX"
        self.page.window_width = 900
        self.page.window_height = 750
        self.page.scroll = "auto"
        self.page.padding = 20
        self.page.theme_mode = "light"

        # Build UI
        self._build_ui()

    def _build_ui(self):
        """Build the main UI layout."""
        # File picker is a service, no need to add to overlay
        self.file_picker = FilePicker()

        # File name display
        self.file_name_text = Text(
            "No file selected", size=14, color="grey", italic=True
        )

        # Column selection container (populated when file is loaded)
        self.column_container = Container(
            content=Text("Load a CSV or Excel file to see columns", color="grey"),
            padding=10,
        )

        # Output field
        self.output_field = TextField(
            label="LaTeX Output",
            multiline=True,
            read_only=True,
            min_lines=10,
            max_lines=20,
            expand=True,
        )

        # Buttons
        self.generate_button = Button(
            "Generate LaTeX",
            icon=Icons.TABLE_CHART,
            on_click=self._generate_latex,
            disabled=True,
        )
        self.copy_button = Button(
            "Copy to Clipboard",
            icon=Icons.COPY,
            on_click=self._copy_to_clipboard,
            disabled=True,
        )

        # Theme switch
        theme_switch = Switch(
            label="Dark Mode",
            value=False,
            on_change=self._toggle_theme,
        )

        # Main layout
        self.page.add(
            Column(
                [
                    # Header
                    Row(
                        [
                            Text("CSV/Excel to LaTeX Converter", size=28, weight="bold"),
                            Container(expand=True),
                            theme_switch,
                        ],
                        alignment="spaceBetween",
                    ),
                    Text(f"Version {__version__}", size=12, color="grey"),
                    Divider(),

                    # File selection
                    Card(
                        content=Container(
                            Column(
                                [
                                    Text("1. Select File", size=18, weight="bold"),
                                    Container(height=10),
                                    Row(
                                        [
                                            OutlinedButton(
                                                "Select CSV or Excel File",
                                                icon=Icons.UPLOAD_FILE,
                                                on_click=self._pick_file,
                                            ),
                                            self.file_name_text,
                                        ],
                                        alignment="start",
                                    ),
                                ],
                                spacing=5,
                            ),
                            padding=15,
                        )
                    ),
                    Container(height=10),

                    # Column selection
                    Card(
                        content=Container(
                            Column(
                                [
                                    Row(
                                        [
                                            Text("2. Select Columns", size=18, weight="bold"),
                                            Container(expand=True),
                                            OutlinedButton(
                                                "Select All",
                                                on_click=self._select_all_columns,
                                            ),
                                            OutlinedButton(
                                                "Deselect All",
                                                on_click=self._deselect_all_columns,
                                            ),
                                        ],
                                    ),
                                    Container(height=10),
                                    self.column_container,
                                ],
                                spacing=5,
                            ),
                            padding=15,
                        )
                    ),
                    Container(height=10),

                    # Generate and copy buttons
                    Card(
                        content=Container(
                            Row(
                                [
                                    self.generate_button,
                                    self.copy_button,
                                    Container(expand=True),
                                    OutlinedButton(
                                        "Clear",
                                        icon=Icons.CLEAR,
                                        on_click=self._clear_all,
                                    ),
                                ],
                                alignment="start",
                            ),
                            padding=15,
                        )
                    ),
                    Container(height=10),

                    # Output
                    Card(
                        content=Container(
                            Column(
                                [
                                    Text("3. LaTeX Output", size=18, weight="bold"),
                                    Container(height=10),
                                    self.output_field,
                                ],
                                spacing=5,
                            ),
                            padding=15,
                        )
                    ),

                    # Footer
                    Container(height=20),
                    Row(
                        [
                            Text("Built by Luigi with Flet", size=12, color="grey"),
                            Container(expand=True),
                            TextButton(
                                "GitHub Repository",
                                on_click=lambda e: self.page.launch_url(
                                    "https://github.com/paluigi/csv2latex_gui"
                                ),
                            ),
                        ],
                    ),
                ],
                scroll="auto",
            )
        )

    async def _pick_file(self, e):
        """Open file picker and handle selection."""
        files = await self.file_picker.pick_files(
            allowed_extensions=["csv", "xlsx", "xls"],
            allow_multiple=False,
            file_type=FilePickerFileType.CUSTOM,
        )

        if not files:
            return

        file = files[0]
        self.file_path = file.path

        # Update file name display
        self.file_name_text.value = f"Selected: {file.name}"
        self.file_name_text.color = "green"
        self.file_name_text.italic = False
        self.file_name_text.update()

        # Load the file
        self._load_file()

    def _load_file(self):
        """Load CSV or Excel file into DataFrame."""
        try:
            path = Path(self.file_path)
            suffix = path.suffix.lower()

            if suffix == ".csv":
                self.df = pd.read_csv(self.file_path)
            elif suffix in [".xlsx", ".xls"]:
                self.df = pd.read_excel(self.file_path)
            else:
                self._show_snack_bar("Unsupported file format", error=True)
                return

            # Build column selection UI
            self._build_column_selection()

            # Enable generate button
            self.generate_button.disabled = False
            self.generate_button.update()

            self._show_snack_bar(f"Loaded {len(self.df)} rows, {len(self.df.columns)} columns")

        except Exception as ex:
            self._show_snack_bar(f"Error loading file: {str(ex)}", error=True)

    def _build_column_selection(self):
        """Build the column selection UI."""
        self.column_checkboxes.clear()
        self.decimal_dropdowns.clear()

        # Identify numeric columns
        numeric_cols = self.df.select_dtypes(include=["number"]).columns.tolist()

        # Build column checkboxes
        column_rows = []
        for col in self.df.columns:
            is_numeric = col in numeric_cols

            checkbox = Checkbox(
                label=f"{col} {'(numeric)' if is_numeric else '(text)'}",
                value=True,
                on_change=self._on_column_change,
            )
            self.column_checkboxes[col] = checkbox

            row_controls = [checkbox]

            if is_numeric:
                # Add decimal dropdown for numeric columns
                decimal_dropdown = Dropdown(
                    label="Decimals",
                    value="2",
                    options=[dropdown.Option(str(i)) for i in range(7)],  # 0-6
                    width=100,
                )
                self.decimal_dropdowns[col] = decimal_dropdown
                row_controls.append(Container(expand=True))
                row_controls.append(decimal_dropdown)

            column_rows.append(Row(row_controls, alignment="start"))

        # Update column container
        self.column_container.content = Column(column_rows, scroll="auto")
        self.column_container.update()

    def _on_column_change(self, e):
        """Handle column checkbox change."""
        # Enable/disable generate button based on selection
        any_selected = any(cb.value for cb in self.column_checkboxes.values())
        self.generate_button.disabled = not any_selected
        self.generate_button.update()

    def _select_all_columns(self, e):
        """Select all columns."""
        for checkbox in self.column_checkboxes.values():
            checkbox.value = True
            checkbox.update()
        self._on_column_change(None)

    def _deselect_all_columns(self, e):
        """Deselect all columns."""
        for checkbox in self.column_checkboxes.values():
            checkbox.value = False
            checkbox.update()
        self._on_column_change(None)

    def _generate_latex(self, e):
        """Generate LaTeX table from selected columns."""
        if self.df is None:
            self._show_snack_bar("Please load a file first", error=True)
            return

        # Get selected columns
        selected_cols = [
            col for col, checkbox in self.column_checkboxes.items() if checkbox.value
        ]

        if not selected_cols:
            self._show_snack_bar("Please select at least one column", error=True)
            return

        try:
            # Filter to selected columns
            df_export = self.df[selected_cols].copy()

            # Build formatters dictionary for numeric columns
            formatters = {}
            for col in selected_cols:
                if col in self.decimal_dropdowns:
                    decimals = int(self.decimal_dropdowns[col].value)
                    # Create a format function for this column
                    formatters[col] = lambda x, d=decimals: f"{x:.{d}f}" if pd.notna(x) else ""

            # Generate LaTeX with formatters
            self.latex_output = df_export.to_latex(index=False, escape=False, formatters=formatters)

            # Update output field
            self.output_field.value = self.latex_output
            self.output_field.update()

            # Enable copy button
            self.copy_button.disabled = False
            self.copy_button.update()

            self._show_snack_bar("LaTeX table generated successfully!")

        except Exception as ex:
            self._show_snack_bar(f"Error generating LaTeX: {str(ex)}", error=True)

    async def _copy_to_clipboard(self, e):
        """Copy LaTeX output to clipboard."""
        if not self.latex_output:
            self._show_snack_bar("No LaTeX output to copy", error=True)
            return

        try:
            await self.page.clipboard.set(self.latex_output)
            self._show_snack_bar("Copied to clipboard!")
        except Exception as ex:
            self._show_snack_bar(f"Error copying to clipboard: {str(ex)}", error=True)

    def _clear_all(self, e):
        """Clear all inputs and outputs."""
        self.df = None
        self.file_path = None
        self.latex_output = ""

        # Reset UI
        self.file_name_text.value = "No file selected"
        self.file_name_text.color = "grey"
        self.file_name_text.italic = True
        self.file_name_text.update()

        self.column_container.content = Text(
            "Load a CSV or Excel file to see columns", color="grey"
        )
        self.column_container.update()

        self.output_field.value = ""
        self.output_field.update()

        self.generate_button.disabled = True
        self.generate_button.update()

        self.copy_button.disabled = True
        self.copy_button.update()

        self._show_snack_bar("Cleared all")

    def _toggle_theme(self, e):
        """Toggle between light and dark theme."""
        is_dark = e.control.value
        self.page.theme_mode = "dark" if is_dark else "light"
        self.page.update()
        self._show_snack_bar(f"Theme changed to {'dark' if is_dark else 'light'} mode")

    def _show_snack_bar(self, message: str, error: bool = False):
        """Display a snack bar message."""
        snackbar = SnackBar(
            Text(message, color="white" if error else None),
            bgcolor="red" if error else None,
        )
        self.page.show_dialog(snackbar)


if __name__ == "__main__":
    app = Application()
    flet.run(main=app.main)