import tkinter as tk
from ui.agenda_view import AgendaView
from ui.professor_form import ProfessorForm
from ui.turno_form import TurnoForm
from ui.disciplina_form import DisciplinaForm
from ui.turma_form import TurmaForm
from ui.curso_form import CursoForm
from ui.lista_view import ListaView


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

        menu_cadastros = tk.Menu(menubar, tearoff=0)
        menu_cadastros.add_command(
            label="Professores",
            command=lambda: self.open_lista("professor")
        )
        menu_cadastros.add_command(
            label="Cursos",
            command=lambda: self.open_lista("curso")
        )
        menu_cadastros.add_command(
            label="Disciplinas",
            command=lambda: self.open_lista("disciplina")
        )
        menu_cadastros.add_command(
            label="Turmas",
            command=lambda: self.open_lista("turma")
        )
        menu_cadastros.add_command(
            label="Turnos",
            command=lambda: self.open_lista("turno")
        )

        menubar.add_cascade(label="Cadastros", menu=menu_cadastros)

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
        
    def open_lista(self, tipo):
        ListaView(self.root, tipo)

