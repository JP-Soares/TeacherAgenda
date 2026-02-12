from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4, landscape

from datetime import timedelta


class RelatorioService:

    @staticmethod
    def gerar_pdf(dados, data_inicio, data_fim, caminho_arquivo):

        doc = SimpleDocTemplate(
            caminho_arquivo,
            pagesize=landscape(A4)
        )

        elementos = []
        styles = getSampleStyleSheet()

        # =============================
        # TÍTULO
        # =============================
        elementos.append(Paragraph("Relatório de Agenda", styles["Heading1"]))
        elementos.append(Spacer(1, 0.3 * inch))

        periodo_texto = f"Período: {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}"
        elementos.append(Paragraph(periodo_texto, styles["Normal"]))
        elementos.append(Spacer(1, 0.5 * inch))

        # =============================
        # ORGANIZAR DATAS POR SEMANA (SEM DOMINGO)
        # =============================
        data_atual = data_inicio
        semanas = []

        while data_atual <= data_fim:
            semana = []
            for _ in range(7):
                if data_atual > data_fim:
                    break

                # Ignorar domingo
                if data_atual.weekday() != 6:
                    semana.append(data_atual)

                data_atual += timedelta(days=1)

            if semana:
                semanas.append(semana)

        dias_semana = {
            0: "Seg",
            1: "Ter",
            2: "Qua",
            3: "Qui",
            4: "Sex",
            5: "Sáb",
        }

        # =============================
        # GERAR UMA TABELA POR SEMANA
        # =============================
        for indice, semana in enumerate(semanas):

            elementos.append(Paragraph(f"Semana {indice + 1}", styles["Heading3"]))
            elementos.append(Spacer(1, 0.2 * inch))

            cabecalho = ["Professor"]

            for data in semana:
                dia = dias_semana.get(data.weekday())
                cabecalho.append(f"{data.strftime('%d/%m')} ({dia})")

            tabela = [cabecalho]

            # =============================
            # LINHAS DOS PROFESSORES
            # =============================
            for professor in sorted(dados.keys()):

                linha = [professor]
                agenda_prof = dados.get(professor, {})

                for data in semana:
                    data_str = data.strftime("%Y-%m-%d")
                    registros = agenda_prof.get(data_str, [])

                    if registros:
                        textos = []

                        for item in registros:

                            if isinstance(item, dict):

                                turno = item.get("turno", "")
                                disciplina = item.get("disciplina", "")
                                turma = item.get("turma", "")
                                curso = item.get("curso", "")
                                localidade = item.get("localidade", "")

                                texto = (
                                    f"<b>{turno}</b><br/>"
                                    f"{disciplina}<br/>"
                                    f"Turma: {turma} - {localidade}<br/>"
                                    f"{curso}"
                                )
                            else:
                                texto = f"<b>{item}</b>"

                            textos.append(texto)

                        conteudo = "<br/><br/>".join(textos)
                        linha.append(Paragraph(conteudo, styles["Normal"]))
                    else:
                        linha.append("-")

                tabela.append(linha)

            table = Table(
                tabela,
                repeatRows=1
            )

            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))

            elementos.append(table)
            elementos.append(Spacer(1, 0.5 * inch))

        doc.build(elementos)
