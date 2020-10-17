import redis


class QueueHelperRedisAPI(object):
    """
    Used for storing new articles for perocess and which words are ready for writing to the disk
    """
    host = "host.docker.internal"
    port = 6379
    db = 0
    conn = redis.Redis(host=host, port=port, db=db)
    files_path_queue = '.file_queue'  # queue name for the articles file on disk
    words_to_flush_queue = '.words_flush_queue'  # queue name for words that need a flush to disk
    words_in_queue_set = '.queue_words_set'

    @classmethod
    def get_file_name(cls):
        return cls.conn.rpop(cls.files_path_queue)

    @classmethod
    def add_file_name(cls, path):
        cls.conn.lpush(cls.files_path_queue, path)

    @classmethod
    def get_word_to_flush(cls):
        word = cls.conn.rpop(cls.words_to_flush_queue)
        if not word:
            return word

        if cls.conn.sismember(cls.words_in_queue_set, word):  # not to add the same word to the queue
            cls.conn.srem(cls.words_in_queue_set, word)

        return word

    @classmethod
    def add_word_to_flush(cls, word):
        if not cls.conn.sismember(cls.words_in_queue_set, word):
            cls.conn.sadd(cls.words_in_queue_set, word)  # mark the word as part of the flush queue
            cls.conn.lpush(cls.words_to_flush_queue, word)

    @classmethod
    def get_lock(cls, word):
        """
        used to lock word files so no two writer will write at the same time
        """
        return cls.conn.lock(word)
