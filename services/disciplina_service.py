from database.db import get_connection

class DisciplinaService:
    @staticmethod
    def get_all():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nome FROM disciplina")
        data = cur.fetchall()
        conn.close()
        return data

    @staticmethod
    def add(nome, carga):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO disciplina (nome, carga_horaria) VALUES (?,?)",
            (nome, carga)
        )
        conn.commit()
        conn.close()
