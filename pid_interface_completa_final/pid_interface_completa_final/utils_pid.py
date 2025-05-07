import numpy as np
import control as ctrl

def simular_pid(Kp, Ti, Td, k, tau, theta, tempo, ordem_pade, setpoint=1.0):
    # Validação básica dos parâmetros
    if Kp <= 0 or Ti <= 0 or Td < 0 or k == 0 or tau == 0:
        raise ValueError("Parâmetros inválidos: Kp, Ti, Td, k e tau devem ser positivos.")

    # Criação do controlador PID
    PID = ctrl.tf([Kp * Td, Kp, Kp / Ti], [1, 0])

    # Aproximação de Padé para o atraso
    num_pade, den_pade = ctrl.pade(theta, ordem_pade)
    atraso = ctrl.tf(num_pade, den_pade)

    # Modelo da planta com atraso
    G_open = ctrl.series(ctrl.tf([k], [tau, 1]), atraso)

    # Sistema em malha fechada com PID
    sistema_pid = ctrl.feedback(PID * G_open)

    # Simulação da resposta ao degrau
    try:
        t_pid, y_pid = ctrl.step_response(sistema_pid, T=tempo)
        y_pid *= setpoint  # Escalando pela referência desejada

        # Cálculo manual das métricas
        y_final = np.mean(y_pid[-int(0.05 * len(y_pid)):])  # média dos últimos 5%
        y_max = np.max(y_pid)
        overshoot = ((y_max - y_final) / y_final) * 100 if y_final != 0 else 0

        # Tempo de pico
        tp_index = np.argmax(y_pid)
        tp = t_pid[tp_index]

        # Tempo de subida (10% a 90% do valor final)
        tr = None
        t10 = t90 = None
        for i, y in enumerate(y_pid):
            if t10 is None and y >= 0.1 * y_final:
                t10 = t_pid[i]
            if t90 is None and y >= 0.9 * y_final:
                t90 = t_pid[i]
                break
        if t10 is not None and t90 is not None:
            tr = t90 - t10

        # Tempo de acomodação (±2%)
        tol = 0.02
        upper = y_final * (1 + tol)
        lower = y_final * (1 - tol)
        ts = None
        for i in reversed(range(len(y_pid))):
            if not (lower <= y_pid[i] <= upper):
                ts = t_pid[i + 1] if i + 1 < len(t_pid) else t_pid[-1]
                break
        if ts is None:
            ts = t_pid[-1]

        info = {
            "PeakTime": tp,
            "Overshoot": overshoot,
            "RiseTime": tr if tr else 0,
            "SettlingTime": ts
        }

        return t_pid, y_pid, info

    except Exception as e:
        raise RuntimeError(f"Erro na simulação PID: {str(e)}")
