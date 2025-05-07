import tkinter as tk
from PIL import Image, ImageTk

class AbaHome(tk.Frame):
    def __init__(self, master, abas):
        super().__init__(master)

        tk.Label(self, text="Bem-vindo ao Projeto de C213 - Sistemas Embarcados", font=("Arial", 16)).pack(pady=20)

        try:
            img = Image.open("Logo-Inatel.png").resize((200, 80))
            self.logo = ImageTk.PhotoImage(img)
            tk.Label(self, image=self.logo).pack(pady=10)
        except:
            tk.Label(self, text="[Logo não carregada]").pack(pady=10)

        tk.Label(self, text="Use os botões abaixo ou as abas superiores para navegar pelo projeto.").pack(pady=10)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(pady=20)

        # Botões empilhados verticalmente
        botoes = [
            ("Identificação", 1),
            ("Controle PID", 2),
            ("EQM - Modelos", 3),
            ("Gráficos Smith", 4),
            ("Histórico de Simulações", 5),
        ]

        for texto, idx in botoes:
            tk.Button(frame_botoes, text=texto, width=25, command=lambda i=idx: abas.select(i)).pack(pady=4)
