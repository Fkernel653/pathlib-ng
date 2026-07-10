"""Custom Path implementation mimicking pathlib.Path."""

import os
from typing import Iterator, Union


class Path:
    """Custom Path implementation."""

    def __init__(self, *args):
        """Initialize Path object.

        Args:
            *args: Path components to join.
        """
        if not args:
            self._path = ""
        else:
            parts = []
            for arg in args:
                if isinstance(arg, Path):
                    parts.append(str(arg))
                elif hasattr(arg, "__fspath__"):
                    parts.append(os.fspath(arg))
                else:
                    parts.append(str(arg))

            parts = [p for p in parts if p]
            self._path = os.path.join(*parts) if parts else ""

    def __str__(self) -> str:
        return self._path

    def __repr__(self) -> str:
        return f"Path('{self._path}')"

    def __fspath__(self) -> str:
        return self._path

    def __truediv__(self, other: Union[str, "Path"]) -> "Path":
        return Path(self._path, str(other))

    def __rtruediv__(self, other: str) -> "Path":
        return Path(str(other), self._path)

    @property
    def parent(self) -> "Path":
        """Return parent directory."""
        parts = self._path.rsplit("/", 1)
        return Path(parts[0] if len(parts) > 1 else "")

    @property
    def name(self) -> str:
        """Return file/directory name."""
        return self._path.rsplit("/", 1)[-1] if "/" in self._path else self._path

    @property
    def suffix(self) -> str:
        """Return file extension."""
        name = self.name
        return name[name.rfind(".") :] if "." in name else ""

    @property
    def stem(self) -> str:
        """Return filename without extension."""
        name = self.name
        return name[: name.rfind(".")] if "." in name else name

    def exists(self) -> bool:
        """Check if path exists."""
        return os.path.exists(self._path)

    def is_dir(self) -> bool:
        """Check if path is a directory."""
        return os.path.isdir(self._path)

    def is_file(self) -> bool:
        """Check if path is a file."""
        return os.path.isfile(self._path)

    def mkdir(self, parents: bool = False, exist_ok: bool = False) -> None:
        """Create directory."""
        if parents:
            os.makedirs(self._path, exist_ok=exist_ok)
        else:
            os.mkdir(self._path)

    def rmdir(self) -> None:
        """Remove empty directory."""
        os.rmdir(self._path)

    def unlink(self, missing_ok: bool = False) -> None:
        """Remove file."""
        try:
            os.unlink(self._path)
        except FileNotFoundError:
            if not missing_ok:
                raise

    def rename(self, target: Union[str, "Path"]) -> "Path":
        """Rename path."""
        os.rename(self._path, str(target))
        return Path(target)

    def read_text(self, encoding: str = "utf-8") -> str:
        """Read file content as text."""
        with open(self._path, "r", encoding=encoding) as f:
            return f.read()

    def write_text(self, data: str, encoding: str = "utf-8") -> int:
        """Write text to file."""
        with open(self._path, "w", encoding=encoding) as f:
            return f.write(data)

    def read_bytes(self) -> bytes:
        """Read file content as bytes."""
        with open(self._path, "rb") as f:
            return f.read()

    def write_bytes(self, data: bytes) -> int:
        """Write bytes to file."""
        with open(self._path, "wb") as f:
            return f.write(data)

    def resolve(self) -> "Path":
        """Resolve absolute path."""
        return Path(os.path.abspath(self._path))

    def expanduser(self) -> "Path":
        """Expand ~ to user home."""
        return Path(os.path.expanduser(self._path))

    def absolute(self) -> "Path":
        """Return absolute path."""
        return Path(os.path.abspath(self._path))

    def iterdir(self) -> Iterator["Path"]:
        """Iterate over directory contents."""
        for item in os.listdir(self._path):
            yield Path(self._path, item)

    def glob(self, pattern: str) -> Iterator["Path"]:
        """Glob pattern."""
        import glob

        for item in glob.glob(os.path.join(self._path, pattern)):
            yield Path(item)

    def rglob(self, pattern: str) -> Iterator["Path"]:
        """Recursive glob pattern."""
        import glob

        for item in glob.glob(os.path.join(self._path, "**", pattern), recursive=True):
            yield Path(item)

    def stat(self):
        """Return stat info."""
        return os.stat(self._path)

    def touch(self, exist_ok: bool = True) -> None:
        """Create empty file."""
        if not exist_ok and self.exists():
            raise FileExistsError(f"File exists: {self._path}")
        self.parent.mkdir(parents=True, exist_ok=True)
        with open(self._path, "a"):
            os.utime(self._path, None)

    def absolute_path(self) -> str:
        """Return absolute path string."""
        return os.path.abspath(self._path)

    @classmethod
    def home(cls) -> "Path":
        """Return user home directory."""
        return cls(os.path.expanduser("~"))

    @classmethod
    def cwd(cls) -> "Path":
        """Return current working directory."""
        return cls(os.getcwd())
