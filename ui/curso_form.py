import tkinter as tk
from services.disciplina_service import DisciplinaService
from services.curso_service import CursoService

class CursoForm:
    def __init__(self, parent):
        self.w = tk.Toplevel(parent)
        self.w.title("Curso")
        self.w.geometry("450x500")

        tk.Label(self.w, text="Nome").pack()
        self.nome = tk.Entry(self.w)
        self.nome.pack(fill="x", padx=20)

        tk.Label(self.w, text="Carga Horária").pack()
        self.carga = tk.Entry(self.w)
        self.carga.pack(fill="x", padx=20)

        tk.Label(self.w, text="Disciplinas").pack(pady=10)
        self.listbox = tk.Listbox(self.w, selectmode=tk.MULTIPLE)
        self.listbox.pack(fill="both", padx=20)

        self.disciplinas = DisciplinaService.get_all()
        for d in self.disciplinas:
            self.listbox.insert(tk.END, d[1])

        tk.Button(self.w, text="Salvar", command=self.save).pack(pady=20)

    def save(self):
        ids = [self.disciplinas[i][0] for i in self.listbox.curselection()]
        CursoService.add(self.nome.get(), self.carga.get(), ids)
        self.w.destroy()
