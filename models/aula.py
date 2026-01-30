from database.db import get_connection

class Aula:
    def __init__(self, id, id_professor, id_disciplina, id_curso, id_agenda, id_turno, id_turma):
        self.id = id
        self.id_professor = id_professor
        self.id_disciplina = id_disciplina
        self.id_curso = id_curso
        self.id_agenda = id_agenda
        self.id_turno = id_turno
        self.id_turma = id_turma

    @staticmethod
    def validate(id_professor, id_disciplina, id_curso, id_agenda, id_turno, id_turma):
        if all([id_professor, id_disciplina, id_curso, id_agenda, id_turno, id_turma]):
            return True
        return False

    @staticmethod
    def add(id_professor, id_disciplina, id_curso, id_agenda, id_turno, id_turma):
        if Aula.validate(id_professor, id_disciplina, id_curso, id_agenda, id_turno, id_turma):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO aula (id_professor, id_disciplina, id_curso, id_agenda, id_turno, id_turma) VALUES (?, ?, ?, ?, ?, ?)",
                               (id_professor, id_disciplina, id_curso, id_agenda, id_turno, id_turma))
                conn.commit()
                conn.close()
                return True
            except Exception as e:
                print("Erro ao adicionar aula:", e)
                return False
        return False

    @staticmethod
    def update(id, id_professor, id_disciplina, id_curso, id_agenda, id_turno, id_turma):
        if Aula.validate(id_professor, id_disciplina, id_curso, id_agenda, id_turno, id_turma):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE aula SET id_professor=?, id_disciplina=?, id_curso=?, id_agenda=?, id_turno=?, id_turma=? WHERE id=?",
                               (id_professor, id_disciplina, id_curso, id_agenda, id_turno, id_turma, id))
                conn.commit()
                conn.close()
                return True
            except Exception as e:
                print("Erro ao atualizar aula:", e)
                return False
        return False

    @staticmethod
    def getById(id):
        if id != '':
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM aula WHERE id = ?", (id,))
                resultado = cursor.fetchone()
                conn.close()
                return resultado
            except Exception as e:
                print("Erro ao buscar aula:", e)
                return None
        return None

    @staticmethod
    def getByProfessorAgendaTurno(id_professor, id_agenda, id_turno):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM aula
            WHERE id_professor = ?
            AND id_agenda = ?
            AND id_turno = ?
        """, (id_professor, id_agenda, id_turno))
        result = cursor.fetchall()
        conn.close()
        return result
