from database.db import get_connection

class Agenda:
    def __init__(self, id, dia, id_turno, id_professor):
        self.id = id
        self.dia = dia
        self.id_turno = id_turno
        self.id_professor = id_professor

    @staticmethod
    def validate(dia, id_turno, id_professor):
        if dia != '' and id_turno != '' and id_professor != '':
            return True
        return False

    @staticmethod
    def add(dia, id_turno, id_professor):
        if Agenda.validate(dia, id_turno, id_professor):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO agenda (dia, id_turno, id_professor) VALUES (?, ?, ?)",
                               (dia, id_turno, id_professor))
                conn.commit()
                conn.close()
                return True
            except Exception as e:
                print("Erro ao adicionar agenda:", e)
                return False
        return False

    @staticmethod
    def update(id, dia, id_turno, id_professor):
        if Agenda.validate(dia, id_turno, id_professor):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE agenda SET dia=?, id_turno=?, id_professor=? WHERE id=?",
                               (dia, id_turno, id_professor, id))
                conn.commit()
                conn.close()
                return True
            except Exception as e:
                print("Erro ao atualizar agenda:", e)
                return False
        return False

    @staticmethod
    def getById(id):
        if id != '':
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM agenda WHERE id = ?", (id,))
                resultado = cursor.fetchone()
                conn.close()
                return resultado
            except Exception as e:
                print("Erro ao buscar agenda:", e)
                return None
        return None
    
    @staticmethod
    def getAll():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM agenda")
            resultado = cursor.fetchall()
            conn.close()
            return resultado
        except Exception as e:
                print("Erro ao buscar agenda:", e)
                return None
        
    @staticmethod
    def getByDia(dia, mes, ano):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id FROM agenda
            WHERE dia = ? AND mes = ? AND ano = ?
        """, (dia, mes, ano))

        agenda = cursor.fetchone()

        # Se não existir, cria
        if not agenda:
            cursor.execute("""
                INSERT INTO agenda (dia, mes, ano)
                VALUES (?, ?, ?)
            """, (dia, mes, ano))
            conn.commit()
            agenda_id = cursor.lastrowid
        else:
            agenda_id = agenda[0]

        conn.close()
        return agenda_id
