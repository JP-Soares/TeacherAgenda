from models.aula import Aula
from models.agenda import Agenda

def can_schedule(id_professor, id_agenda, id_turno):
    aulas = Aula.getByProfessorAndAgenda(id_professor, id_agenda, id_turno)
    return len(aulas) == 0

def schedule_class(id_professor, id_disciplina, id_curso, id_agenda, id_turno, id_turma):
    if not can_schedule(id_professor, id_agenda, id_turno):
        return "Conflito de horário para o professor"

    Aula.add(id_professor, id_disciplina, id_curso, id_agenda, id_turno, id_turma)
    return "Aula agendada com sucesso"
