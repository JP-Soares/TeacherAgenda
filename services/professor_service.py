from database.db import get_connection
from models.professor import Professor
from models.aula import Aula
from models.indisponibilidade import Indisponibilidade

class ProfessorService:
    @staticmethod
    def add(nome, matricula, ids_disciplinas):

        if not nome or not nome.strip():
            return False, "O nome do professor é obrigatório."

        if not matricula or not matricula.strip():
            return False, "A matrícula é obrigatória."

        if not ids_disciplinas:
            return False, "Selecione pelo menos uma disciplina."

        try:
            Professor.add(nome.strip(), matricula.strip(), ids_disciplinas)
            return True, "Professor cadastrado com sucesso."
        except Exception as e:
            return False, f"Erro ao cadastrar professor: {str(e)}"


    @staticmethod
    def update(id_professor, nome, matricula, ids_disciplinas):
        if not nome or not matricula:
            return False, "campos obrigatórios não preenchidos"
        
        if not ids_disciplinas:
            return False, "Selecione pelo menos uma disciplina."

        sucesso = Professor.update_com_disciplinas(
            id_professor,
            nome,
            matricula,
            ids_disciplinas
        )

        if sucesso:
            return True, "professor atualizado com sucesso"

        return False, "erro ao atualizar professor"

