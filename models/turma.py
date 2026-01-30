from database.db import get_connection

class Turma:
    def __init__(self, id, nome, empresa, localidade):
        self.id = id
        self.nome = nome
        self.empresa = empresa,
        self.localidade = localidade

    @staticmethod
    def validate(nome, empresa, localidade):
        if nome != '' and empresa != '' and localidade != '':
            return True
        return False

    @staticmethod
    def add(nome, empresa, localidade):
        if Turma.validate(nome, empresa, localidade):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO turma (nome, empresa, localidade) VALUES (?, ?, ?)",
                               (nome, empresa, localidade))
                conn.commit()
                conn.close()
                return True
            except Exception as e:
                print("Erro ao adicionar turma:", e)
                return False
        return False

    @staticmethod
    def update(id, nome, empresa, localidade):
        if Turma.validate(nome, empresa, localidade):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE turma SET nome=?, empresa=?, localidade=? WHERE id=?",
                               (nome, empresa, localidade, id))
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
