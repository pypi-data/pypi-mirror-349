from typing import Optional, Any
from pathlib import Path

from ._connections import get_storage_client, get_storage_fs
from .config import get_settings

def has_file(name: str, prefix: str = 'LAS', settings_override: Optional[dict[str, Any]] = None) -> bool:
    settings = get_settings(**(settings_override or {}))
    fs = get_storage_fs(settings_override=settings_override)

    BASE = Path(settings.storage_bucket_name) / prefix
    return fs.exists(str(BASE / name))


def download_file(name: str, prefix: str = 'LAS', target: str = ".", settings_override: Optional[dict[str, Any]] = None) -> Path:
    settings = get_settings(**(settings_override or {}))
    fs = get_storage_fs(settings_override=settings_override)

    BASE = Path(settings.storage_bucket_name) / prefix
    path = BASE / name
    
    if not fs.exists(str(path)):
        raise FileNotFoundError(f"File {path} not found")
    
    target = Path(target)
    if not target.is_dir():
        target = target.parent

    fs.download(str(path), str(target))

    return target


