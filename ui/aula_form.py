import tkinter as tk
from tkinter import ttk, messagebox

from services.aula_service import AulaService
from models.professor import Professor
from models.disciplina import Disciplina
from models.curso import Curso
from models.turma import Turma
from models.turno import Turno
from models.agenda import Agenda


class AulaForm:
    def __init__(self, parent, day, month, year):
        self.window = tk.Toplevel(parent)
        self.window.title("Cadastro de Aula")
        self.window.geometry("480x520")
        self.window.configure(bg="#f4f6f8")

        self.day = day
        self.month = month
        self.year = year

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
        self.disciplinas = Disciplina.getAll()
        self.disc_var = tk.StringVar()
        self.disc_combo = self.create_combo(
            frame, "Disciplina", self.disc_var, []
        )

        # ===== Curso =====
        self.cursos = Curso.getAll()
        self.curso_var = tk.StringVar()
        self.curso_combo = self.create_combo(
            frame, "Curso", self.curso_var, []
        )

        # ===== Turma =====
        self.turmas = Turma.getAll()
        self.turma_var = tk.StringVar()
        self.create_combo(frame, "Turma", self.turma_var,
                          self.turmas)

        # ===== Turno =====
        self.turnos = Turno.getAll()
        self.turno_var = tk.StringVar()
        self.create_combo(frame, "Turno", self.turno_var,
                          self.turnos)

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

        valores = [item[1] for item in data]

        combo = ttk.Combobox(
            parent,
            textvariable=var,
            values=valores,
            state="readonly"
        )
        combo.pack(fill="x", pady=5)

        if valores:
            combo.current(0)

        return combo


    # ================= SAVE =================
    def salvar(self):
        try:
            id_professor = self.get_id(self.prof_var.get(), self.professores)
            id_disciplina = self.get_id(self.disc_var.get(), self.disciplinas)
            id_curso = self.get_id(self.curso_var.get(), self.cursos)
            id_turma = self.get_id(self.turma_var.get(), self.turmas)
            id_turno = self.get_id(self.turno_var.get(), self.turnos)

            # 🔹 DATA NO PADRÃO DO BANCO
            data = f"{self.year:04d}-{self.month:02d}-{self.day:02d}"

            # 🔹 BUSCA OU CRIA AGENDA
            id_agenda = Agenda.get_or_create(
                data,
                id_turno,
                id_professor
            )

            sucesso, msg = AulaService.agendar_aula(
                id_professor,
                id_disciplina,
                id_curso,
                id_agenda,
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

    def get_id(self, nome, lista):
        for item in lista:
            if item[1] == nome:
                return item[0]
        return None
    
    def on_professor_change(self, event):
        id_professor = self.get_id(
            self.prof_var.get(),
            self.professores
        )

        # 🔹 Disciplinas do professor
        self.disciplinas = Disciplina.getByProfessor(id_professor)
        self.update_combo(self.disc_combo, self.disc_var, self.disciplinas)

        # 🔹 Cursos relacionados às disciplinas
        ids_disc = [d[0] for d in self.disciplinas]
        self.cursos = Curso.getByDisciplinas(ids_disc)
        self.update_combo(self.curso_combo, self.curso_var, self.cursos)

    def update_combo(self, combo, var, data):
        valores = [item[1] for item in data]
        combo["values"] = valores

        if valores:
            var.set(valores[0])
        else:
            var.set("")


