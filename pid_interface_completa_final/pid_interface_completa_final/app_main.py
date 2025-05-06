import tkinter as tk
from tkinter import ttk
from scipy.io import loadmat, whosmat
from aba_identificacao import AbaIdentificacao
from aba_pid import AbaPID
from aba_eqm import AbaEQM
from aba_home import AbaHome
from Aba_Smith import AbaSmith
import numpy as np


def carregar_dados():
    data = loadmat("Dataset_Grupo7.mat")
    data = data.get(whosmat("Dataset_Grupo7.mat")[0][0])[0][0]
    tempo, entrada, saida, _, _ = data
    return tempo[0].astype(float), entrada[0], saida[0]


class AppPID(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interface PID Completa")
        self.geometry("1024x700")

        # Carregamento e identificação
        tempo, entrada, saida = carregar_dados()
        self.amplitude = entrada.mean()
        self.k = (saida[-1] - saida[0]) / self.amplitude
        y1 = saida[0] + 0.283 * (saida[-1] - saida[0])
        y2 = saida[0] + 0.632 * (saida[-1] - saida[0])
        t1 = tempo[np.argmax(saida >= y1)]
        t2 = tempo[np.argmax(saida >= y2)]
        self.tau = 1.5 * (t2 - t1)
        self.theta = t2 - self.tau

        # Criação das abas
        abas = ttk.Notebook(self)
        abas.pack(fill="both", expand=True)

        abas.add(AbaHome(abas, abas), text="Início")  # Aba 0
        abas.add(AbaIdentificacao(abas, tempo, entrada, saida), text="Identificação")  # Aba 1
        abas.add(AbaPID(abas, self.k, self.tau, self.theta, tempo, entrada, saida), text="Controle PID")  # Aba 2
        abas.add(AbaEQM(abas, tempo, entrada, saida, self.k), text="EQM - Modelos")  # Aba 3
        abas.add(AbaSmith(abas, self.k, self.tau, self.theta, tempo, entrada, saida), text="Gráficos Smith")

if __name__ == "__main__":
    AppPID().mainloop()
