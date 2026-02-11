from database.db import get_connection
from models.base_model import BaseModel

class Turma:
    def __init__(self, id, nome, empresa, localidade, id_curso):
        self.id = id
        self.nome = nome
        self.empresa = empresa,
        self.localidade = localidade
        self.id_curso = id_curso

    @staticmethod
    def validate(nome, empresa, localidade, id_curso):
        if nome != '' and empresa != '' and localidade != '' and id_curso != '':
            return True
        return False

    @staticmethod
    def add(nome, empresa, localidade, id_curso):
        if Turma.validate(nome, empresa, localidade, id_curso):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO turma (nome, empresa, localidade, id_curso) VALUES (?, ?, ?, ?)",
                               (nome, empresa, localidade, id_curso))
                conn.commit()
                conn.close()
                return True
            except Exception as e:
                print("Erro ao adicionar turma:", e)
                return False
        return False

    @staticmethod
    def update(id, nome, empresa, localidade, id_curso):
        if Turma.validate(nome, empresa, localidade, id_curso):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE turma SET nome=?, empresa=?, localidade=?, id_curso=? WHERE id=?",
                               (nome, empresa, localidade, id_curso, id))
                conn.commit()
                conn.close()
                return True
            except Exception as e:
                print("Erro ao atualizar turma:", e)
                return False
        return False

    @staticmethod
    def getById(id):
        if id != '':
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM turma WHERE id = ?", (id,))
                resultado = cursor.fetchone()
                conn.close()
                return resultado
            except Exception as e:
                print("Erro ao buscar turma:", e)
                return None
        return None
    
    @staticmethod
    def getAll():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM turma")
            resultado = cursor.fetchall()
            conn.close()
            return resultado
        except Exception as e:
                print("Erro ao buscar turma:", e)
                return None
        
    @staticmethod
    def getByCurso(id_curso):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, nome
            FROM turma
            WHERE id_curso = ?
            ORDER BY nome
            """,
            (id_curso,)
        )

        dados = cursor.fetchall()
        conn.close()
        return dados
    
    @staticmethod
    def delete(id_turma):
        queries = [
            "DELETE FROM aula WHERE id_turma = ?",
            "DELETE FROM turma WHERE id = ?"
        ]

        params = [
            (id_turma,),
            (id_turma,)
        ]

        BaseModel.execute_delete(queries, params)
