This is a toy project for experimenting and getting to work with nvim.

The server is developed using FastAPI, and it allows for downloading files from the specified directory.

To get it up and running, build the image with ´´´docker build file_transfer .´´´ and then start it up with ´´´docker run --rm -p 8000:8000 -v <your_files_directory></your>:/data:ro file_transfer´´´ where your_files_directory is the directory that contains the files you want to download from.

The project also contains some basic frontend, done with NiceGUI.
