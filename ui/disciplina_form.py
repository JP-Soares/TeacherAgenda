import tkinter as tk
from services.disciplina_service import DisciplinaService

class DisciplinaForm:
    def __init__(self, parent):
        self.w = tk.Toplevel(parent)
        self.w.title("Disciplina")
        self.w.geometry("400x300")

        tk.Label(self.w, text="Nome").pack()
        self.nome = tk.Entry(self.w)
        self.nome.pack(fill="x", padx=20)

        tk.Label(self.w, text="Carga Horária").pack()
        self.carga = tk.Entry(self.w)
        self.carga.pack(fill="x", padx=20)

        tk.Button(self.w, text="Salvar", command=self.save).pack(pady=20)

    def save(self):
        DisciplinaService.add(self.nome.get(), self.carga.get())
        self.w.destroy()
