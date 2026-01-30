import tkinter as tk
from ui.agenda_view import AgendaView

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Agenda de Professores")
        self.root.geometry("900x600")

        self.create_menu()
        self.create_home()

        self.root.mainloop()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)

        agenda_menu = tk.Menu(menu_bar, tearoff=0)
        agenda_menu.add_command(label="Agenda", command=self.open_agenda)
        agenda_menu.add_separator()
        agenda_menu.add_command(label="Sair", command=self.root.quit)

        menu_bar.add_cascade(label="Menu", menu=agenda_menu)
        self.root.config(menu=menu_bar)

    def create_home(self):
        label = tk.Label(
            self.root,
            text="Sistema de Agenda de Professores",
            font=("Arial", 20)
        )
        label.pack(expand=True)

    def open_agenda(self):
        AgendaView(self.root)

    def open_agenda(self):
        AgendaView(self.root)

    def open_agenda(self):
        self.root.withdraw()  # esconde a tela principal
        AgendaView(self.root)



if __name__ == "__main__":
    MainWindow()
