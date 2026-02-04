from models.aula import Aula
from models.indisponibilidade import Indisponibilidade


class AulaService:

    @staticmethod
    def validar_campos(
        data,
        id_professor,
        id_disciplina,
        id_curso,
        id_turno,
        id_turma
    ):
        if not all([
            data,
            id_professor,
            id_disciplina,
            id_curso,
            id_turno,
            id_turma
        ]):
            return False, "todos os campos obrigatórios devem ser preenchidos."

        return True, None

    @staticmethod
    def professor_tem_aula(
        id_professor,
        data,
        id_turno
    ):
        aulas = Aula.getByProfessorDataTurno(
            id_professor,
            data,
            id_turno
        )
        return len(aulas) > 0

    @staticmethod
    def turma_tem_aula(
        id_turma,
        data,
        id_turno
    ):
        aulas = Aula.getByTurmaDataTurno(
            id_turma,
            data,
            id_turno
        )
        return len(aulas) > 0

    @staticmethod
    def professor_esta_indisponivel(
        id_professor,
        data,
        id_turno
    ):
        indisps = Indisponibilidade.getByProfessorDataTurno(
            id_professor,
            data,
            id_turno
        )
        return len(indisps) > 0

    @staticmethod
    def adicionar(
        data,
        id_professor,
        id_disciplina,
        id_curso,
        id_turno,
        id_turma
    ):
        valido, msg = AulaService.validar_campos(
            data,
            id_professor,
            id_disciplina,
            id_curso,
            id_turno,
            id_turma
        )
        if not valido:
            return False, msg

        if AulaService.professor_esta_indisponivel(
            id_professor,
            data,
            id_turno
        ):
            return False, (
                "não é possível agendar aula. "
                "o professor está indisponível neste dia e turno."
            )

        if AulaService.professor_tem_aula(
            id_professor,
            data,
            id_turno
        ):
            return False, (
                "o professor já possui aula neste dia e turno."
            )

        if AulaService.turma_tem_aula(
            id_turma,
            data,
            id_turno
        ):
            return False, (
                "a turma já possui aula neste dia e turno."
            )

        Aula.add(
            data,
            id_professor,
            id_disciplina,
            id_curso,
            id_turno,
            id_turma
        )

        return True, "aula cadastrada com sucesso."

    @staticmethod
    def excluir(id_aula):
        sucesso = Aula.delete(id_aula)
        if sucesso:
            return True, "aula excluída com sucesso."
        return False, "erro ao excluir aula."
