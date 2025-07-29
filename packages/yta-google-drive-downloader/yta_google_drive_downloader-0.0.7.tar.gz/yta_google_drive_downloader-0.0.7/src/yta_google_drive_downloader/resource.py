from yta_google_drive_downloader.utils import parse_url, get_filename_from_url, get_id_from_url
from yta_google_drive_downloader.downloader import GoogleDriveDownloader
from yta_file.filename.handler import FilenameHandler
from yta_file.handler import FileHandler
from yta_validation.parameter import ParameterValidator
from typing import Union


class GoogleDriveResource:
    """
    Class to handle Google Drive Resources. Just instantiate
    it with its Google Drive url and it will be ready for
    download if the url is valid and available.

    A valid 'drive_url' must be like this:
    https://drive.google.com/file/d/1rcowE61X8c832ynh0xOt60TH1rJfcJ6z/view?usp=sharing&confirm=1
    """

    @property
    def id(
        self
    ) -> str:
        """
        The id of the resource, extracted from the given url.
        """
        if not hasattr(self, '_id'):
            self._id = get_id_from_url(self.url)

        return self._id
    
    @property
    def filename(
        self
    ) -> str:
        """
        The filename of the original resource as stored in
        Google Drive. It includes the extension.
        """
        if not hasattr(self, '_filename'):
            self._filename = get_filename_from_url(self.url)

        return self._filename
    
    # TODO: Maybe create 'file_name' (?)
    
    @property
    def extension(
        self
    ) -> str:
        """
        The extension of the original resource as stored in
        Google Drive. It doesn't include the dot '.'.
        """
        return FilenameHandler.get_extension(self.filename)

    def __init__(
        self,
        drive_url: str
    ):
        """
        Initialize the instance by setting the provided 'drive_url',
        that must be a valid one. This method will fire a GET request
        to obtain the real resource filename (if a valid resource).

        This method will raise an Exception if the 'drive_url'
        parameter is not a valid, open and sharable Google Drive
        url.
        """
        ParameterValidator.validate_mandatory_string('drive_url', drive_url, do_accept_empty = False)

        self.url = parse_url(drive_url)
        """
        The shareable url that contains the resource id.
        """
        # Force 'filename' to be obtained firing the request
        if self.filename is None:
            raise Exception('No original "filename" found, so it is not accesible.')

    def download(
        self,
        output_filename: Union[str, None] = None,
        do_force: bool = False
    ) -> str:
        """
        Download the Google Drive resource to the local
        storage with the given 'output_filename'. If the
        given 'output_filename' exists, it will be 
        returned unless the 'do_force' parameter is set
        as True.

        This method returns the filename from the local
        storage.
        """
        ParameterValidator.validate_string('output_filename', output_filename)
        ParameterValidator.validate_mandatory_bool('do_force', do_force)

        return (
            output_filename
            if (
                not do_force and
                output_filename is not None and
                FileHandler.is_file(output_filename)
            ) else
            GoogleDriveDownloader.download(self, output_filename)
        )