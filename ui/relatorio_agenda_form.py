import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from services.agenda_service import AgendaService
from services.relatorio_service import RelatorioService
from datetime import datetime


class RelatorioAgendaForm:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)
        self.window.title("Emitir Relatório")
        self.window.geometry("400x300")

        tk.Label(self.window, text="Data Início").pack()
        self.entry_inicio = tk.Entry(self.window)
        self.entry_inicio.pack()
        self.entry_inicio.bind("<KeyRelease>", RelatorioAgendaForm.formatar_data)

        tk.Label(self.window, text="Data Fim").pack()
        self.entry_fim = tk.Entry(self.window)
        self.entry_fim.pack()
        self.entry_fim.bind("<KeyRelease>", RelatorioAgendaForm.formatar_data)


        tk.Label(self.window, text="Tipo de Relatório").pack()

        self.tipo = ttk.Combobox(
            self.window,
            values=[
                "1 - Somente Aulas",
                "2 - Aulas + Indisponibilidade",
                "3 - Somente Indisponibilidade"
            ]
        )
        self.tipo.pack(fill="x", padx=20)

        tk.Button(
            self.window,
            text="Gerar Relatório",
            command=self.gerar
        ).pack(pady=20)


    def gerar(self):

        if not self.entry_inicio.get() or not self.entry_fim.get():
            messagebox.showerror("Erro", "Informe o período.")
            return

        if not self.tipo.get():
            messagebox.showerror("Erro", "Selecione o tipo de relatório.")
            return

        try:
            # Converter para datetime REAL
            data_inicio_obj = datetime.strptime(
                self.entry_inicio.get(), "%d/%m/%Y"
            )

            data_fim_obj = datetime.strptime(
                self.entry_fim.get(), "%d/%m/%Y"
            )

        except ValueError:
            messagebox.showerror("Erro", "Data inválida.")
            return

        tipo = int(self.tipo.get()[0])

        dados = AgendaService.gerar_dados_relatorio(
            tipo,
            data_inicio_obj.strftime("%Y-%m-%d"),
            data_fim_obj.strftime("%Y-%m-%d")
        )

        caminho = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )

        if not caminho:
            return

        RelatorioService.gerar_pdf(
            dados,
            data_inicio_obj,   # ← agora é datetime
            data_fim_obj,      # ← agora é datetime
            caminho
        )

        messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")
        self.window.destroy()


    def formatar_data(event):
        texto = event.widget.get()
        texto = texto.replace("/", "")

        if len(texto) > 2:
            texto = texto[:2] + "/" + texto[2:]
        if len(texto) > 5:
            texto = texto[:5] + "/" + texto[5:9]

        event.widget.delete(0, "end")
        event.widget.insert(0, texto)
