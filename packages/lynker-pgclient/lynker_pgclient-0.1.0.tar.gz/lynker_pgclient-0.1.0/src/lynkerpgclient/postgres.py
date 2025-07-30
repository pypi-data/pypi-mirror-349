# src/mypgclient/postgres.py

import psycopg2

class PostgresClient:
    """
    A simple wrapper around psycopg2 for connecting to Postgres.
    """

    def __init__(self, dsn: str):
        """
        :param dsn: e.g. "dbname=mydb user=me password=secret host=localhost port=5432"
        """
        self.dsn = dsn
        self.conn = None

    def connect(self):
        """Open a connection if not already open."""
        if self.conn is None or self.conn.closed:
            self.conn = psycopg2.connect(self.dsn)

    def query(self, sql: str, params=None):
        """
        Execute a SQL query and return all rows.
        :param sql: SQL string, possibly with %s placeholders
        :param params: tuple of parameters
        """
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()

    def close(self):
        """Close the connection."""
        if self.conn and not self.conn.closed:
            self.conn.close()
