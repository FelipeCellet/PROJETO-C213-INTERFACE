import numpy as np
import control as ctrl

def simular_pid(Kp, Ti, Td, k, tau, theta, tempo, ordem_pade, setpoint=1.0):
    PID = ctrl.tf([Kp * Td, Kp, Kp / Ti], [1, 0])
    num_pade, den_pade = ctrl.pade(theta, ordem_pade)
    atraso = ctrl.tf(num_pade, den_pade)
    G_open = ctrl.series(ctrl.tf([k], [tau, 1]), atraso)
    sistema_pid = ctrl.feedback(PID * G_open)
    
    t_pid, y_pid = ctrl.step_response(sistema_pid, T=tempo)
    y_pid *= setpoint  # Ajuste da saída com base no setpoint
    
    info = ctrl.step_info(sistema_pid)
    return t_pid, y_pid, info
