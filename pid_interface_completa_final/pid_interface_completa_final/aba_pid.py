import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from tkinter import simpledialog

from utils_pid import simular_pid

class AbaPID(tk.Frame):
    def __init__(self, master, k, tau, theta, tempo, entrada, saida, historico, label_y, unidade_y, label_x, unidade_x):
        super().__init__(master)
        self.historico = historico
        self.label_y = label_y
        self.unidade_y = unidade_y
        self.label_x = label_x
        self.unidade_x = unidade_x

        self.configure(bg="white")

        self.k = float(k)
        self.tau = float(tau)
        self.theta = float(theta)
        self.tempo = tempo
        self.entrada = entrada
        self.saida = saida


        self.metodo_var = tk.StringVar(value="Cohen-Coon")
        self.pade_var = tk.StringVar(value="1")
        self.setpoint_var = tk.DoubleVar(value=100.0)

        style = ttk.Style()
        style.theme_use("default")
        style.map("TCombobox",
                  fieldbackground=[("readonly", "white")],
                  background=[("readonly", "white")],
                  selectbackground=[("readonly", "white")],
                  selectforeground=[("readonly", "black")],
                  foreground=[("readonly", "black")])

        frame_controle = tk.Frame(self, bg="white")
        frame_controle.grid(row=0, column=0, sticky="ns", padx=25, pady=25)
        frame_controle.grid_columnconfigure(0, weight=1)

        ttk.Label(frame_controle, text="Método de Sintonia", font=("Arial", 12), background="white").grid(row=0, column=0, sticky="w")
        self.metodo_cb = ttk.Combobox(frame_controle, textvariable=self.metodo_var,
                                      values=["Cohen-Coon", "Ziegler-Nichols", "Manual"],
                                      state="readonly", font=("Arial", 11))
        self.metodo_cb.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        self.metodo_cb.bind("<<ComboboxSelected>>", self.bloquear_campos)

        ttk.Label(frame_controle, text="Ordem de Padé", font=("Arial", 12), background="white").grid(row=2, column=0, sticky="w")
        self.pade_cb = ttk.Combobox(frame_controle, textvariable=self.pade_var,
                                    values=["1", "2", "3", "4", "5","20"], state="readonly", font=("Arial", 11))
        self.pade_cb.grid(row=3, column=0, sticky="ew", pady=(0, 15))

        ttk.Label(frame_controle, text="Setpoint", font=("Arial", 12), background="white").grid(row=4, column=0, sticky="w")
        self.setpoint_entry = tk.Entry(frame_controle, textvariable=self.setpoint_var, font=("Arial", 12), width=10)
        self.setpoint_entry.grid(row=5, column=0, sticky="ew", pady=(0, 15))

        frame_pid = tk.LabelFrame(frame_controle, text="Parâmetros PID", font=("Arial", 11), bg="white", fg="black")
        frame_pid.grid(row=6, column=0, sticky="ew", pady=(0, 15))
        frame_pid.configure(highlightbackground="gray", highlightthickness=1)
        self.kp_entry = self._criar_entrada(frame_pid, "Kp", 0)
        self.ti_entry = self._criar_entrada(frame_pid, "Ti", 1)
        self.td_entry = self._criar_entrada(frame_pid, "Td", 2)

        frame_param = tk.LabelFrame(frame_controle, text="Parâmetros do Sistema", font=("Arial", 11), bg="white", fg="black")
        frame_param.grid(row=7, column=0, sticky="ew", pady=(0, 15))
        frame_param.configure(highlightbackground="gray", highlightthickness=1)
        tk.Label(frame_param, text=f"k = {self.k:.4f}", font=("Arial", 12), bg="white").grid(row=0, column=0, sticky="w")
        tk.Label(frame_param, text=f"τ = {self.tau:.2f}", font=("Arial", 12), bg="white").grid(row=1, column=0, sticky="w")
        tk.Label(frame_param, text=f"θ = {self.theta:.2f}", font=("Arial", 12), bg="white").grid(row=2, column=0, sticky="w")

        ttk.Button(frame_controle, text="Aplicar Método", command=self.aplicar_metodo).grid(row=8, column=0, sticky="ew", pady=(5, 10))
        ttk.Button(frame_controle, text="Simular", command=self.simular).grid(row=9, column=0, sticky="ew")

        # Botões de exportação
        ttk.Button(frame_controle, text="Exportar PNG", command=self.exportar_png).grid(row=10, column=0, sticky="ew", pady=(5, 5))
        ttk.Button(frame_controle, text="Exportar PDF", command=self.exportar_pdf).grid(row=11, column=0, sticky="ew")

        ttk.Button(frame_controle, text="Salvar Simulação", command=self.salvar_simulacao).grid(row=12, column=0, sticky="ew", pady=(5, 5))


        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.bloquear_campos()

    def _criar_entrada(self, parent, label, row):
        tk.Label(parent, text=label, font=("Arial", 12), bg="white").grid(row=row, column=0, padx=5, sticky="e")
        entry = tk.Entry(parent, width=10, font=("Arial", 12))
        entry.grid(row=row, column=1, padx=5, pady=3)
        return entry

    def bloquear_campos(self, *args):
        metodo = self.metodo_var.get()

        if metodo == "Manual":
            senha = simpledialog.askstring("Autenticação", "Digite a senha de 6 dígitos para liberar o modo Manual:")
            if senha != "123456":
                messagebox.showwarning("Acesso Negado", "Senha incorreta. Voltando para 'Cohen-Coon'.")
                self.metodo_var.set("Cohen-Coon")
                metodo = "Cohen-Coon"

        estado = "normal" if metodo == "Manual" else "disabled"
        for entry in [self.kp_entry, self.ti_entry, self.td_entry]:
            entry.config(state=estado)

    def aplicar_metodo(self):
        metodo = self.metodo_var.get()
        try:
            if metodo == "Cohen-Coon":
                # Kp conforme tabela
                kp_num = (16 * self.tau + 3 * self.theta)
                kp_den = 12 * self.tau
                Kp = (self.tau / (self.k * self.theta)) * (kp_num / kp_den)

                # Ti reescrita na forma exata solicitada
                Ti = self.theta * ((32 + (6 * self.theta) / self.tau) / (13 + (8 * self.theta) / self.tau))

                # Td permanece igual
                Td = (4 * self.theta) / (11 + (2 * self.theta) / self.tau)

            elif metodo == "Ziegler-Nichols":
                Kp = (1.2 * self.tau) / (self.k * self.theta)
                Ti = 2 * self.theta
                Td = self.theta / 2
            else:
                return

            # Preenche os campos da interface
            for val, entry in zip([Kp, Ti, Td], [self.kp_entry, self.ti_entry, self.td_entry]):
                entry.config(state="normal")  # libera temporariamente para inserir
                entry.delete(0, tk.END)
                entry.insert(0, f"{val:.4f}")

            self.bloquear_campos()  # bloqueia novamente se necessário

        except ZeroDivisionError:
            messagebox.showerror("Erro", "θ (theta), τ (tau) e k não podem ser zero.")

    def simular(self):
        try:
            Kp = float(self.kp_entry.get())
            Ti = float(self.ti_entry.get())
            Td = float(self.td_entry.get())
            ordem = int(self.pade_var.get())
            setpoint = float(self.setpoint_var.get())
        except ValueError:
            return

        t, y, info = simular_pid(Kp, Ti, Td, self.k, self.tau, self.theta, self.tempo, ordem, setpoint=setpoint)

        self.ax.clear()
        self.ax.plot(t, y, label="Resposta PID", color="black")
        self.ax.axhline(setpoint, color="red", linestyle="--", label="Setpoint")

        tp = info.get("PeakTime", 0)
        mp = info.get("Overshoot", 0)
        ts = info.get("SettlingTime", 0)
        tr = info.get("RiseTime", 0)
        ymax = max(y)

        x_offset = max(t) * 0.7
        y_offset = min(y) + (max(y) - min(y)) * 0.3

        self.ax.annotate(f"Pico: {ymax:.2f}\nOvershoot: {mp:.1f}%",
                         xy=(tp, ymax),
                         xytext=(x_offset, y_offset),
                         fontsize=11,
                         bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="purple", lw=1.5))

        self.ax.axvline(tr, color="blue", linestyle="--", label=f"T subida: {tr:.2f}s")
        self.ax.axvline(ts, color="green", linestyle="--", label=f"T acomodação: {ts:.2f}s")

        self.ax.set_title("Resposta do Sistema com PID")
        self.ax.set_xlabel(f"{self.label_x} ({self.unidade_x})")
        self.ax.set_ylabel(f"{self.label_y} ({self.unidade_y})")

        self.ax.grid()
        self.ax.legend()
        self.canvas.draw()
        self.ultima_simulacao = {
            "tempo": t,
            "saida": y,
            "Kp": Kp,
            "Ti": Ti,
            "Td": Td,
            "setpoint": setpoint,
            "info": info
        }


    def exportar_png(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if caminho:
            self.fig.savefig(caminho)
            messagebox.showinfo("Exportação", f"Gráfico exportado como PNG em:\n{caminho}")

    def exportar_pdf(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if caminho:
            self.fig.savefig(caminho)
            messagebox.showinfo("Exportação", f"Gráfico exportado como PDF em:\n{caminho}")

    def salvar_simulacao(self):
        if hasattr(self, 'ultima_simulacao'):
            nome = simpledialog.askstring("Salvar Simulação", "Digite um nome para esta simulação:")
            if not nome:
                return

            sim = self.ultima_simulacao  # para facilitar

            def plotar(ax):
                ax.clear()  # <- garante que o gráfico anterior não atrapalhe
                ax.plot(sim["tempo"], sim["saida"], label="Resposta PID", color="black")
                ax.axhline(sim["setpoint"], color="red", linestyle="--", label="Setpoint")

                info = sim["info"]
                tp = info.get("PeakTime", 0)
                mp = info.get("Overshoot", 0)
                ts = info.get("SettlingTime", 0)
                tr = info.get("RiseTime", 0)
                ymax = max(sim["saida"])

                ax.annotate(f"Pico: {ymax:.2f}\nOvershoot: {mp:.1f}%",
                            xy=(tp, ymax),
                            xytext=(tp + 10, ymax - 10),
                            fontsize=10,
                            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="purple", lw=1.5))

                ax.axvline(tr, color="blue", linestyle="--", label=f"T subida: {tr:.2f}s")
                ax.axvline(ts, color="green", linestyle="--", label=f"T acomod.: {ts:.2f}s")

                ax.set_title(f"Simulação: {nome}")
                ax.set_xlabel(f"{self.label_x} ({self.unidade_x})")
                ax.set_ylabel(f"{self.label_y} ({self.unidade_y})")
                ax.grid(True)
                ax.legend()

            self.historico.append({
                "nome": nome,
                "fig": plotar,
                "dados": sim
            })

            messagebox.showinfo("Salvo", f"Simulação '{nome}' salva com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Nenhuma simulação realizada para salvar.")
