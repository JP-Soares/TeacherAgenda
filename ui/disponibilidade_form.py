import tkinter as tk
from tkinter import ttk, messagebox

from models.professor import Professor
from models.turno import Turno
from services.indisponibilidade_service import IndisponibilidadeService


class DisponibilidadeForm:
    def __init__(self, parent, data):
        self.window = tk.Toplevel(parent)
        self.window.title("Indisponibilidade do Professor")
        self.window.geometry("420x420")
        self.window.configure(bg="#f4f6f8")
        self.window.resizable(False, False)

        self.data = data

        self.build_form()

    # ================= FORM =================
    def build_form(self):
        frame = tk.Frame(self.window, bg="#ffffff", padx=20, pady=20)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            frame,
            text="Indisponibilidade",
            font=("Segoe UI", 16, "bold"),
            bg="#ffffff"
        ).pack(pady=(0, 10))

        tk.Label(
            frame,
            text=f"Data: {self.data}",
            font=("Segoe UI", 10),
            bg="#ffffff"
        ).pack(pady=(0, 15))

        # ===== Professor =====
        tk.Label(frame, text="Professor", bg="#ffffff").pack(anchor="w")

        self.professores = Professor.getAll()
        self.prof_var = tk.StringVar()

        self.prof_combo = ttk.Combobox(
            frame,
            textvariable=self.prof_var,
            state="readonly",
            values=[p[1] for p in self.professores]
        )
        self.prof_combo.pack(fill="x", pady=5)

        if self.professores:
            self.prof_combo.current(0)

        # ===== Turnos (multiselect) =====
        tk.Label(
            frame,
            text="Turnos indisponíveis",
            bg="#ffffff"
        ).pack(anchor="w", pady=(10, 0))

        self.turnos = Turno.getAll()

        self.turnos_listbox = tk.Listbox(
            frame,
            selectmode="multiple",
            height=5,
            exportselection=False
        )
        self.turnos_listbox.pack(fill="x", pady=5)

        for turno in self.turnos:
            self.turnos_listbox.insert("end", turno[1])

        # ===== Motivo =====
        tk.Label(
            frame,
            text="Motivo (opcional)",
            bg="#ffffff"
        ).pack(anchor="w", pady=(10, 0))

        self.motivo_entry = tk.Entry(frame)
        self.motivo_entry.pack(fill="x", pady=5)

        # ===== Botão =====
        tk.Button(
            frame,
            text="Salvar",
            bg="#e53935",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            command=self.salvar
        ).pack(pady=20, ipadx=10, ipady=6)

    # ================= SAVE =================
    def salvar(self):
        professor_nome = self.prof_var.get()
        turnos_indices = self.turnos_listbox.curselection()
        motivo = self.motivo_entry.get().strip()

        if not professor_nome:
            messagebox.showwarning(
                "Atenção",
                "Selecione um professor."
            )
            return

        if not turnos_indices:
            messagebox.showwarning(
                "Atenção",
                "Selecione ao menos um turno."
            )
            return

        id_professor = self.get_id(
            professor_nome,
            self.professores
        )

        turnos_ids = [
            self.turnos[i][0] for i in turnos_indices
        ]

        sucesso, msg = IndisponibilidadeService.adicionar(
            id_professor,
            self.data,
            turnos_ids,
            motivo
        )

        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.window.destroy()
        else:
            messagebox.showerror("Erro", msg)

    # ================= UTILS =================
    def get_id(self, nome, lista):
        for item in lista:
            if item[1] == nome:
                return item[0]
        return None
