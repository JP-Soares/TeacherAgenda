import tkinter as tk
from tkinter import ttk, messagebox

from services.aula_service import AulaService
from models.professor import Professor
from models.disciplina import Disciplina
from models.curso import Curso
from models.turma import Turma
from models.turno import Turno


class AulaForm:
    def __init__(self, parent, data):
        self.window = tk.Toplevel(parent)
        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus_force()
        self.window.lift()
        self.window.attributes("-topmost", True)
        self.window.after(100, lambda: self.window.attributes("-topmost", False))

        self.data = data

        self.window.title("Cadastro de Aula")
        self.window.geometry("480x520")
        self.window.configure(bg="#f4f6f8")

        self.build_form()

    # ================= FORM =================
    def build_form(self):
        frame = tk.Frame(self.window, bg="#ffffff", padx=20, pady=20)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            frame,
            text="Agendar Aula",
            font=("Segoe UI", 16, "bold"),
            bg="#ffffff"
        ).pack(pady=(0, 20))

        # ===== Professor =====
        self.professores = Professor.getAll()
        self.prof_var = tk.StringVar()
        self.prof_combo = self.create_combo(
            frame, "Professor", self.prof_var, self.professores
        )
        self.prof_combo.bind("<<ComboboxSelected>>", self.on_professor_change)

        # ===== Disciplina =====
        self.disciplinas = []
        self.disc_var = tk.StringVar()
        self.disc_combo = self.create_combo(
            frame, "Disciplina", self.disc_var, []
        )
        self.disc_combo.bind("<<ComboboxSelected>>", self.on_disciplina_change)

        # ===== Curso =====
        self.cursos = []
        self.curso_var = tk.StringVar()
        self.curso_combo = self.create_combo(
            frame, "Curso", self.curso_var, []
        )
        self.curso_combo.bind("<<ComboboxSelected>>", self.on_curso_change)

        # ===== Turma =====
        self.turmas = []
        self.turma_var = tk.StringVar()
        self.turma_combo = self.create_combo(
            frame, "Turma", self.turma_var, []
        )

        # ===== Turno =====
        self.turnos = Turno.getAll()
        self.turno_var = tk.StringVar()
        self.turno_combo = self.create_combo(
            frame, "Turno", self.turno_var, self.turnos
        )

        # ===== Botão =====
        tk.Button(
            frame,
            text="Salvar",
            bg="#1976d2",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            command=self.salvar
        ).pack(pady=25, ipadx=10, ipady=6)

    # ================= COMPONENT =================
    def create_combo(self, parent, label, var, data):
        tk.Label(parent, text=label, bg="#ffffff").pack(anchor="w")

        valores = [""] + [item[1] for item in data]

        combo = ttk.Combobox(
            parent,
            textvariable=var,
            values=valores,
            state="readonly"
        )
        combo.pack(fill="x", pady=5)

        var.set("")  # começa vazio SEM seleção automática

        return combo

    # ================= SAVE =================
    def salvar(self):
        id_professor = self.get_id(self.prof_var.get(), self.professores)
        id_disciplina = self.get_id(self.disc_var.get(), self.disciplinas)
        id_curso = self.get_id(self.curso_var.get(), self.cursos)
        id_turma = self.get_id(self.turma_var.get(), self.turmas)
        id_turno = self.get_id(self.turno_var.get(), self.turnos)

        dados = {
            "Professor": id_professor,
            "Disciplina": id_disciplina,
            "Curso": id_curso,
            "Turma": id_turma,
            "Turno": id_turno
        }

        if not self.validar(dados):
            return

        try:
            sucesso, msg = AulaService.adicionar(
                self.data,
                id_professor,
                id_disciplina,
                id_curso,
                id_turno,
                id_turma
            )

            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                self.window.destroy()
            else:
                messagebox.showwarning("Atenção", msg)

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # ================= HELPERS =================
    def get_id(self, nome, lista):
        for item in lista:
            if item[1] == nome:
                return item[0]
        return None

    def validar(self, dados):
        for nome, valor in dados.items():
            if valor is None:
                messagebox.showwarning(
                    "Atenção",
                    f"Campo obrigatório não selecionado: {nome}"
                )
                return False
        return True

    # ================= EVENTS =================
    def on_professor_change(self, event):
        id_professor = self.get_id(self.prof_var.get(), self.professores)

        self.disciplinas = Disciplina.getByProfessor(id_professor)
        self.update_combo(self.disc_combo, self.disc_var, self.disciplinas)

        self.cursos = []
        self.update_combo(self.curso_combo, self.curso_var, self.cursos)

        self.turmas = []
        self.update_combo(self.turma_combo, self.turma_var, self.turmas)

    def on_curso_change(self, event):
        id_curso = self.get_id(self.curso_var.get(), self.cursos)
        if not id_curso:
            return

        self.turmas = Turma.getByCurso(id_curso)
        self.update_combo(self.turma_combo, self.turma_var, self.turmas)



    def on_disciplina_change(self, event):
        id_disciplina = self.get_id(self.disc_var.get(), self.disciplinas)
        if not id_disciplina:
            return

        self.cursos = Curso.getByDisciplinas([id_disciplina])
        self.update_combo(self.curso_combo, self.curso_var, self.cursos)

        self.update_combo(self.turma_combo, self.turma_var, [])



    def update_combo(self, combo, var, data):
        valores = [""] + [item[1] for item in data]
        combo["values"] = valores
        var.set("")

