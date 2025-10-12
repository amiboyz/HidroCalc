import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#output_notebook()
# Fungsi untuk menghitung limpasan berdasarkan metode CN
def infiltrasi_CN(P, ARF, CN, Im, jumlah_data_hujan, dist_jam, T):
    coef_dist = dist_jam[:int(jumlah_data_hujan)]
    Pjam = coef_dist * P
    Pjam_cum = np.cumsum(Pjam)
    # Tanpa Area Reduction F
    Pjam_ARF = Pjam * ARF  # Hujan Jam Jaman dikali dengan area reduction factor
    Pjam_ARF_cum = np.cumsum(Pjam_ARF)
    absis = T[:int(jumlah_data_hujan)] # np.arange(1, len(Pjam_ARF) + 1)  # Membuat array sumbu x (jumlah jam)

    Pjam_ARF = np.array(Pjam_ARF)
    Pkum = np.array(Pjam_ARF_cum)

    def limpCN(CN, P):  # membuat fungsi dengan nilai CN dan Hujan
        '''P dalam mm, limp dalam mm'''
        S = 1000 / CN - 10  # persamaan hubungan storage dengan nilai CN
        k = 0.2  # where K is varied between 0-0.26 (springer et al.), K=0.2 is recommended by SCS
        Pkum = []  # membuat array hujan kumulatif
        Ptot = 0  # mendefinisikan hujan total =0
        for i in range(len(Pjam_ARF)):  # membuat nilai i sejumlah hujan jam-jaman yang diberikan
            Ptot += Pjam_ARF[i] / 25.4  # Hujan total baru adalah hujan total sebelumnya di tambah hujan pada jam i (diubah dari mm ke inch)
            Pkum.append(Ptot)  # Menyimpan hujan kumulatif ke dalam array Pkum
        reff = []  # membua tarray hujan efektif
        infil = []  # membuat array infiltrasi
        Iab = []  # membuat array Inital Abstraction
        reffkumseb = 0  # memberikan nilai hujan efektif sebelumnya
        Faseb = 0  # memberikan nilai infiltrasi sebelumnya
        for i in range(len(Pkum)):  # membuat nilai i sejumlah Hujan kumulatif
            Ia = k * S  # initial abtraction koefisien x dengan storage
            if (Pkum[i] > Ia):  # Cek apakah nilai hujan kumulatif pada jam tersebut lebih besar dari initial abtraction
                Ia = Ia  # jika hujan kumulatif > Ia maka berikan nilai Ia adalah Ia
                Iab.append(Ia)
            else:
                Ia = Pkum[i]  # jika hujan kumulatif < atau = Ia maka berikan nilai Ia adalah hujan kumulatif pada jam tersebut
                Iab.append(Ia)
            Fa = (S * (Pkum[i] - Ia) / (Pkum[i] - Ia + S)) # continuing abstraction (Fa) = storage x (hujan kumulatif - initial abstraction) / (hujan kumulatif - initial abstraction + storage)
            infil.append(Fa - Faseb)  # memasukan nilai infiltrasi yaitu continuing abstraction (Fa) - continuing abstraction sebelumnya (Fa)
            Faseb = Fa  # update nilai continuing abstraction (Fa) sebelumnya
            reffkum = Pkum[i] - Ia - Fa  # hujan efektif kumulatif = Hujan kumulatif - Ia -Fa
            reff.append(reffkum - reffkumseb)  # memasukan nilai hujan efektif = hujan efektif kumulatif - hujan efektif kumulatif sebelumnya
            reffkumseb = reffkum  # update nilai hujan kumulatif
        infil = np.array(infil) * 25.4  # membuat array infiltrasi dan mnejadikan dari inch ke mm
        reff = np.array(reff) * 25.4  # membuat array hujan dan menjadikan dari inch ke mm
        Iab = np.array(Iab) * 25.4 # membuat array intial abstraction dan menjadikan dari inch ke mm
        return (reff, infil, Iab)  # Menyimpan fungsi hujan efektif dan infiltrasi

    reff, infil, Iab = (limpCN(CN, P))  # Memanggil fungsi limpasan CN
    
    #Hujan Efektif Jam-jaman 
    
    ##########################
    Iab_jam = np.zeros(len(Iab))
    Iab_jam[0]=Iab[0]
    Iab_jam[1:] = np.diff(Iab)
    # print('intial jam',Iab_jam)
    # print('infil jam ',infil)
    #Hujan Efektif Jam-jaman 
    
    #reff_jam = reff
    infiltrasi_jam = (Iab_jam+infil)
    infiltrasi_jam = infiltrasi_jam-(infiltrasi_jam*Im/100)
    reff_jam = Pjam_ARF - infiltrasi_jam
    infiltrasi_kum = np.cumsum(infiltrasi_jam)  
    reff_kum = np.cumsum(reff_jam)
    
    reffkumtab = {
        'Hours': absis,
        'Planned Rainfall ': Pjam_cum,
        'Planned Rainfall (ARF)': Pkum,
        'Infiltration': infiltrasi_kum,
        'Effective Rainfall': reff_kum,
    #    'Iab': Iab,
        #'Nilai CN': CN,s
        #'Nilai Impervious (%)': Im,
    }
    dfreffkum = pd.DataFrame(reffkumtab)  

        # Menyimpan hasil perhitungan dalam DataFrame
    refftab = {
        'Hours': absis,
        'Planned Rainfall ': Pjam,
        'Planned Rainfall (ARF)': Pjam_ARF,
        'Infiltration': infiltrasi_jam,
        'Effective Rainfall': reff_jam,
    #    'Iab': Iab_jam,
        #'Nilai CN': CN,
        #'Nilai Impervious (%)': Im,
    }
    dfreff = pd.DataFrame(refftab)
    
    # First plot using Matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(absis + 0.25, reff_kum, width=0.2, color="orange", label="Effective Rainfall [mm]")
    ax.bar(absis, infiltrasi_kum, width=0.2, color="greenyellow", label="Infiltration [mm]")
    ax.set_xlabel('Hours', fontsize=14)
    ax.set_ylabel('Effective Rainfall / Infiltration (mm)', fontsize=14)
    ax.set_title("Grafik Hujan Jam-Jaman Kumulatif dengan P = {} mm/hari (Metode SCS-CN)".format(np.round(np.sum(P) / ARF, 3)), fontsize=13)
    ax.tick_params(axis='both', labelsize=12)
    ax.legend(loc='upper left', fontsize=12)
    fig.tight_layout()

    # Second plot using Matplotlib
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.bar(absis + 0.25, reff, width=0.2, color="orange", label="Hujan efektif [mm]")
    ax2.bar(absis, infiltrasi_jam, width=0.2, color="greenyellow", label="Infiltrasi [mm]")
    ax2.set_xlabel('Jam ke-', fontsize=14)
    ax2.set_ylabel('Hujan Efektif / Infiltrasi (mm)', fontsize=14)
    ax2.set_title("Grafik Hujan Jam-Jaman dengan P = {} mm/hari (Metode SCS-CN)".format(np.round(np.sum(P) / ARF, 3)), fontsize=13)
    ax2.tick_params(axis='both', labelsize=12)
    ax2.legend(loc='upper left', fontsize=12)
    fig2.tight_layout()

    # Tampilkan tabel
    print("Tabel Hujan Efektif Kumulatif (Metode SCS-CN)")
    print(dfreffkum)
    print("Tabel Hujan Efektif Jam-jaman (Metode SCS-CN)")
    print(dfreff)
    return  absis, Pjam, Pjam_ARF, infiltrasi_jam, reff_jam, dfreffkum, dfreff, fig, fig2, Iab

def infiltrasi_Horton(P, ARF, k, f0, fc, jumlah_data_hujan, dist_jam, T):
    coef_dist = dist_jam[:int(jumlah_data_hujan)]
    Pjam = coef_dist * P
    Pjam_cum = np.cumsum(Pjam)
    # Tanpa Area Reduction F
    Pjam_ARF = Pjam * ARF  # Hujan Jam Jaman dikali dengan area reduction factor
    Pjam_ARF_cum = np.cumsum(Pjam_ARF)
    absis = T[:int(jumlah_data_hujan)] # np.arange(1, len(Pjam_ARF) + 1)  # Membuat array sumbu x (jumlah jam)
    Pkum = np.array(Pjam_ARF_cum)
    # Menghitung infiltrasi per jam menggunakan rumus Horton
    infiltrasi_jam = []
    f0=f0*P
    for t in absis:
        infil_value = fc + (f0 - fc) * np.exp(-k * t)
        infiltrasi_jam.append(infil_value)

    # Menghitung runoff per jam
    reff_jam = []
    for i in range(len(infiltrasi_jam)):
        if infiltrasi_jam[i] >= Pjam_ARF[i]:
            reff_value = 0
        else:
            reff_value = Pjam_ARF[i] - infiltrasi_jam[i]
        reff_jam.append(reff_value)

    infiltrasi_kum = np.cumsum(infiltrasi_jam)
    reff_kum = np.cumsum(reff_jam)
    reff = reff_jam
    reffkumtab = {
        'Jam ke-': absis,
        'Hujan Rencana ': Pjam_cum,
        'Hujan Rencana (ARF)': Pkum,
        'Infiltrasi': infiltrasi_kum,
        'Hujan Efektif': reff_kum,
        # Iab': Iab,
        #'Nilai CN': CN,s
        #'Nilai Impervious (%)': Im,
        }
    dfreffkum = pd.DataFrame(reffkumtab)  

        # Menyimpan hasil perhitungan dalam DataFrame
    refftab = {
        'Jam ke-': absis,
        'Hujan Rencana ': Pjam,
        'Hujan Rencana (ARF)': Pjam_ARF,
        'Infiltrasi': infiltrasi_jam,
        'Hujan Efektif': reff_jam,
    #    'Iab': Iab_jam,
        #'Nilai CN': CN,
        #'Nilai Impervious (%)': Im,
    }
    dfreff = pd.DataFrame(refftab)
    
    # First plot using Matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(absis + 0.25, reff_kum, width=0.2, color="orange", label="Hujan efektif [mm]")
    ax.bar(absis, infiltrasi_kum, width=0.2, color="greenyellow", label="Infiltrasi [mm]")
    ax.set_xlabel('Jam Ke-', fontsize=14)
    ax.set_ylabel('Curah Hujan (mm)', fontsize=14)
    ax.set_title("Grafik Hujan Jam-Jaman Kumulatif dengan P = {} mm/hari (Metode Horton)".format(np.round(np.sum(P) / ARF, 3)), fontsize=13)
    ax.tick_params(axis='both', labelsize=12)
    ax.legend(loc='upper left', fontsize=12)
    fig.tight_layout()

    # Second plot using Matplotlib
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.bar(absis + 0.25, reff, width=0.2, color="orange", label="Hujan efektif [mm]")
    ax2.bar(absis, infiltrasi_jam, width=0.2, color="greenyellow", label="Infiltrasi [mm]")
    ax2.set_xlabel('Jam ke-', fontsize=14)
    ax2.set_ylabel('Curah Hujan (mm)', fontsize=14)
    ax2.set_title("Grafik Hujan Jam-Jaman dengan P = {} mm/hari (Metode Horton)".format(np.round(np.sum(P) / ARF, 3)), fontsize=13)
    ax2.tick_params(axis='both', labelsize=12)
    ax2.legend(loc='upper left', fontsize=12)
    fig2.tight_layout()

    # Tampilkan tabel
    print("Tabel Hujan Efektif Kumulatif (Metode Horton)")
    print(dfreffkum)
    print("Tabel Hujan Efektif Jam-jaman (Metode Horton)")
    print(dfreff)
    return  absis, Pjam, Pjam_ARF, infiltrasi_jam, reff_jam, dfreffkum, dfreff, fig, fig2
