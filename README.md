# MCP (Management Control Panel) Server Tools

A collection of powerful tools for AI assistants integration - both Claude Desktop and Cursor IDE.

## Overview

This repository contains two distinct sets of integrations:

1. **Claude Desktop Tools** - Python-based tools for file management, weather information, and WhatsApp chat analysis
2. **Cursor IDE Integrations** - Direct service integrations with Supabase, Stripe, and GitHub

## Claude Desktop Tools

### Features

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

### Prerequisites

- Python 3.13 or later
- pip (Python package installer)

### Installation

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

### Usage

#### Weather Tools

```python
from weather.weather import get_alerts, get_forecast

# Get weather alerts for California
alerts = await get_alerts("CA")

# Get weather forecast for San Francisco
forecast = await get_forecast(37.7749, -122.4194)
```

#### File Management Tools

```python
from files.files import list_directory, search_files, read_file

# List contents of Downloads directory
contents = await list_directory("~/Downloads")

# Search for PDF files
pdfs = await search_files("*.pdf", "~/Documents")

# Read a text file
text = await read_file("path/to/file.txt")
```

#### WhatsApp Chat Tools

```python
from whatsapp.whatsapp import analyze_chat, find_chats

# Find WhatsApp chat exports
chats = await find_chats()

# Analyze a chat file
stats = await analyze_chat("path/to/chat.txt")
```

### Claude Desktop Integration

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

#### Configuration Steps:

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

## Cursor IDE Integrations

The new release adds powerful integrations for Cursor IDE with Supabase, Stripe, and GitHub MCP servers. 
This allows direct interaction with these services while working in Cursor.

### Features

- **Supabase Integration**
  - Database management and queries
  - Schema operations
  - User authentication

- **Stripe Integration**
  - Payment processing
  - Customer management
  - Subscription handling

- **GitHub Integration**
  - Repository management
  - Pull request workflows
  - Issue tracking

### Prerequisites

- Cursor IDE
- Node.js and npm (for Supabase and Stripe)
- Docker (for GitHub)
- API keys/tokens for each service

### Setup Instructions for Cursor MCP

To set up the Cursor MCP integration, you'll need to create/modify the `.cursor/mcp.json` file in your project:

1. Create the `.cursor` directory in your project root (if it doesn't exist)
```bash
mkdir -p .cursor
```

2. Create a `mcp.json` file with your service configurations:
```json
{
  "mcpServers": {
    "stripe": {
      "command": "npx",
      "args": [
        "-y", 
        "@stripe/mcp"
      ],
      "env": {
        "STRIPE_SECRET_KEY": "your_stripe_test_key_here"
      }
    },
    "supabase": {
      "command": "npx",
      "args": [
        "-y",
        "@supabase/mcp-server-supabase@latest",
        "--access-token",
        "your_supabase_access_token_here"
      ]
    },
    "github": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_github_personal_access_token_here"
      }
    }
  }
}
```

3. Replace the placeholder values with your actual API keys and tokens:
   - `your_stripe_test_key_here`: Your Stripe test API key
   - `your_supabase_access_token_here`: Your Supabase access token
   - `your_github_personal_access_token_here`: Your GitHub personal access token

### Service-Specific Setup

#### Supabase Setup

1. Create a Supabase account at https://supabase.com
2. Create a new project in the Supabase dashboard
3. Get your access token from Account -> API Tokens
4. Add the token to your `mcp.json` file

#### Stripe Setup

1. Create a Stripe account at https://stripe.com
2. Get your API test key from the Stripe Dashboard -> Developers -> API keys
3. Add the test key to your `mcp.json` file
4. *Important*: Never use production keys in development environments

#### GitHub Setup

1. Create a personal access token at https://github.com/settings/tokens
2. Ensure the token has appropriate permissions (repo, workflow, etc.)
3. Add the token to your `mcp.json` file
4. Ensure Docker is installed and running for the GitHub MCP server

### Video Demo Guide

Our new release includes three demo videos showcasing the integration of these services:

#### Video 1: Supabase Database Operations in Cursor
- Creating and querying Supabase tables
- Managing database schema
- Authenticating users through Supabase

#### Video 2: Stripe Payment Processing in Cursor
- Setting up customer accounts
- Creating and managing payment methods
- Processing test payments
- Viewing transaction history

#### Video 3: GitHub Repository Management in Cursor
- Creating and managing repositories
- Handling pull requests and issues
- Committing code changes
- Managing repository settings

Stay tuned for these demo videos, which will provide a comprehensive guide to leveraging these powerful integrations in your Cursor IDE workflow!

## General Information

### Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Acknowledgments

- National Weather Service (NWS) for their public API
- The MCP framework developers
- Supabase, Stripe and GitHub for their developer tools and APIs
