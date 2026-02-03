from models.aula import Aula

class AulaService:

    @staticmethod
    def verifica_campos(
        id_professor,
        id_disciplina,
        id_curso,
        id_agenda,
        id_turno,
        id_turma
    ):
        if not all([
            id_professor,
            id_disciplina,
            id_curso,
            id_agenda,
            id_turno,
            id_turma
        ]):
            return False, 'Campos inválidos!'
        return True, None

    @staticmethod
    def professor_tem_conflito(id_professor, id_agenda, id_turno):
        aulas = Aula.getByProfessorAgendaTurno(
            id_professor,
            id_agenda,
            id_turno
        )
        return len(aulas) > 0

    @staticmethod
    def turma_tem_conflito(id_turma, id_agenda, id_turno):
        aulas = Aula.getByTurmaAgendaTurno(
            id_turma,
            id_agenda,
            id_turno
        )
        return len(aulas) > 0

    @staticmethod
    def agendar_aula(
        id_professor,
        id_disciplina,
        id_curso,
        id_agenda,
        id_turno,
        id_turma
    ):
        # 1. valida campos
        valido, msg = AulaService.verifica_campos(
            id_professor,
            id_disciplina,
            id_curso,
            id_agenda,
            id_turno,
            id_turma
        )
        if not valido:
            return False, msg

        #2. conflito de professor
        if AulaService.professor_tem_conflito(
            id_professor, id_agenda, id_turno
        ):
            return False, "O professor já possui aula neste dia e turno."

        #3. conflito de turma
        if AulaService.turma_tem_conflito(
            id_turma, id_agenda, id_turno
        ):
            return False, "A turma já possui aula neste dia e turno."

        #4. persistência (MODEL)
        Aula.add(
            id_professor,
            id_disciplina,
            id_curso,
            id_agenda,
            id_turno,
            id_turma
        )

        return True, "Aula cadastrada com sucesso!"
    
    @staticmethod
    def excluir_aula(id_aula):
        sucesso = Aula.delete(id_aula)
        if sucesso:
            return True, "Aula excluída com sucesso!"
        return False, "Erro ao excluir aula."
