from database.db import get_connection

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
