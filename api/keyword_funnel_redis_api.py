import redis


class KeywordFunnelRedisAPI(object):
    """
    Used as a queue for each word with articles names needed to be written to the disk
    """
    host = "host.docker.internal"
    port = 6379
    db = 1
    conn = redis.Redis(host=host, port=port, db=db)

    @classmethod
    def get_all_articles_by_word(cls, word):
        """
        empties the queue of a world filled with articles names
        """

        out = []
        count = cls.conn.llen(word)
        for i in range(count):
            article = cls.conn.rpop(word)
            if not article:
                break

            out.append(article)

        return out

    @classmethod
    def add_article_by_word(cls, word, article):
        cls.conn.lpush(word, article)

    @classmethod
    def get_articles_count(cls, word):
        return cls.conn.llen(word)
