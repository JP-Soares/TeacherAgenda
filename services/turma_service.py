from database.db import get_connection

class TurmaService:
    @staticmethod
    def add(nome, empresa, localidade):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO turma (nome, empresa, localidade) VALUES (?,?,?)",
            (nome, empresa, localidade)
        )
        conn.commit()
        conn.close()
