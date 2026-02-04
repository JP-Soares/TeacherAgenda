from database.db import get_connection


class Aula:

    @staticmethod
    def add(
        data,
        id_professor,
        id_disciplina,
        id_curso,
        id_turno,
        id_turma
    ):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            insert into aula (
                data,
                id_professor,
                id_disciplina,
                id_curso,
                id_turno,
                id_turma
            )
            values (?, ?, ?, ?, ?, ?)
            """,
            (
                data,
                id_professor,
                id_disciplina,
                id_curso,
                id_turno,
                id_turma
            )
        )

        conn.commit()
        conn.close()

    @staticmethod
    def delete(id_aula):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "delete from aula where id = ?",
            (id_aula,)
        )

        conn.commit()
        linhas = cursor.rowcount
        conn.close()

        return linhas > 0

    @staticmethod
    def getByData(data):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                select
                    a.id,
                    d.nome as disciplina,
                    t.nome as turma,
                    tu.nome as turno,
                    p.nome as professor
                from aula a
                join disciplina d on d.id = a.id_disciplina
                join turma t on t.id = a.id_turma
                join turno tu on tu.id = a.id_turno
                join professor p on p.id = a.id_professor
                where a.data = ?
                order by tu.id
                """,
                (data,)
            )

            return cursor.fetchall()

        except Exception as e:
            print("erro ao buscar aulas:", e)
            return []

        finally:
            conn.close()

    @staticmethod
    def getByProfessorDataTurno(
        id_professor,
        data,
        id_turno
    ):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            select id
            from aula
            where id_professor = ?
              and data = ?
              and id_turno = ?
            """,
            (id_professor, data, id_turno)
        )

        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def getByTurmaDataTurno(
        id_turma,
        data,
        id_turno
    ):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            select id
            from aula
            where id_turma = ?
              and data = ?
              and id_turno = ?
            """,
            (id_turma, data, id_turno)
        )

        result = cursor.fetchall()
        conn.close()
        return result
