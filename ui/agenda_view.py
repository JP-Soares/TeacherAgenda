import tkinter as tk
import calendar
from datetime import datetime
from ui.aula_form import AulaForm


class AgendaView:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Agenda do Professor")
        self.window.geometry("1000x750")
        self.window.configure(bg="#f4f6f8")

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.year = datetime.now().year
        self.month = datetime.now().month

        self.build_header()
        self.build_calendar()

    # ================= HEADER =================
    def build_header(self):
        self.header = tk.Frame(self.window, bg="#ffffff", pady=15)
        self.header.pack(fill="x")

        tk.Button(
            self.header,
            text="◀",
            command=self.prev_month,
            bg="#dddddd",
            relief="flat",
            width=3
        ).pack(side="left", padx=10)

        self.title_label = tk.Label(
            self.header,
            text=f"{calendar.month_name[self.month]} {self.year}",
            font=("Segoe UI", 18, "bold"),
            bg="#ffffff"
        )
        self.title_label.pack(side="left", padx=20)

        tk.Button(
            self.header,
            text="▶",
            command=self.next_month,
            bg="#dddddd",
            relief="flat",
            width=3
        ).pack(side="left")

    # ================= CALENDAR + SCROLL =================
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

        self.draw_calendar()
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)



    def draw_calendar(self):
        days = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        for i, day in enumerate(days):
            tk.Label(
                self.calendar_frame,
                text=day,
                font=("Segoe UI", 10, "bold"),
                bg="#f4f6f8"
            ).grid(row=0, column=i, pady=5)

        month_days = calendar.monthcalendar(self.year, self.month)

        for row, week in enumerate(month_days, start=1):
            for col, day in enumerate(week):
                self.create_day_card(row, col, day)

        for i in range(7):
            self.calendar_frame.columnconfigure(i, weight=1)

    # ================= DAY CARD =================
    def create_day_card(self, row, col, day):
        card = tk.Frame(
            self.calendar_frame,
            bg="#ffffff",
            bd=1,
            relief="solid",
            height=120
        )
        card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

        if day == 0:
            return

        tk.Label(
            card,
            text=str(day),
            font=("Segoe UI", 11, "bold"),
            bg="#ffffff"
        ).pack(anchor="nw", padx=6, pady=4)

        # 🔹 Mock de aula (substituir depois pelo banco)
        if day % 2 == 0:
            tk.Label(
                card,
                text="Matemática\nTurma A\nSala 2",
                font=("Segoe UI", 9),
                fg="#1565c0",
                bg="#ffffff",
                justify="left"
            ).pack(pady=4)

        tk.Button(
            card,
            text="Editar",
            font=("Segoe UI", 9),
            bg="#1976d2",
            fg="white",
            relief="flat",
            command=lambda d=day: self.open_aula_form(d)
        ).pack(side="bottom", pady=6)

    # ================= ACTIONS =================
    def open_aula_form(self, day):
        AulaForm(self.window, day, self.month, self.year)

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
