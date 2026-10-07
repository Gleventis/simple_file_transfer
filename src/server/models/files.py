"""contains the pydantic models for the files"""

from pydantic import BaseModel


class FilesInfo(BaseModel):
    """pydantic model for the metadata of a file"""

    name: str
    size: int


class DownloadFiles(BaseModel):
    """pydantic model for specifying list of files to be downloaded"""

    files: list[str]
