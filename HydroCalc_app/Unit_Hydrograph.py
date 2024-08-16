import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

########################################################
############### Unit Hydrogpraph Syntetic ##############
########################################################


##############################################################
######################## SCS-CN ##############################
##############################################################
def Qp_SCS_CN(L,CN_sal,S,A):
    tl=L**0.8*(2540-22.86*CN_sal)**0.7/(14104*CN_sal**0.7*S**0.5)
    Tp=10/9*tl
    tr=2/9*tl
    Qp=2.083*A/Tp/10
    tpertp=np.arange(0.0,5.1,0.2)
    qperqp=np.array([0,0.1,0.31,0.66,0.93,1,0.93,0.78,0.56,0.39,0.28,0.207,0.147,0.107,0.077,0.055,0.04,0.029,0.021,0.015,0.011,
                    0.01,0.007,0.003,0.0015,0])
    T=tpertp*Tp
    Q=qperqp*Qp
    return T,Q,Qp,Tp

##############################################################
######################## SCS #################################
##############################################################
# def Qp_SCS(L,S,A,C):
#     L=L/1000
#     Tc=0.927*(L/S**0.5)**0.47 #waktu konsentrasi (jam)
#     print('Tc',Tc)
#     tp= 0.6*Tc #waktu naik  
#     print('tp',tp)
#     tr=2*tp/9
#     print('tr',tr)
#     Tp=tr/2+tp
#     #Tp=3.14
#     print('Tp',Tp)
    
#     #C = 2.08 #koefisien
#     Tb=2.67 * Tp 
#     Qp=C*A/Tp
#     print('Qp',Qp)
#     qperqp=np.array([0,0.18,0.66,0.99,0.86,0.57,0.28,0.17,0.12,0.09,0.06,
#                      0.04,0.02,0.02,0.01,0.01])
#     t = np.arange(len(qperqp))
#     tpertp = t/Tp
#     # Tambahan nilai 0 sebanyak n
#     n = 1
#     qperqp = np.concatenate((qperqp, np.zeros(n)))

#     # Menghitung T dan Q awal
#     T = tpertp * Tp
#     Q = qperqp * Qp

#     # Memperpanjang tpertp dengan langkah 0.5
#     tpertp_extension = np.arange(tpertp[-1] + 0.5, tpertp[-1] + 0.5 * (n + 1), 0.5)
#     tpertp = np.concatenate((tpertp, tpertp_extension))

#     # Memperbarui T dan Q dengan tpertp yang diperpanjang
#     T = tpertp * Tp
#     Q = qperqp * Qp

#     return T,Q,Qp,Tp
def Qp_SCS(L,S,A,tr):
    Tc=0.01947*L**0.77*S**(-0.385) #waktu konsentrasi (menit)
    tp_aw= Tc/60 #waktu kelambatan (jam), Tc ubah dari menit ke jam 
    Tp= tr/2 + tp_aw #waktu naik  
    C = 2.08 #koefisien
    Qp=C*A/Tp/10
    tp=2.67 * Tp 
    tpertp = np.concatenate([
    np.arange(0, 1.6, 0.1),  # dari 0 hingga 1.6 dengan langkah 0.1
    np.arange(1.6, 3.1, 0.2), # dari 1.6 hingga 3 dengan langkah 0.2
    np.arange(3.5, 5.1, 0.5)  # dari 3.5 hingga 5 dengan langkah 0.5
    ])
    qperqp=np.array([0,0.015,0.075,0.16,0.28,0.43,0.6,0.77,0.89,0.97,1,
                     0.98,0.92,0.84,0.75,0.66,0.56,0.42,0.32,0.24,0.18,0.13,
                     0.098,0.075,0.036,0.018,0.009,0.004])
    # Tambahan nilai 0 sebanyak n
    n = 50
    qperqp = np.concatenate((qperqp, np.zeros(n)))

    # Menghitung T dan Q awal
    T = tpertp * Tp
    Q = qperqp * Qp

    # Memperpanjang tpertp dengan langkah 0.5
    tpertp_extension = np.arange(tpertp[-1] + 0.5, tpertp[-1] + 0.5 * (n + 1), 0.5)
    tpertp = np.concatenate((tpertp, tpertp_extension))

    # Memperbarui T dan Q dengan tpertp yang diperpanjang
    T = tpertp * Tp
    Q = qperqp * Qp

    return T,Q,Qp,Tp

##############################################################
######################## Snyder ##############################
##############################################################

def Qp_Snyder(L,Lc,A,tr,ct,cp):
    n = 0.3
    tp= ct * (L/1000 * Lc/1000)**n
    #print('tp',tp)
    tc = tp/5.5
    #print('tc',tc)
    qp=275*cp/tp #debit maksimum limpasan [liter/det/km2]
    #print('qp',qp)
    if tc >= tr:
        t__p=tp+0.25*(tr-tc)
        Tp=t__p+0.5*tr#(tr-tc)
    else:
        t__p=tp + 0.25*(tr-tc)
        Tp=t__p + 0.5*(tr-tc)#tr
    #print('Tp',Tp)
    qp=275*cp/Tp #debit maksimum limpasan [liter/det/km2]
    Qp=qp*A/1000 #1 mm
    #print('Qp',Qp)
    #Qp=qp
    tpertp=np.arange(0.1,10,0.1)
    lamda = (Qp*Tp*1000)/(1000*A)
    a=1.32*lamda**2+0.15*lamda+0.045
    qperqp=10**-(a*(1-tpertp)**2/tpertp)
    T=tpertp*Tp
    Q=qperqp*Qp
    T = np.insert(T,0,0)
    Q = np.insert(Q,0,0)    
    return T,Q,Qp,Tp

##############################################################
######################## ITB 1a ##############################
##############################################################

def HSS_ITB_1(ct,tr,cp,L,Lc,A,Alpha):
    # Perhitungan waktu puncak
    n = 0.3
    tp= ct * (L/1000 * Lc/1000)**n #time leg sndyder
    Tp = tp + tr * 0.5  # waktu puncak
    Tb = 50 * Tp  # Tb/Tp = 20 (ditetapkan)
    T = np.arange(1, Tb, 1)
    T = np.insert(T, math.floor(Tp), Tp)  # Menyisipkan Tp ke dalam array T
    tpertp = T/Tp
    #Alpha = 1.5
    qperqp = np.exp(2-tpertp-1/tpertp)**(Alpha*cp)
    A_Hss_j=np.zeros_like(tpertp, dtype=float)
    # Perhitugan A HSS dengan integral
    for i in range(len(tpertp)-1):
            A_Hss_j[i] = 0.5*(tpertp[i]-tpertp[i-1])*(qperqp[i]+qperqp[i-1])
    A_Hss_j[0]=0
    A_Hss = np.sum(A_Hss_j)
    # Perhitungan Debit Puncak
    Kp = 1/(3.6*A_Hss)
    Qp = Kp*A/Tp
    Vol_Hujan = 1000*tr*A
    Q=qperqp*Qp
    # Perhitugan Volume hujan dengan integral
    V=np.zeros_like(T, dtype=float)
    for i in range(len(tpertp)-1):
            V[i] = 0.5*(T[i]-T[i-1])*(Q[i]+Q[i-1])
    V[0]=0
    T = np.insert(T,0,0)
    Q = np.insert(Q,0,0)
    return T,Q,Qp,Tp
##############################################################
######################## ITB 2 ###############################
##############################################################

def HSS_ITB_2(ct,tr,cp,L,A,Alpha,betha):
    # Perhitungan waktu puncak
    #n = 0.3
    #metode nakayasu
    if L < 15:
         tl= ct * 0.201*(L/1000)**0.7
    else:
         tl= ct * (0.527+0.058*(L/1000))   
    #tl= ct * (0.0394*(L/1000)+0.201*(L/1000)**0.5) 
    Tp = 1.6* tl # waktu puncak
    Tb = 50 * Tp  # Tb/Tp = 20 (ditetapkan)
    T = np.arange(1, Tb, 1)
    T = np.insert(T, math.floor(Tp), Tp)  # Menyisipkan Tp ke dalam array T
    tpertp = T/Tp
    #Alpha = 2.5
    #betha = 0.72
    qperqp=np.zeros_like(tpertp, dtype=float)   
    for i in range (len(tpertp)):
        if tpertp[i] <1:
            qperqp[i] = tpertp[i]**Alpha
        elif tpertp[i] >= 1 :
            qperqp[i] = np.exp(1-tpertp[i]**(betha*cp))
    A_Hss_j=np.zeros_like(tpertp, dtype=float)        
    # Perhitugan A HSS dengan integral
    for i in range(len(tpertp)-1):
            A_Hss_j[i] = 0.5*(tpertp[i]-tpertp[i-1])*(qperqp[i]+qperqp[i-1])
    A_Hss_j[0]=0
    A_Hss = np.sum(A_Hss_j)
    # Perhitungan Debit Puncak
    Kp = 1/(3.6*A_Hss)
    Qp = Kp*A/Tp
    Vol_Hujan = 1000*tr*A
    Q=qperqp*Qp
    # Perhitugan Volume hujan dengan integral
    V=np.zeros_like(T, dtype=float)
    for i in range(len(tpertp)-1):
            V[i] = 0.5*(T[i]-T[i-1])*(Q[i]+Q[i-1])
    V[0]=0
    T = np.insert(T,0,0)
    Q = np.insert(Q,0,0)
    return T,Q,Qp,Tp