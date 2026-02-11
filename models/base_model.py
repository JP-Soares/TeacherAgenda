from database.db import get_connection

class BaseModel:

    @staticmethod
    def execute_delete(queries, params):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON")

        try:
            for query, param in zip(queries, params):
                cursor.execute(query, param)

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
