import random
import pandas as pd
import copy
from math import exp
import time as sure

#Algoritma_degerleri
#-----------------------------------------------------------------
T = 5000 #Sıcaklık
ao = 0.99 #Soğuma Oranı
ds = 10000 #İterasyon Sayısı
g_s = 0 #Gant şeması oluşturulacaksa=1, oluşturulmayacaksa=0
i_g = 0 #Her iterasyonda çıktılar görünecekse=1, görünmeyecekse=0 - Aktif bırakmak performansı olumsuz etkileyebilir
#-----------------------------------------------------------------

b_s = sure.time() #calisma_suresini_hesaplatmak_icin
e = exp(1)

#tavlama_benzetiminde_kullanmak_icin_bir_sezgisel_algoritma
def sezgisel(il, ciktilar): #il-is_listesi
    r = 0.5
    a = random.random()
    if ciktilar == 1:
        print("\n**************************************************\n")
        print("Sezgisel Alogritma Çıktıları:\n")
        print('a = ', a, '\nr = ', r)
    m1, m2 = random.sample(range(1, len(il)+1), 2)
    if a > r:
        j1 = random.sample(il[m1 - 1][1], 1)[0]
        j2 = random.sample(il[m2 - 1][1], 1)[0]
        idx1 = il[m1 - 1][1].index(j1)
        idx2 = il[m2 - 1][1].index(j2)
        il[m1 - 1][1].remove(j1)
        il[m2 - 1][1].remove(j2)
        il[m1 - 1][1].insert(idx2, j2)
        il[m2 - 1][1].insert(idx1, j1)

        if ciktilar == 1:
            print("\na > r :")
            print(m1, "numaralı makinede bulunan", j1[0], 'numaralı iş,',
                  m2, "numaralı makinede bulunan", j2[0], "numaralı iş ile değiştirildi.")
            print("Çizelgeleme planı şu şekilde güncellendi:\n")
    else:
        j1 = random.sample(il[m1 - 1][1], 1)[0]
        if len(il[m1-1][1]) > 1:
            idx1 = il[m1 - 1][1].index(j1)
            il[m1 - 1][1].remove(j1)
            il[m2 - 1][1].insert(idx1, j1)
            if ciktilar == 1:
                print('\nr > a :')
                print(m1, "numaralı makinede bulunan", j1[0], "numaralı iş,", m2, "numaralı makineye aktarıldı.")
                print("Çizelgeleme planı şu şekilde güncellendi:\n")
        else:
            if ciktilar == 1:
                print('\nr > a :')
                print(m1, "numaralı makinede yalnızca bir iş olduğundan aktarma yapılamadı, algoritma devam ediyor.\n")

    return il

def spt(makine_sayisi, is_sayisi, is_listesi):
    spt_ciktisi = list()#makinedeki_isler_listesi
    for i in range(makine_sayisi):
        spt_ciktisi.append([i + 1, []])
    #spt_kullanarak_makinelere_is_atama
    for i in range(is_sayisi):
        spt_min = min(is_listesi)
        spt_ciktisi[i % m_s][1].append([spt_min[1], spt_min[0]])
        is_listesi.remove(spt_min)
    return spt_ciktisi

def gecikmeleri_hesapla(is_listesi, ciktilar):
    time = 0
    gm = int() #makinedeki_gecikme
    gt_inner = int() #total_gecikme
    if ciktilar == 1: print("Makinelerdeki gecikme süreleri:")
    for i in is_listesi:
        for j in i[1]:
            time += j[1][0]
            gm += max(0, time - j[1][1])
        if ciktilar == 1: print(is_listesi.index(i) + 1, "---->", gm)
        gt_inner += gm
        gm = 0
        time = 0
    if ciktilar == 1: print("Toplam gecikme değeri =", gt_inner)
    return gt_inner

def gannt(is_listesi):
    islem_araliklari = list()
    lg = list()
    for i in is_listesi:
        time = 0
        for j in i[1]:
            lg.append([j[0], time, time + j[1][0]])
            time += j[1][0]
        islem_araliklari.append(lg)
        lg = []

    for i in islem_araliklari:
        print('   0 ', sep='', end='')
        for j1 in i:
            if j1[2] <10:
                x2 = 1
            elif 9 < j1[2] < 100:
                x2 = 2
            else:
                x2 = 3
            for m in range(j1[2] - j1[1] - x2):
                print(" ", end='')
            print(j1[2], sep='', end='')

        print('')
        if islem_araliklari.index(i) < 9:
            print(islem_araliklari.index(i) + 1, '  |', end='', sep='')
        elif 8 < islem_araliklari.index(i) < 99:
            print(islem_araliklari.index(i) + 1, ' |', end='', sep='')
        else:
            print(islem_araliklari.index(i) + 1, '|', end='', sep='')

        for j in i:
            if 9 < j[0] < 100:
                x = 2
            elif j[0] < 10:
                x = 1
            else:
                x = 3

            if int((j[2]-j[1])/2) == (j[2] - j[1])/2:
                for m in range(int((j[2]-j[1])/2) - x):
                    print("■", end='')
                print(j[0], sep='', end='')
                for n in range(int((j[2]-j[1])/2) - 1):
                    print("■", end='')
            else:
                for m in range(int((j[2]-j[1])/2) - x):
                    print("■", end='')
                print(j[0], sep='', end='')
                for n in range(int((j[2]-j[1])/2)):
                    print("■", end='')
            print('|', sep='', end='')
        print('\n')

#excel_uzerinden_is_ve_makine_sayilarini_cekme
mveis = pd.read_excel(io='veriler.xlsx', usecols="G:G", nrows=2, header=None)
m_s = mveis.iloc[0, 0] #makine_sayisi
i_s = mveis.iloc[1, 0] #is_sayisi
is_tablosu = pd.read_excel(io='veriler.xlsx', usecols="A:C", skiprows= 1, nrows = i_s, header=None)

#pandas_formatini_listeye_cevirme
lt = list()
for i in is_tablosu:
    lt.append(list(is_tablosu.get(i)))

#islerin_oldugu_bir_dict_degiskeni_tanimlama
isler_dict = dict()
for i in lt[0]:
    isler_dict[i] = (lt[1][i-1], lt[2][i-1])

spt_is_l = list() #sptde_kullanmak_icin_is_listesi
for i in isler_dict:
    spt_is_l.append([isler_dict.get(i), i])

#makinedeki_isler_listesinin_olusturulmasi
mi_l = spt(m_s, i_s, spt_is_l)

print("\n**************************************************\n")
if i_g == 1:
    print("Başlangıç çözümü;")
z = gecikmeleri_hesapla(mi_l, i_g) #iterasyon_sonunda_kabul_edilen_deger
if i_g != 1:
    print("Başlangıç z değeri =", z)
eicl = [(z, mi_l)] #iterasyonlardaki_en_iyi_cozumu_tutan_liste

while ds > 0:
    mi2_l = copy.deepcopy(mi_l)  # makinedeki_isler_backup
    sezgisel(mi2_l, i_g)
    if i_g == 1:
        for i in mi2_l:#sezgisel_algoritma_ciktisi
            print(i[0], end=' --> | ')
            for j in i[1]:
                print(j[0], end=' | ')
            print("")
        print("")

    #makineler_icin_ve_toplam_gecikmeler_hesaplaniyor
    gt = gecikmeleri_hesapla(mi2_l, i_g)

    #tavlama_benzetimi_algoritmasina_gore_yeni_sonuc_seciliyor
    if i_g == 1: print("Mevcut z değeri =", z)
    if gt <= z:
        z = gt
        mi_l = copy.deepcopy(mi2_l)
        if i_g == 1: print('\nİyileşme var, yeni en iyi sonuç =', z, '\n')
    else:
        k_ol = e**((z - gt) / T)#kabul_olasiligi
        r2 = random.random()
        if i_g == 1:
            print("\nKabul olasılığı hesaplanmalı:")
            print('Rassal sayı =', r2)
            print('Kabul olasılığı değeri =', k_ol)
        if r2 < k_ol:
            eicl.append((z, mi2_l))
            z = gt
            mi_l = copy.deepcopy(mi2_l)
            if i_g == 1: print('\nOlasılık kabul edildi, yeni z değeri =', z, '\n')
        else:
            if i_g == 1: print('\nOlasılık reddedildi. Z değeri değişmedi.\n')
            mi2_l = copy.deepcopy(mi_l)
            pass
    T = T*ao
    ds -= 1
    if i_g == 1: print('Kalan iterasyon sayısı =', ds)

print("\n\n\nÇIKTILAR:\n------------------------")
print("Nihai z değeri =", z)
print("------------------------")

print("Nihai z değerinin çizelgesi:")
for i in mi_l:
    print(i[0], end=' --> | ')
    for j in i[1]:
        print(j[0], end=' | ')
    print("")

if z > min(eicl)[0]:
    print("\n------------------------\nGeçmiş iterasyonlarda nihai sonuçtan daha iyi bir değer bulunuyor.")
    print("İterasyonlar sonucunda bulunan eniyi z değeri =", min(eicl)[0])
    print("------------------------")
    print("Bulunan eniyi z değeri için makine çizelgesi:")
    for i in min(eicl)[1]:
        print(i[0], end=' --> | ')
        for j in i[1]:
            print(j[0], end=' | ')
        print("")
else:
    print("\nNihai z değeri yapılan iterasyonlar arasında bulunan en iyi sonuç.")

if g_s == 1:
    print("\nBulunan eniyi çözüme ait gantt şeması:")
    gannt(min(eicl)[1])
elif g_s == 0:
    print("\nİsteğiniz doğrultusunda gantt şeması oluşturulmadı.")
else:
    print("\nGeçersiz g_s değeri, şema oluşturulmayacak.")
    pass

print("\n", "Bu kodun tamamlanması", sure.time() - b_s, "saniye sürdü.")