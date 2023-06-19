import os
from typing import Dict, List


class UserInterfaceClass:
    """
    UserInterfaceClass is an abstract base class that provides a uniform interface
    for various user interface implementations.

    This class defines key methods expected from any UI: start to initialize the UI,
    handle_request to process user requests with additional data,
    return_success to notify a successful operation,
    return_invalid_request to signal an invalid request,
    and return_audio to provide the requested audio file.
    Each of these methods raises a NotImplementedError in the base class,
    signaling they should be implemented in any concrete subclass.
    """

    def __init__(self, max_file_size_mb: int) -> None:
        self.max_file_size_mb = max_file_size_mb

    def start(self) -> None:
        raise NotImplementedError

    def handle_request(self, additional_data: Dict[str, str]) -> None:
        raise NotImplementedError

    def return_success(self) -> None:
        raise NotImplementedError

    def return_invalid_request(self) -> None:
        raise NotImplementedError

    def return_audio(self, audio_file: str) -> None:
        raise NotImplementedError

    def split_audio_to_files(self, audio_file: str) -> List[str]:
        """
        Splits the given audio file into multiple smaller files.
        The smaller files are named by appending the index to the original file name.
        """
        ...
