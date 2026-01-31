from soar.modules.database.get_db import get_db_context


def create_table():
    get_db_context().execute("""
                             CREATE TABLE IF NOT EXISTS `analytics`
                             (
                                 time
                                 TIMESTAMP
                                 NOT
                                 NULL
                                 DEFAULT
                                 (
                                 datetime
                             (
                                 'now',
                                 '+8 hours'
                             )),
                                 `FUNCTION`
                                 TEXT
                                 NOT
                                 NULL
                                 )""")


def _insert(name: str):
    get_db_context().execute("""INSERT INTO `analytics` (`FUNCTION`)
                                VALUES (?)""", (name,))
