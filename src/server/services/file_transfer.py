"""Shared module for the file transfering functionality"""

from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZIP_DEFLATED, ZipFile

from fastapi import HTTPException, status

from server.config.config import settings
from server.models.files import FilesInfo


def construct_full_paths(files: list) -> list:
    """function for returning full paths given a list of files

    Args:
        files: list of files to be downloaded

    Returns:
        list of full path names

    Raises:
        HTTPException: 404, in case a file doesn't exist
    """
    selected_files: list = []

    base_dir: Path = settings.files_dir.resolve()

    for filename in files:
        full_name: Path = (base_dir / filename).resolve()

        if not full_name.is_file():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{full_name} is not available",
            )

        selected_files.append(full_name)

    return selected_files


def create_temp_zip(selected_files: list) -> str:
    """Creates a temporary zip file with the selected_files

    Args:
        selected_files: a list of files to be included in the zip

    Returns:
        name of zip
    """
    temp_zip = NamedTemporaryFile(suffix=".zip", delete=False)

    temp_zip.close()

    with ZipFile(temp_zip.name, "w", ZIP_DEFLATED) as archive:
        for path in selected_files:
            archive.write(path, path.name)

    return temp_zip.name


def get_available_files() -> list:
    """function for extracting the available files in the directory specified in the settings

    Returns:
        a list of files
    """
    return [
        FilesInfo(name=file.name, size=file.stat().st_size)
        for file in settings.files_dir.iterdir()
        if file.is_file()
    ]
