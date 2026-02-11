from database.db import get_connection
from models.base_model import BaseModel

class Disciplina:
    def __init__(self, id, nome, carga_horaria):
        self.id = id
        self.nome = nome
        self.carga_horaria = carga_horaria

    @staticmethod
    def validate(nome, carga_horaria):
        if nome != '' and carga_horaria != '':
            return True
        return False

    @staticmethod
    def add(nome, carga_horaria):
        if Disciplina.validate(nome, carga_horaria):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO disciplina (nome, carga_horaria) VALUES (?, ?)",
                               (nome, carga_horaria))
                conn.commit()
                conn.close()
                return True
            except Exception as e:
                print("Erro ao adicionar disciplina:", e)
                return False
        return False

    @staticmethod
    def update(id, nome, carga_horaria):
        if Disciplina.validate(nome, carga_horaria):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE disciplina SET nome=?, carga_horaria=? WHERE id=?",
                               (nome, carga_horaria, id))
                conn.commit()
                conn.close()
                return True
            except Exception as e:
                print("Erro ao atualizar disciplina:", e)
                return False
        return False

    @staticmethod
    def getById(id):
        if id != '':
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "select id, nome, carga_horaria from disciplina where id = ?",
                    (id)
                )
                resultado = cursor.fetchone()
                conn.close()
                return resultado
            except Exception as e:
                print("Erro ao buscar disciplina:", e)
                return None
        return None
    
    @staticmethod
    def getAll():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM disciplina")
            resultado = cursor.fetchall()
            conn.close()
            return resultado
        except Exception as e:
                print("Erro ao buscar disciplina:", e)
                return None

    @staticmethod
    def getByProfessor(id_professor):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT d.id, d.nome
            FROM disciplina d
            JOIN professor_disciplina pd ON pd.id_disciplina = d.id
            WHERE pd.id_professor = ?
        """, (id_professor,))

        dados = cursor.fetchall()
        conn.close()
        return dados
    
    @staticmethod
    def delete(id_disciplina):
        queries = [
            "DELETE FROM aula WHERE id_disciplina = ?",
            "DELETE FROM professor_disciplina WHERE id_disciplina = ?",
            "DELETE FROM curso_disciplina WHERE id_disciplina = ?",
            "DELETE FROM disciplina WHERE id = ?"
        ]

        params = [
            (id_disciplina,),
            (id_disciplina,),
            (id_disciplina,),
            (id_disciplina,)
        ]

        BaseModel.execute_delete(queries, params)
