from database.db import get_connection

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
                cursor.execute("SELECT * FROM disciplina WHERE id = ?", (id,))
                resultado = cursor.fetchone()
                conn.close()
                return resultado
            except Exception as e:
                print("Erro ao buscar disciplina:", e)
                return None
        return None
