import tkinter as tk
from ui.agenda_view import AgendaView
from ui.professor_form import ProfessorForm
from ui.turno_form import TurnoForm
from ui.disciplina_form import DisciplinaForm
from ui.turma_form import TurmaForm
from ui.curso_form import CursoForm


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Agenda de Professores")
        self.root.geometry("900x600")

        self.build_menu()

        tk.Label(
            self.root,
            text="Sistema de Agenda",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=40)

        tk.Button(
            self.root,
            text="Abrir Agenda",
            font=("Segoe UI", 12),
            width=20,
            command=self.open_agenda
        ).pack(pady=20)

        self.root.mainloop()

    # ================= MENU =================
    def build_menu(self):
        menubar = tk.Menu(self.root)

        cadastros_menu = tk.Menu(menubar, tearoff=0)
        cadastros_menu.add_command(
            label="Professor",
            command=self.open_professor
        )
        cadastros_menu.add_command(
            label="Turno",
            command=self.open_turno
        )
        cadastros_menu.add_command(
            label="Disciplina",
            command=self.open_disciplina
        )
        cadastros_menu.add_command(
            label="Turma",
            command=self.open_turma
        )
        cadastros_menu.add_command(
            label="Curso",
            command=self.open_curso
        )

        menubar.add_cascade(label="Cadastros", menu=cadastros_menu)

        self.root.config(menu=menubar)

    # ================= ACTIONS =================
    def open_agenda(self):
        self.root.withdraw()
        AgendaView(self.root)

    def open_professor(self):
        ProfessorForm(self.root)

    def open_turno(self):
        TurnoForm(self.root)

    def open_disciplina(self):
        DisciplinaForm(self.root)

    def open_turma(self):
        TurmaForm(self.root)

    def open_curso(self):
        CursoForm(self.root)
