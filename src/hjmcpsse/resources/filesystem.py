"""
File system resource implementation for MCP server
"""

import os
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class FileInfo:
    """Information about a file"""
    name: str
    size: int
    is_directory: bool
    path: str


@dataclass
class DirectoryListing:
    """Directory listing with files and subdirectories"""
    path: str
    files: List[FileInfo]
    directories: List[FileInfo]


def list_directory(path: str) -> DirectoryListing:
    """List contents of a directory
    
    Args:
        path: Directory path to list
        
    Returns:
        DirectoryListing with files and subdirectories
        
    Raises:
        OSError: If directory cannot be accessed
    """
    directory_path = Path(path).resolve()
    
    if not directory_path.exists():
        raise OSError(f"Directory does not exist: {path}")
    
    if not directory_path.is_dir():
        raise OSError(f"Path is not a directory: {path}")
    
    files = []
    directories = []
    
    try:
        for item in directory_path.iterdir():
            try:
                stat_info = item.stat()
                file_info = FileInfo(
                    name=item.name,
                    size=stat_info.st_size,
                    is_directory=item.is_dir(),
                    path=str(item)
                )
                
                if item.is_dir():
                    directories.append(file_info)
                else:
                    files.append(file_info)
                    
            except (OSError, PermissionError):
                continue
                
    except PermissionError:
        raise OSError(f"Permission denied accessing directory: {path}")
    
    files.sort(key=lambda x: x.name.lower())
    directories.sort(key=lambda x: x.name.lower())
    
    return DirectoryListing(
        path=str(directory_path),
        files=files,
        directories=directories
    )


def get_file_content(path: str, max_size: int = 1024 * 1024) -> str:
    """Get content of a text file
    
    Args:
        path: File path to read
        max_size: Maximum file size to read (default 1MB)
        
    Returns:
        File content as string
        
    Raises:
        OSError: If file cannot be accessed or is too large
    """
    file_path = Path(path).resolve()
    
    if not file_path.exists():
        raise OSError(f"File does not exist: {path}")
    
    if not file_path.is_file():
        raise OSError(f"Path is not a file: {path}")
    
    try:
        stat_info = file_path.stat()
        if stat_info.st_size > max_size:
            raise OSError(f"File too large: {stat_info.st_size} bytes (max {max_size})")
        
        encodings = ['utf-8', 'utf-16', 'latin-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        
        with open(file_path, 'rb') as f:
            content = f.read()
            return f"Binary file ({len(content)} bytes): {content[:100].hex()}..."
            
    except PermissionError:
        raise OSError(f"Permission denied reading file: {path}")
    except Exception as e:
        raise OSError(f"Error reading file {path}: {str(e)}")
