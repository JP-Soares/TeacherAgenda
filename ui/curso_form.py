import tkinter as tk
from services.disciplina_service import DisciplinaService
from services.curso_service import CursoService
from models.curso import Curso
from tkinter import messagebox

class CursoForm:
    def __init__(self, parent, id_curso=None):
        self.id_curso = id_curso

        self.window = tk.Toplevel(parent)
        self.window.title("Professor")

        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus_force()
        
        self.window.title("curso")
        self.window.geometry("450x500")

        tk.Label(self.window, text="nome").pack()
        self.nome = tk.Entry(self.window)
        self.nome.pack(fill="x", padx=20)

        tk.Label(self.window, text="carga horária").pack()
        self.carga = tk.Entry(self.window)
        self.carga.pack(fill="x", padx=20)

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

        tk.Button(self.window, text="salvar", command=self.save).pack(pady=20)

        if self.id_curso:
            self.carregar_dados()

    def carregar_dados(self):
        curso = Curso.getById(self.id_curso)

        self.nome.insert(0, curso[1])
        self.carga.insert(0, curso[2])

        disciplinas_curso = Curso.getDisciplinas(self.id_curso)
        ids = [d[0] for d in disciplinas_curso]

        for i, d in enumerate(self.disciplinas):
            if d[0] in ids:
                self.listbox.selection_set(i)

    def save(self):
        ids = [self.disciplinas[i][0] for i in self.listbox.curselection()]

        if self.id_curso:
            sucesso, msg = CursoService.update(
                self.id_curso,
                self.nome.get(),
                self.carga.get(),
                ids
            )
        else:
            sucesso, msg = CursoService.add(
                self.nome.get(),
                self.carga.get(),
                ids
            )

        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.window.destroy()
        else:
            messagebox.showerror("Erro", msg)
