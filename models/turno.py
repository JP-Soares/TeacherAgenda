from database.db import get_connection

class Turno:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

    @staticmethod
    def validate(nome):
        if nome != '':
            return True
        return False

    @staticmethod
    def add(nome):
        if Turno.validate(nome):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO turno (nome) VALUES (?)",
                               (nome))
                conn.commit()
                conn.close()
                return True
            except Exception as e:
                print("Erro ao adicionar turno:", e)
                return False
        return False

    @staticmethod
    def update(id, nome):
        if Turno.validate(nome):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE turno SET nome=? WHERE id=?",
                               (nome, id))
                conn.commit()
                conn.close()
                return True
            except Exception as e:
                print("Erro ao atualizar turno:", e)
                return False
        return False

    @staticmethod
    def getById(id):
        if id != '':
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM turno WHERE id = ?", (id,))
                resultado = cursor.fetchone()
                conn.close()
                return resultado
            except Exception as e:
                print("Erro ao buscar turno:", e)
                return None
        return None
    
    @staticmethod
    def getAll():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM turno")
            resultado = cursor.fetchall()
            conn.close()
            return resultado
        except Exception as e:
                print("Erro ao buscar turno:", e)
                return None
