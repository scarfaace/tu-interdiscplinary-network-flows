import os

from transcription.constants import TMP_STREAMS_FOLDER, TMP_FILE_PATH_FORMAT


class StreamFlusher:

    @classmethod
    def flush(cls, streams):
        for stream_key in streams.keys():
            file_path = TMP_FILE_PATH_FORMAT.format(stream_key)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "a") as file:
                symbols_stream = cls.__join_symbols_stream(streams[stream_key])
                file.write(symbols_stream)
                file.close()


    @classmethod
    def __join_symbols_stream(cls, symbols_arr) -> str:
        return ''.join(symbols_arr)

