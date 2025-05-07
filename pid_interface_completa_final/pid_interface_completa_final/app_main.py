import tkinter as tk
from tkinter import ttk
from scipy.io import loadmat, whosmat
from aba_identificacao import AbaIdentificacao
from aba_pid import AbaPID
from aba_eqm import AbaEQM
from aba_home import AbaHome
from Aba_Smith import AbaSmith
from aba_historico import AbaHistorico
import numpy as np

def carregar_dados():
    from scipy.io import loadmat, whosmat
    data = loadmat("Dataset_Grupo7.mat")
    data = data.get(whosmat("Dataset_Grupo7.mat")[0][0])[0][0]
    tempo, entrada, saida, label, unidade = data

    # Corrigir o tipo para strings simples (sem colchetes ou array)
    label = str(label[0][0]) if isinstance(label, np.ndarray) else str(label)
    unidade = str(unidade[0][0]) if isinstance(unidade, np.ndarray) else str(unidade)

    return tempo[0].astype(float), entrada[0], saida[0], label, unidade

class AppPID(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interface PID Completa")
        self.geometry("1024x700")

        tempo, entrada, saida, label, unidade = carregar_dados()
        self.amplitude = entrada.mean()
        self.k = (saida[-1] - saida[0]) / self.amplitude
        y1 = saida[0] + 0.283 * (saida[-1] - saida[0])
        y2 = saida[0] + 0.632 * (saida[-1] - saida[0])
        t1 = tempo[np.argmax(saida >= y1)]
        t2 = tempo[np.argmax(saida >= y2)]
        self.tau = 1.5 * (t2 - t1)
        self.theta = t2 - self.tau

        self.historico_simulacoes = []

        abas = ttk.Notebook(self)
        abas.pack(fill="both", expand=True)

        abas.add(AbaHome(abas, abas), text="Início")
        abas.add(AbaIdentificacao(abas, tempo, entrada, saida, label, unidade), text="Identificação")
        abas.add(AbaPID(abas, self.k, self.tau, self.theta, tempo, entrada, saida, self.historico_simulacoes, label, unidade), text="Controle PID")
        abas.add(AbaEQM(abas, tempo, entrada, saida, self.k, label, unidade), text="EQM - Modelos")
        abas.add(AbaSmith(abas, self.k, self.tau, self.theta, tempo, entrada, saida, label, unidade), text="Gráficos Smith")
        abas.add(AbaHistorico(abas, self.historico_simulacoes), text="Histórico de Simulações")

if __name__ == "__main__":
    AppPID().mainloop()
