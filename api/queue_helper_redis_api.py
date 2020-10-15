import redis


class QueueHelperRedisAPI(object):
    # host = "localhost"
    host = "host.docker.internal"
    port = 6379
    db = 0
    conn = redis.Redis(host=host, port=port, db=db)
    files_path_queue = '.file_queue'
    words_to_flush_queue = '.words_flush_queue'

    @classmethod
    def get_file_name(cls):
        return cls.conn.rpop(cls.files_path_queue)

    @classmethod
    def add_file_name(cls, path):
        cls.conn.lpush(cls.files_path_queue, path)

    @classmethod
    def get_word_to_flush(cls):
        return cls.conn.rpop(cls.words_to_flush_queue)

    @classmethod
    def add_word_to_flush(cls, word):
        cls.conn.lpush(cls.words_to_flush_queue, word)

    @classmethod
    def get_lock(cls, word):
        return cls.conn.lock(word)



