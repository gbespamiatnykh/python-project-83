import psycopg2
from psycopg2.extras import RealDictCursor


class UrlRepository:
    def __init__(self, db_url):
        self.db_url = db_url

    def _execute(self, query, params=None, fetch=None, do_commit=False):
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

    def add(self, url, date):
        row = self._execute(
            """
            INSERT INTO urls (name, created_at) VALUES (%s, %s)
            RETURNING id
            """,
            (url, date),
            fetch="one",
            do_commit=True,
        )
        return row["id"]

    def find_by_name(self, url):
        return self._execute(
            "SELECT * FROM urls WHERE name = %s", (url,), fetch="one"
        )

    def find_by_id(self, id):
        return self._execute(
            "SELECT * FROM urls WHERE id = %s", (id,), fetch="one"
        )

    def get_all(self):
        return self._execute(
            """
            SELECT u.id, u.name, uc.status_code, uc.created_at AS last_check
            FROM urls u LEFT JOIN
            (SELECT DISTINCT ON (url_id) url_id, status_code, created_at
            FROM url_checks ORDER BY url_id, created_at DESC) uc
            ON u.id = uc.url_id ORDER BY u.id DESC
            """,
            fetch="all",
        )

    def add_check(self, url_id, status_code, html_data, creation_date):
        return self._execute(
            """
            INSERT INTO url_checks
            (url_id, status_code, h1, title, description, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                url_id,
                status_code,
                html_data.get("h1"),
                html_data.get("title"),
                html_data.get("description"),
                creation_date,
            ),
            fetch="one",
            do_commit=True,
        )

    def get_checks(self, id):
        return self._execute(
            "SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC",
            (id,),
            fetch="all",
        )

    def get_last_check(self, id):
        return self._execute(
            """
            SELECT * FROM url_checks WHERE url_id = %s
            ORDER BY id DESC LIMIT 1
            """,
            (id,),
            fetch="one",
        )
