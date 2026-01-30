import tkinter as tk
from services.turma_service import TurmaService

class TurmaForm:
    def __init__(self, parent):
        self.w = tk.Toplevel(parent)
        self.w.title("Turma")
        self.w.geometry("400x350")

        for label in ["Nome", "Empresa", "Localidade"]:
            tk.Label(self.w, text=label).pack()
            entry = tk.Entry(self.w)
            entry.pack(fill="x", padx=20)
            setattr(self, label.lower(), entry)

        tk.Button(self.w, text="Salvar", command=self.save).pack(pady=20)

    def save(self):
        TurmaService.add(
            self.nome.get(),
            self.empresa.get(),
            self.localidade.get()
        )
        self.w.destroy()
