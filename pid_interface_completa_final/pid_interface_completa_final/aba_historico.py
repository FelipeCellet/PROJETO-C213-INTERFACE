import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class AbaHistorico(tk.Frame):
    def __init__(self, master, historico):
        super().__init__(master)
        self.historico = historico  # Lista de dicionários com {'nome', 'fig', 'dados'}
        
        self.lista_simulacoes = tk.Listbox(self, font=("Arial", 11))
        self.lista_simulacoes.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        self.lista_simulacoes.bind("<<ListboxSelect>>", self.exibir_simulacao)

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        botoes = tk.Frame(self)
        botoes.grid(row=1, column=1, sticky="e", padx=10, pady=10)

        ttk.Button(botoes, text="Exportar PNG", command=self.exportar_png).grid(row=0, column=0, padx=5)
        ttk.Button(botoes, text="Exportar PDF", command=self.exportar_pdf).grid(row=0, column=1, padx=5)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.atualizar_lista()

    def atualizar_lista(self):
        self.lista_simulacoes.delete(0, tk.END)
        for item in self.historico:
            self.lista_simulacoes.insert(tk.END, item["nome"])

    def exibir_simulacao(self, event):
        idx = self.lista_simulacoes.curselection()
        if not idx:
            return
        sim = self.historico[idx[0]]
        self.ax.clear()
        sim["fig"](self.ax)  # função que redesenha o gráfico
        self.canvas.draw()

    def exportar_png(self):
        self._exportar("png")

    def exportar_pdf(self):
        self._exportar("pdf")

    def _exportar(self, tipo):
        idx = self.lista_simulacoes.curselection()
        if not idx:
            messagebox.showwarning("Exportação", "Selecione uma simulação.")
            return
        sim = self.historico[idx[0]]
        caminho = filedialog.asksaveasfilename(defaultextension=f".{tipo}", filetypes=[(f"{tipo.upper()} Files", f"*.{tipo}")])
        if caminho:
            fig, ax = plt.subplots(figsize=(6, 4))
            sim["fig"](ax)
            fig.savefig(caminho)
            plt.close(fig)
            messagebox.showinfo("Exportado", f"Gráfico exportado como {tipo.upper()} para:\n{caminho}")
