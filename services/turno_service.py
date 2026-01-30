from database.db import get_connection

class TurnoService:
    @staticmethod
    def add(nome):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO turno (nome) VALUES (?)", (nome,))
        conn.commit()
        conn.close()
