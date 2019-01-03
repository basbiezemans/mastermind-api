import sqlite3

class SQLiteDatabase:
    def __init__(self):
        self.con = sqlite3.connect(':memory:', check_same_thread=False)
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
        self.con.row_factory = dict_factory
        self.cursor = self.con.cursor()
        sql = (
            'CREATE TABLE IF NOT EXISTS game ('
            'token TEXT PRIMARY KEY,'
            'datetime_created TEXT,'
            'codemaker_score INTEGER,'
            'codebreaker_score INTEGER )'
        )
        self.con.execute(sql)

    def insert(self, game):
        sql = 'INSERT OR REPLACE INTO game VALUES (?, ?, ?, ?)'
        values = (game.token, game.created) + game.score()
        try:
            self.con.execute(sql, values)
        except sqlite3.Error as e:
            print('An error occurred:', e.args[0])
            return False
        return True

    def update(self, game):
        return self.insert(game)

    def select(self, sql, *args):
        try:
            self.cursor.execute(sql, args)
            if self.cursor.arraysize == 1:
                result = self.cursor.fetchone()
            else:
                result = self.cursor.fetchall()
        except sqlite3.Error as e:
            print('An error occurred:', e.args[0])
            return None
        return result

    def delete(self, token):
        sql = 'DELETE FROM game WHERE token = ?'
        count = self.con.execute(sql, (token,)).rowcount
        return bool(count)

    def filter_by(self, **kwargs):
        sql = 'SELECT * FROM game WHERE '
        sql += ', '.join(f'{key} = ?' for key in kwargs.keys())
        values = list(kwargs.values())
        return self.select(sql, *values)
