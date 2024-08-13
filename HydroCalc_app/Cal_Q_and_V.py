import numpy as np
import matplotlib.pyplot as plt


def calculate_Q_and_V(p,time_step_hours, Q_qp, time_to_compute):
    # Memotong atau menambah elemen di array p sesuai dengan time_to_compute
    if len(p) >= time_to_compute:
        p = p[:time_to_compute]
    elif len(p) < time_to_compute:
        p = np.pad(p, (0, time_to_compute - len(p)), 'constant', constant_values=(0,))

    # Mendefinisikan array untuk T
    T = np.arange(1, time_to_compute + time_step_hours, time_step_hours)
    #T = np.arange(1, time_to_compute + 1)

    # Inisialisasi matriks Q
    Q = np.zeros((len(p), len(Q_qp)))

    # Menghitung array baru Q untuk setiap elemen dalam p
    for i in range(len(p)):
        Q[i, :] = Q_qp * p[i]

    # Inisialisasi array QSI dengan nol
    QSI = np.zeros_like(Q)

    # Terapkan transformasi untuk menghasilkan QSI
    for i in range(Q.shape[0]):
        QSI[i, i:] = Q[i, :len(Q[i]) - i]

    Qtot = np.sum(QSI, axis=0)

    # Konversi T dari jam ke detik
    T_sec = T * time_step_hours * 3600

    # Inisialisasi array V_j dengan nol
    V_j = np.zeros_like(T, dtype=float)

    # Menghitung volume kumulatif untuk setiap delta T
    for i in range(len(T) - 1):
        V_j[i] = np.trapz(Qtot[i:i + 2], T_sec[i:i + 2])

    Vtot = np.sum(V_j)
    V_cum = np.cumsum(V_j)

    # Plot hubungan antara T dan Qtot
    #plt.figure(figsize=(12, 6))

    #plt.subplot(1, 2, 1)
    #plt.plot(T, Qtot[:len(T)], marker='o')
    #plt.title('Hubungan antara T dan Qtot')
    #plt.xlabel('T (Jam)')
    #plt.ylabel('Q (m3/det)')

    # Plot hubungan antara T dan Vtot
    #plt.subplot(1, 2, 2)
    #plt.plot(T[:-1], V_cum[:-1], marker='o')
    #plt.title('Hubungan antara T dan Vtot')
    #plt.xlabel('T (Jam)')
    #plt.ylabel('V (m3)')

    #plt.tight_layout()
    #plt.show()
    Q_peak = np.max(Qtot[:time_to_compute])
    max_index_Q = np.argmax(Qtot[:time_to_compute])
    t_peak_Q = T[max_index_Q]-1
    # Menghitung nilai maksimum dari V_cum
    V_total = np.max(V_cum)
    max_index_V = np.argmax(V_cum[:time_to_compute])
    t_peak_V = T[max_index_V]-1
    #print('Qpuncak', Q_peak,'m3/s')
    #print('t Qpuncak',t_peak_Q,'jam')
    #print('V puncak', V_total,'m3')
    #print('t Vpuncak', t_peak_V,'jam')
    return  Q_peak, t_peak_Q, V_total, t_peak_V, T, Qtot,V_cum
    