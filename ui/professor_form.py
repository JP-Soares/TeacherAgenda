import tkinter as tk
from services.disciplina_service import DisciplinaService
from services.professor_service import ProfessorService


class ProfessorForm:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("professor")
        self.window.geometry("450x500")

        tk.Label(self.window, text="nome").pack()
        self.nome = tk.Entry(self.window)
        self.nome.pack(fill="x", padx=20)

        tk.Label(self.window, text="matrícula").pack()
        self.matricula = tk.Entry(self.window)
        self.matricula.pack(fill="x", padx=20)

        tk.Label(self.window, text="disciplinas").pack(pady=10)
        self.listbox = tk.Listbox(self.window, selectmode=tk.MULTIPLE)
        self.listbox.pack(fill="both", padx=20, expand=True)

        self.disciplinas = DisciplinaService.get_all()
        for d in self.disciplinas:
            self.listbox.insert(tk.END, d[1])

        tk.Button(
            self.window,
            text="salvar",
            command=self.save
        ).pack(pady=20)

    def save(self):
        ids = [self.disciplinas[i][0] for i in self.listbox.curselection()]
        ProfessorService.add(
            self.nome.get(),
            self.matricula.get(),
            ids
        )
        self.window.destroy()
