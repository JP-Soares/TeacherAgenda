import tkinter as tk
from tkinter import messagebox

from services.turno_service import TurnoService
from models.turno import Turno


class TurnoForm:
    def __init__(self, parent, id_turno=None):
        self.id_turno = id_turno

        self.window = tk.Toplevel(parent)
        self.window.title("Professor")

        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus_force()
        
        self.window.title("turno")
        self.window.geometry("300x200")

        tk.Label(self.window, text="nome").pack(pady=(20, 0))
        self.nome = tk.Entry(self.window)
        self.nome.pack(fill="x", padx=20)

        tk.Button(
            self.window,
            text="salvar",
            command=self.save
        ).pack(pady=20)

        if self.id_turno:
            self.carregar_dados()

    def carregar_dados(self):
        turno = Turno.getById(self.id_turno)
        if not turno:
            return

        _, nome = turno
        self.nome.insert(0, nome)

    def save(self):
        nome = self.nome.get().strip()

        if not nome:
            messagebox.showerror(
                "erro",
                "preencha o nome"
            )
            return

        if self.id_turno:
            sucesso, msg = TurnoService.update(
                self.id_turno,
                nome
            )
        else:
            sucesso, msg = TurnoService.add(nome)

        if sucesso:
            self.window.destroy()
        else:
            messagebox.showerror("erro", msg)
