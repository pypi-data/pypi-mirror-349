from pathlib import Path
import json
import yaml
from pprint import pformat
from datetime import datetime, timedelta
import asyncio
import threading
import time

class DearDir:
    """
    DearDir is a utility class for validating and optionally creating
    file and folder structures based on a defined schema.

    Main features:
    - Validate project directory structures against JSON/YAML/dict/list schema
    - Automatically create missing files/folders if enabled
    - Live asynchronous monitoring with configurable interval

    Attributes:
        entitys (list[Path]): List of root paths to validate.
        schema (dict | list): Parsed schema representing the desired file structure.
        missing (set): Set of missing paths found during the last validation.
        created (set): Set of paths that were created when create_missing is enabled.
        create_missing (bool): Whether missing paths should be automatically created.
        _stop_live (bool): Flag to interrupt live validation loop.
        info (dict): Combined status information for representation.
    """

    def __init__(self, root_paths: list[Path] = None, schema: Path | dict | list = None):
        """
        Initialize the DearDir instance.

        Args:
            root_paths (list[Path], optional): Root directories to be validated.
            schema (Path | dict | list, optional): File path or object defining the target structure.
        """
        self.entitys: list[Path] = list(root_paths) if root_paths else []
        self.schema: dict | list = self._load_schema(schema) if schema else []
        self.missing: set = set()
        self.created: set = set()

        self.create_missing: bool = False 
        self._stop_live = False

        self.info = {"entitys": self.entitys,
                     "schema": self.schema,
                     "missing": self.missing,
                     "created": self.created}


    def __repr__(self):
        """
        Returns a formatted string representation of the current state.

        Returns:
            str: Summary of root paths, schema, missing and created items.
        """
        return (
            f"<{self.__class__.__name__}>\n"
            f"{pformat(self.info, indent=4)}\n"
        )


    def add_path(self, path: Path):
        """
        Add a new root path if it exists.

        Args:
            path (Path): Path to an existing file or directory.

        Raises:
            FileNotFoundError: If the path does not exist.
        """
        if path.exists():
            self.entitys.append(path)
        else:
            raise FileNotFoundError(f"File does not exist {path}")


    def remove_path(self, path: Path):
        """
        Remove a root path from the list.

        Args:
            path (Path): Path to remove.

        Raises:
            ValueError: If the path is not in the list.
        """
        try:
            self.entitys.remove(path)
        except ValueError:
            raise ValueError(f"Path {path} not found in entitys.")
        

    def set_schema(self, schema: Path | dict | list):
        """
        Set or reload the schema used for structure validation.

        Args:
            schema (Path | dict | list): Schema as file path or inline object.
        """
        self.schema = self._load_schema(schema)


    def validate(self):
        """
        Validates the current root paths against the loaded schema.
        Stores any missing elements in self.missing. If create_missing is True,
        missing paths will be created automatically.

        Raises:
            AttributeError: If schema or root paths are not defined.
        """
        def _recursive_check(entry: object, root: Path, missing: set):
            if isinstance(entry, str | int):
                this_path: Path = root / str(entry)
                if not this_path.exists():                    
                    if self.create_missing:
                        if not self._try_mkpath(this_path):
                            missing.add(this_path)
                    else:
                        missing.add(this_path)

            elif isinstance(entry, list):
                for e in entry:
                    if isinstance(e, list):
                        raise ValueError("Nested lists are not allowed in schema. Use dicts for structure.")
                    elif isinstance(e, dict):
                        _recursive_check(e, root, missing)
                    else:
                        this_path = root / str(e)
                        if not this_path.exists():
                            if self.create_missing:
                                if not self._try_mkpath(this_path):
                                    missing.add(this_path)
                            else:
                                missing.add(this_path)


            elif isinstance(entry, dict):
                for directory, child in entry.items():
                    parent = root / str(directory)
                    if not parent.exists():                        
                        if self.create_missing and self._try_mkpath(parent):
                            _recursive_check(child, parent, missing)
                        else:
                            missing.add(parent)
                            _recursive_check(child, parent, missing)
                    else:
                        _recursive_check(child, parent, missing)

        if self.schema and self.entitys:
            self.missing.clear()
            for root in self.entitys:
                for entry in self.schema:
                    _recursive_check(entry, root, self.missing)
        else:
            raise AttributeError("Schema or path not set yet.")


    def live(self, interval: int = 30, duration: int = None, mode: int = 0, daemon: bool = False):
        """
        Performs live validation either synchronously, asynchronously, or in a separate thread.

        Args:
            interval (int): Seconds to wait between validation cycles.
            duration (int, optional): Maximum runtime in seconds. If None, runs indefinitely.
            mode (int): Execution mode:
                0 = synchronous (default)
                1 = asynchronous using asyncio.to_thread()
                2 = threaded using threading.Thread()
            daemon (bool): Whether to start the thread as a daemon (default: False).
        """
        if not self.entitys:
            raise AttributeError("No root paths set yet.")
        if not self.schema:
            raise AttributeError("No schema set yet.")
        if not isinstance(interval, int) or interval <= 0:
            raise ValueError("Interval must be a positive integer.")    
        if duration is not None and (not isinstance(duration, int) or duration <= 0):
            raise ValueError("Duration must be a positive integer.")
        if mode not in [0, 1, 2]:
            raise ValueError("Mode must be 0 (sync), 1 (async), or 2 (thread).")

        def _live_loop():
            start = datetime.now()
            print(f"[{start.isoformat()}] Starte Live-Überwachung...")

            try:
                while True:
                    now = datetime.now()
                    self.validate()

                    if self.missing:
                        print(f"[{datetime.now().isoformat()}] Fehlende Pfade:")
                        for path in sorted(self.missing):
                            print(f"  - {path}")
                            if self.create_missing:
                                self._try_mkpath(path)
                                print("    ↳ erstellt")
                    else:
                        print(f"[{datetime.now().isoformat()}] Alles vorhanden ✓")

                    if duration is not None and now - start >= timedelta(seconds=duration):
                        print(f"[{now.isoformat()}] Beende Live-Überwachung...")
                        break

                    time.sleep(interval)

                    if self._stop_live:
                        print(f"[{datetime.now().isoformat()}] Live monitoring stopped by user.")
                        break

            except KeyboardInterrupt:
                print(f"[{datetime.now().isoformat()}] Live monitoring interrupted by user.")
            except Exception as e:
                print(f"[{datetime.now().isoformat()}] Fehler: {e}")

        # Moduswahl
        if mode == 0:
            _live_loop()

        elif mode == 1:
            try:
                asyncio.run(asyncio.to_thread(_live_loop))
            except RuntimeError:
                # Falls bereits ein Loop läuft (z. B. in einer GUI/WebApp)
                return asyncio.get_event_loop().create_task(asyncio.to_thread(_live_loop))

        elif mode == 2:
            thread = threading.Thread(target=_live_loop, daemon=daemon)
            thread.start()
            return thread # Return the thread object for external control 
            


        else:
            raise ValueError("Ungültiger Modus: 0 = sync, 1 = async, 2 = thread")


    def stop_live(self):
        """
        Sets the stop_live flag to True (placeholder for external control).
        """
        self._stop_live = True


    def _try_mkpath(self, path: Path) -> bool:
        """
        Attempt to create a file or directory.

        Args:
            path (Path): Target path to create.

        Returns:
            bool: True if creation succeeded or path already exists, False otherwise.
        """
        try:
            if path.exists():
                return True

            if path.suffix: 
                path.parent.mkdir(parents=True, exist_ok=True)  
                path.touch(exist_ok=True)
            else:
                path.mkdir(parents=True, exist_ok=True)

            self.created.add(path)

            return True
        except Exception as e:
            print(f"Error creating path {path}: {e}")
            return False


    def _load_schema(self, schema: Path | dict | list):
        """
        Load schema from various sources (file or inline).

        Args:
            schema (Path | dict | list): Schema input.

        Returns:
            list: A normalized list-based schema structure.

        Raises:
            ValueError: If schema format is unsupported.
        """
        if isinstance(schema, Path):
            return self._load_from_file(schema)

        elif isinstance(schema, dict):
            return [{key: value} for key, value in schema.items()]

        elif isinstance(schema, list):
            return schema

        else:
            raise ValueError(f"Schematype is not supported {schema}")


    def _load_from_file(self, path: Path) -> dict | list:
        """
        Load and parse a schema file from disk.

        Args:
            path (Path): File path to JSON or YAML schema.

        Returns:
            dict | list: Parsed schema content.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file format is not supported.
        """
        if not path.exists():
            raise FileNotFoundError(f"File does not exist {path}")

        if path.suffix == ".json":
            return json.loads(path.read_text(encoding="utf-8"))

        elif path.suffix in [".yml", ".yaml"]:
            return yaml.safe_load(path.read_text(encoding="utf-8"))

        elif path.suffix == ".txt":
            ... # Future versions

        else:
            raise ValueError("The schema file needs to be .json, .yaml or .txt!")


