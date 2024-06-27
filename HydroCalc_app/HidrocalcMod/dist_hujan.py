# %%
import pandas as pd

#Dataseries Distribusi Hujan

ITB_delta_t1 = {
    'Jam': [1.00, 2.00, 3.00, 4.00, 5.00, 6.00, 7.00, 8.00, 9.00, 10.00, 11.00, 12.00, 13.00, 14.00, 15.00, 16.00, 17.00, 18.00, 19.00, 20.00, 21.00, 22.00, 23.00, 24.00],
    '6_jam': [0.0675, 0.1003, 0.5503, 0.1430, 0.0799, 0.0590, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
    '12_jam': [0.0304, 0.0350, 0.0418, 0.0535, 0.0796, 0.4368, 0.1135, 0.0634, 0.0468, 0.0380, 0.0325, 0.0286, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
    '18_jam': [0.0196, 0.0214, 0.0236, 0.0265, 0.0306, 0.0366, 0.0468, 0.0696, 0.3816, 0.0992, 0.0554, 0.0409, 0.0332, 0.0284, 0.0250, 0.0224, 0.0205, 0.0189, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
    '24_jam': [0.0145, 0.0154, 0.0165, 0.0178, 0.0194, 0.0215, 0.0241, 0.0278, 0.0332, 0.0425, 0.0632, 0.3467, 0.0901, 0.0503, 0.0371, 0.0302, 0.0258, 0.0227, 0.0204, 0.0186, 0.0171, 0.0160, 0.0149, 0.0141]
}

ITB_t6_delta_t_1per2 = {
    'Jam': [0.5000, 1.0000, 1.5000, 2.0000, 2.5000, 3.0000, 3.5000, 4.0000, 4.5000, 5.0000, 5.5000, 6.0000],
    'dis_itb_1per2': [0.0304, 0.0350, 0.0418, 0.0535, 0.0796, 0.4368, 0.1135, 0.0634, 0.0468, 0.0380, 0.0325, 0.0286]
}
ITB_t6_delta_t_1per3 = {
    'Jam': [0.333333333, 0.666666667, 1, 1.333333333, 1.6667, 2, 2.333333333, 2.666666667, 3, 3.333333333, 3.666666667, 4, 4.333333333, 4.666666667, 5, 5.333333333, 5.666666667, 6],
    'dis_itb_1per3': [0.018872447, 0.020463685, 0.02243929, 0.024973236, 0.0284, 0.033222972, 0.040883334, 0.055385656, 0.099178443, 0.381571414, 0.069571351, 0.046771076, 0.036558582, 0.030557698, 0.026536537, 0.023621637, 0.021394637, 0.019627839]
}
ITB_t6_delta_t_1per4 = {
    'Jam': [0.25, 0.5, 0.75, 1, 1.2500, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75, 5, 5.25, 5.5, 5.75, 6],
    'dis_itb_1per4': [0.014500836, 0.015429563, 0.016522887, 0.017833075, 0.0194, 0.021461682, 0.024110044, 0.027763511, 0.033215676, 0.042494343, 0.063209768, 0.346680637, 0.090109595, 0.050321208, 0.037144974, 0.030185073, 0.025776006, 0.022689691, 0.020387448, 0.018592491, 0.017146756, 0.015952845, 0.014947189, 0.014086383]
}
#ITB_t6_delta_t_1per5 = {
#    'Jam': [0.2, 0.4, 0.6, 0.8, 1.0000, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3, 3.2, 3.4, 3.6, 3.8, 4, 4.2, 4.4, 4.6, 4.8, 5, 5.2, 5.4, 5.6, 5.8, 6]
#,
#    'dis_itb_1per5': [0.321829795, 0.011498288, 0.012069883, 0.012718262, 0.0135, 0.014323537, 0.01533849, 0.016554761, 0.018044936, 0.01992326, 0.022381782, 0.02577336, 0.030834703, 0.039448253, 0.05867875, 0.083650338, 0.046714072, 0.034482339, 0.02802134, 0.023928324, 0.021063243, 0.01892603, 0.01725974, 0.015917638, 0.01480931, 0.013875741, 0.01307664, 0.012383473, 0.011775421, 0.011236906]
#}
ITB_t6_delta_t_1per6 = {
    'Jam': [0.333333333, 0.5, 0.666666667, 0.833333333, 1, 1.166666667, 1.333333333, 1.5, 1.666666667, 1.833333333, 2, 2.166666667, 2.333333333, 2.5, 2.666666667, 2.833333333, 3, 3.166666667, 3.333333333, 3.5, 3.666666667, 3.833333333, 4, 4.166666667, 4.333333333, 4.5, 4.666666667, 4.833333333, 5, 5.166666667, 5.333333333, 5.5, 5.666666667, 5.833333333, 6],
    'dis_itb_1per6': [0.009913067, 0.010341883, 0.010820303, 0.011358194, 0.011968343, 0.012667647, 0.013478964, 0.014434072, 0.015578626, 0.016980934, 0.018748506, 0.021062063, 0.024253661, 0.029016566, 0.037122228, 0.055218818, 0.302853432, 0.078717982, 0.043959624, 0.032449124, 0.02636909, 0.022517415, 0.019821271, 0.017810076, 0.016242037, 0.014979071, 0.013936094, 0.013057572, 0.012305589, 0.011653294, 0.011081096, 0.010574334, 0.010121801, 0.009714772, 0.009346341]
}

PSA_007_delta_t1 = {
    'Jam': [1.00, 2.00, 3.00, 4.00, 5.00, 6.00, 7.00, 8.00, 9.00, 10.00, 11.00, 12.00, 13.00, 14.00, 15.00, 16.00, 17.00, 18.00, 19.00, 20.00, 21.00, 22.00, 23.00, 24.00],
    '6_jam': [0.0500, 0.1000, 0.6000, 0.1600, 0.0600, 0.0300, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
    '12_jam': [0.0200, 0.0200, 0.0300, 0.0500, 0.0900, 0.4500, 0.1500, 0.0700, 0.0500, 0.0300, 0.0300, 0.0100, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
    '24_jam': [0.0075, 0.0075, 0.0125, 0.0125, 0.0150, 0.0150, 0.0250, 0.0250, 0.0350, 0.0500, 0.0900, 0.3300, 0.1200, 0.0600, 0.0400, 0.0350, 0.0250, 0.0250, 0.0150, 0.0150, 0.0125, 0.0125, 0.0075, 0.0075]
}

ITB_delta_t1=pd.DataFrame(ITB_delta_t1)
ITB_t6_delta_t_1per2=pd.DataFrame(ITB_t6_delta_t_1per2)
ITB_t6_delta_t_1per3=pd.DataFrame(ITB_t6_delta_t_1per3)
ITB_t6_delta_t_1per4=pd.DataFrame(ITB_t6_delta_t_1per4)
#ITB_t6_delta_t_1per5=pd.DataFrame(ITB_t6_delta_t_1per5)
ITB_t6_delta_t_1per6=pd.DataFrame(ITB_t6_delta_t_1per6)
PSA_007_delta_t1=pd.DataFrame(PSA_007_delta_t1)

#fungsi memanggil jenis distibusi hujan
def coef_dist_hujan(input_method_dis, jumlah_jam_hujan, delta_jam_hujan):
    if input_method_dis == "PSA-007":
        if delta_jam_hujan == 1:
            T = PSA_007_delta_t1['Jam']
            if jumlah_jam_hujan == 6:
                distribusi = PSA_007_delta_t1['6_jam']
            elif jumlah_jam_hujan == 12:
                distribusi = PSA_007_delta_t1['12_jam']
            elif jumlah_jam_hujan == 24:
                distribusi = PSA_007_delta_t1['24_jam']
            else:
                raise ValueError("Jumlah jam hujan tidak valid untuk PSA-007, Hanya bisa 6 jam, 12 jam atau 24 jam")
        else:
            raise ValueError("Jumlah delta hujan tidak valid untuk PSA-007, PSA-007 hanya mengakomodir delta t hujan 1 jam")
    elif input_method_dis == "ITB":
        if jumlah_jam_hujan == 6:
            if delta_jam_hujan == 1:
                T = ITB_delta_t1['Jam']
                distribusi = ITB_delta_t1['6_jam']
            elif delta_jam_hujan == 1/2:
                T = ITB_t6_delta_t_1per2['Jam']
                distribusi = ITB_t6_delta_t_1per2['dis_itb_1per2']
            elif delta_jam_hujan == 1/3:
                T = ITB_t6_delta_t_1per3['Jam']
                distribusi = ITB_t6_delta_t_1per3['dis_itb_1per3']
            elif delta_jam_hujan == 1/4:
                T = ITB_t6_delta_t_1per4['Jam']
                distribusi = ITB_t6_delta_t_1per4['dis_itb_1per4']
            #elif delta_jam_hujan == '1/5':
            #    T = ITB_t6_delta_t_1per5['Jam']
            #    distribusi = ITB_t6_delta_t_1per5['dis_itb_1per5']
            elif delta_jam_hujan == 1/6:
                T = ITB_t6_delta_t_1per6['Jam']
                distribusi = ITB_t6_delta_t_1per6['dis_itb_1per6']
            else:
                raise ValueError("Delta jam hujan tidak valid untuk ITB")
        elif jumlah_jam_hujan == 12:
                if delta_jam_hujan == 1:
                    T = ITB_delta_t1['Jam']
                    distribusi = ITB_delta_t1['12_jam']
                else:
                    raise ValueError("Untuk Jumlah Hujan 12 Jam maka Delta jam hujan hanya 1 Jam untuk metode ITB")
        elif jumlah_jam_hujan == 18:
                if delta_jam_hujan == 1:
                    T = ITB_delta_t1['Jam']
                    distribusi = ITB_delta_t1['18_jam']
                else:
                    raise ValueError("Untuk Jumlah Hujan 18 Jam maka Delta jam hujan hanya 1 Jam untuk metode ITB")
        elif jumlah_jam_hujan == 24:
                if delta_jam_hujan == 1:
                    T = ITB_delta_t1['Jam']
                    distribusi = ITB_delta_t1['24_jam']
                else:
                    raise ValueError("Untuk Jumlah Hujan 24 Jam maka Delta jam hujan hanya 1 Jam untuk metode ITB")
        else:
            raise ValueError("Jumlah Hujan tidak valid Gunakan 6, 12, 18 atau 24")
    else:
        raise ValueError("Metode yang dipilih tidak valid")
    Table_Dist_Rain = pd.DataFrame({'Jam ke':T,'Koefisien': distribusi})
    return T, distribusi, Table_Dist_Rain 



# %%
