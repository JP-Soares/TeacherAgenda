from models.indisponibilidade import Indisponibilidade
from models.aula import Aula


class IndisponibilidadeService:

    @staticmethod
    def validar_campos(
        id_professor,
        data,
        turnos
    ):
        if not id_professor or not data or not turnos:
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
    def professor_ja_indisponivel(
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
        id_professor,
        data,
        turnos,
        motivo
    ):
        valido, msg = IndisponibilidadeService.validar_campos(
            id_professor,
            data,
            turnos
        )
        if not valido:
            return False, msg

        for id_turno in turnos:

            if IndisponibilidadeService.professor_tem_aula(
                id_professor,
                data,
                id_turno
            ):
                return False, (
                    "não é possível cadastrar indisponibilidade. "
                    "o professor possui aula neste dia e turno."
                )

            if IndisponibilidadeService.professor_ja_indisponivel(
                id_professor,
                data,
                id_turno
            ):
                return False, (
                    "indisponibilidade já cadastrada "
                    "para este dia e turno."
                )

            Indisponibilidade.add(
                id_professor,
                data,
                id_turno,
                motivo
            )

        return True, "indisponibilidade cadastrada com sucesso."

    @staticmethod
    def excluir(id_indisponibilidade):
        sucesso = Indisponibilidade.delete(id_indisponibilidade)
        if sucesso:
            return True, "indisponibilidade removida com sucesso."
        return False, "erro ao remover indisponibilidade."

    @staticmethod
    def getByData(data):
        return Indisponibilidade.getByData(data)
