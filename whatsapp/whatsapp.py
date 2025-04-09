from typing import Dict, List, Optional
from datetime import datetime
import re
from pathlib import Path
from collections import Counter
from mcp.server.fastmcp import FastMCP
import os

# Initialize FastMCP server
mcp = FastMCP("whatsapp")

def get_chat_directory() -> str:
    """Get the WhatsApp chat directory."""
    paths = [
        os.path.expanduser("~/Desktop/WhatsAppChat"),
        os.path.expanduser("~/Downloads"),
    ]
    
    for path in paths:
        if os.path.exists(path):
            return path
            
    # Create default directory if none exists
    whatsapp_dir = os.path.expanduser("~/Desktop/WhatsAppChat")
    os.makedirs(whatsapp_dir, exist_ok=True)
    return whatsapp_dir

@mcp.tool()
async def find_chats() -> str:
    """Find all WhatsApp chat exports."""
    chat_dir = get_chat_directory()
    pattern = r'^\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\]'
    
    found_chats = []
    for root, _, files in os.walk(chat_dir):
        for file in files:
            if file.endswith('.txt'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        if re.match(pattern, f.readline().strip()):
                            found_chats.append(path)
                except:
                    continue
                    
    if not found_chats:
        return "No WhatsApp chat exports found"
        
    return "\n".join(f"- {chat}" for chat in found_chats)

class WhatsAppChat:
    def __init__(self, chat_path: str = None):
        if chat_path is None:
            # Auto-find the most recent WhatsApp chat file
            whatsapp_dir = self._get_whatsapp_directory()  # Sync version
            chat_files = [f for f in os.listdir(whatsapp_dir) if f.endswith('.txt')]
            if not chat_files:
                raise ValueError("No WhatsApp chat files found")
            chat_path = os.path.join(whatsapp_dir, sorted(chat_files)[-1])  # Get most recent
        
        if not self._validate_whatsapp_file(chat_path):
            raise ValueError("Not a valid WhatsApp chat export file")
        self.messages = self._parse_chat_file(chat_path)
    
    def _parse_chat_file(self, path: str) -> List[Dict]:
        """Parse WhatsApp chat export file.
        
        Args:
            path: Path to the WhatsApp chat .txt file
            
        Returns:
            List of message dictionaries with date, sender, and content
        """
        messages = []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    # Skip empty lines
                    if not line.strip():
                        continue
                        
                    # Check if line starts with timestamp
                    if line.startswith('['):
                        try:
                            # Split timestamp and content
                            timestamp_end = line.find(']')
                            if timestamp_end == -1:
                                continue
                                
                            timestamp = line[1:timestamp_end]
                            content = line[timestamp_end + 2:]  # Skip "] "
                            
                            # Split sender and message
                            if ':' in content:
                                sender, message = content.split(':', 1)
                                messages.append({
                                    'timestamp': timestamp.strip(),
                                    'sender': sender.strip(),
                                    'content': message.strip()
                                })
                        except:
                            continue
                            
            return messages
        except Exception as e:
            raise ValueError(f"Error parsing chat file: {str(e)}")

    def _validate_whatsapp_file(self, path: str) -> bool:
        """Validate that the file is a WhatsApp chat export."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                return bool(re.match(r'^\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\]', first_line))
        except:
            return False

    def _get_whatsapp_directory(self) -> str:
        """Sync version of get_whatsapp_directory."""
        try:
            # Check standard locations
            possible_paths = [
                os.path.expanduser("~/Desktop/WhatsAppChat"),  # Desktop WhatsApp folder
                os.path.expanduser("~/Downloads"),  # Downloads folder
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    # Check if any .txt files are WhatsApp chats
                    for file in os.listdir(path):
                        if file.endswith('.txt'):
                            full_path = os.path.join(path, file)
                            try:
                                with open(full_path, 'r', encoding='utf-8') as f:
                                    first_line = f.readline().strip()
                                    if re.match(r'^\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\]', first_line):
                                        return path
                            except:
                                continue
                                
            # If no existing WhatsApp directory found, create one
            whatsapp_dir = os.path.expanduser("~/Desktop/WhatsAppChat")
            os.makedirs(whatsapp_dir, exist_ok=True)
            return whatsapp_dir
            
        except Exception as e:
            raise ValueError(f"Error finding WhatsApp directory: {str(e)}")

@mcp.tool()
async def analyze_chat(path: str) -> str:
    """Analyze a WhatsApp chat export file and generate statistics.
    
    Args:
        path: Path to the WhatsApp chat export file (.txt)
    """
    try:
        chat = WhatsAppChat(path)
        
        # Basic statistics
        total_messages = len(chat.messages)
        senders = Counter(msg['sender'] for msg in chat.messages)
        
        if not total_messages:
            return "No messages found in the chat file."
        
        # Format statistics
        stats = f"Chat Analysis:\nTotal Messages: {total_messages}\n\n"
        stats += "Top Participants:\n"
        
        for sender, count in senders.most_common(5):
            percentage = (count / total_messages) * 100
            stats += f"- {sender}: {count} messages ({percentage:.1f}%)\n"
            
        return stats
    except Exception as e:
        return f"Error analyzing chat: {str(e)}"

@mcp.tool()
async def read_whatsapp_chat(path: str) -> str:
    """Read a WhatsApp chat export file.
    
    Args:
        path: Path to the WhatsApp chat .txt file
    """
    try:
        # Simple file read with UTF-8 encoding
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
            
    except Exception as e:
        return f"Error reading WhatsApp chat: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport='stdio')
