from database.db import get_connection
from models.base_model import BaseModel

class Professor:
    def __init__(self, id, matricula, nome):
        self.id = id
        self.nome = nome
        self.matricula = matricula

    @staticmethod
    def validate(nome, matricula):
        if nome != '' and matricula != '':
            return True
        return False

    @staticmethod
    def add(nome, matricula, ids_disciplinas):
        if Professor.validate(nome, matricula):
            try:
                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute(
                    "INSERT INTO professor (nome, matricula) VALUES (?, ?)",
                    (nome, matricula)
                )

                id_professor = cursor.lastrowid

                for id_disciplina in ids_disciplinas:
                    cursor.execute(
                        "INSERT INTO professor_disciplina (id_professor, id_disciplina) VALUES (?, ?)",
                        (id_professor, id_disciplina)
                    )

                conn.commit()
                conn.close()
                return True
            except Exception as e:
                print("Erro ao adicionar professor:", e)
                return False
        return False

    @staticmethod
    def update(id, nome, matricula):
        if Professor.validate(nome, matricula):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE professor SET nome=?, matricula=? WHERE id=?",
                               (nome, matricula, id))
                conn.commit()
                conn.close()
                return True
            except Exception as e:
                print("Erro ao atualizar professor:", e)
                return False
        return False

    @staticmethod
    def getById(id):
        if id != '':
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM professor WHERE id = ?", (id,))
                resultado = cursor.fetchone()
                conn.close()
                return resultado
            except Exception as e:
                print("Erro ao buscar professor:", e)
                return None
        return None
    
    @staticmethod
    def getAll():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM professor")
            resultado = cursor.fetchall()
            conn.close()
            return resultado
        except Exception as e:
                print("Erro ao buscar professor:", e)
                return None
        
    @staticmethod
    def getDisciplinas(id_professor):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            select d.id
            from disciplina d
            join professor_disciplina pd
                on pd.id_disciplina = d.id
            where pd.id_professor = ?
            """,
            (id_professor,)
        )

        rows = cursor.fetchall()
        conn.close()

        return [r[0] for r in rows]
    
    @staticmethod
    def deleteDisciplinas(id_professor):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            delete from professor_disciplina
            where id_professor = ?
            """,
            (id_professor,)
        )

        conn.commit()
        conn.close()

    @staticmethod
    def addDisciplina(id_professor, id_disciplina):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            insert into professor_disciplina (id_professor, id_disciplina)
            values (?, ?)
            """,
            (id_professor, id_disciplina)
        )

    @staticmethod
    def update(id_professor, nome, matricula):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                update professor
                set nome = ?, matricula = ?
                where id = ?
                """,
                (nome, matricula, id_professor)
            )

            conn.commit()
            return True

        except Exception as e:
            print("erro ao atualizar professor:", e)
            return False

        finally:
            conn.close()

    @staticmethod
    def update_com_disciplinas(id_professor, nome, matricula, ids_disciplinas):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # 1. atualiza dados básicos
            cursor.execute(
                """
                update professor
                set nome = ?, matricula = ?
                where id = ?
                """,
                (nome, matricula, id_professor)
            )

            # 2. remove vínculos antigos
            cursor.execute(
                "delete from professor_disciplina where id_professor = ?",
                (id_professor,)
            )

            # 3. adiciona novos vínculos
            for id_disciplina in ids_disciplinas:
                cursor.execute(
                    """
                    insert into professor_disciplina (id_professor, id_disciplina)
                    values (?, ?)
                    """,
                    (id_professor, id_disciplina)
                )

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            print("erro ao atualizar professor:", e)
            return False

        finally:
            conn.close()

    @staticmethod
    def delete(id_professor):
        queries = [
            "DELETE FROM aula WHERE id_professor = ?",
            "DELETE FROM professor_indisponibilidade WHERE id_professor = ?",
            "DELETE FROM professor_disciplina WHERE id_professor = ?",
            "DELETE FROM professor WHERE id = ?"
        ]

        params = [
            (id_professor,),
            (id_professor,),
            (id_professor,),
            (id_professor,)
        ]

        BaseModel.execute_delete(queries, params)