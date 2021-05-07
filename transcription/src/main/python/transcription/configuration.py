import uuid

class Configuration:
    TMP_STREAMS_ROOT_FOLDER = 'tmp_streams'
    TMP_STREAMS_NESTED_FOLDER = uuid.uuid4().hex
    TMP_STEAM_PATH_FORMAT = TMP_STREAMS_ROOT_FOLDER + '/' + TMP_STREAMS_NESTED_FOLDER + '/{}.txt'

    MILLISECONDS_PER_GAP = 1000


configuration = Configuration()
