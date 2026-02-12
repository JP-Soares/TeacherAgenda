from models.aula import Aula
from database.db import get_connection

def can_schedule(id_professor, id_agenda, id_turno):
    aulas = Aula.getByProfessorAndAgenda(id_professor, id_agenda, id_turno)
    return len(aulas) == 0

def schedule_class(id_professor, id_disciplina, id_curso, id_agenda, id_turno, id_turma):
    if not can_schedule(id_professor, id_agenda, id_turno):
        return "Conflito de horário para o professor"

    Aula.add(id_professor, id_disciplina, id_curso, id_agenda, id_turno, id_turma)
    return "Aula agendada com sucesso"

class AgendaService:

    @staticmethod
    def gerar_dados_relatorio(tipo, data_inicio, data_fim):
        conn = get_connection()
        cursor = conn.cursor()

        dados = {}

        # =========================
        # AULAS
        # =========================
        if tipo in [1, 2]:

            query_aulas = """
                SELECT 
                    p.nome,
                    a.data,
                    t.nome as turno,
                    d.nome as disciplina,
                    tu.nome as turma,
                    c.nome as curso,
                    tu.localidade
                FROM aula a
                JOIN professor p ON p.id = a.id_professor
                JOIN turno t ON t.id = a.id_turno
                JOIN disciplina d ON d.id = a.id_disciplina
                JOIN turma tu ON tu.id = a.id_turma
                JOIN curso c ON c.id = tu.id_curso
                WHERE a.data BETWEEN ? AND ?
            """

            cursor.execute(query_aulas, (data_inicio, data_fim))
            resultados = cursor.fetchall()

            for nome, data, turno, disciplina, turma, curso, localidade in resultados:

                if nome not in dados:
                    dados[nome] = {}

                if data not in dados[nome]:
                    dados[nome][data] = []

                dados[nome][data].append({
                    "turno": turno,
                    "disciplina": disciplina,
                    "turma": turma,
                    "curso": curso,
                    "localidade": localidade
                })

        # =========================
        # INDISPONIBILIDADE
        # =========================
        if tipo in [2, 3]:

            query_ind = """
                SELECT 
                    p.nome,
                    i.data,
                    t.nome as turno
                FROM professor_indisponibilidade i
                JOIN professor p ON p.id = i.id_professor
                JOIN turno t ON t.id = i.id_turno
                WHERE i.data BETWEEN ? AND ?
            """

            cursor.execute(query_ind, (data_inicio, data_fim))
            resultados = cursor.fetchall()

            for nome, data, turno in resultados:

                if nome not in dados:
                    dados[nome] = {}

                if data not in dados[nome]:
                    dados[nome][data] = []

                dados[nome][data].append({
                    "turno": f"Indisponível ({turno})",
                    "disciplina": "",
                    "turma": "",
                    "curso": "",
                    "localidade": ""
                })

        conn.close()
        return dados



    @staticmethod
    def organizar_dados(registros):
        """
        Retorna estrutura:
        {
            "Professor": {
                "Segunda": ["Manhã", "Noite"],
                ...
            }
        }
        """

        dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]

        estrutura = {}

        for nome, dia, turno in registros:

            if nome not in estrutura:
                estrutura[nome] = {d: [] for d in dias}

            estrutura[nome][dia].append(turno)

        return estrutura
