import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show
# from HidrocalcMod import (coef_dist_hujan,
#                           infiltrasi_CN, infiltrasi_Horton, 
#                           calculate_Q_and_V,
#                           Qp_SCS,Qp_Snyder,HSS_ITB_1,HSS_ITB_2)
from Cal_Q_and_V import calculate_Q_and_V
from dist_hujan import coef_dist_hujan
from infiltrasi_calc import infiltrasi_CN, infiltrasi_Horton
from Unit_Hydrograph import Qp_SCS,Qp_Snyder,HSS_ITB_1,HSS_ITB_2


#Tabel Input

# Fungsi untuk menjalankan analisis distribusi hujan dan infiltrasi berdasarkan metode yang dipilih

# Mengatur judul dan deskripsi aplikasi
st.title('Analisis Hujan Efektif dan Hidrograf Satuan Sintesis (HSS) dengan Modul HydroCalc')

st.write('Selamat datang di aplikasi berbasis web untuk perhitungan infiltrasi dan hidrograf satuan sintesis (HSS) menggunakan metode distribusi hujan PSA-007 dan ITB. Aplikasi ini dimaksudkan untuk membantu Anda dalam menganalisis hujan efektif dan menghasilkan hidrograf satuan sintesis.')

st.write('### Metode Infiltrasi yang Tersedia:')
st.write('- **SCS-CN**: Metode ini menggunakan parameter Curah Hujan Rencana dan Kurva Angka (Curve Number) untuk menghitung infiltrasi.')
st.write('- **Horton**: Metode ini menggunakan parameter laju infiltrasi awal (f0), laju infiltrasi akhir (fc), dan koefisien penurunan (k) untuk menghitung infiltrasi.')

st.write('### Metode Hidrograf Satuan Sintesis (HSS) yang Tersedia:')
st.write('- **SCS**: Metode ini didasarkan pada unit hidrograf SCS yang dikembangkan oleh Soil Conservation Service.')
st.write('- **Snyder**: Metode ini menggunakan parameter karakteristik DAS untuk menghasilkan unit hidrograf.')
st.write('- **ITB-1**: Metode ini merupakan salah satu metode hidrograf sintesis yang dikembangkan oleh ITB.')
st.write('- **ITB-2**: Metode ini juga merupakan metode hidrograf sintesis yang dikembangkan oleh ITB dengan pendekatan yang berbeda.')

st.write('Aplikasi ini masih dalam proses pengembangaan masukan dan saran silakan hubungi: [miftahhazmi@gmail.com](mailto:miftahhazmi@gmail.com) atau [miftahhazmi@pu.go.id](mailto:miftahhazmi@pu.go.id)')

#st.subheader('Input Parameter Untuk Hujan Efektif', divider='blue')


col1, col2 = st.columns(2)

with col1:
    st.subheader('Input Parameter untuk Hujan Efektif', divider='blue')
    P = st.number_input("Masukkan Hujan Rencana (mm):", value=132.9)
    ARF = st.number_input("Masukkan Area Reduction Factor (ARF):", value=0.97)
# Menyediakan pilihan input untuk metode infiltrasi
    Metode_infiltrasi = st.radio('Pilih Metode Infiltrasi:', ['SCS-CN', 'Horton'])

    # Input untuk parameter-parameter berdasarkan pilihan metode infiltrasi
    if Metode_infiltrasi == 'SCS-CN':
        CN = st.number_input('Masukkan CN:', min_value=0, max_value=100, value=98, step=1)
        Im = st.number_input('Masukkan Im (mm):', min_value=0.0, value=5.0, step=0.1)
    elif Metode_infiltrasi == 'Horton':
        k = st.number_input('Masukkan k (mm/jam):', min_value=0.0, value=1.0, step=0.1)
        f0 = st.number_input('Masukkan f0 (%):', min_value=0, max_value=100, value=50, step=1) / 100
        fc = st.number_input('Masukkan fc (mm):', min_value=0.0, value=5.0, step=0.1)

    # Input lainnya
    input_method_dis = st.radio('Pilih Metode Distribusi:', ['PSA-007', 'ITB'])

    if input_method_dis == 'ITB':
        delta_jam_hujan = st.radio('Pilih Hujan Jam-Jaman (Jam):', ['1', '1/2', '1/3', '1/4', '1/6'])
        if delta_jam_hujan == '1':
            delta_jam_hujan = 1
        elif delta_jam_hujan == '1/2':
            delta_jam_hujan = 1/2
        elif delta_jam_hujan == '1/3':
            delta_jam_hujan = 1/3
        elif delta_jam_hujan == '1/4':
            delta_jam_hujan = 1/4
        elif delta_jam_hujan == '1/6':
            delta_jam_hujan = 1/6
        if delta_jam_hujan == 1:
            jumlah_jam_hujan = st.radio('Jumlah Jam Hujan (Jam):', [6, 12, 24])
        elif delta_jam_hujan != 1:
            jumlah_jam_hujan = st.radio('Jumlah Jam Hujan (Jam):', [6])
    elif input_method_dis == 'PSA-007':
        delta_jam_hujan = st.radio('Pilih Hujan Jam-Jaman (Jam):', [1])
        if delta_jam_hujan == 1:
            jumlah_jam_hujan = st.radio('Jumlah Jam Hujan (Jam):', [6, 12, 24])

    jumlah_data_hujan = jumlah_jam_hujan / delta_jam_hujan
with col2:
    st.subheader('Input Parameter HSS', divider='green')
    L = st.number_input("Masukkan Panjang Sungai (m):", value=28763)  # panjang main stream [m]
    st.write('Nilai Lc = 0.5 x L')
    Lc = 0.5 * L 
    S = st.number_input("Masukkan Nilai Slope Das (m/m):", value=0.006)  # slope
    A = st.number_input("Masukkan Luas DAS (km2):", value=52.297)  # Luas DTA [km2]
    ct = st.number_input("Masukkan nilai ct:", value=1)
    cp = st.number_input("Masukkan nilai cp:", value=1)
    tr = 1

    # Input lamanya waktu Hidrograf
    time_to_compute = st.number_input("Masukkan Lamanya waktu Hidrograf:", value=50) 
# # Menyediakan pilihan input untuk metode infiltrasi
# Metode_infiltrasi = st.radio('Pilih Metode Infiltrasi:', ['SCS-CN', 'Horton'])

# # Input untuk parameter-parameter berdasarkan pilihan metode infiltrasi
# if Metode_infiltrasi == 'SCS-CN':
#     CN = st.number_input('Masukkan CN:', min_value=0, max_value=100, value=98, step=1)
#     Im = st.number_input('Masukkan Im (mm):', min_value=0.0, value=5.0, step=0.1)
# elif Metode_infiltrasi == 'Horton':
#     k = st.number_input('Masukkan k (mm/jam):', min_value=0.0, value=1.0, step=0.1)
#     f0 = st.number_input('Masukkan f0 (%):', min_value=0, max_value=100, value=50, step=1)/100
#     fc = st.number_input('Masukkan fc (mm):', min_value=0.0, value=5.0, step=0.1)

# # Input lainnya

# input_method_dis = st.radio('Pilih Metode Distribusi:', ['PSA-007', 'ITB'])

# if input_method_dis == 'ITB':
#     delta_jam_hujan = st.radio('Pilih Hujan Jam-Jaman (Jam):', ['1', '1/2', '1/3', '1/4', '1/6'])
#     if delta_jam_hujan == '1':
#         delta_jam_hujan = 1
#     elif delta_jam_hujan == '1/2':
#         delta_jam_hujan = 1/2
#     elif delta_jam_hujan == '1/3':
#         delta_jam_hujan = 1/3
#     elif delta_jam_hujan == '1/4':
#         delta_jam_hujan = 1/4
#     elif delta_jam_hujan == '1/6':
#         delta_jam_hujan = 1/6
#     if delta_jam_hujan == 1:
#         jumlah_jam_hujan = st.radio('Jumlah Jam Hujan (Jam):', [6, 12, 24])
#     elif delta_jam_hujan != 1:
#         jumlah_jam_hujan = st.radio('Jumlah Jam Hujan (Jam):', [6])
# elif input_method_dis == 'PSA-007':
#     delta_jam_hujan = st.radio('Pilih Hujan Jam-Jaman (Jam):', [1])
#     if delta_jam_hujan == 1:
#         jumlah_jam_hujan = st.radio('Jumlah Jam Hujan (Jam):', [6, 12, 24])
        
# jumlah_data_hujan = jumlah_jam_hujan / delta_jam_hujan

# st.write('Input Hujan Rencana dan Area Reduction Factor')
# P = st.number_input("Masukkan Hujan Rencana (mm):", value=132.9)
# ARF = st.number_input("Masukkan Area Reduction Factor (ARF):", value=0.97)


# st.subheader('Input Parameter HSS', divider='blue')#Input Karakter DAS 
# L=st.number_input("Masukan Panjang Sungai (m):", value=28763) #panjang main stream [m]
# st.write('Nilai Lc = 0.5 x L')
# Lc = 0.5*L 
# S=st.number_input("Masukkan Nilai Slope Das (m/m):", value=0.006) #slope
# A = st.number_input("Masukkan Luas DAS (km2):", value=52.297)  #Luas DTA [km2]
# ct =st.number_input("Masukkan nilai ct:", value=1)
# cp =st.number_input("Masukkan nilai cp:", value=1)
# tr =1

# #Input lamanya waktu Hidrograf
# time_to_compute = st.number_input("Masukkan Lamanya waktu Hidrograph:", value=50)

# Tombol untuk memulai analisis
if st.button('Analisis Infiltrasi dan HSS'):
    T, distribusi, coef_dist = coef_dist_hujan(input_method_dis, jumlah_jam_hujan, delta_jam_hujan)
    if Metode_infiltrasi == "SCS-CN":
        Jam_ke, Hujan_Rencana, Hujan_Rencana_ARF, Infiltrasi, Hujan_Efektif, dfreffkum, dfreff, fig, fig2= infiltrasi_CN(P, ARF, CN, Im, jumlah_jam_hujan, distribusi, T)
    elif Metode_infiltrasi == "Horton":
        Jam_ke, Hujan_Rencana, Hujan_Rencana_ARF, Infiltrasi, Hujan_Efektif, dfreffkum, dfreff, fig, fig2= infiltrasi_Horton(P, ARF, k, f0, fc, jumlah_jam_hujan, distribusi, T)
    # Menampilkan hasil analisis
    st.subheader('Hasil Analisis Infiltrasi')
    #st.write(dfreffkum)
    #st.bokeh_chart(fig)
    st.write(dfreff)
    st.bokeh_chart(fig2)

    #if st.button('Analisis HSS'):
    ###############################################################
    ########################## Analisis HSS #######################
    ###############################################################

    ##############################
    #Kalkulasi Nilai Q/Qp dan T/Tp
    ##############################

    dt = delta_jam_hujan

    t1,q1,qp1,tp1=Qp_SCS(L,S,A,tr)
    t2,q2,qp2,tp2=Qp_Snyder(L,Lc,A,tr,ct,cp)
    t3,q3,qp3,tp3=HSS_ITB_1(ct,tr,cp,L,Lc,A)
    t4,q4,qp4,tp4=HSS_ITB_2(ct,tr,cp,L,A)

    # Membuat DataFrame
    data1 = {
        'Time SCS': t1,
        'SCS': q1,
    }
    data2 = {
        'Time Synder': t2,
        'Snyder': q2,
    }
    data3 = {
        'Time ITB1': t3,
        'ITB 1': q3,
    }
    data4 = {
        'Time ITB2': t4,
        'ITB 2': q4,
    }  
    df_TperTp_QperQp1 = pd.DataFrame(data1)
    #print(df_TperTp_QperQp1)
    df_TperTp_QperQp2 = pd.DataFrame(data2)
    #print(df_TperTp_QperQp2)
    df_TperTp_QperQp3 = pd.DataFrame(data3)
    #print(df_TperTp_QperQp3)
    df_TperTp_QperQp4 = pd.DataFrame(data4)
    #print(df_TperTp_QperQp4)

    # # Create a new plot with a title and axis labels
    # p = figure(title="Flow Over Time", x_axis_label='Time (Jam)', y_axis_label='Flow (m3/s / mm)', 
    #            x_range=(-3, time_to_compute+3))

    # # Add lines for each dataset
    # line1 = p.line(t1, q1, legend_label='SCS', line_width=2, color='blue')
    # line2 = p.line(t2, q2, legend_label='Snyder', line_width=2, color='green')
    # line3 = p.line(t3, q3, legend_label='ITB 1', line_width=2, color='red')
    # line4 = p.line(t4, q4, legend_label='ITB 2', line_width=2, color='orange')

    # # Customize the legend
    # p.legend.title = 'Methods'
    # p.legend.location = 'top_right'
    # p.legend.click_policy = 'hide'

    # # Show the grid
    # p.grid.visible = True

    # # Show the plot
    # show(p)

    # membuat T dan Q interpolasi
    ti1=np.arange(min(t1),time_to_compute+dt,dt)
    qi1=np.interp(ti1,t1,q1)

    ti2=np.arange(min(t2),time_to_compute+dt,dt)
    qi2=np.interp(ti2,t2,q2)

    ti3=np.arange(min(t3),time_to_compute+dt,dt)
    qi3=np.interp(ti3,t3,q3)

    ti4=np.arange(min(t4),time_to_compute+dt,dt)
    qi4=np.interp(ti4,t4,q4)

    ti=np.arange(min(t1),time_to_compute+dt,dt)

    # membuat tabel Q dan P HSS
    Table_T_Q_SCS=pd.DataFrame({'Jam ke -':t1,'Q SCS':q1})
    Table_T_Q_Snyder=pd.DataFrame({'Jam ke -':t2,'Q Snyder':q2})
    Table_T_Q_ITB1=pd.DataFrame({'Jam ke -':t3,'Q ITB1':q3})
    Table_T_Q_ITB2=pd.DataFrame({'Jam ke -':t4,'Q ITB2':q4})

    # Membuat Tabel Time Peak dan Q peak
    Table_Tp_Qp = pd.DataFrame({
        'Time Peak (Jam)': [tp1, tp2, tp3, tp4],
        'Q Peak (m3/s / mm)': [qp1, qp2, qp3, qp4]}, 
        index=['SCS', 'Snyder', 'ITB 1', 'ITB 2'])

    # Membuat DataFrame
    data = {
        'Time (Jam ke-)': ti1,
        'SCS (m3/s / mm)': qi1,
        'Snyder (m3/s / mm)': qi2,
        'ITB 1 (m3/s / mm)': qi3,
        'ITB 2 (m3/s / mm)': qi4
    }

    df_Q_T_int = pd.DataFrame(data)

    # Menampilkan tabel
    print('Tabel Nilai Tp dan Qp setiap metode')
    print(Table_Tp_Qp)

    print('Tabel Nilai T dan Q setiap metode HSS yang telah Interpolasi per delta t')
    print(df_Q_T_int)

    # Create a new plot with a title and axis labels
    p = figure(title="Interpolated Data", x_axis_label='Time (Jam ke-)', y_axis_label='Flow (m3/s / mm)')

    # Add lines for each dataset
    line1 = p.line(ti, qi1, legend_label='SCS', line_width=2, color='blue')
    line2 = p.line(ti, qi2, legend_label='Snyder', line_width=2, color='green')
    line3 = p.line(ti, qi3, legend_label='ITB 1', line_width=2, color='red')
    line4 = p.line(ti, qi4, legend_label='ITB 2', line_width=2, color='orange')

    # Customize the legend
    p.legend.title = 'Methods'
    p.legend.location = 'top_right'
    p.legend.click_policy = 'hide'
    p_hss=p
    # Show the plot
    show(p)

    ##############################
    #Kalkulasi HSS
    ##############################


    # Fungsi untuk menghitung Q dan V
    def calculate_Q_and_V_wrapper(p, time_step_hours, Q_qp, time_to_compute):
        return calculate_Q_and_V(p, time_step_hours, Q_qp, time_to_compute)

    # Data input
    p = Hujan_Efektif
    time_step_hours = delta_jam_hujan
    Q_qp1 = qi1
    Q_qp2 = qi2
    Q_qp3 = qi3
    Q_qp4 = qi4

    Q_peak1, t_peak1, V_total1, t_peak_V1,T1,Qtot1,V_cum1 =  calculate_Q_and_V(p,time_step_hours, Q_qp1, time_to_compute)
    Q_peak2, t_peak2, V_total2, t_peak_V2,T2,Qtot2,V_cum2 =  calculate_Q_and_V(p,time_step_hours, Q_qp2, time_to_compute)
    Q_peak3, t_peak3, V_total3, t_peak_V3,T3,Qtot3,V_cum3 =  calculate_Q_and_V(p,time_step_hours, Q_qp3, time_to_compute)
    Q_peak4, t_peak4, V_total4, t_peak_V4,T4,Qtot4,V_cum4 =  calculate_Q_and_V(p,time_step_hours, Q_qp4, time_to_compute)


    # Membuat p_bar dengan menambahkan nol hingga panjangnya sama dengan T
    p_bar = np.concatenate((p, np.zeros((len(T1) - len(p)))))
    Infiltrasi_bar = np.concatenate((Infiltrasi, np.zeros((len(T1) - len(Infiltrasi)))))
    plt.figure(figsize=(12, 6))

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Membuat HSS
    ax1.plot(T1, Qtot1[:len(T1)], marker='o', label='SCS')
    ax1.plot(T2, Qtot2[:len(T2)], marker='o', label='Snyder')
    ax1.plot(T3, Qtot3[:len(T3)], marker='o', label='ITB-1')
    ax1.plot(T4, Qtot4[:len(T4)], marker='o', label='ITB-2')
    ax1.set_xlabel('T (Jam)')
    ax1.set_ylabel('Qtot (m3/det)')
    ax1.set_title('Hubungan antara T dan Q serta p')

    # Membuat bar hujan efektif
    ax2 = ax1.twinx()
    ax2.bar(T1, p_bar, alpha=0.3, label='Hujan Efektif (mm)', color='orange')
    ax2.set_ylabel('Hujan Efektif(mm)')
    ax2.set_ylim(0, 200)
    ax2.invert_yaxis()  # Membalikkan arah y-axis
    # Membuat bar infiltrasi

    ax3 = ax1.twinx()
    ax3.bar(T1, Infiltrasi_bar, alpha=0.3, label='Infiltrasi (mm)', color='r')
    ax3.set_ylabel('Hujan Efektif(mm)')
    ax3.set_ylim(0, 200)
    ax3.invert_yaxis() 

    #fig.legend(loc='upper right')
    # Menyatukan legend dari semua sumbu
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    lines3, labels3 = ax3.get_legend_handles_labels()
    ax1.legend(lines + lines2 + lines3, labels + labels2 + labels3, loc='upper right')
    plt.grid(True)
    plt.show()
    fig1=fig
    

    # Tabel Time Peak dan Q Peak
    Table_Tp_Qp_p = pd.DataFrame({
        'Time Peak (jam)': [t_peak1, t_peak2, t_peak3, t_peak4],
        'Q Peak (m3/s)': [Q_peak1, Q_peak2, Q_peak3, Q_peak4]}, 
        index=['SCS', 'Snyder', 'ITB 1', 'ITB 2'])
    print(Table_Tp_Qp_p)

    # Plot hubungan antara T dan Vtot
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(T1[:-1], V_cum1[:-1], marker='o', label='SCS')
    ax1.plot(T2[:-1], V_cum2[:-1], marker='o', label='Snyder')
    ax1.plot(T3[:-1], V_cum3[:-1], marker='o', label='ITB-1')
    ax1.plot(T4[:-1], V_cum4[:-1], marker='o', label='ITB-2')
    ax1.set_xlabel('T (Jam)')
    ax1.set_ylabel('Volume (m3)')
    ax1.set_title('Hubungan antara V dan Q serta p')

    # Membuat bar hujan efektif
    ax2 = ax1.twinx()
    ax2.bar(T1, p_bar, alpha=0.3, label='Hujan Efektif (mm)', color='orange')
    ax2.set_ylabel('Hujan Efektif(mm)')
    ax2.set_ylim(0, 200)
    ax2.invert_yaxis()  # Membalikkan arah y-axis
    # Membuat bar infiltrasi

    ax3 = ax1.twinx()
    ax3.bar(T1, Infiltrasi_bar, alpha=0.3, label='Infiltrasi (mm)', color='r')
    ax3.set_ylabel('Hujan Efektif(mm)')
    ax3.set_ylim(0, 200)
    ax3.invert_yaxis() 

    #fig.legend(loc='upper right')
    # Menyatukan legend dari semua sumbu
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    lines3, labels3 = ax3.get_legend_handles_labels()
    ax1.legend(lines + lines2 + lines3, labels + labels2 + labels3, loc='upper right')
    plt.grid(True)
    plt.show()
    fig2=fig
    
    data = {
        'Time (Jam ke-)': T1,
        'SCS (m3/s)': Qtot1[:len(T1)],
        'Snyder (m3/s)': Qtot2[:len(T1)],
        'ITB 1 (m3/s)': Qtot3[:len(T1)],
        'ITB 2 (m3/s)': Qtot4[:len(T1)]
    }

    df_Q_T = pd.DataFrame(data)

    # Menampilkan tabel
    print('Tabel Nilai T dan Q setiap metode')
    print(df_Q_T)
    # Menampilkan hasil Analisis di Streamlit
    st.subheader('Hasil Analisis HSS')
    #st.write(dfreffkum)
    #st.bokeh_chart(fig)
    st.bokeh_chart(p_hss)
    st.write('Tabel Nilai Tp dan Qp setiap metode')
    st.write(Table_Tp_Qp)
    st.write('Tabel Nilai T dan Q setiap metode HSS yang telah Interpolasi per delta t=1 Jam')
    st.write(df_Q_T_int)
    st.pyplot(fig1)
    st.write(Table_Tp_Qp_p)
    #st.pyplot(fig2)
    st.write(df_Q_T)    
    #st.pyplot(p)
