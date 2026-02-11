import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from services.turma_service import TurmaService
from models.curso import Curso

class TurmaForm:
    import tkinter as tk
from tkinter import ttk, messagebox

from services.turma_service import TurmaService
from models.turma import Turma
from models.curso import Curso


class TurmaForm:
    def __init__(self, parent, id_turma=None):
        self.id_turma = id_turma

        self.window = tk.Toplevel(parent)
        self.window.title("Professor")

        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus_force()
        
        self.window.title("turma")
        self.window.geometry("400x380")

        # campos
        tk.Label(self.window, text="nome").pack()
        self.nome = tk.Entry(self.window)
        self.nome.pack(fill="x", padx=20)

        tk.Label(self.window, text="empresa").pack()
        self.empresa = tk.Entry(self.window)
        self.empresa.pack(fill="x", padx=20)

        tk.Label(self.window, text="localidade").pack()
        self.localidade = tk.Entry(self.window)
        self.localidade.pack(fill="x", padx=20)

        tk.Label(self.window, text="curso").pack(pady=(10, 0))
        self.cursos = Curso.getAll()

        self.combo_curso = ttk.Combobox(
            self.window,
            values=[c[1] for c in self.cursos],
            state="readonly"
        )
        self.combo_curso.pack(fill="x", padx=20)

        tk.Button(
            self.window,
            text="salvar",
            command=self.save
        ).pack(pady=20)

        if self.id_turma:
            self.carregar_dados()


    def save(self):
        nome = self.nome.get().strip()
        empresa = self.empresa.get().strip()
        localidade = self.localidade.get().strip()
        idx = self.combo_curso.current()

        if not nome or not empresa or not localidade:
            messagebox.showerror(
                "erro",
                "preencha todos os campos"
            )
            return

        if idx < 0:
            messagebox.showerror(
                "erro",
                "selecione um curso"
            )
            return

        id_curso = self.cursos[idx][0]

        if self.id_turma:
            sucesso, msg = TurmaService.update(
                self.id_turma,
                nome,
                empresa,
                localidade,
                id_curso
            )
        else:
            TurmaService.add(
                nome,
                empresa,
                localidade,
                id_curso
            )
            sucesso = True

        if sucesso:
            self.window.destroy()
        else:
            messagebox.showerror("erro", msg)


    def carregar_dados(self):
        turma = Turma.getById(self.id_turma)

        if not turma:
            return

        _, nome, empresa, localidade, id_curso = turma

        self.nome.insert(0, nome)
        self.empresa.insert(0, empresa)
        self.localidade.insert(0, localidade)

        for i, curso in enumerate(self.cursos):
            if curso[0] == id_curso:
                self.combo_curso.current(i)
                break

