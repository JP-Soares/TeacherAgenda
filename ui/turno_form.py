import tkinter as tk
from services.turno_service import TurnoService

class TurnoForm:
    def __init__(self, parent):
        self.w = tk.Toplevel(parent)
        self.w.title("Turno")
        self.w.geometry("300x200")

        tk.Label(self.w, text="Nome").pack()
        self.nome = tk.Entry(self.w)
        self.nome.pack(fill="x", padx=20)

        tk.Button(self.w, text="Salvar", command=self.save).pack(pady=20)

    def save(self):
        TurnoService.add(self.nome.get())
        self.w.destroy()
