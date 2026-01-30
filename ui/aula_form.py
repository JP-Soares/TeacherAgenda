import tkinter as tk

class AulaForm:
    def __init__(self, parent, day, month, year):
        self.window = tk.Toplevel(parent)
        self.window.title("Cadastro de Aula")
        self.window.geometry("400x420")
        self.window.configure(bg="#ffffff")

        tk.Label(
            self.window,
            text=f"Aula - {day}/{month}/{year}",
            font=("Segoe UI", 14, "bold"),
            bg="#ffffff"
        ).pack(pady=15)

        self.create_field("Professor")
        self.create_field("Disciplina")
        self.create_field("Turma")
        self.create_field("Sala")
        self.create_field("Turno")

        tk.Button(
            self.window,
            text="Salvar",
            bg="#2e7d32",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat"
        ).pack(pady=20)

    def create_field(self, label):
        tk.Label(self.window, text=label, bg="#ffffff").pack(anchor="w", padx=30)
        tk.Entry(self.window).pack(fill="x", padx=30, pady=5)
