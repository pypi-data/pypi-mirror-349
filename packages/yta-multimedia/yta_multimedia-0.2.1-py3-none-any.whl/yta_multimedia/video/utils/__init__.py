from yta_multimedia.video.parser import VideoParser
from yta_image.parser import ImageParser
from yta_general_utils.programming.validator.parameter import ParameterValidator
from yta_validation import PythonValidator
from yta_programming.output import Output
from yta_constants.file import FileType
# TODO: We need to avoid the use of FileReturn
# because it uses a lot of dependencies to parse
# the file content dynamically and that is not a
# good thing...
from yta_general_utils.dataclasses import FileReturn
from moviepy import ImageClip
from moviepy.Clip import Clip
from typing import Union, Any
import numpy as np


def generate_video_from_image(
    image: Union[str, Any, ImageClip],
    duration: float = 1,
    fps: float = 60,
    output_filename: Union[str, None] = None
) -> Union[FileReturn, Clip]:
    """
    Create an ImageClip of 'duration' seconds with the
    given 'image' and store it locally if 'output_filename'
    is provided.

    This method return a Clip instance if the file is not
    written, and a FileReturn instance if yes.
    """
    ParameterValidator.validate_mandatory_positive_number('duration', duration, do_include_zero = False)

    if not PythonValidator.is_instance(image, ImageClip):
        video = ImageClip(ImageParser.to_numpy(image), duration = duration).with_fps(fps)

    if output_filename:
        video.write_videofile(Output.get_filename(output_filename, FileType.VIDEO))

    return (
        video
        if output_filename is None else
        FileReturn(
            video,
            FileType.VIDEO,
            output_filename
        )
    )

def is_video_transparent(
    video: Clip
):
    """
    Checks if the first frame of the mask of the
    given 'video' has, at least, one transparent
    pixel.
    """
    # We need to detect the transparency from the mask
    video = VideoParser.to_moviepy(video, do_include_mask = True)

    # We need to find, by now, at least one transparent pixel
    # TODO: I would need to check all frames to be sure of this above
    # TODO: The mask can have partial transparency, which 
    # is a value greater than 0, so what do we consider
    # 'transparent' here (?)
    return np.any(video.mask.get_frame(t = 0) == 1)