from transcription.configuration import configuration, Configuration
from transcription.constants import TMP_FILE_PATH_FORMAT


class TmpStreamReader:

    def __init__(self, configurationParam: Configuration):
        self.configuration = configurationParam

    @classmethod
    def read_stream_from_file(cls, stream_key) -> str:
        # tmp_file_path = self.configuration.TMP_STEAM_PATH_FORMAT.format(stream_key)
        tmp_file_path = TMP_FILE_PATH_FORMAT.format(stream_key)
        with open(tmp_file_path) as f:
            return f.readline()


tmpStreamReader = TmpStreamReader(configuration)
