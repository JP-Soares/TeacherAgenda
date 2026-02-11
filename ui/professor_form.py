import tkinter as tk
from services.disciplina_service import DisciplinaService
from services.professor_service import ProfessorService
from models.professor import Professor
from tkinter import messagebox


class ProfessorForm:
    def __init__(self, parent, id_professor=None):
        self.id_professor = id_professor

        self.window = tk.Toplevel(parent)
        self.window.title("Professor")

        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus_force()
        
        self.window.title("professor")
        self.window.geometry("450x500")

        tk.Label(self.window, text="nome").pack()
        self.nome = tk.Entry(self.window)
        self.nome.pack(fill="x", padx=20)

        tk.Label(self.window, text="matrícula").pack()
        self.matricula = tk.Entry(self.window)
        self.matricula.pack(fill="x", padx=20)

        tk.Label(self.window, text="disciplinas").pack(pady=10)
        self.listbox = tk.Listbox(
            self.window,
            selectmode=tk.MULTIPLE,
            exportselection=False
        )
        self.listbox.pack(fill="both", padx=20, expand=True)

        self.disciplinas = DisciplinaService.get_all()
        for d in self.disciplinas:
            self.listbox.insert(tk.END, d[1])

        if self.id_professor:
            self.carregar_dados()

        tk.Button(
            self.window,
            text="salvar",
            command=self.save
        ).pack(pady=20)

    def carregar_dados(self):
        professor = Professor.getById(self.id_professor)

        self.nome.insert(0, professor[1])
        self.matricula.insert(0, professor[2])

        disciplinas_prof = Professor.getDisciplinas(self.id_professor)

        for i, d in enumerate(self.disciplinas):
            if d[0] in disciplinas_prof:
                self.listbox.selection_set(i)



    def save(self):
        ids = [self.disciplinas[i][0] for i in self.listbox.curselection()]

        if self.id_professor:
            sucesso, msg = ProfessorService.update(
                self.id_professor,
                self.nome.get(),
                self.matricula.get(),
                ids
            )
        else:
            sucesso, msg = ProfessorService.add(
                self.nome.get(),
                self.matricula.get(),
                ids
            )

        if sucesso:
            self.window.destroy()
        else:
            messagebox.showerror("erro", msg)
