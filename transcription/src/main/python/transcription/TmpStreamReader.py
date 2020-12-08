from transcription.constants import TMP_FILE_PATH_FORMAT


class TmpStreamReader:

    @classmethod
    def read_stream_from_file(cls, stream_key) -> str:
        tmp_file_path = TMP_FILE_PATH_FORMAT.format(stream_key)
        with open(tmp_file_path) as f:
            return f.readline()
