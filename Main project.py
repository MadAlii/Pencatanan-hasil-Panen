# Projek.py

import tkinter as tk
from PIL import ImageTk, Image
import locale, psycopg2
from tabulate import tabulate
from datetime import datetime

#CONNECTION DATABASE POSTGRESQP
def database(tabel,akses, xxx): 
    
    conn_string = "host='localhost' port=5432 dbname='proalgo' user='postgres' password='QWERTY30'"

    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        query = f"SELECT * FROM {tabel}"
        cursor.execute(query)
        rows = cursor.fetchall()
        dt = [list(sublist) for sublist in rows] # list kompresion
        ii = len(dt)

        def tmbhLOG(xxx):
            Id = ii+1
            query = f"INSERT INTO {tabel} (id_user, username, pasword) VALUES (%s, %s, %s)"
            values = (Id, xxx[0], xxx[1])
            cursor.execute(query, values)
            conn.commit()
            return [Id,xxx[0],xxx[1]]
        
        def tmbhdt(xxx):
            Id = ii+1
            query = f"INSERT INTO {tabel} (id_data, Tanggal, Waktu, Berat_Gabah, Harga_Gudang, Total_Penghasilan, Penghasilan_Pemilik, Jumlah_Pekerja, Upah_Pekerja, id_user) VALUES (%s, %s, %s,%s, %s, %s, %s,%s, %s, %s)"
            values = (Id, xxx[0], xxx[1], xxx[2], xxx[3], xxx[4], xxx[5], xxx[6], xxx[7], xxx[8])
            cursor.execute(query, values)
            conn.commit()
        if akses == 1:
            return tmbhLOG(xxx)
        elif akses == 2:
            tmbhdt(xxx)
        elif akses == 3:
            return dt

    except (Exception, psycopg2.Error) as error:
        print("Koneksi gagal:", error)
    finally:

        if cursor:
            cursor.close()
        if conn:
            conn.close()

    
#============================================================================================================================================


#MEMBUAT TAMPILAN TKINTER
root = tk.Tk()

width, height = root.winfo_screenwidth(), root.winfo_screenheight()

root.geometry(f"{width}x{height-70}")

image = Image.open("bb.jpg")

image = image.resize((width, height), Image.ANTIALIAS)

background_image = ImageTk.PhotoImage(image)



def log():
    global background_label
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    datalog = database("login",3,"") 
    def get_input():
        input1 = entry1.get() 
        input2 = entry2.get()
        usernm = False
        pasww = False
        for i in datalog:
            if i[1] == input1:
                usernm = True
                if i[2] == input2:
                    pasww = True
                    break
                else:
                    break
        if usernm:
            if pasww:
                for widget in root.winfo_children():
                    widget.destroy()
                menu(i)
            else:
                label10 = tk.Label(root, text="Password Salah!!! ",width=24, height= 2,font=("Arial", 12),fg ="red",bg="black", anchor="w")
                label10.place(relx=0.42, y=height//2-155)
        else:
            if pasww == False:
                label10 = tk.Label(root, text="Username dan Password",width=24,font=("Arial", 12),fg ="red",bg="black", anchor="w")
                label10.place(relx=0.42, y=height//2-155)
                label11 = tk.Label(root, text="Tidak Terdaftar!!!",width=24,font=("Arial", 12),fg ="red",bg="black", anchor="w")
                label11.place(relx=0.42, y=height//2-137)

    def get_input2():
        input1 = entry1.get()
        input2 = entry2.get()
        username = True
        for i in datalog:
            if input1 == i[1]:
                username = False
                break
        if username:
            if len(input1) >= 4:              
                if len(input2) >= 8:
                    data = database("login",1,[input1,input2])
                    print("\n\n\n",data)
                    datalog.append([data])
                    def delayed_execution():
                        labell.destroy()
                        menu(data)
                    for widget in root.winfo_children():
                        if widget == background_label:
                            pass
                        else:
                            widget.destroy()
                    labell = tk.Label(root, font=("Arial", 13),height= 2,text = "Registrasi Berhasil, Tunggu Beberapa Saat")
                    labell.place(relx=0.5,rely=0.4,anchor=tk.CENTER)
                    root.after(2000, delayed_execution)
                else:
                    label10 = tk.Label(root, text="Password minimal 8 char!!! ",width=24, height= 2,font=("Arial", 12),fg ="red",bg="black", anchor="w")
                    label10.place(relx=0.42, y=height//2-155)
            else:
                label10 = tk.Label(root, text="Username minimal 4 char!!! ",width=24, height= 2,font=("Arial", 12),fg ="red",bg="black", anchor="w")
                label10.place(relx=0.42, y=height//2-155)

        else:
            label10 = tk.Label(root, text="Username Telah Digunakan",width=24,font=("Arial", 12),fg ="red",bg="black", anchor="w")
            label10.place(relx=0.42, y=height//2-155)
            label11 = tk.Label(root, text="Silahkan Buat Username Lain",width=24,font=("Arial", 12),fg ="red",bg="black", anchor="w")
            label11.place(relx=0.42, y=height//2-137)
            


    def textbox(b,c):
        label = tk.Label(root, text=c,font=("Arial", 12),width=23)
        label.place(relx=0.42, y=b-23)
        entry = tk.Entry(root,font=("Arial", 18),width=16) # textBox
        entry.place(relx=0.42, y=b)
        return entry
    
    def reg():
        button1.destroy()
        button2.destroy()
        button3 = tk.Button(root, text="Registrasi ", bg="green", command=get_input2)
        button3.place(relx=0.4683,y=height//2+20)

    entry1 = textbox(height//2-80,"Username")
    
    entry2 = textbox(height//2-20,"Password")

    button1 = tk.Button(root, text="Login ", bg="green", command=get_input)
    button1.place(relx=0.453,y=height//2+20,x=70)
    button2 = tk.Button(root, text="Registrasi ", bg="green", command=reg)
    button2.place(relx=0.451,y=height//2+20)


def menu(index):
    global lmenu, lmenu1, lmenu2, background_label
    background_label = tk.Label(root, image=background_image)
    background_label.place(relx=0.0823, y=0, relwidth=1, relheight=1)
    
    lmenu = tk.Label(root, text="", width=25, height= 100, font=("Courier", 10), bg="gray", fg = "white")
    lmenu.place(x=0, y=0)
    lmenu2 = tk.Label(root, bg="gray", fg = "black",text=f"Username : {index[1]}",font=("Courier", 12))
    lmenu2.place(x=0, y=3)
    lmenu1 = tk.Label(root, text="Menu :", font=("Courier", 19), bg="gray", fg = "black")
    lmenu1.place(x=0, y=26)
    buttonLH = tk.Button(root, text="Lihat Data ", bg="gray", fg = "black", width=12, height=1,command= lambda:lihat(index))
    buttonLH.place(x=100,y=34)
    buttonTD = tk.Button(root, text="Tambah Data ", bg="gray", fg = "black", width=12, height=1,command= lambda:tambh(index))
    buttonTD.place(x=100,y=64)
    logout()



def logout():
    global buttonLO
    def hapusElement():
        for elemen in root.winfo_children():
            elemen.destroy()
    buttonLO = tk.Button(root, text="Log Out ", bg="red", fg = "black", width=25, height=1,command= lambda:(hapusElement(),log()))
    buttonLO.place(x=10,y=754)



#ALGORTIMA INTI LIHAT DATA
def merge_sort(arr,idx):
    if len(arr) <= 1:
        return arr
    mid = len(arr)//2
    kiri = arr[:mid]
    kanan = arr[mid:]
    kiri = merge_sort(kiri,idx)
    kanan = merge_sort(kanan, idx)
    return merge(kiri, kanan,idx)

def merge(left, right,idx):
    result = []
    left_idx = right_idx = 0
    
    while left_idx < len(left) and right_idx < len(right):
        if left[left_idx][idx] < right[right_idx][idx]:
            result.append(left[left_idx])
            left_idx += 1
        else:
            result.append(right[right_idx])
            right_idx += 1
    
    while left_idx < len(left):
        result.append(left[left_idx])
        left_idx += 1
    while right_idx < len(right):
        result.append(right[right_idx])
        right_idx += 1
    
    return result




def searchB(arr1, arr2,tar):
    def cekkanan(tar, kanan1, kanan2):
        data = []
        if tar in kanan2:
            mid = len(kanan2)//2
            if tar != kanan2[mid]:
                data = searchB(kanan1,kanan2,tar)
            else:
                for j in range(len(kanan2)):
                    if kanan2[j] == tar:
                        break
                for i in range(len(kanan2),0,-1):
                    if kanan2[i-1] == tar:
                        data.extend(kanan1[j:i])
                        break
        return data

    def cekkiri(tar, kiri1, kiri2):
        data = []
        if tar in kiri2:
            mid = len(kiri2)//2
            if tar != kiri2[mid]:
                data = searchB(kiri1,kiri2,tar)
            else:
                for j in range(len(kiri2)):
                    if kiri2[j] == tar:
                        break
                for i in range(len(kiri2),0,-1):
                    if kiri2[i-1] == tar:
                        break
                data.extend(kiri1[j:i])
        return data
    
    data = []
    mid = len(arr2)//2
    kiri1 = arr1[:mid]
    kiri2 = arr2[:mid]
    kanan1 = arr1[mid:]
    kanan2 = arr2[mid:]
    ckr = cekkiri(tar, kiri1, kiri2)
    ckn = cekkanan(tar, kanan1, kanan2)
    data += ckr
    data += ckn
    return data 


def lihat(index):
    arr = database("data_panen",3,"")
    sorted_arr = merge_sort(arr,9)
    kompres = [sublist[9] for sublist in sorted_arr]
    a = searchB(sorted_arr, kompres, index[0])[::-1]
    a = [[i+1, sublist[1], sublist[2], sublist[3], sublist[4], sublist[7], sublist[5], sublist[8], sublist[6]] for i, sublist in enumerate(a)]
    hed = ['ID','Tanggal','Waktu','Berat Gabah','Harga Gudang','Jumlah Pekerja','Penghasilan','Upah/Orang','Penghasilan Pemilik']
    data = []

    if width < 1500:
        ul = 8
        bd = 40
    else:
        ul = 11
        bd = 38

    if len(a)<bd:
        perl = 1
    else:
        perl = len(a)//bd
        if len(a)%bd != 0:
            perl += 1

    for i in range(perl):
        aw = bd * i
        ak = bd * (i+1)
        data.extend([a[aw:ak]])

    def hps():
        labeldt.destroy()
        buttonpr.destroy()
        buttonnx.destroy()
        
    def lll(page = 0):
        global labeldt, buttonnx, buttonpr
        b = data[page]
        tablt = tabulate(b, headers=hed,tablefmt="rounded_outline")
        labeldt = tk.Label(root, text=tablt, font=("Courier", ul))
        labeldt.place(x=230, y=15)
        if page == 0:
            sn = tk.ACTIVE
            sf = tk.DISABLED
        elif page < len(data):
            sn = tk.DISABLED
            sf = tk.ACTIVE
            
        if len(data) > 1:
            buttonnx = tk.Button(root, text="Next >", width=9, height= 1, command= lambda : (hps(),lll(page+1)), state= sn)
            buttonnx.place(relx=0.526, rely=0.94,x=60)
            buttonpr = tk.Button(root, text="< Prev ", width=9, height= 1,command= lambda : (hps(),lll(page-1)), state= sf)
            buttonpr.place(relx=0.5227, rely=0.94)
        else:
            buttonnx = tk.Button(root, text="Next >", bg="green", width=9, height= 1, state= "disabled")
            buttonnx.place(relx=0.526, rely=0.94,x=60)
            buttonpr = tk.Button(root, text="< Prev ", bg="green", width=9, height= 1, state= "disabled")
            buttonpr.place(relx=0.5227, rely=0.94)
            
    buttonLH1 = tk.Button(root, text="Lihat Data ", bg="dark gray", width=12, height= 1, state= tk.DISABLED)
    buttonLH1.place(x=100,y=34)
    buttonTD1 = tk.Button(root, text="Tambah Data ", bg="gray", width=12, height= 1,command= lambda : (hps(),tambh(index)))
    buttonTD1.place(x=100,y=64)
    # logout()
    lll()


#ALGORITMA INTI TAMBAH DATA
def tambh(index):
    def get_input(): 
        global labela
        input1 = entry1.get()
        input2 = entry2.get()
        input3 = entry3.get()

        if input1.isdigit() and input2.isdigit() and input3.isdigit():
            hps()
            def BeratPanen(inp):
                if inp > 9:
                    kw = inp % 10
                    if kw == 0:
                        berat = f'{inp//10} Ton'
                    else:
                        ton = (inp - kw) // 10
                        berat = f'{ton} Ton {kw} Kw'
                elif inp > 0:
                    berat = f'{inp} Kw'
                return berat


            def MataUang(ai):
                locale.setlocale(locale.LC_ALL, "id_ID")
                MU = locale.currency(ai, grouping=True)
                MU = MU.replace(",00","")
                return MU
            
            def last():
                hps()
                buttonLH = tk.Button(root, text="Lihat Data ", bg="gray", fg = "black", width=12, height= 1,command= lambda:(lihat(index), last.destroy()))
                buttonLH.place(x=100,y=34)
                buttonTD = tk.Button(root, text="Tambah Data ", bg="gray", fg = "black", width=12, height= 1,command= lambda:(tambh(index), last.destroy()))
                buttonTD.place(x=100,y=64)
                last = tk.Label(root, font=("Arial", 15),height= 2,text = "Data telah ditambahkan ke dalam database")
                last.place(relx=0.6,rely=0.4,anchor=tk.CENTER)
                logout()

            def KonfirmasiData(data_b):
                konfirmasi = tk.Label(root, font=("Arial", 15),height= 2,text = f"apakah betul hasil panen anda {data_b[2]}, harga gudang saat ini {data_b[3]}, dan anda memiliki {data_b[6]} pekerja")
                konfirmasi.place(relx=0.6,rely=0.4,anchor=tk.CENTER)
                button2 = tk.Button(root, font=("Arial", 11), text="Benar ", width=12, height= 1,bg="lime", command= lambda : (database("data_panen",2, data_b), last()))
                button2.place(relx=0.6,rely=0.4,x=-30 ,y=50)
                button2 = tk.Button(root, font=("Arial", 11), text="Salah ", width=12, height= 1,bg="red", command=lambda: (hps(),tambh(index)))
                button2.place(relx=0.5,rely=0.4,x=-30 ,y=50)

            
            def TambahData():
                tgl = datetime.now().strftime('%Y-%m-%d')
                jam = datetime.now().strftime('%H:%M:%S')
                total = int(input1) * int(input2)
                pekerja = total // 6
                pemilik = pekerja * 5
                berat = BeratPanen(int(input1))
                hg = MataUang(int(input2))
                ttp = MataUang(total * 100)
                pp = MataUang(pemilik * 100)
                up = MataUang(pekerja * 100 // int(input3))
                jp = f'{int(input3)} orang'
                data_b = [tgl, jam, berat, hg, ttp, pp, jp, up, index[0]]
                KonfirmasiData(data_b)
            TambahData()

        else:
            if input1.isdigit():
                pass
            else:
                entry1.delete(0, tk.END)
            if input2.isdigit():
                pass
            else:
                entry2.delete(0, tk.END)
            if input3.isdigit():
                pass
            else:
                entry3.delete(0, tk.END)
            labela = tk.Label(root, text="Tolong Masukkan Inputan Angka Saja!!!",font=("Arial", 16), fg="red")
            labela.place(x=width//2-90, y=180)


   
    def hps():
       for widget in root.winfo_children():
            if widget == background_label:
                pass
            elif widget == lmenu:
                pass
            elif widget == lmenu1:
                pass
            elif widget == lmenu2:
                pass
            else:
                widget.destroy() 

    label1 = tk.Label(root, text="Berapa Kuintal hasil panen saat ini ( /kw)",font=("Arial", 12), width=40, height= 1)
    label1.place(x=width//2-90, y=227)
    entry1 = tk.Entry(root,font=("Arial", 25))
    entry1.place(x=width//2-90, y=250)

    label2 = tk.Label(root, text="Harga gudang saat ini ( /Kg)",font=("Arial", 12), width=40, height= 1)
    label2.place(x=width//2-90, y=307)
    entry2 = tk.Entry(root,font=("Arial", 25))
    entry2.place(x=width//2-90, y=330)

    label3 = tk.Label(root, text="Ada berapa pekerja",font=("Arial", 12), width=40, height= 1)
    label3.place(x=width//2-90, y=387)
    entry3 = tk.Entry(root,font=("Arial", 25))
    entry3.place(x=width//2-90, y=410)

    buttonLH = tk.Button(root, text="Lihat Data ", bg="gray", width=12, height= 1, command= lambda:(hps(),lihat(index)))
    buttonLH.place(x=100,y=34)
    buttonTD = tk.Button(root, text="Tambah Data ", bg="dark gray", width=12, height= 1,state= tk.DISABLED)
    buttonTD.place(x=100,y=64)
    buttonsm = tk.Button(root, text="Simpan ", bg="green", font=("arial",11), command=lambda : (get_input()))
    buttonsm.place(x=width//2+60,y=465)
    logout()



log()
root.mainloop()
