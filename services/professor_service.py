from database.db import get_connection

class ProfessorService:
    @staticmethod
    def add(nome, matricula, disciplinas_ids):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO professor (nome, matricula) VALUES (?,?)",
            (nome, matricula)
        )
        professor_id = cur.lastrowid

        for d_id in disciplinas_ids:
            cur.execute(
                "INSERT INTO professor_disciplina (id_professor, id_disciplina) VALUES (?,?)",
                (professor_id, d_id)
            )

        conn.commit()
        conn.close()
