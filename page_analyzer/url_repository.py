import psycopg2
from psycopg2.extras import RealDictCursor


class UrlRepository:
    def __init__(self, db_url):
        self.db_url = db_url

    def _execute(self, query, params=None, fetch=None, do_commit=False):
        result = None
        with psycopg2.connect(self.db_url) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                if fetch == "one":
                    result = cur.fetchone()
                elif fetch == "all":
                    result = cur.fetchall()
            if do_commit:
                conn.commit()
        return result

    def save(self, url, date):
        row = self._execute(
            """
            INSERT INTO urls (name, created_at) VALUES (%s, %s)
            RETURNING id
            """,
            (url, date),
            "one",
            True,
        )
        return row["id"]

    def get_by_url(self, url):
        return self._execute(
            "SELECT * FROM urls WHERE name = %s", (url,), "one"
        )

    def get_by_id(self, id):
        return self._execute("SELECT * FROM urls WHERE id = %s", (id,), "one")

    def get_all(self):
        return self._execute(
            "SELECT * FROM urls ORDER BY id DESC",
            fetch="all"
            )
