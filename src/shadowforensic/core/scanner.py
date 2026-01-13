import os
import shutil
import fnmatch
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional
from loguru import logger
from shadowforensic.utils.exceptions import RecoveryError

class RecoveryOptions:
    def __init__(
        self,
        filters: List[str] = None,
        min_size: int = 0,
        max_size: Optional[int] = None,
        preserve_metadata: bool = True
    ):
        self.filters = filters or ["*"]
        self.min_size = min_size
        self.max_size = max_size
        self.preserve_metadata = preserve_metadata

class FileScanner:
    """Scans and recovers files from a mounted shadow copy."""

    def __init__(self, source_path: str, target_path: str, options: RecoveryOptions):
        self.source_path = source_path
        self.target_path = target_path
        self.options = options
        self._executor = ThreadPoolExecutor(max_workers=os.cpu_count() or 4)

    def run(self):
        """Starts the scanning and recovery process."""
        if not os.path.exists(self.source_path):
            raise RecoveryError(f"Source path {self.source_path} does not exist.")

        logger.info(f"Starting recovery from {self.source_path} to {self.target_path}")
        
        tasks = []
        for root, dirs, files in os.walk(self.source_path):
            for file in files:
                if self._should_recover(file, root):
                    source_file = os.path.join(root, file)
                    rel_path = os.path.relpath(source_file, self.source_path)
                    dest_file = os.path.join(self.target_path, rel_path)
                    
                    tasks.append(self._executor.submit(self._copy_file, source_file, dest_file))
        
        # Optionally wait for all tasks (or handle them as they finish)
        # For now, we wait.
        for task in tasks:
            task.result()
            
        logger.info("Recovery completed.")

    def _should_recover(self, filename: str, directory: str) -> bool:
        """Applies filters to determine if a file should be recovered."""
        # Check filters
        match = False
        for pattern in self.options.filters:
            if fnmatch.fnmatch(filename, pattern):
                match = True
                break
        
        if not match:
            return False

        # Check size constraints
        full_path = os.path.join(directory, filename)
        try:
            size = os.path.getsize(full_path)
            if size < self.options.min_size:
                return False
            if self.options.max_size and size > self.options.max_size:
                return False
        except (OSError, PermissionError):
            return False

        return True

    def _copy_file(self, source: str, destination: str):
        """Copies a single file, preserving metadata if requested."""
        try:
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            if self.options.preserve_metadata:
                shutil.copy2(source, destination)
            else:
                shutil.copy(source, destination)
            logger.debug(f"Recovered: {source} -> {destination}")
        except Exception as e:
            logger.error(f"Failed to recover {source}: {e}")
