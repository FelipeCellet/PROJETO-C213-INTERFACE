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
    data = loadmat("Dataset_Grupo7.mat")
    key = whosmat("Dataset_Grupo7.mat")[0][0]
    estrutura = data[key][0, 0]

    tempo = estrutura["sampleTime"][0]
    entrada = estrutura["dataInput"][0]
    saida = estrutura["dataOutput"][0]

    # Eixo Y (Temperatura)
    label_y = estrutura["physicalQuantity"][0, 1][0]
    unidade_y = estrutura["units"][0, 1][0]

    # Eixo X (Tempo)
    label_x = estrutura["physicalQuantity"][0, 0][0]
    unidade_x = estrutura["units"][0, 0][0]

    return tempo.astype(float), entrada, saida, label_y, unidade_y, label_x, unidade_x

class AppPID(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interface PID Completa")
        self.geometry("1024x700")

        # Agora recebendo todos os labels e unidades
        tempo, entrada, saida, label_y, unidade_y, label_x, unidade_x = carregar_dados()

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
        abas.add(AbaIdentificacao(abas, tempo, entrada, saida, label_y, unidade_y, label_x, unidade_x), text="Identificação")
        abas.add(AbaPID(abas, self.k, self.tau, self.theta, tempo, entrada, saida, self.historico_simulacoes, label_y, unidade_y, label_x, unidade_x), text="Controle PID")
        abas.add(AbaEQM(abas, tempo, entrada, saida, self.k, label_y, unidade_y), text="EQM - Modelos")
        abas.add(AbaSmith(abas, self.k, self.tau, self.theta, tempo, entrada, saida, label_y, unidade_y, label_x, unidade_x, self.historico_simulacoes), text="Gráficos Smith")

        abas.add(AbaHistorico(abas, self.historico_simulacoes), text="Histórico de Simulações")

if __name__ == "__main__":
    AppPID().mainloop()
