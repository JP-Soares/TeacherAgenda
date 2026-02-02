import tkinter as tk
from tkinter import ttk, messagebox

from models.professor import Professor
from models.curso import Curso
from models.disciplina import Disciplina
from models.turma import Turma
from models.turno import Turno
from ui.professor_form import ProfessorForm
from ui.curso_form import CursoForm
from ui.disciplina_form import DisciplinaForm
from ui.turma_form import TurmaForm
from ui.turno_form import TurnoForm



MODELS = {
    "professor": (Professor, ["ID", "Nome", "Matrícula"]),
    "curso": (Curso, ["ID", "Nome", "Carga Horária"]),
    "disciplina": (Disciplina, ["ID", "Nome", "Carga Horária"]),
    "turma": (Turma, ["ID", "Nome", "Empresa", "Localidade"]),
    "turno": (Turno, ["ID", "Nome"])
}

FORMS = {
    "professor": ProfessorForm,
    "curso": CursoForm,
    "disciplina": DisciplinaForm,
    "turma": TurmaForm,
    "turno": TurnoForm
}



class ListaView:
    def __init__(self, parent, tipo):
        self.tipo = tipo
        self.model, self.columns = MODELS[tipo]

        self.window = tk.Toplevel(parent)
        self.window.title(f"Lista de {tipo.capitalize()}")
        self.window.geometry("600x400")

        self.build_ui()
        self.load_data()

    def build_ui(self):
        frame = tk.Frame(self.window)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(
            frame,
            columns=self.columns,
            show="headings"
        )

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="w")

        self.tree.pack(fill="both", expand=True)

        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=8)

        tk.Button(
            btn_frame,
            text="Novo",
            command=self.novo
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Excluir",
            command=self.excluir
        ).pack(side="left", padx=5)

    def load_data(self):
        self.tree.delete(*self.tree.get_children())

        for item in self.model.getAll():
            self.tree.insert("", "end", values=item)

    def novo(self):
        form_class = FORMS.get(self.tipo)

        if not form_class:
            
            return

        form = form_class(self.window)
        self.window.wait_window(form.window)

        #Atualiza lista após salvar
        self.load_data()


    def excluir(self):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        id_item = values[0]

        if messagebox.askyesno("Confirmar", "Deseja excluir?"):
            self.model.delete(id_item)
            self.load_data()
