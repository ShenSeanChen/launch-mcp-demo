# MCP (Management Control Panel) Server Tools

A collection of powerful command-line tools for file management, weather information, and WhatsApp chat analysis.

📹 Full YouTube Guide: [Youtube link](https://www.youtube.com/watch?v=ad1BxZufer8&list=PLE9hy4A7ZTmpGq7GHf5tgGFWh2277AeDR&index=8](https://www.youtube.com/watch?v=sfCBCyNyw7U)

🚀 X Post: [X link](https://x.com/ShenSeanChen/status/1895163913161109792)

☕️ Buy me a coffee: [Cafe Latte](https://buy.stripe.com/5kA176bA895ggog4gh)

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

## Claude Desktop Integration

To integrate these tools with Claude Desktop, you'll need to set up a configuration file at:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

Here's an example configuration:

```json
{
  "mcpServers": {
    "weather": {
      "command": "/path/to/your/python/environment",
      "args": [
        "--directory",
        "/path/to/launch-mcp-demo/weather",
        "run",
        "weather.py"
      ]
    },
    "files": {
      "command": "/path/to/your/python/environment",
      "args": [
        "--directory",
        "/path/to/launch-mcp-demo/files",
        "run",
        "files.py"
      ]
    }
  }
}
```

### Configuration Steps:

1. Create the Claude configuration directory if it doesn't exist
```bash
# macOS
mkdir -p ~/Library/Application\ Support/Claude

# Windows (in Command Prompt)
mkdir "%APPDATA%\Claude"

# Linux
mkdir -p ~/.config/Claude
```

2. Create the configuration file `claude_desktop_config.json` in the appropriate directory

3. Update the paths in the configuration:
   - Replace `/path/to/your/python/environment` with your Python interpreter path
   - Replace `/path/to/launch-mcp-demo` with the absolute path to your cloned repository

4. Verify the configuration:
   - Restart Claude Desktop
   - The MCP tools should now be available in your Claude conversations

Note: You can find your Python interpreter path using:
```bash
which python  # On macOS/Linux
where python  # On Windows
```

If you're using a virtual environment, make sure to use its Python interpreter path.
