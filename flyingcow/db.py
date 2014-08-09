try:
    import torndb

    # db errors aliased for convenience.
    IntegrityError = torndb.IntegrityError
    OperationalError = torndb.OperationalError
    Connection = torndb.Connection
except ImportError:
    import tornado.database

    # db errors aliased for convenience.
    IntegrityError = tornado.database.IntegrityError
    OperationalError = tornado.database.OperationalError
    Connection = tornado.database.Connection


class NoConnectionRegistered(Exception):
    """
    Raised when a connection is attempted to be used without
    having one registered to begin with.
    """

class ConnectionManager(object):
    """
    Helps manage a connection between modules.
    """
    def __init__(self):
        self._connection = None
    
    def register(self, host='localhost', name=None, user=None, password=None):
        self._connection = Connection(host, name, user, password)
        return self._connection
    
    def connection(self):
        if not self._connection:
            raise NoConnectionRegistered
        return self._connection

_connection_manager = ConnectionManager()
register_connection = _connection_manager.register
connection = _connection_manager.connection
