import os
from pathlib import Path
from typing import List, Dict, Any
from pydantic import BaseModel


class FileInfo(BaseModel):
    name: str
    path: str
    type: str
    size: int
    modified: float


class DirectoryListing(BaseModel):
    path: str
    files: List[FileInfo]
    directories: List[FileInfo]


def list_directory(path: str) -> DirectoryListing:
    """List contents of a directory"""
    try:
        directory_path = Path(path)
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory {path} does not exist")
        
        if not directory_path.is_dir():
            raise NotADirectoryError(f"{path} is not a directory")
        
        files = []
        directories = []
        
        for item in directory_path.iterdir():
            try:
                stat = item.stat()
                file_info = FileInfo(
                    name=item.name,
                    path=str(item),
                    type="file" if item.is_file() else "directory",
                    size=stat.st_size,
                    modified=stat.st_mtime
                )
                
                if item.is_file():
                    files.append(file_info)
                elif item.is_dir():
                    directories.append(file_info)
            except (PermissionError, OSError):
                continue
        
        return DirectoryListing(
            path=str(directory_path),
            files=sorted(files, key=lambda x: x.name.lower()),
            directories=sorted(directories, key=lambda x: x.name.lower())
        )
    
    except Exception as e:
        raise RuntimeError(f"Error listing directory {path}: {str(e)}")


def get_file_content(path: str, max_size: int = 1024 * 1024) -> str:
    """Get content of a text file"""
    try:
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"File {path} does not exist")
        
        if not file_path.is_file():
            raise IsADirectoryError(f"{path} is not a file")
        
        if file_path.stat().st_size > max_size:
            raise ValueError(f"File {path} is too large (max {max_size} bytes)")
        
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    
    except Exception as e:
        raise RuntimeError(f"Error reading file {path}: {str(e)}")
