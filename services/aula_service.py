from models.aula import Aula

class AulaService:

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
    def agendar_aula(id_professor, id_disciplina, id_curso, id_agenda, id_turno, id_turma):

        if AulaService.professor_tem_conflito(id_professor, id_agenda, id_turno):
            return False, "Professor já possui aula nesse horário"

        if AulaService.turma_tem_conflito(id_turma, id_agenda, id_turno):
            return False, "Turma já possui aula nesse horário"

        sucesso = Aula.add(
            id_professor,
            id_disciplina,
            id_curso,
            id_agenda,
            id_turno,
            id_turma
        )

        if sucesso:
            return True, "Aula agendada com sucesso"

        return False, "Erro ao agendar aula"
