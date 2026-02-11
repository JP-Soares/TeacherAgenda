from models.turno import Turno
from models.aula import Aula
from models.indisponibilidade import Indisponibilidade

class TurnoService:

    @staticmethod
    def add(nome):
        sucesso = Turno.add(nome)
        if sucesso:
            return True, "Turno cadastrado com sucesso"
        return False, "Não foi possível cadastrar o turno"

    @staticmethod
    def update(id_turno, nome):
        sucesso = Turno.update(id_turno, nome)
        if sucesso:
            return True, "Turno atualizado com sucesso"
        return False, "Não foi possível atualizar o turno"

    @staticmethod
    def delete(id_turno):
        aulas = Aula.deleteByTurno(id_turno)
        indisponibilidades = Indisponibilidade.deleteByTurno(id_turno)
        sucesso = Turno.delete(id_turno)

        if sucesso:
            return True, (
                "Turno excluído com sucesso.\n\n"
                f"Aulas removidas: {aulas}\n"
                f"Indisponibilidades removidas: {indisponibilidades}"
            )

        return False, "Não foi possível excluir o turno"