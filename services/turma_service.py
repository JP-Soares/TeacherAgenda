from database.db import get_connection
from models.turma import Turma
from models.aula import Aula

class TurmaService:

    @staticmethod
    def add(nome, empresa, localidade, id_curso):
        if not all([nome, empresa, localidade, id_curso]):
            return False, "campos obrigatórios não preenchidos"

        Turma.add(nome, empresa, localidade, id_curso)
        return True, "turma cadastrada com sucesso"
    
    @staticmethod
    def update(id_turma, nome, empresa, localidade, id_curso):
        if not nome or not empresa or not localidade:
            return False, "preencha todos os campos"

        if not id_curso:
            return False, "selecione um curso"

        Turma.update(id_turma, nome, empresa, localidade, id_curso)
        return True, "turma atualizada com sucesso"
    
    @staticmethod
    def delete(id_turma):
        aulas = Aula.deleteByTurma(id_turma)
        sucesso = Turma.delete(id_turma)

        if sucesso:
            return True, f"Turma excluída.\nAulas removidas: {aulas}"
        return False, "Não foi possível excluir a turma"

