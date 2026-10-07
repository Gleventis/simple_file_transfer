"""The route for the file-transfering"""

from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse

from server.helpers.clean import clean
from server.models.files import DownloadFiles
from server.services.file_transfer import (
    construct_full_paths,
    create_temp_zip,
    get_available_files,
)

router = APIRouter(prefix="/fts")


@router.get("/available_files")
def get_avail_files() -> JSONResponse:
    """Returns the available files in the directory

    Returns:
        list of the available files
    """
    avail_files = get_available_files()
    return JSONResponse(
        {"available_files": jsonable_encoder(avail_files)}, status.HTTP_200_OK
    )


@router.post("/download")
def download_files(
    request: DownloadFiles, background_tasks: BackgroundTasks
) -> FileResponse:
    """File for downloading the specified files

    Args:
        request: pydantic model that contains the specified files

    Returns:
        The downloaded files in zip

    Raises:
        HTTPException: Exception when the file specified is not valid
    """
    if not request.files:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="No files were specified for download",
        )

    selected_files: list = construct_full_paths(request.files)

    zip_name: str = create_temp_zip(selected_files=selected_files)

    background_tasks.add_task(clean, zip_name)

    return FileResponse(
        path=zip_name,
        status_code=status.HTTP_200_OK,
        media_type="application/zip",
        filename="files.zip",
    )
