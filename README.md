# Interface PID com Identificação de Sistemas – Projeto C213

Este projeto tem como objetivo a **identificação e controle PID** de um processo simulado baseado na **resposta térmica** de um sistema (representando o branqueamento da glicerina). A aplicação foi desenvolvida em Python com uma interface gráfica utilizando **Tkinter** e gráficos interativos via **Matplotlib**.

## Sumário

- [Objetivo](#objetivo)
- [Descrição do Processo](#descrição-do-processo)
- [Funcionalidades](#funcionalidades)
- [Instalação](#instalação)
- [Métodos de Identificação](#métodos-de-identificação)
- [Sintonia PID](#sintonia-pid)
- [Histórico de Simulações](#histórico-de-simulações)
- [Autores](#autores)

---

## Objetivo

Desenvolver uma ferramenta completa para:

- Carregar dados experimentais de um sistema térmico simulado;
- Identificar os parâmetros da planta (ganho, atraso e constante de tempo);
- Simular diferentes métodos de sintonia PID;
- Exportar os resultados gráficos;
- Armazenar o histórico de simulações para exportação posterior.

---

## Descrição do Processo

O sistema simula o **controle da temperatura** no processo de **branqueamento da glicerina**, onde a variável controlada é a temperatura, e a entrada é um degrau de controle.

Este é um processo com **características de atraso e resposta lenta**, ideal para modelagem como **sistema de primeira ordem com atraso (FOPDT)**.

---

## Funcionalidades

- Interface com abas separadas:
  - Início
  - Identificação
  - Controle PID
  - EQM dos modelos
  - Gráficos com modelo de Smith
  - Histórico de simulações
- Métodos de sintonia implementados:
  - **Ziegler-Nichols**
  - **Cohen-Coon**
  - **Manual** (com autenticação via senha)
- Cálculo e visualização de:
  - Ganho (k), Constante de tempo (τ), Atraso (θ)
  - Overshoot, tempo de subida, tempo de acomodação
  - Erro Quadrático Médio (EQM)
- Exportação dos gráficos em PNG e PDF
- Armazenamento de simulações para revisão posterior

---

## Instalação

### Requisitos

- Python 3.10 ou superior
- Bibliotecas:
  - `numpy`
  - `scipy`
  - `matplotlib`
  - `control`
  - `tkinter` (incluso no Python)

### Instalar dependências

```bash
pip install numpy scipy matplotlib control


---

## Métodos de Identificação

Utilizamos o modelo **FOPDT** com:

- **Método de Smith** (padrão do projeto)
  - Simples e robusto para processos com atraso
- **Parâmetros extraídos:**
  - `k` (Ganho)
  - `τ` (Constante de tempo)
  - `θ` (Atraso puro)
- Atraso modelado com **aproximação de Padé** (ajustável entre ordem 1 a 20)

---

## Sintonia PID

### Métodos disponíveis

- **Ziegler-Nichols**
- **Cohen-Coon**
- **Manual** (exige senha de 6 dígitos: `123456`)

### Recursos

- Visualização da resposta do sistema
- Curvas com tempo de subida, acomodação e pico
- Exportação dos resultados

---

## Histórico de Simulações

Cada simulação realizada pode ser **armazenada em memória** com:

- Gráfico da resposta
- Parâmetros usados (Kp, Ti, Td)
- Métricas do sistema (Overshoot, Rise Time, Settling Time)
- Exportação futura (PDF/PNG)

Essa funcionalidade visa ajudar na **comparação entre diferentes configurações PID** ao longo do projeto.

---

## Autores

- **Felipe Siqueira Mohallem Cellet**
- _[Adicione os demais membros aqui]_

**Instituto Nacional de Telecomunicações – INATEL**  
Disciplina: **C213 – Sistemas Embarcados**  
Curso: **Engenharia da Computação – 2025**
