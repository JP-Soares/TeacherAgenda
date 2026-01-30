from database.db import get_connection

class Professor:
    def __init__(self, id, matricula, nome):
        self.id = id
        self.nome = nome
        self.marticula = matricula

    @staticmethod
    def validate(nome, marticula):
        if nome != '' and marticula != '':
            return True
        return False

    @staticmethod
    def add(nome, marticula):
        if Professor.validate(nome, marticula):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO professor (nome, marticula) VALUES (?, ?)",
                               (nome, marticula))
                conn.commit()
                conn.close()
                return True
            except Exception as e:
                print("Erro ao adicionar professor:", e)
                return False
        return False

    @staticmethod
    def update(id, nome, marticula):
        if Professor.validate(nome, marticula):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE professor SET nome=?, marticula=? WHERE id=?",
                               (nome, marticula, id))
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