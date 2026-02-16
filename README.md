# csv2latex_gui

Cross-platform GUI application to convert CSV and Excel files into LaTeX tables.

Built with [Flet](https://flet.dev/) - a Python framework for building cross-platform desktop, mobile, and web applications.

## Features

- **Multi-format support**: Import CSV (.csv) and Excel (.xlsx, .xls) files
- **Column selection**: Choose which columns to include in the LaTeX output
- **Decimal formatting**: Configure the number of decimal places for each numeric column
- **Clipboard support**: Copy generated LaTeX directly to clipboard
- **Dark/Light theme**: Toggle between themes
- **Cross-platform**: Runs on Windows, macOS, Linux, iOS, Android, and Web

## Installation

### Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Linux Requirements

On Linux, the file picker requires [Zenity](https://help.gnome.org/users/zenity/stable/):

```bash
sudo apt-get install zenity
```

## Usage

### Desktop App

```bash
uv run python main.py
```

Or with Flet CLI:

```bash
uv run flet run
```

## How to Use

1. **Select File**: Click "Select CSV or Excel File" to choose your data file
2. **Select Columns**: Check/uncheck the columns you want to include in the output
3. **Configure Decimals**: For numeric columns, select how many decimal places to display
4. **Generate LaTeX**: Click "Generate LaTeX" to create the table
5. **Copy to Clipboard**: Click "Copy to Clipboard" to copy the LaTeX code

## Development

### Install Dependencies

```bash
uv sync
```

### Run in Development Mode

```bash
uv run python main.py
```

## Building

Build for your target platform using Flet CLI:

```bash
# Windows
uv run flet build windows

# macOS
uv run flet build macos

# Linux
uv run flet build linux

# Web
uv run flet build web
```

For more details on building and signing, refer to the [Flet Packaging Guide](https://docs.flet.dev/publish/).

## Tech Stack

- **Framework**: [Flet](https://flet.dev/) - Cross-platform UI framework based on Flutter
- **Data Processing**: [pandas](https://pandas.pydata.org/) - Data manipulation library
- **Excel Support**: [openpyxl](https://openpyxl.readthedocs.io/) - Excel file reader

## Version

- Version: 0.2.0
- Updated: 2026-02-16

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Suggestions and contributions are welcome! Feel free to open an issue or submit a pull request.

---

Built with ❤️ by [RandomDataScience](https://randomds.com)