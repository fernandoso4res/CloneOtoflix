from ext.database import redis_conn

conn = redis_conn()


def check_if_key_exists(key):
    return conn.exists(key)

def set(key, value, expire=None):
    if expire:
        conn.set(key, value, ex=expire)
    else:
        conn.set(key, value)
    return True

def get(key):
    return conn.get(key)


def getdel(key):
    return conn.getdel(key)

def delete(key):
    conn.delete(key)
    return True

