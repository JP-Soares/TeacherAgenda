from database.db import get_connection


class Indisponibilidade:

    @staticmethod
    def add(
        id_professor,
        data,
        id_turno,
        motivo
    ):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            insert into professor_indisponibilidade (
                id_professor,
                data,
                id_turno,
                motivo
            )
            values (?, ?, ?, ?)
            """,
            (id_professor, data, id_turno, motivo)
        )

        conn.commit()
        conn.close()

    @staticmethod
    def delete(id_indisponibilidade):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "delete from professor_indisponibilidade where id = ?",
            (id_indisponibilidade,)
        )

        conn.commit()
        linhas = cursor.rowcount
        conn.close()

        return linhas > 0

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
            from professor_indisponibilidade
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
    def getByData(data):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            select
                i.id,
                p.nome as professor,
                t.nome as turno,
                i.motivo
            from professor_indisponibilidade i
            join professor p on p.id = i.id_professor
            join turno t on t.id = i.id_turno
            where i.data = ?
            order by t.id
            """,
            (data,)
        )

        result = cursor.fetchall()
        conn.close()
        return result
    
    @staticmethod
    def deleteByProfessor(id_professor):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM professor_indisponibilidade WHERE id_professor = ?",
            (id_professor,)
        )
        conn.commit()
        linhas = cursor.rowcount
        conn.close()
        return linhas

    @staticmethod
    def deleteByTurno(id_turno):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM professor_indisponibilidade WHERE id_turno = ?",
            (id_turno,)
        )
        conn.commit()
        linhas = cursor.rowcount
        conn.close()
        return linhas
