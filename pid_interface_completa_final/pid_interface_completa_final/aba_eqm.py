import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import control as ctrl
import matplotlib.pyplot as plt

class AbaEQM(tk.Frame):
    def __init__(self, master, tempo, entrada, saida, k, label, unidade):
        super().__init__(master)
        self.tempo = tempo
        self.entrada = entrada
        self.saida = saida
        self.k = k
        self.label = label
        self.unidade = unidade
        self.amplitude = np.mean(entrada)
        self.metodo_var = tk.StringVar(value="Smith")

        frame = tk.Frame(self)
        frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(frame, text="Método").pack()
        ttk.Combobox(frame, textvariable=self.metodo_var, values=["Smith", "Sundaresan"], state="readonly").pack()

        ttk.Button(frame, text="Calcular EQM", command=self.plotar_eqm).pack(pady=10)

        self.label_k = ttk.Label(frame, text="k =")
        self.label_k.pack()
        self.label_tau = ttk.Label(frame, text="τ =")
        self.label_tau.pack()
        self.label_theta = ttk.Label(frame, text="θ =")
        self.label_theta.pack()
        self.eqm_label = ttk.Label(frame, text="EQM =")
        self.eqm_label.pack()

        self.fig, self.ax_eqm = plt.subplots(figsize=(6, 4))
        self.canvas_eqm = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_eqm.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def plotar_eqm(self):
        t = self.tempo
        y_real = self.saida
        y0 = y_real[0]
        y_final = y_real[-1]

        if self.metodo_var.get() == "Smith":
            #pontos da curva
            y1 = y0 + 0.283 * (y_final - y0)
            y2 = y0 + 0.632 * (y_final - y0)
            #instantes de tempo que se atinge os pontos
            t1 = t[np.argmax(y_real >= y1)]
            t2 = t[np.argmax(y_real >= y2)]
            tau = 1.5 * (t2 - t1)
            theta = t2 - tau
        else:
            y1 = y0 + 0.353 * (y_final - y0)
            y2 = y0 + 0.853 * (y_final - y0)
            t1 = t[np.argmax(y_real >= y1)]
            t2 = t[np.argmax(y_real >= y2)]
            tau = 0.67 * (t2 - t1)
            theta = 1.3 * t1 - 0.29 * t2

        #Função de tranferencia
        G = ctrl.tf([self.k], [tau, 1])
        #Atraso
        num_pade, den_pade = ctrl.pade(theta, 1)
        atraso = ctrl.tf(num_pade, den_pade)
        #Modelo completo com atraso
        modelo = ctrl.series(G, atraso)
        #simulando resposta ao degrau
        t_sim, y_sim = ctrl.step_response(modelo * self.amplitude, T=t)
        #EQM - comparando a saida real com a simulada
        eqm = np.sqrt(np.mean((y_real - y_sim) ** 2))

        self.ax_eqm.clear()
        self.ax_eqm.plot(t, y_real, 'r', label='Saída Real')
        self.ax_eqm.plot(t_sim, y_sim, 'b--', label='Modelo')
        self.ax_eqm.set_title(f'Modelo {self.metodo_var.get()} - EQM: {eqm:.4f}')
        self.ax_eqm.set_xlabel("Tempo (s)")
        self.ax_eqm.set_ylabel(f"{self.label} ({self.unidade})")  # <-- Dinâmico
        self.ax_eqm.grid(True)
        self.ax_eqm.legend()
        self.canvas_eqm.draw()

        self.label_k.config(text=f"k = {self.k:.4f}")
        self.label_tau.config(text=f"τ = {tau:.2f}")
        self.label_theta.config(text=f"θ = {theta:.2f}")
        self.eqm_label.config(text=f"EQM = {eqm:.4f}")
