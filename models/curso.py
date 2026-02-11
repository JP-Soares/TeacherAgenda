from database.db import get_connection
from models.base_model import BaseModel

class Curso:
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
        if Curso.validate(nome, carga_horaria):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO curso (nome, carga_horaria) VALUES (?, ?)",
                               (nome, carga_horaria))
                conn.commit()
                conn.close()
                return True
            except Exception as e:
                print("Erro ao adicionar curso:", e)
                return False
        return False

    @staticmethod
    def update(id, nome, carga_horaria):
        if Curso.validate(nome, carga_horaria):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE curso SET nome=?, carga_horaria=? WHERE id=?",
                               (nome, carga_horaria, id))
                conn.commit()
                conn.close()
                return True
            except Exception as e:
                print("Erro ao atualizar curso:", e)
                return False
        return False

    @staticmethod
    def getById(id):
        if id != '':
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM curso WHERE id = ?", (id,))
                resultado = cursor.fetchone()
                conn.close()
                return resultado
            except Exception as e:
                print("Erro ao buscar curso:", e)
                return None
        return None
    
    @staticmethod
    def getAll():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM curso")
            resultado = cursor.fetchall()
            conn.close()
            return resultado
        except Exception as e:
                print("Erro ao buscar curso:", e)
                return None

    @staticmethod
    def getByDisciplinas(ids_disciplinas):
        if not ids_disciplinas:
            return []

        placeholders = ",".join("?" * len(ids_disciplinas))

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT DISTINCT c.id, c.nome
            FROM curso c
            JOIN curso_disciplina cd ON cd.id_curso = c.id
            WHERE cd.id_disciplina IN ({placeholders})
        """, ids_disciplinas)

        dados = cursor.fetchall()
        conn.close()
        return dados
    
    @staticmethod
    def getDisciplinas(id_curso):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            select d.id, d.nome
            from disciplina d
            join curso_disciplina cd on cd.id_disciplina = d.id
            where cd.id_curso = ?
            order by d.nome
        """, (id_curso,))

        disciplinas = cursor.fetchall()
        conn.close()
        return disciplinas
    
    @staticmethod
    def delete(id_curso):
        queries = [
            "DELETE FROM aula WHERE id_curso = ?",
            "DELETE FROM turma WHERE id_curso = ?",
            "DELETE FROM curso_disciplina WHERE id_curso = ?",
            "DELETE FROM curso WHERE id = ?"
        ]

        params = [
            (id_curso,),
            (id_curso,),
            (id_curso,),
            (id_curso,)
        ]

        BaseModel.execute_delete(queries, params)
