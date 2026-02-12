import tkinter as tk
import calendar
from datetime import datetime
from tkinter import messagebox

from ui.relatorio_agenda_form import RelatorioAgendaForm
from ui.aula_form import AulaForm
from ui.disponibilidade_form import DisponibilidadeForm

from services.aula_service import AulaService
from services.indisponibilidade_service import IndisponibilidadeService
from models.aula import Aula


class AgendaView:
    def __init__(self, parent):

        self.parent = parent

        self.window = tk.Toplevel(parent)
        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus_force()

        self.window.title("agenda do professor")
        self.window.geometry("1280x750")
        self.window.configure(bg="#f4f6f8")

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.year = datetime.now().year
        self.month = datetime.now().month

        self.build_header()
        self.build_calendar()
        tk.Button(
            self.window,
            text="Emitir Relatório 📄",
            bg="#1976D2",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.abrir_relatorio
        ).pack(pady=10)


    # ================= header =================

    def build_header(self):
        self.header = tk.Frame(self.window, bg="#ffffff", pady=15)
        self.header.pack(fill="x")

        tk.Button(
            self.header,
            text="<",
            width=3,
            command=self.prev_month
        ).pack(side="left", padx=10)

        self.title_label = tk.Label(
            self.header,
            text=f"{calendar.month_name[self.month]} {self.year}",
            font=("segoe ui", 18, "bold"),
            bg="#ffffff"
        )
        self.title_label.pack(side="left", padx=20)

        tk.Button(
            self.header,
            text=">",
            width=3,
            command=self.next_month
        ).pack(side="left")

    # ================= calendar =================

    def build_calendar(self):
        self.calendar_container = tk.Frame(self.window, bg="#f4f6f8")
        self.calendar_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(
            self.calendar_container,
            bg="#f4f6f8",
            highlightthickness=0
        )
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(
            self.calendar_container,
            orient="vertical",
            command=self.canvas.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.calendar_frame = tk.Frame(self.canvas, bg="#f4f6f8")

        self.calendar_window = self.canvas.create_window(
            (0, 0),
            window=self.calendar_frame,
            anchor="nw"
        )

        self.calendar_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(
                self.calendar_window,
                width=e.width
            )
        )

        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        self.draw_calendar()

    def draw_calendar(self):
        dias = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]

        for i, dia in enumerate(dias):
            tk.Label(
                self.calendar_frame,
                text=dia,
                font=("segoe ui", 10, "bold"),
                bg="#f4f6f8"
            ).grid(row=0, column=i, pady=5)

        month_days = calendar.monthcalendar(self.year, self.month)

        for row, week in enumerate(month_days, start=1):
            for col, day in enumerate(week):
                self.create_day_card(row, col, day)

        for i in range(7):
            self.calendar_frame.columnconfigure(i, weight=1, uniform="cal")

        for i in range(len(month_days) + 1):
            self.calendar_frame.rowconfigure(i, weight=1, uniform="row")

    # ================= day card =================

    def create_day_card(self, row, col, day):
        card = tk.Frame(
            self.calendar_frame,
            bg="#ffffff",
            bd=1,
            relief="solid",
            width=180,
            height=180
        )
        card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")
        card.grid_propagate(False)

        if day == 0:
            return

        data = f"{self.year}-{self.month:02d}-{day:02d}"

        tk.Label(
            card,
            text=str(day),
            font=("segoe ui", 11, "bold"),
            bg="#ffffff"
        ).pack(anchor="nw", padx=6, pady=2)

        aulas = Aula.getByData(data)
        indisps = IndisponibilidadeService.getByData(data)

        self.render_aulas(card, aulas)
        self.render_indisponibilidades(card, indisps)

        tk.Button(
            card,
            text="adicionar",
            font=("segoe ui", 9),
            command=lambda d=data: self.open_add_popup(d)
        ).pack(side="bottom", pady=4)

    # ================= render =================

    def render_aulas(self, card, aulas):
        if not aulas:
            return

        tk.Label(
            card,
            text="aulas",
            font=("segoe ui", 9, "bold"),
            fg="#1976d2",
            bg="#ffffff"
        ).pack(anchor="w", padx=6)

        for id_aula, disciplina, turma, turno, professor in aulas:
            linha = tk.Frame(card, bg="#ffffff")
            linha.pack(fill="x", padx=6, pady=1)

            tk.Label(
                linha,
                text=f"{turno} • {disciplina} • {turma} • {professor}",
                font=("segoe ui", 8),
                wraplength=120,
                justify="left",
                bg="#ffffff"
            ).pack(side="left", fill="x", expand=True)

            tk.Button(
                linha,
                text="x",
                width=2,
                command=lambda i=id_aula: self.confirmar_delete_aula(i)
            ).pack(side="right")

    def render_indisponibilidades(self, card, indisps):
        if not indisps:
            return

        tk.Label(
            card,
            text="indisponível",
            font=("segoe ui", 9, "bold"),
            fg="#d32f2f",
            bg="#ffffff"
        ).pack(anchor="w", padx=6, pady=(4, 0))

        for id_disp, professor, turno, motivo in indisps:
            linha = tk.Frame(card, bg="#ffffff")
            linha.pack(fill="x", padx=6, pady=1)

            texto = f"{turno} • {professor}"
            if motivo:
                texto += f" ({motivo})"

            tk.Label(
                linha,
                text=texto,
                font=("segoe ui", 8),
                fg="#d32f2f",
                wraplength=120,
                justify="left",
                bg="#ffffff"
            ).pack(side="left", fill="x", expand=True)

            tk.Button(
                linha,
                text="x",
                width=2,
                command=lambda i=id_disp: self.confirmar_delete_indisponibilidade(i)
            ).pack(side="right")

    # ================= actions =================

    def open_add_popup(self, data):
        popup = tk.Toplevel(self.window)
        popup.title("adicionar")
        popup.geometry("300x180")
        popup.resizable(False, False)
        popup.transient(self.window)
        popup.grab_set()

        tk.Label(
            popup,
            text=f"o que deseja adicionar no dia {data}?",
            font=("segoe ui", 11, "bold")
        ).pack(pady=15)

        tk.Button(
            popup,
            text="aula",
            font=("segoe ui", 10),
            width=22,
            command=lambda d=data: self.open_aula_form(popup, d)
        ).pack(pady=5)

        tk.Button(
            popup,
            text="indisponibilidade do professor",
            font=("segoe ui", 10),
            width=22,
            command=lambda d=data: self.open_indisponibilidade_form(popup, d)
        ).pack(pady=5)

    def open_aula_form(self, popup, data):
        popup.destroy()

        form = AulaForm(
            self.window,
            data
        )
        self.window.wait_window(form.window)
        self.refresh()

    def open_indisponibilidade_form(self, popup, data):
        popup.destroy()
        form = DisponibilidadeForm(self.window, data)
        self.window.wait_window(form.window)
        self.refresh()

    def confirmar_delete_aula(self, id_aula):
        if messagebox.askyesno("confirmação", "deseja excluir esta aula?"):
            sucesso, msg = AulaService.excluir_aula(id_aula)
            if sucesso:
                self.refresh()
            else:
                messagebox.showerror("erro", msg)

    def confirmar_delete_indisponibilidade(self, id_disp):
        if messagebox.askyesno("confirmação", "deseja excluir esta indisponibilidade?"):
            sucesso, msg = IndisponibilidadeService.excluir(id_disp)
            if sucesso:
                self.refresh()
            else:
                messagebox.showerror("erro", msg)

    # ================= navigation =================

    def prev_month(self):
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -= 1
        self.refresh()

    def next_month(self):
        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1
        self.refresh()

    def refresh(self):
        self.header.destroy()
        self.calendar_container.destroy()
        self.build_header()
        self.build_calendar()

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_close(self):
        self.parent.deiconify()
        self.window.destroy()

    def abrir_relatorio(self):
        RelatorioAgendaForm(self.window)

