import tkinter as tk
import calendar
from datetime import datetime

class AgendaView:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Agenda de Professores")
        self.window.geometry("900x600")

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.year = datetime.now().year
        self.month = datetime.now().month

        self.header = tk.Frame(self.window)
        self.header.pack(pady=10)

        self.calendar_frame = tk.Frame(self.window)
        self.calendar_frame.pack(expand=True, fill="both")

        self.build_header()
        self.build_calendar()

    def build_header(self):
        for widget in self.header.winfo_children():
            widget.destroy()

        tk.Button(self.header, text="◀", width=3, command=self.prev_month).pack(side="left")

        tk.Label(
            self.header,
            text=f"{calendar.month_name[self.month]} {self.year}",
            font=("Arial", 18)
        ).pack(side="left", padx=20)

        tk.Button(self.header, text="▶", width=3, command=self.next_month).pack(side="left")

    def build_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        days_of_week = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

        for col, day in enumerate(days_of_week):
            tk.Label(self.calendar_frame, text=day, font=("Arial", 10, "bold")) \
                .grid(row=0, column=col, sticky="nsew")

        month_days = calendar.monthcalendar(self.year, self.month)

        for row, week in enumerate(month_days, start=1):
            for col, day in enumerate(week):
                cell = tk.Frame(
                    self.calendar_frame,
                    borderwidth=1,
                    relief="solid",
                    height=90,
                    width=120
                )
                cell.grid(row=row, column=col, sticky="nsew")

                if day != 0:
                    tk.Label(cell, text=str(day), anchor="nw").pack(fill="x")

                    # 🔹 Exemplo visual (mock)
                    if day == 10:
                        tk.Label(
                            cell,
                            text="Matemática\nTurma A\nSala 2",
                            font=("Arial", 8),
                            fg="blue"
                        ).pack()

        for i in range(7):
            self.calendar_frame.columnconfigure(i, weight=1)

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
        self.build_header()
        self.build_calendar()

    def on_close(self):
        self.parent.deiconify()  # mostra a tela principal de novo
        self.window.destroy()
