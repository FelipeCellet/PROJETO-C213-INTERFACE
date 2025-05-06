import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class AbaIdentificacao(tk.Frame):
    def _on_hover(self, event):
        vis = self.annotation.get_visible()
        if event.inaxes == self.ax:
            x, y = event.xdata, event.ydata
            self.annotation.xy = (x, y)
            text = f"x={x:.2f}\ny={y:.2f}"
            self.annotation.set_text(text)
            self.annotation.set_visible(True)
            self.canvas.draw_idle()
        elif vis:
            self.annotation.set_visible(False)
            self.canvas.draw_idle()
    

    def __init__(self, master, tempo, entrada, saida):
        super().__init__(master)

        # Frame interno para centralizar
        frame_central = tk.Frame(self)
        frame_central.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Criação do gráfico
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.ax.plot(tempo, entrada, label="Entrada", linestyle="--", color="blue")
        self.ax.plot(tempo, saida, label="Saída", color="red")
        self.ax.set_title("Identificação do Sistema")
        self.ax.set_xlabel("Tempo (s)")
        self.ax.set_ylabel("Temperatura (°C)")
        self.ax.legend()
        self.ax.grid(True)

        # Canvas do gráfico
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_central)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky="nsew")
        self.canvas.draw()

        # Mensagem explicativa centralizada e maior
        self.label = tk.Label(
            frame_central,
            text="Comportamento típico de sistema de primeira ordem com atraso.",
            font=("Arial", 14),
            wraplength=800,
            justify="center"
        )
        self.label.grid(row=1, column=0, pady=(15, 0))

        # Configurar expansão
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        frame_central.grid_rowconfigure(0, weight=1)
        frame_central.grid_columnconfigure(0, weight=1)

                # Anotação flutuante
        self.annotation = self.ax.annotate(
            "", xy=(0, 0), xytext=(15, 15), textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->")
        )
        self.annotation.set_visible(False)

        # Conectar evento de movimento do mouse
        self.canvas.mpl_connect("motion_notify_event", self._on_hover)

