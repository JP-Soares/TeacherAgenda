from models.curso import Curso
from database.db import get_connection
from models.turma import Turma
from models.aula import Aula

class CursoService:

    @staticmethod
    def validar_campos(nome, carga_horaria):
        if not nome or not carga_horaria:
            return False, "preencha todos os campos"

        if not str(carga_horaria).isdigit():
            return False, "carga horária inválida"

        return True, None

    @staticmethod
    def add(nome, carga_horaria, disciplinas_ids):
        valido, msg = CursoService.validar_campos(nome, carga_horaria)
        if not valido:
            return False, msg

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "insert into curso (nome, carga_horaria) values (?, ?)",
                (nome, carga_horaria)
            )
            id_curso = cursor.lastrowid

            for id_disciplina in disciplinas_ids:
                cursor.execute(
                    "insert into curso_disciplina (id_curso, id_disciplina) values (?, ?)",
                    (id_curso, id_disciplina)
                )

            conn.commit()
            return True, "curso cadastrado com sucesso"

        except Exception as e:
            conn.rollback()
            print("erro ao cadastrar curso:", e)
            return False, "erro ao cadastrar curso"

        finally:
            conn.close()

    @staticmethod
    def update(id_curso, nome, carga_horaria, disciplinas_ids):
        valido, msg = CursoService.validar_campos(nome, carga_horaria)
        if not valido:
            return False, msg

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "update curso set nome = ?, carga_horaria = ? where id = ?",
                (nome, carga_horaria, id_curso)
            )

            # remove disciplinas antigas
            cursor.execute(
                "delete from curso_disciplina where id_curso = ?",
                (id_curso,)
            )

            # adiciona as novas
            for id_disciplina in disciplinas_ids:
                cursor.execute(
                    "insert into curso_disciplina (id_curso, id_disciplina) values (?, ?)",
                    (id_curso, id_disciplina)
                )

            conn.commit()
            return True, "curso atualizado com sucesso"

        except Exception as e:
            conn.rollback()
            print("erro ao atualizar curso:", e)
            return False, "erro ao atualizar curso"

        finally:
            conn.close()

    @staticmethod
    def delete(id_curso):
        aulas = Aula.deleteByCurso(id_curso)
        CursoDisciplina.deleteByCurso(id_curso)
        turmas = Turma.getByCurso(id_curso)
        qtd_turmas = len(turmas)
        for t in turmas:
            Aula.deleteByTurma(t[0])
            Turma.delete(t[0])
        sucesso = Curso.delete(id_curso)
        if sucesso:
            return True, (
                "Curso excluído com sucesso.\n\n"
                f"Turmas removidas: {qtd_turmas}\n"
                f"Aulas removidas: {aulas}"
            )
        return False, "Não foi possível excluir o curso"