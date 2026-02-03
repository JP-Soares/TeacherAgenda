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
    def existe_conflito(id_turma, id_agenda, id_turno):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 1
            FROM aula
            WHERE id_turma = ?
              AND id_agenda = ?
              AND id_turno = ?
        """, (id_turma, id_agenda, id_turno))

        existe = cursor.fetchone() is not None
        conn.close()
        return existe

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

    #get class from a specific teacher, date and shift
    @staticmethod
    def getByProfessorAgendaTurno(id_professor, id_agenda, id_turno):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM aula
                WHERE id_professor = ?
                AND id_agenda = ?
                AND id_turno = ?
            """, (id_professor, id_agenda, id_turno))

            resultado = cursor.fetchall()
            conn.close()

            return resultado or []  # 👈 SEMPRE lista

        except Exception as e:
            print("Erro ao buscar aulas do professor:", e)
            return []
    
    @staticmethod
    def getAll():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM aula")
            resultado = cursor.fetchall()
            conn.close()
            return resultado
        except Exception as e:
                print("Erro ao buscar aula:", e)
                return None
        
    @staticmethod
    def getByData(dia, mes, ano):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            data = f"{ano:04d}-{mes:02d}-{dia:02d}"

            cursor.execute("""
                SELECT
                    a.id,
                    d.nome AS disciplina,
                    t.nome AS turma,
                    tu.nome AS turno,
                    p.nome AS professor
                FROM aula a
                JOIN agenda ag ON ag.id = a.id_agenda
                JOIN disciplina d ON d.id = a.id_disciplina
                JOIN turma t ON t.id = a.id_turma
                JOIN turno tu ON tu.id = a.id_turno
                JOIN professor p ON p.id = a.id_professor
                WHERE ag.data = ?
                ORDER BY tu.nome
            """, (data,))

            aulas = cursor.fetchall()
            conn.close()
            return aulas

        except Exception as e:
            print("Erro ao buscar aulas:", e)
            return []
        
    @staticmethod
    def getByTurmaAgendaTurno(id_turma, id_agenda, id_turno):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM aula
                WHERE id_turma = ?
                  AND id_agenda = ?
                  AND id_turno = ?
            """, (id_turma, id_agenda, id_turno))

            resultado = cursor.fetchall()
            conn.close()

            #SEMPRE retorna lista
            return resultado or []

        except Exception as e:
            print("Erro ao buscar aulas da turma:", e)
            return []
        
    @staticmethod
    def delete(id_aula):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM aula WHERE id = ?",
                (id_aula,)
            )

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print("Erro ao deletar aula:", e)
            return False
