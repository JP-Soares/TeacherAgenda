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
    def agendar_aula(
        id_professor,
        id_disciplina,
        id_curso,
        id_agenda,
        id_turno,
        id_turma
    ):
        #regra de negócio
        if Aula.existe_conflito(id_turma, id_agenda, id_turno):
            return False, "Já existe aula para esta turma neste dia e turno."

        # 🔹 persistência delegada ao model
        Aula.add(
            id_professor,
            id_disciplina,
            id_curso,
            id_agenda,
            id_turno,
            id_turma
        )

        return True, "Aula cadastrada com sucesso!"
