from typing import Any, List
import os
import datetime
from pathlib import Path
from mcp.server.fastmcp import FastMCP
import re

# Initialize FastMCP server
mcp = FastMCP("files")

# Helper function to resolve common paths
def resolve_path(path: str) -> str:
    """Resolve special paths like ~/Downloads to absolute paths."""
    if path.startswith("~"):
        path = os.path.expanduser(path)
    elif path.lower() == "downloads":
        path = os.path.expanduser("~/Downloads")
    elif path.lower() == "documents":
        path = os.path.expanduser("~/Documents")
    elif path.lower() == "desktop":
        path = os.path.expanduser("~/Desktop")
    return os.path.abspath(path)

@mcp.tool()
async def list_directory(path: str = ".") -> str:
    """List contents of a directory.
    
    Args:
        path: Directory path to list (can use ~ for home directory, or common names like Downloads)
    """
    try:
        # Convert to absolute path
        abs_path = resolve_path(path)
        if not os.path.exists(abs_path):
            return f"Path not found: {abs_path}"
            
        entries = os.listdir(abs_path)
        
        # Format the output
        results = []
        for entry in entries:
            full_path = os.path.join(abs_path, entry)
            stat = os.stat(full_path)
            size = stat.st_size
            modified = datetime.datetime.fromtimestamp(stat.st_mtime)
            type_ = "Directory" if os.path.isdir(full_path) else "File"
            
            results.append(f"{entry}\n  Type: {type_}\n  Size: {size:,} bytes\n  Modified: {modified}\n")
            
        return f"Contents of {abs_path}:\n\n" + "\n".join(results)
    except Exception as e:
        return f"Error listing directory: {str(e)}"

@mcp.tool()
async def search_files(pattern: str, path: str = ".", max_results: int = 10) -> str:
    """Search for files matching a pattern.
    
    Args:
        pattern: Search pattern (e.g., "*.txt" or "doc*")
        path: Directory to search in (defaults to current directory)
        max_results: Maximum number of results to return
    """
    try:
        abs_path = os.path.abspath(path)
        results = []
        
        for root, _, files in os.walk(abs_path):
            for file in files:
                if len(results) >= max_results:
                    break
                if Path(file).match(pattern):
                    full_path = os.path.join(root, file)
                    stat = os.stat(full_path)
                    size = stat.st_size
                    modified = datetime.datetime.fromtimestamp(stat.st_mtime)
                    results.append(f"{full_path}\n  Size: {size:,} bytes\n  Modified: {modified}\n")
        
        if not results:
            return f"No files matching '{pattern}' found in {abs_path}"
        
        return "\n".join(results)
    except Exception as e:
        return f"Error searching files: {str(e)}"

@mcp.tool()
async def read_file(path: str, max_size_mb: int = 10) -> str:
    """Read contents of a text file with size limits and chunked reading.
    
    Args:
        path: Path to the file to read
        max_size_mb: Maximum file size in MB (default 10MB)
    """
    try:
        abs_path = resolve_path(path)
        
        if not os.path.exists(abs_path):
            return f"File not found: {abs_path}"
            
        # Check file size first
        file_size = os.path.getsize(abs_path)
        max_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes
        
        if file_size > max_bytes:
            return f"File is too large ({file_size / 1024 / 1024:.1f}MB). Please export a smaller chat history (maximum {max_size_mb}MB)."
            
        # Read in chunks with a buffer
        content = []
        chunk_size = 1024 * 8  # 8KB chunks
        
        with open(abs_path, 'r', encoding='utf-8', errors='replace') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                content.append(chunk)
                
                # Safety check for memory usage
                if len(''.join(content)) > max_bytes:
                    return f"File content exceeded maximum size of {max_size_mb}MB while reading"
                    
        return ''.join(content)
            
    except UnicodeDecodeError:
        return "Error: File contains invalid characters. Please ensure it's a valid WhatsApp chat export."
    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp.tool()
async def find_whatsapp_chats(path: str = ".") -> str:
    """Find WhatsApp chat export files in the given directory."""
    try:
        abs_path = os.path.abspath(path)
        results = []
        
        def validate_whatsapp_file(file_path: str) -> bool:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    # Skip any initial non-timestamped messages
                    for line in f:
                        line = line.replace('\u200e', '').strip()
                        if not line:  # Skip empty lines
                            continue
                            
                        # Check if line starts with timestamp pattern
                        if line.startswith('['):
                            # Updated pattern to match WhatsApp export format
                            if re.match(r'^\[\d{1,2}/\d{1,2}/\d{2,4},\s+\d{1,2}:\d{2}:\d{2}(?:\s*[AP]M)?\]', line):
                                return True
                            
                    return False
            except Exception as e:
                print(f"Error validating WhatsApp file: {e}")
                return False

        for root, _, files in os.walk(abs_path):
            for file in files:
                if file.endswith('.txt'):
                    full_path = os.path.join(root, file)
                    if validate_whatsapp_file(full_path):
                        stat = os.stat(full_path)
                        size = stat.st_size
                        modified = datetime.datetime.fromtimestamp(stat.st_mtime)
                        results.append(f"Found WhatsApp chat: {full_path}\n  Size: {size:,} bytes\n  Modified: {modified}\n")
        
        if not results:
            return "No WhatsApp chat files found"
            
        return "\n".join(results)
    except Exception as e:
        return f"Error searching for WhatsApp chats: {str(e)}"

@mcp.tool()
async def get_whatsapp_directory() -> str:
    """Get or create the WhatsApp chat directory."""
    try:
        # Check standard locations
        possible_paths = [
            os.path.expanduser("~/Desktop/WhatsAppChat"),  # Desktop WhatsApp folder
            os.path.expanduser("~/Downloads"),  # Downloads folder
        ]
        
        def validate_whatsapp_file(path: str) -> bool:
            """Validate that the file is a WhatsApp chat export."""
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    # Skip any initial non-timestamped messages
                    for line in f:
                        line = line.replace('\u200e', '').strip()
                        if not line:  # Skip empty lines
                            continue
                            
                        # Check if line starts with timestamp pattern
                        if line.startswith('['):
                            # Updated pattern to match WhatsApp export format
                            if re.match(r'^\[\d{1,2}/\d{1,2}/\d{2,4},\s+\d{1,2}:\d{2}:\d{2}(?:\s*[AP]M)?\]', line):
                                return True
                            
                    return False
            except Exception as e:
                print(f"Error validating WhatsApp file: {e}")
                return False

        for path in possible_paths:
            if os.path.exists(path):
                # Check if any .txt files are WhatsApp chats
                for file in os.listdir(path):
                    if file.endswith('.txt'):
                        full_path = os.path.join(path, file)
                        if validate_whatsapp_file(full_path):
                            return path
                            
        # If no existing WhatsApp directory found, create Desktop/WhatsAppChat
        whatsapp_dir = os.path.expanduser("~/Desktop/WhatsAppChat")
        os.makedirs(whatsapp_dir, exist_ok=True)
        return whatsapp_dir
        
    except Exception as e:
        return f"Error finding WhatsApp directory: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport='stdio')