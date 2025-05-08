import numpy as np
import control as ctrl

def simular_pid(Kp, Ti, Td, k, tau, theta, tempo, ordem_pade, setpoint=1.0):
    if Kp <= 0 or Ti <= 0 or Td < 0 or k == 0 or tau == 0:
        raise ValueError("Parâmetros inválidos: Kp, Ti, Td, k e tau devem ser positivos.")

    PID = ctrl.tf([Kp * Td, Kp, Kp / Ti], [1, 0])
    num_pade, den_pade = ctrl.pade(theta, ordem_pade)
    atraso = ctrl.tf(num_pade, den_pade)
    G_open = ctrl.series(ctrl.tf([k], [tau, 1]), atraso)
    sistema_pid = ctrl.feedback(PID * G_open)

    try:
        t_pid, y_pid = ctrl.step_response(sistema_pid, T=tempo)
        y_pid *= setpoint


        info_raw = ctrl.step_info(sistema_pid, T=tempo)

        rise_time_corrigido = max(0, info_raw["RiseTime"] - theta)

        y_final = np.mean(y_pid[-int(0.05 * len(y_pid)):])
        y_max = np.max(y_pid)
        overshoot = ((y_max - y_final) / y_final) * 100 if y_final != 0 else 0

        # Tempo de pico
        tp_index = np.argmax(y_pid)
        tp = t_pid[tp_index]

        # Tempo de acomodação (±2%) reusado do cálculo manual
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
            "RiseTime": rise_time_corrigido,
            "SettlingTime": ts
        }

        return t_pid, y_pid, info

    except Exception as e:
        raise RuntimeError(f"Erro na simulação PID: {str(e)}")
