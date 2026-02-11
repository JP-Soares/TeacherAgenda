from database.db import get_connection
from models.disciplina import Disciplina
from models.aula import Aula

class DisciplinaService:
    @staticmethod
    def validar_campos(nome, carga):
        if not nome or not nome.strip():
            return False, "Informe o nome da disciplina."

        if not carga or not str(carga).strip():
            return False, "Informe a carga horária."

        if not str(carga).isdigit():
            return False, "Carga horária deve ser numérica."

        return True, None


    @staticmethod
    def get_all():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nome FROM disciplina")
        data = cur.fetchall()
        conn.close()
        return data

    @staticmethod
    def add(nome, carga):
        valido, msg = DisciplinaService.validar_campos(nome, carga)
        if not valido:
            return False, msg

        sucesso = Disciplina.add(nome.strip(), carga)

        if sucesso:
            return True, "Disciplina cadastrada com sucesso."
        return False, "Erro ao cadastrar disciplina."


    @staticmethod
    def update(id_disciplina, nome, carga):
        valido, msg = DisciplinaService.validar_campos(nome, carga)
        if not valido:
            return False, msg

        sucesso = Disciplina.update(id_disciplina, nome.strip(), carga)

        if sucesso:
            return True, "Disciplina atualizada com sucesso."
        return False, "Erro ao atualizar disciplina."