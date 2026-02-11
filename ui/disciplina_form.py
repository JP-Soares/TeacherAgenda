import tkinter as tk
from services.disciplina_service import DisciplinaService
from models.disciplina import Disciplina
from tkinter import messagebox

class DisciplinaForm:
    def __init__(self, parent, id_disciplina=None):
        
        self.window = tk.Toplevel(parent)
        self.window.title("Professor")

        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus_force()
        
        self.window.title("disciplina")
        self.window.geometry("400x300")

        self.id_disciplina = id_disciplina

        tk.Label(self.window, text="nome").pack()
        self.nome = tk.Entry(self.window)
        self.nome.pack(fill="x", padx=20)

        tk.Label(self.window, text="carga horária").pack()
        self.carga = tk.Entry(self.window)
        self.carga.pack(fill="x", padx=20)

        tk.Button(
            self.window,
            text="salvar",
            command=self.save
        ).pack(pady=20)

        if self.id_disciplina:
            self.carregar_dados()


    def save(self):
        nome = self.nome.get()
        carga = self.carga.get()

        if self.id_disciplina:
            sucesso, msg = DisciplinaService.update(
                self.id_disciplina,
                nome,
                carga
            )
        else:
            sucesso, msg = DisciplinaService.add(
                nome,
                carga
            )

        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.window.destroy()
        else:
            messagebox.showerror("Erro", msg)


    def carregar_dados(self):
        disciplina = Disciplina.getById(self.id_disciplina)

        self.nome.insert(0, disciplina[1])
        self.carga.insert(0, disciplina[2])

