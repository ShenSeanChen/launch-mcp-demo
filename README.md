# MCP (Management Control Panel) Server Tools

A collection of powerful command-line tools for file management, weather information, and WhatsApp chat analysis.

## Features

- **Weather Tools**
  - Get weather alerts for any US state
  - Get detailed weather forecasts by location coordinates
  - Uses the National Weather Service (NWS) API

- **File Management Tools**
  - List directory contents with detailed information
  - Search files with pattern matching
  - Read and analyze text files
  
- **WhatsApp Chat Tools**
  - Find and analyze WhatsApp chat exports
  - Generate chat statistics
  - Parse and read WhatsApp chat files

## Prerequisites

- Python 3.13 or later
- pip (Python package installer)

## Installation

1. Clone the repository
```bash
git clone https://github.com/ShenSeanChen/launch-mcp-demo.git
cd launch-mcp-demo
```

2. Create and activate a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the package and dependencies
```bash
pip install -e .
```

## Usage

### Weather Tools

```python
from weather.weather import get_alerts, get_forecast

# Get weather alerts for California
alerts = await get_alerts("CA")

# Get weather forecast for San Francisco
forecast = await get_forecast(37.7749, -122.4194)
```

### File Management Tools

```python
from files.files import list_directory, search_files, read_file

# List contents of Downloads directory
contents = await list_directory("~/Downloads")

# Search for PDF files
pdfs = await search_files("*.pdf", "~/Documents")

# Read a text file
text = await read_file("path/to/file.txt")
```

### WhatsApp Chat Tools

```python
from whatsapp.whatsapp import analyze_chat, find_chats

# Find WhatsApp chat exports
chats = await find_chats()

# Analyze a chat file
stats = await analyze_chat("path/to/chat.txt")
```

## Configuration

No additional configuration is required. The tools use public APIs and local file system access.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- National Weather Service (NWS) for their public API
- The MCP framework developers
