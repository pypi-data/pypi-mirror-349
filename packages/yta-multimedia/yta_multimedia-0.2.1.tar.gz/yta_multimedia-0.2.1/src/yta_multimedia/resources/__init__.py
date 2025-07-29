"""
TODO: This module has to be refactored and maybe moved
to the new 'yta_google_drive_downloader' library being
able to handle local files (that library is not
handling it right now)
"""
from yta_google_drive_downloader import GoogleDriveResource
from yta_temp import Temp
from yta_programming.path import PathHandler
from yta_general_utils.checker.url import is_google_drive_url
from yta_programming.path import DevPathHandler
from yta_file.handler import FileHandler
from yta_validation.parameter import ParameterValidator


# TODO: I think this is now in the
# 'yta_google_drive_downloader' library but...
class Resource:
    """
    Class to simplify the way we work with a local resource or with one that
    is stored in Google Drive.
    """

    @staticmethod
    def get(
        filename_or_google_drive_url: str,
        output_filename: str = None
    ):
        """
        This method has been built to be used internally to obtain
        the resources this software needs always in the same way
        and to be able to speed up the process by avoiding external
        downloads as much as possible.
        
        If the provided 'filename_or_google_drive_url' is a Google
        Drive url, the first time a resource is downloaded from the
        given 'google_drive_url', if 'output_filename' provided, will 
        be stored locally with that filename. Next time, as it will
        be found locally, it will be returned and we will have not to
        wait for the download.
        """
        ParameterValidator.validate_mandatory('filename_or_google_drive_url', filename_or_google_drive_url)
        
        if (
            output_filename and
            FileHandler.is_file(output_filename)
        ):
            return output_filename
        
        if is_google_drive_url(filename_or_google_drive_url):
            # TODO: Check that abspath / output_filename is valid

            # We force to create all folders if they don't exist
            PathHandler.create_file_abspath(f'{DevPathHandler.get_project_abspath()}{output_filename}')

            output_filename = GoogleDriveResource(filename_or_google_drive_url).download(output_filename)
        else:
            if not FileHandler.is_file(filename_or_google_drive_url):
                raise Exception(f'The provided "filename" parameter {filename_or_google_drive_url} does not exist.')
            
            # TODO: I can copy it to be found as output_filename,
            # but I don't want by now.
            # if filename_or_google_drive_url != output_filename:
            #     copy_file(filename_or_google_drive_url, output_filename)
            output_filename = filename_or_google_drive_url

        return output_filename


# TODO: Remove this below when refactored
def get_resource(google_drive_url: str, output_filename: str = None):
    """
    This method has been built to be used internally to obtain
    the resources this software needs. This method will look
    for the 'output_filename' if provided, and if it exist
    locally stored, it will return that filename. If it doesn't
    exist or the 'output_filename' is not provided, it will 
    download the resource from the given 'google_drive_url',
    store it locally and return it.

    The first time a resource is downloaded from the given
    'google_drive_url', if 'output_filename' provided, will
    be stored locally with that filename. Next time, as it 
    will be found locally, it will be returned and we will
    have not to wait for the download.

    This method has been created to optimize the resource
    getting process.

    @param
        **google_drive_url**
        The Google Drive url in which we can found (and
        download) the resource.

    @param
        **output_filename**
        The filename of the resource we want to get, that
        must be a relative path from the current project
        abspath.
    """
    if not google_drive_url:
        raise Exception('No "google_drive_url" parameter provided.')
    
    output_abspath = Temp.get_filename('tmp_resource.mp3')
    
    if output_filename:
        # We try to find it and return or we create the folder if doesn't exist
        output_abspath = DevPathHandler.get_project_abspath() + output_filename

        if FileHandler.is_file(output_abspath):
            return output_abspath
        
        # We force to create all folders
        PathHandler.create_file_abspath(output_abspath)
    
    # We download the file and store it locally
    return GoogleDriveResource(google_drive_url).download(output_abspath)


    # Has 'output_filename'
        # Resource is Google Drive url
            # => We check if 'output_filename' and return if yes
            # => We check if 'output_filename' and download if not as it
        # Resource is filename (?)
            # => We check if 'output_filename' exist and return it (!)
            # => We copy the filename as 'output_filename' and return it
    # Doesn't have 'output_filename'
        # Resource is Google Drive url
            # => We download it and return the temporary file downloaded
        # Resource is filename
            # => We check if existing and return the filename as it is
    