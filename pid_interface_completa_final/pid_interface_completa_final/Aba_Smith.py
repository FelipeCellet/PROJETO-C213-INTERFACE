import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import control as ctrl

class AbaSmith(tk.Frame):
    def __init__(self, master, k, tau, theta, tempo, entrada, saida, label, unidade):
        super().__init__(master)
        self.k = k
        self.tau = tau
        self.theta = theta
        self.tempo = tempo
        self.entrada = entrada
        self.saida = saida
        self.label = label
        self.unidade = unidade

        self.malha_var = tk.StringVar(value="Malha Fechada")
        self.pade_var = tk.StringVar(value="1")

        painel = tk.Frame(self)
        painel.grid(row=0, column=0, sticky="ns", padx=20, pady=20)

        ttk.Label(painel, text="Tipo de Malha:", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
        ttk.Combobox(painel, textvariable=self.malha_var,
                     values=["Malha Aberta", "Malha Fechada"], state="readonly", width=20).grid(row=1, column=0, pady=(0, 15))

        ttk.Label(painel, text="Ordem de Padé:", font=("Arial", 12)).grid(row=2, column=0, sticky="w")
        ttk.Combobox(painel, textvariable=self.pade_var,
                     values=["1", "2", "3", "4", "5", "20"], state="readonly", width=20).grid(row=3, column=0, pady=(0, 15))

        ttk.Button(painel, text="Plotar Gráfico", command=self.plotar).grid(row=4, column=0, pady=10)

        self.fig, self.ax = plt.subplots(figsize=(7, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def plotar(self):
        self.ax.clear()
        try:
            ordem = int(self.pade_var.get())
            tipo_malha = self.malha_var.get()

            valor_final = self.saida[-1]
            y1 = self.saida[0] + 0.283 * (valor_final - self.saida[0])
            y2 = self.saida[0] + 0.632 * (valor_final - self.saida[0])
            t1 = self.tempo[np.where(self.saida >= y1)[0][0]]
            t2 = self.tempo[np.where(self.saida >= y2)[0][0]]
            tau = 1.5 * (t2 - t1)
            theta = t2 - tau
            k = (valor_final - self.saida[0]) / self.entrada.mean()
            amplitude_degrau = self.entrada.mean()

            # Modelo base
            G_s = ctrl.tf([k], [tau, 1])
            num_pade, den_pade = ctrl.pade(theta, ordem)
            Pade_approx = ctrl.tf(num_pade, den_pade)

            G_atrasada = ctrl.series(Pade_approx, G_s)

            if tipo_malha == "Malha Fechada":
                resposta_modelo = ctrl.feedback(G_atrasada, 1)
            else:  # Malha Aberta
                resposta_modelo = G_atrasada

            # Simulação com entrada escalada
            t_sim, y_modelo = ctrl.step_response(resposta_modelo * amplitude_degrau, T=self.tempo)

            # EQM
            EQM = np.sqrt(np.mean((self.saida - y_modelo) ** 2))

            # Plotagem
            self.ax.plot(self.tempo, self.saida, 'black', label="Resposta Real")
            self.ax.plot(self.tempo, self.entrada, color="blue", label="Entrada (Degrau)")
            self.ax.plot(t_sim, y_modelo, 'red', label=f"Modelo Identificado ({tipo_malha})")

            self.ax.set_title(f"Identificação via Método de Smith (Grupo 7 - {tipo_malha})")
            self.ax.set_xlabel("Tempo (s)")
            self.ax.set_ylabel(f"{self.label} ({self.unidade})")  # Dinâmico aqui
            self.ax.grid(True)
            self.ax.legend(loc="lower right")

            # Caixa de texto com parâmetros
            props = dict(boxstyle='round', facecolor='white', alpha=0.8)
            textstr = '\n'.join((
                f'Ganho (k): {k:.4f}',
                f'Atraso (θ): {theta:.2f} s',
                f'Tempo (T): {tau:.2f} s',
                f'EQM: {EQM:.2f}'
            ))
            self.ax.text(self.tempo[-1] * 0.65, max(self.saida) * 0.7, textstr, fontsize=10, bbox=props)

            self.canvas.draw()

        except Exception as e:
            self.ax.clear()
            self.ax.set_title("Erro ao simular sistema")
            self.ax.text(0.5, 0.5, str(e), ha="center", va="center", wrap=True)
            self.canvas.draw()
