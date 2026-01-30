from database.db import get_connection

class CursoService:
    @staticmethod
    def add(nome, carga, disciplinas_ids):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO curso (nome, carga_horaria) VALUES (?,?)",
            (nome, carga)
        )
        curso_id = cur.lastrowid

        for d_id in disciplinas_ids:
            cur.execute(
                "INSERT INTO curso_disciplina (id_curso, id_disciplina) VALUES (?,?)",
                (curso_id, d_id)
            )

        conn.commit()
        conn.close()
