import tkinter as tk
from tkinter import Tk

# pencere oluşturma
pencere = Tk()

# pencere başlığı verme
pencere.title("LİMAN OTOMASYONU")

# pencere boyutlandırma
pencere.attributes('-fullscreen', True)


# pencereden çıkış tuşu için fonksiyon tanımlama
def kapat(event):
    pencere.destroy()


# çıkış tuşunu esc olarak ayarlama
pencere.bind("<Escape>", kapat)

# menüye saniye sayacı ekleme
saniye_sayaci = 0


def update_saniye():
    global saniye_sayaci
    saniye_sayaci += 1
    sayac.config(text=f"Saniye: {saniye_sayaci}")

    tir_gelisi()
    gemi_gelisi()
    istifleme()
    yuklenmis_gemi()

    pencere.after(1000, update_saniye)  # Her 1 saniyede bir günceller


sayac = tk.Label(pencere, text="0", font=("Times New Roman", 12), fg="black")
sayac.grid(row=0, column=0, padx=5, pady=0)


# tir için sınıf oluşturma
class Tir:
    with open('olaylar.csv', 'r') as dosya:
        # Dosya okunur ve her satır eleman olarak listeye eklenir
        tir_liste1 = [satir.split(",") for satir in dosya.readlines()]
        # Başlıklar olan ilk eleman listeden atılır
        tir_liste1.pop(0)
        # Maliyet kısmının sonunda oluşan '\n' ifadesinden kurtulma
        for i in tir_liste1:
            i[6] = i[6][:-1]

    # tır listesine erişim fonskiyonu
    def tir_liste(listet=tir_liste1):
        return listet

    # tır bilgisi sorgulama fonksiyonu
    def tir_sorgulama(plaka, bilgiler=tir_liste1):
        tbilgiler = {}
        for liste in bilgiler:
            if plaka in liste:
                print(liste)
                tbilgiler['Plaka'] = str(plaka)
                tbilgiler['Yükün gideceği ülke'] = liste[2]
                tbilgiler['20 tonluk konteynır adet'] = liste[3]
                tbilgiler['30 tonluk konteynır adet'] = liste[4]
                tbilgiler['Yük miktarı'] = liste[5]
                tbilgiler['Maliyet'] = liste[6]
                break
        # plakasına göre sorgulanan tır için sözlük oluşturulur
        # sözlük menüye yazılır
        label_listesi = []  # Label'ları tutacak liste
        row_index = 5  # Başlangıç satırı
        for anahtar, deger in tbilgiler.items():
            yazi = f"{anahtar} : {deger}"
            label = tk.Label(pencere, text=yazi)
            label.grid(row=row_index, column=0, padx=0, pady=0)
            label_listesi.append(label)
            row_index += 1

    # tirları geliş zamanına göre bir sözlüğe ekleme
    def gelis_zamani_t(liste=tir_liste()):
        gelmis_tir = {}

        for tirlar in liste:
            if tirlar[0] in gelmis_tir:
                gelmis_tir[tirlar[0]].append(tirlar)
            else:
                gelmis_tir[tirlar[0]] = [tirlar]
        sirali_tir_liste = {}
        # sözlüğe eklenmiş tırların aynı zamanda gelenlerini
        # sorted ile plaka numarasına göre küçükten büyüğe sıralama

        for anahtar, deger in gelmis_tir.items():
            sirali_deger = sorted(deger, key=lambda x: int(((x[1]).split("_"))[-1]))
            sirali_tir_liste[anahtar] = sirali_deger

        return sirali_tir_liste


class Gemi:
    with open('gemiler.csv', 'r') as dosya:
        # Dosya okunur ve her satır eleman olarak listeye eklenir
        gemi_liste = [satir.split(",") for satir in dosya.readlines()]
        # Başlıklar olan ilk eleman listeden atılır
        gemi_liste.pop(0)
        # Maliyet kısmının sonunda oluşan '\n' ifadesinden kurtulma
        for i in gemi_liste:
            i[3] = i[3][:-1]

    def gemi_liste(listeg=gemi_liste):
        return listeg

    # gemi bilgisi sargulama fonksiyonu
    def gemi_sorgulama(plaka, bilgiler=gemi_liste()):
        gbilgiler = {}
        for satir in bilgiler:
            if plaka == satir[1]:
                gbilgiler['Gemi Adı'] = str(plaka)
                gbilgiler['Yükün gideceği ülke'] = satir[3]
                gbilgiler['Kapasite'] = satir[2]
                break

        # sorgulanan gemi numarasına göre verileri yazdırır
        label_listesi = []  # Label'ları tutacak liste
        row_index = 5  # Başlangıç satırı
        for anahtar, deger in gbilgiler.items():
            yazi = f"{anahtar} : {deger}"
            label = tk.Label(pencere, text=yazi)
            label.grid(row=row_index, column=1, padx=0, pady=0)
            label_listesi.append(label)
            row_index += 1

        # gemileri geliş zamanına göre bir sözlüğe ekleme

    def gelis_zamani_g(liste=gemi_liste()):
        gelmis_gemi = {}

        for gemiler in liste:
            if gemiler[0] in gelmis_gemi:
                gelmis_gemi[gemiler[0]].append(gemiler)
            else:
                gelmis_gemi[gemiler[0]] = [gemiler]

        return gelmis_gemi

    def ulkeye_gore_gemiler(liste=gemi_liste()):
        ulkeye_gore_gemiler = {}
        for gemi in liste:
            if gemi[3] in ulkeye_gore_gemiler:
                ulkeye_gore_gemiler[gemi[3]].append([gemi[1], gemi[2]])
            else:
                ulkeye_gore_gemiler[gemi[3]] = [[gemi[1], gemi[2]]]
        return ulkeye_gore_gemiler

    def gemi_yukleme(liste=Tir.tir_liste()):
        yukleme = {}
        for yuk in liste:
            if yuk[0] in yukleme:
                yukleme[yuk[0]].append([yuk[2], yuk[5]])
            else:
                yukleme[yuk[0]] = [[yuk[2], yuk[5]]]

        return yukleme


def tir_gelisi():
    labels = []
    global tir_label_frame
    global tir_canvas
    global tir_label_inside

    # Tir modülünden liste al
    liste = Tir.gelis_zamani_t()

    for anahtart, degert in liste.items():
        if int(anahtart) == saniye_sayaci:
            for tirlar in degert:
                text = tirlar
                label = tk.Label(tir_label_inside, text=text, font=("Times New Roman", 15))
                label.pack()
                labels.append(label)
                tir_label_inside.update_idletasks()

                # Canvas içeriğinin boyutunu güncelle
                tir_canvas.update_idletasks()
                tir_canvas.config(scrollregion=tir_canvas.bbox("all"))


# Tir listesinin olacağı label frame oluşturma
tir_label_frame = tk.LabelFrame(pencere, text="Tır Listesi")
tir_label_frame.grid(row=1, column=0, padx=10, pady=10)

# kaydırma çubuğu oluşturma
tir_scrollbar = tk.Scrollbar(tir_label_frame)
tir_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# kaydırma çubuğu ile birlikte bir kanvas oluşturma
tir_canvas = tk.Canvas(tir_label_frame, yscrollcommand=tir_scrollbar.set)
tir_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

tir_scrollbar.config(command=tir_canvas.yview)

# kanvasın içine pencere için çerçeve oluşturulur
tir_label_inside = tk.Frame(tir_canvas)
tir_canvas.create_window((0, 0), window=tir_label_inside, anchor=tk.NW)


def istifleme():
    ilabels = []
    yuk_miktari = 0

    # Tir modülünden liste al
    liste = Tir.gelis_zamani_t()

    for anahtar, deger in liste.items():
        if int(anahtar) == saniye_sayaci:
            for d in deger:
                yuk = d[5]
                yuk_miktari += int(d[5])
                yer = d[2]
                text = f"Yük: {yuk} Gideceği Yer: {yer}"
                label = tk.Label(istif1_label_inside, text=text, font=("Times New Roman", 13))
                label.pack()
                ilabels.append(label)
                istif1_label_inside.update_idletasks()

                # Canvas içeriğinin boyutunu güncelle
                istif1_canvas.update_idletasks()
                istif1_canvas.config(scrollregion=istif1_canvas.bbox("all"))

                # En üstteki etiketi göster
                istif1_canvas.yview_moveto(0)


istif1_label_frame = tk.LabelFrame(pencere, text="İstif Alanı 1")
istif1_label_frame.grid(row=2, column=0, padx=10, pady=10)
istif1_label_frame.configure(width=300, height=100)

istif1_scrollbar = tk.Scrollbar(istif1_label_frame)
istif1_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

istif1_canvas = tk.Canvas(istif1_label_frame, yscrollcommand=istif1_scrollbar.set)
istif1_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

istif1_scrollbar.config(command=istif1_canvas.yview)

istif1_label_inside = tk.Frame(istif1_canvas)
istif1_canvas.create_window((0, 0), window=istif1_label_inside, anchor=tk.NW)

istif2_label_frame = tk.LabelFrame(pencere, text="İstif Alanı 2")
istif2_label_frame.grid(row=2, column=1, padx=10, pady=10)
istif2_canvas = tk.Canvas(istif2_label_frame)
istif2_scrollbar = tk.Scrollbar(istif2_label_frame, orient=tk.VERTICAL, command=istif2_canvas.yview)
istif2_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
istif2_canvas.config(yscrollcommand=istif2_scrollbar.set)
istif2_label_inside = tk.Label(istif2_label_frame, text="")
istif2_label_inside.pack(padx=100, pady=100)


def gemi_gelisi():
    labelg = []
    global gemi_label_frame
    global gemi_canvas
    global gemi_label_inside

    # Tir modülünden liste al
    liste = Gemi.gelis_zamani_g()

    for anahtarg, degerg in liste.items():
        if int(anahtarg) == saniye_sayaci:
            for gemiler in degerg:
                text = gemiler
                label = tk.Label(gemi_label_inside, text=text, font=("Times New Roman", 15))
                label.pack()
                labelg.append(label)
                gemi_label_inside.update_idletasks()

                # Canvas içeriğinin boyutunu güncelle
                gemi_canvas.update_idletasks()
                gemi_canvas.config(scrollregion=gemi_canvas.bbox("all"))


# Gemi listesinin olacağı label frame oluşturma
gemi_label_frame = tk.LabelFrame(pencere, text="Limana Gelen Gemi Listesi")
gemi_label_frame.grid(row=1, column=1, padx=10, pady=10)

# kaydırma çubuğu oluşturma
gemi_scrollbar = tk.Scrollbar(gemi_label_frame)
gemi_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# kaydırma çubuğu ile birlikte bir kanvas oluşturma
gemi_canvas = tk.Canvas(gemi_label_frame, yscrollcommand=gemi_scrollbar.set)
gemi_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

gemi_scrollbar.config(command=gemi_canvas.yview)

# kanvasın içine pencere için çerçeve oluşturulur
gemi_label_inside = tk.Frame(gemi_canvas)
gemi_canvas.create_window((0, 0), window=gemi_label_inside, anchor=tk.NW)


def gemi_yuklenisi():
    gemi_yukleri = {}
    alinan_yukler = set()

    # Tir modülünden liste al
    yuk_liste = Tir.tir_liste()
    gemi_liste = Gemi.gemi_liste()

    for gemi in gemi_liste:
        gemi_adi = gemi
        gemi_kapasite = int(gemi[2])
        yuklenen_miktar = 0

        for yuk in yuk_liste:
            yuk_id = yuk[1]
            if yuk_id not in alinan_yukler and yuk[2] == gemi[3]:
                yuk_miktari = int(yuk[5])
                if yuklenen_miktar + yuk_miktari < gemi_kapasite:
                    yuklenen_miktar += yuk_miktari
                    alinan_yukler.add(yuk_id)
                elif yuklenen_miktar + yuk_miktari >= gemi_kapasite:
                    if str(gemi_adi) not in gemi_yukleri:
                        gemi_yukleri[str(gemi_adi)] = [yuklenen_miktar, yuk[0]]
                    break

    return gemi_yukleri


def yuklenmis_gemi():
    labelgy = []
    global ygemi_label_frame
    global ygemi_canvas
    global ygemi_label_inside

    # Tir modülünden liste al
    liste = gemi_yuklenisi()

    for anahtarg, degerg in liste.items():
        if int(degerg[1]) == saniye_sayaci:
            text = f"Sn: {degerg[1]} {anahtarg} Yük: {degerg[0]}"
            label = tk.Label(ygemi_label_inside, text=text, font=("Times New Roman", 15))
            label.pack()
            labelgy.append(label)
            ygemi_label_inside.update_idletasks()

            # Canvas içeriğinin boyutunu güncelle
            ygemi_canvas.update_idletasks()
            ygemi_canvas.config(scrollregion=ygemi_canvas.bbox("all"))


# Gemi listesinin olacağı label frame oluşturma
ygemi_label_frame = tk.LabelFrame(pencere, text="Yüklenmiş Gemi Listesi")
ygemi_label_frame.grid(row=1, column=2, padx=10, pady=10)

# kaydırma çubuğu oluşturma
ygemi_scrollbar = tk.Scrollbar(ygemi_label_frame)
ygemi_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# kaydırma çubuğu ile birlikte bir kanvas oluşturma
ygemi_canvas = tk.Canvas(ygemi_label_frame, yscrollcommand=ygemi_scrollbar.set)
ygemi_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

ygemi_scrollbar.config(command=ygemi_canvas.yview)

# kanvasın içine pencere için çerçeve oluşturulur
ygemi_label_inside = tk.Frame(ygemi_canvas)
ygemi_canvas.create_window((0, 0), window=ygemi_label_inside, anchor=tk.NW)

# plakasına göre tır bilgisi sorgulamak
tir_sorgula = tk.Entry()
tir_sorgula.grid(row=4, column=0, padx=00, pady=00)
tir_sorgulama_butonu = tk.Button(text="Tır Bilgisi Sorgula", command=lambda: Tir.tir_sorgulama(tir_sorgula.get()))
tir_sorgulama_butonu.grid(row=3, column=0, padx=10, pady=10)

# numarasına göre gemi bilgisi sorgulamak
gemi_sorgula = tk.Entry()
gemi_sorgula.grid(row=4, column=1, padx=00, pady=00)
gemi_sorgulama_butonu = tk.Button(text="Gemi Bilgisi Sorgula", command=lambda: Gemi.gemi_sorgulama(gemi_sorgula.get()))
gemi_sorgulama_butonu.grid(row=3, column=1, padx=10, pady=10)

# fonksiyonlar çağırılır
update_saniye()

pencere.mainloop()
