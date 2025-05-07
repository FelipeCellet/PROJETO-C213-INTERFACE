from matplotlib.backends.backend_pdf import PdfPages
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class AbaHistorico(tk.Frame):
    def __init__(self, master, historico):
        super().__init__(master)
        self.historico = historico  

        # Frame com checkboxes
        self.frame_checkboxes = tk.Frame(self)
        self.frame_checkboxes.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        self.check_vars = []

        # Área do gráfico
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Botões
        botoes = tk.Frame(self)
        botoes.grid(row=1, column=1, sticky="e", padx=10, pady=10)

        ttk.Button(botoes, text="Exibir Selecionado", command=self.exibir_primeira_selecao).grid(row=0, column=0, padx=5)
        ttk.Button(botoes, text="Exportar PDF", command=self.exportar_pdf).grid(row=0, column=1, padx=5)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.bind("<Visibility>", lambda e: self.atualizar_lista())

    def atualizar_lista(self):
        for widget in self.frame_checkboxes.winfo_children():
            widget.destroy()
        self.check_vars.clear()

        for i, sim in enumerate(self.historico):
            var = tk.IntVar()
            chk = tk.Checkbutton(self.frame_checkboxes, text=sim["nome"], variable=var, font=("Arial", 10))
            chk.pack(anchor="w")
            self.check_vars.append((var, i))

    def exibir_primeira_selecao(self):
        for var, i in self.check_vars:
            if var.get():
                sim = self.historico[i]
                self.ax.clear()
                sim["fig"](self.ax)
                self.canvas.draw()
                break

    def exportar_pdf(self):
        selecionados = [i for var, i in self.check_vars if var.get()]
        if not selecionados:
            messagebox.showwarning("Exportação", "Nenhuma simulação selecionada.")
            return

        caminho = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not caminho:
            return

        with PdfPages(caminho) as pdf:
            for idx in selecionados:
                sim = self.historico[idx]
                fig, ax = plt.subplots(figsize=(6, 4))
                sim["fig"](ax)
                fig.suptitle(sim["nome"], fontsize=14)
                pdf.savefig(fig)
                plt.close(fig)

        messagebox.showinfo("Exportação Concluída", f"{len(selecionados)} simulação(ões) exportadas para:\n{caminho}")
