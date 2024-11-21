import shutil
import tarfile
from abc import ABC, abstractmethod
from collections.abc import Callable
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile, is_zipfile

from langflow.custom import Component
from langflow.io import BoolInput, FileInput, HandleInput, Output
from langflow.schema import Data


class BaseFileComponent(Component, ABC):
    """Base class for handling file processing components.

    This class provides common functionality for resolving, validating, and
    processing file paths. Child classes must define valid file extensions
    and implement the `process_files` method.
    """

    class BaseFile:
        """Internal class to represent a file with additional metadata."""

        def __init__(self, data: Data | list[Data], path: Path, *, delete_after_processing: bool = False):
            self.data = data
            self.path = path
            self.delete_after_processing = delete_after_processing

        @property
        def data(self) -> list[Data]:
            return self._data or []

        @data.setter
        def data(self, value: Data | list[Data]):
            if isinstance(value, Data):
                self._data = [value]
            elif isinstance(value, list) and all(isinstance(item, Data) for item in value):
                self._data = value
            else:
                msg = f"data must be a Data object or a list of Data objects. Got: {type(value)}"
                self.log(msg)
                if not self.silent_errors:
                    raise ValueError(msg)

        def merge_data(self, new_data: Data | list[Data] | None) -> list[Data]:
            r"""Generate a new list of Data objects by merging `new_data` into the current `data`.

            Args:
                new_data (Data | list[Data] | None): The new Data object(s) to merge into each existing Data object.
                    If None, the current `data` is returned unchanged.

            Returns:
                list[Data]: A new list of Data objects with `new_data` merged.
            """
            if new_data is None:
                return self.data

            if isinstance(new_data, Data):
                new_data_list = [new_data]
            elif isinstance(new_data, list) and all(isinstance(item, Data) for item in new_data):
                new_data_list = new_data
            else:
                msg = "new_data must be a Data object, a list of Data objects, or None."
                self.log(msg)
                if not self.silent_errors:
                    raise ValueError(msg)
                return self.data

            return [
                Data(data={**data.data, **new_data_item.data})
                for data in self.data
                for new_data_item in new_data_list
            ]

        def __str__(self):
            if len(self.data) == 0:
                text_preview = ""
            elif len(self.data) == 1:
                max_text_length = 50
                text_preview = self.data.get_text()[:max_text_length]
                if len(self.data.get_text()) > max_text_length:
                    text_preview += "..."
                text_preview = f"text_preview='{text_preview}'"
            else:
                text_preview = f"{len(self.data)} data objects"
            return (
                f"BaseFile(path={self.path}"
                f", delete_after_processing={self.delete_after_processing}"
                f", {text_preview}"
            )

    # Subclasses can override these class variables
    VALID_EXTENSIONS = []  # To be overridden by child classes
    IGNORE_STARTS_WITH = [".", "__MACOSX"]

    SERVER_FILE_PATH_FIELDNAME = "file_path"
    SUPPORTED_BUNDLE_EXTENSIONS = ["zip", "tar", "tgz", "bz2", "gz"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically update FileInput to include valid extensions and bundles
        self._base_inputs[0].file_types = [*self.valid_extensions, *self.SUPPORTED_BUNDLE_EXTENSIONS]

        file_types = ", ".join(self.valid_extensions)
        bundles = ", ".join(self.SUPPORTED_BUNDLE_EXTENSIONS)
        self._base_inputs[
            0
        ].info = f"Supported file extensions: {file_types}; optionally bundled in file extensions: {bundles}"

    _base_inputs = [
        FileInput(
            name="path",
            display_name="Path",
            file_types=[],  # Dynamically set in __init__
            info="",  # Dynamically set in __init__
            required=False,
        ),
        HandleInput(
            name="file_path",
            display_name="Server File Path",
            info=(
                f"Data object with a '{SERVER_FILE_PATH_FIELDNAME}' property pointing to server file. "
                "Supercedes 'Path'. "
            ),
            required=False,
            input_types=["Data"],
        ),
        BoolInput(
            name="silent_errors",
            display_name="Silent Errors",
            advanced=True,
            info="If true, errors will not raise an exception.",
        ),
        BoolInput(
            name="delete_server_file_after_processing",
            display_name="Delete Server File After Processing",
            advanced=True,
            value=True,
            info="If true, the Server File Path will be deleted after processing.",
        ),
        BoolInput(
            name="ignore_unsupported_extensions",
            display_name="Ignore Unsupported Extensions",
            advanced=True,
            value=True,
            info="If true, files with unsupported extensions will not be processed.",
        ),
    ]

    _base_outputs = [Output(display_name="Data", name="data", method="load_files")]

    @abstractmethod
    def process_files(self, file_list: list[BaseFile]) -> list[BaseFile]:
        """Processes a list of files.

        Args:
            file_list (list[BaseFile]): A list of file objects.

        Returns:
            list[BaseFile]: A list of BaseFile objects with updated `data`.
        """

    def load_files(self) -> list[Data]:
        """Loads and parses file(s), including unpacked file bundles.

        Returns:
            list[Data]: Parsed data from the processed files.
        """
        self._temp_dirs = []
        try:
            # Step 1: Validate the provided paths
            files = self._validate_and_resolve_paths()

            # Step 2: Handle bundles recursively
            all_files = self._unpack_and_collect_files(files)

            # Step 3: Final validation of file types
            final_files = self._filter_and_mark_files(all_files)

            # Step 4: Process files
            processed_files = self.process_files(final_files)

            # Extract and flatten Data objects to return
            return [data for file in processed_files for data in file.data if file.data]

        finally:
            # Delete temporary directories
            for temp_dir in self._temp_dirs:
                temp_dir.cleanup()

            # Delete files marked for deletion
            for file in final_files:
                if file.delete_after_processing and file.path.exists():
                    if file.path.is_dir():
                        shutil.rmtree(file.path)
                    else:
                        file.path.unlink()

    @property
    def valid_extensions(self) -> list[str]:
        """Returns valid file extensions for the class.

        This property can be overridden by child classes to provide specific
        extensions.

        Returns:
            list[str]: A list of valid file extensions without the leading dot.
        """
        return self.VALID_EXTENSIONS

    @property
    def ignore_starts_with(self) -> list[str]:
        """Returns prefixes to ignore when unpacking file bundles.

        Returns:
            list[str]: A list of prefixes to ignore when unpacking file bundles.
        """
        return self.IGNORE_STARTS_WITH

    def rollup_data(
        self,
        base_files: list[BaseFile],
        data_list: list[Data | None],
        path_field: str = SERVER_FILE_PATH_FIELDNAME,
    ) -> list[BaseFile]:
        r"""Rolls up Data objects into corresponding BaseFile objects in order given by `base_files`.

        Args:
            base_files (list[BaseFile]): The original BaseFile objects.
            data_list (list[Data | None]): The list of data to be aggregated into the BaseFile objects.
            path_field (str): The field name on the data_list objects that holds the file path as a string.

        Returns:
            list[BaseFile]: A new list of BaseFile objects with merged `data` attributes.
        """

        def _build_data_dict(data_list: list[Data | None], data_list_field: str) -> dict[str, list[Data]]:
            """Builds a dictionary grouping Data objects by a specified field."""
            data_dict = {}
            for data in data_list:
                if data is None:
                    continue
                key = data.data.get(data_list_field)
                if key is None:
                    msg = f"Data object missing required field '{data_list_field}': {data}"
                    self.log(msg)
                    if not self.silent_errors:
                        msg = f"Data object missing required field '{data_list_field}': {data}"
                        self.log(msg)
                        raise ValueError(msg)
                    continue
                data_dict.setdefault(key, []).append(data)
            return data_dict

        # Build the data dictionary from the provided data_list
        data_dict = _build_data_dict(data_list, path_field)

        # Generate the updated list of BaseFile objects, preserving the order of base_files
        updated_base_files = []
        for base_file in base_files:
            new_data_list = data_dict.get(str(base_file.path), [])
            merged_data_list = base_file.merge_data(new_data_list)
            updated_base_files.append(
                BaseFileComponent.BaseFile(
                    data=merged_data_list,
                    path=base_file.path,
                    delete_after_processing=base_file.delete_after_processing,
                )
            )

        return updated_base_files

    def _validate_and_resolve_paths(self) -> list[BaseFile]:
        """Validate that all input paths exist and are valid, and create BaseFile instances.

        Returns:
            list[BaseFile]: A list of valid BaseFile instances.

        Raises:
            ValueError: If any path does not exist.
        """
        resolved_files = []

        def add_file(data: Data, path: str | Path, *, delete_after_processing: bool):
            resolved_path = Path(self.resolve_path(path))
            if not resolved_path.exists():
                msg = f"File or directory not found: {path}"
                self.log(msg)
                if not self.silent_errors:
                    raise ValueError(msg)
            resolved_files.append(
                BaseFileComponent.BaseFile(data, resolved_path, delete_after_processing=delete_after_processing)
            )

        if self.path and not self.file_path:  # Only process self.path if file_path is not provided
            # Wrap self.path into a Data object
            data_obj = Data(file_path=self.path)
            add_file(data=data_obj, path=self.path, delete_after_processing=False)
        elif self.file_path:
            if isinstance(self.file_path, Data):
                self.file_path = [self.file_path]
            elif not isinstance(self.file_path, list):
                msg = f"Expected list of Data objects in file_path but got {type(self.file_path)}."
                self.log(msg)
                if not self.silent_errors:
                    raise ValueError(msg)
                return []

            for obj in self.file_path:
                if not isinstance(obj, Data):
                    msg = f"Expected Data object in file_path but got {type(obj)}."
                    self.log(msg)
                    if not self.silent_errors:
                        raise ValueError(msg)
                    continue

                server_file_path = obj.data.get(self.SERVER_FILE_PATH_FIELDNAME)
                if server_file_path:
                    add_file(
                        data=obj,
                        path=server_file_path,
                        delete_after_processing=self.delete_server_file_after_processing,
                    )
                else:
                    msg = f"Data object missing '{self.SERVER_FILE_PATH_FIELDNAME}' property."
                    self.log(msg)
                    if not self.silent_errors:
                        raise ValueError(msg)

        return resolved_files

    def _unpack_and_collect_files(self, files: list[BaseFile]) -> list[BaseFile]:
        """Recursively unpack bundles and collect files into BaseFile instances.

        Args:
            files (list[BaseFile]): List of BaseFile instances to process.

        Returns:
            list[BaseFile]: Updated list of BaseFile instances.
        """
        collected_files = []

        for file in files:
            path = file.path
            delete_after_processing = file.delete_after_processing
            data = file.data

            if path.is_dir():
                # Recurse into directories
                collected_files.extend(
                    [
                        BaseFileComponent.BaseFile(data, sub_path, delete_after_processing=delete_after_processing)
                        for sub_path in path.rglob("*")
                        if sub_path.is_file()
                    ]
                )
            elif path.suffix[1:] in self.SUPPORTED_BUNDLE_EXTENSIONS:
                # Unpack supported bundles
                temp_dir = TemporaryDirectory()
                self._temp_dirs.append(temp_dir)
                temp_dir_path = Path(temp_dir.name)
                self._unpack_bundle(path, temp_dir_path)
                subpaths = list(temp_dir_path.iterdir())
                self.log(f"Unpacked bundle {path.name} into {subpaths}")
                collected_files.extend(
                    [
                        BaseFileComponent.BaseFile(data, sub_path, delete_after_processing=delete_after_processing)
                        for sub_path in subpaths
                    ]
                )
            else:
                collected_files.append(file)

        # Recurse again if any directories or bundles are left in the list
        if any(
            file.path.is_dir() or file.path.suffix[1:] in self.SUPPORTED_BUNDLE_EXTENSIONS for file in collected_files
        ):
            return self._unpack_and_collect_files(collected_files)

        return collected_files

    def _safe_extract(
        self,
        extract_func: Callable[[Path], None],
        members: list[str],
        output_dir: Path,
        archive_type: str,
    ):
        """Safely extract files from an archive, ensuring no path traversal.

        Args:
            extract_func (Callable): Function to perform the extraction.
            members (list[str]): List of members (file paths) to extract.
            output_dir (Path): Directory where files will be extracted.
            archive_type (str): Type of archive (ZIP or TAR) for logging.

        Raises:
            ValueError: If an attempted path traversal is detected.
        """
        for member in members:
            member_path = output_dir / member
            if not member_path.resolve().is_relative_to(output_dir.resolve()):
                msg = f"Attempted Path Traversal in {archive_type} File: {member}"
                raise ValueError(msg)
            extract_func(output_dir, member)

    def _unpack_bundle(self, bundle_path: Path, output_dir: Path):
        """Unpack a bundle into a temporary directory.

        Args:
            bundle_path (Path): Path to the bundle.
            output_dir (Path): Directory where files will be extracted.

        Raises:
            ValueError: If the bundle format is unsupported or cannot be read.
        """
        if is_zipfile(bundle_path):
            with ZipFile(bundle_path, "r") as bundle:
                self._safe_extract(
                    lambda output_dir, member: bundle.extract(member, path=output_dir),
                    bundle.namelist(),
                    output_dir,
                    "ZIP",
                )
        elif tarfile.is_tarfile(bundle_path):
            with tarfile.open(bundle_path, "r:*") as bundle:
                self._safe_extract(
                    lambda output_dir, member: bundle.extract(member, path=output_dir),
                    [member.name for member in bundle.getmembers()],
                    output_dir,
                    "TAR",
                )
        else:
            msg = f"Unsupported bundle format: {bundle_path.suffix}"
            self.log(msg)
            if not self.silent_errors:
                raise ValueError(msg)

    def _filter_and_mark_files(self, files: list[BaseFile]) -> list[BaseFile]:
        """Validate file types and mark files for removal.

        Args:
            files (list[BaseFile]): List of BaseFile instances.

        Returns:
            list[BaseFile]: Validated BaseFile instances.

        Raises:
            ValueError: If unsupported files are encountered and `ignore_unsupported_extensions` is False.
        """
        final_files = []
        ignored_files = []

        for file in files:
            if not file.path.is_file():
                self.log(f"Not a file: {file.path.name}")
                continue

            if file.path.suffix[1:] not in self.valid_extensions:
                if self.ignore_unsupported_extensions:
                    ignored_files.append(file.path.name)
                    continue
                msg = f"Unsupported file extension: {file.path.suffix}"
                self.log(msg)
                if not self.silent_errors:
                    raise ValueError(msg)

            final_files.append(file)

        if ignored_files:
            self.log(f"Ignored files: {ignored_files}")

        return final_files
