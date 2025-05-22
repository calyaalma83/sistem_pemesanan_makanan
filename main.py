import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime

# ===== Data menu =====
menu = [
    {"id": 1, "nama": "Ayam Betutu", "harga": 125000, "gambar": "menu_images/ayambetutuu.jpeg"},
    {"id": 2, "nama": "Coto Makassar", "harga": 35000, "gambar": "menu_images/coto.jpeg"},
    {"id": 3, "nama": "Gado-gado", "harga": 15000, "gambar": "menu_images/gadogado.jpeg"},
    {"id": 4, "nama": "Gudeg", "harga": 15000, "gambar": "menu_images/gudeg.jpeg"},
    {"id": 5, "nama": "Ketak Telor", "harga": 8000, "gambar": "menu_images/keraktelor.jpeg"},
    {"id": 6, "nama": "Nasi Liwet", "harga": 12000, "gambar": "menu_images/nasiliwet.jpeg"},
    {"id": 7, "nama": "Opor", "harga": 13000, "gambar": "menu_images/opor.jpeg"},
    {"id": 8, "nama": "Pempek", "harga": 10000, "gambar": "menu_images/pempek.jpeg"},
    {"id": 9, "nama": "Rawon", "harga": 13000, "gambar": "menu_images/rawon.jpeg"},
    {"id": 10, "nama": "Rendang", "harga": 15000, "gambar": "menu_images/rendang.jpeg"},
    {"id": 11, "nama": "Rujak Cingur", "harga": 15000, "gambar": "menu_images/rujakcingur.jpeg"},
    {"id": 12, "nama": "Udang Selingkuh", "harga": 45000, "gambar": "menu_images/udangselingkuh.jpeg"},
    
]

pesanan = []

# ===== Fungsi =====
def tampilkan_menu():
    for widget in inner_frame.winfo_children():
        widget.destroy()

    max_row = 3
    row = 0
    col = 0

    for i, item in enumerate(menu):
        frame = tk.Frame(inner_frame, bg="#1a1a2e", padx=5, pady=5, bd=2, relief=tk.RIDGE, width=300, height=90)
        frame.grid(row=row, column=col, padx=10, pady=5, sticky="n")
        frame.grid_propagate(False)

        inner = tk.Frame(frame, bg="#1a1a2e")
        inner.pack(fill=tk.BOTH, expand=True)

        if os.path.exists(item["gambar"]):
            img = Image.open(item["gambar"])
            img = img.resize((60, 40))
            img_tk = ImageTk.PhotoImage(img)
            lbl_img = tk.Label(inner, image=img_tk, bg="#1a1a2e")
            lbl_img.image = img_tk
            lbl_img.pack(side=tk.LEFT, padx=5)
        else:
            tk.Label(inner, text="(No Image)", bg="#1a1a2e", fg="red", width=9).pack(side=tk.LEFT, padx=5)

        info = f"{item['nama']:<15} - Rp{item['harga']}"
        lbl_info = tk.Label(inner, text=info, bg="#1a1a2e", fg="#00ffe7", font=("Courier New", 10), anchor="w")
        lbl_info.pack(side=tk.LEFT)

        row += 1
        if row >= max_row:
            row = 0
            col += 1

def isi_id_dan_fokus(item):
    entry_id.delete(0, tk.END)
    entry_id.insert(0, item["id"])
    entry_jumlah.focus()

def tambah_pesanan():
    try:
        id_makanan = int(entry_id.get())
        jumlah = int(entry_jumlah.get())
        nama = entry_nama.get().strip()

        if not nama:
            messagebox.showwarning("Input Kosong", "Masukkan nama pelanggan.")
            return

        for item in menu:
            if item["id"] == id_makanan:
                total = item["harga"] * jumlah
                pesanan.append({
                    "nama_pelanggan": nama,
                    "nama": item["nama"],
                    "jumlah": jumlah,
                    "total": total,
                    "gambar": item["gambar"]
                })
                tampilkan_gambar(item["gambar"])
                loading_label.config(text="✓ Berhasil dipesan!", fg="green")
                entry_id.delete(0, tk.END)
                entry_jumlah.delete(0, tk.END)
                return

        messagebox.showerror("Error", "ID makanan tidak ditemukan.")

    except ValueError:
        messagebox.showerror("Error", "Masukkan angka yang valid.")

def tampilkan_gambar(path):
    if os.path.exists(path):
        img = Image.open(path)
        img = img.resize((150, 100))
        img_tk = ImageTk.PhotoImage(img)
        gambar_label.config(image=img_tk)
        gambar_label.image = img_tk
    else:
        gambar_label.config(text="(Gambar tidak tersedia)", image="", fg="red")

def lihat_pesanan():
    text_pesanan.delete(1.0, tk.END)
    if not pesanan:
        text_pesanan.insert(tk.END, "Belum ada pesanan.")
        return
    nama_pelanggan = pesanan[0]["nama_pelanggan"]
    text_pesanan.insert(tk.END, f"=== Struk Pesanan ===\nNama Pelanggan: {nama_pelanggan}\n\n")
    total_bayar = 0
    for item in pesanan:
        text_pesanan.insert(tk.END, f"{item['nama']} x {item['jumlah']} = Rp{item['total']}\n")
        total_bayar += item['total']
    text_pesanan.insert(tk.END, f"\nTotal Bayar: Rp{total_bayar}")

def simpan_riwayat():
    if not pesanan:
        messagebox.showwarning("Kosong", "Belum ada pesanan yang disimpan.")
        return
    with open("riwayat_pesanan.txt", "a") as f:
        f.write(f"\n=== Pesanan {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        f.write(f"Nama Pelanggan: {pesanan[0]['nama_pelanggan']}\n")
        for item in pesanan:
            f.write(f"{item['nama']} x {item['jumlah']} = Rp{item['total']}\n")
        total_bayar = sum(i['total'] for i in pesanan)
        f.write(f"Total Bayar: Rp{total_bayar}\n")
    messagebox.showinfo("Tersimpan", "Pesanan berhasil disimpan ke riwayat.")

def reset_pesanan():
    if messagebox.askyesno("Reset", "Yakin reset semua pesanan?"):
        pesanan.clear()
        text_pesanan.delete(1.0, tk.END)
        gambar_label.config(image="")
        loading_label.config(text="")

def on_exit():
    if messagebox.askokcancel("Keluar", "Yakin ingin keluar?"):
        root.destroy()

# ===== UI utama =====
root = tk.Tk()
root.title("Sistem Pemesanan Makanan")
root.geometry("500x700")
root.configure(bg="#0f0f1a")
root.protocol("WM_DELETE_WINDOW", on_exit)

# Frame menu (scrollable + tengah)
canvas = tk.Canvas(root, height=200, bg="#0f0f1a", highlightthickness=0)
scroll_frame = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scroll_frame.set)

scroll_frame.pack(side=tk.RIGHT, fill=tk.Y)
canvas.pack(fill=tk.BOTH, expand=False)

daftar_menu_frame = tk.Frame(canvas, bg="#0f0f1a")
inner_frame = tk.Frame(daftar_menu_frame, bg="#0f0f1a")
inner_frame.pack(anchor="center")

canvas.create_window((0, 0), window=daftar_menu_frame, anchor="nw")

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

daftar_menu_frame.bind("<Configure>", on_frame_configure)

# Input pemesanan
frame_input = tk.Frame(root, bg="#0f0f1a")
frame_input.pack(pady=10)

tk.Label(frame_input, text="Nama Pelanggan:", bg="#0f0f1a", fg="#ff00ff").grid(row=0, column=0)
entry_nama = tk.Entry(frame_input, bg="#1a1a2e", fg="#ffffff")
entry_nama.grid(row=0, column=1)

tk.Label(frame_input, text="ID Makanan:", bg="#0f0f1a", fg="#ff00ff").grid(row=1, column=0)
entry_id = tk.Entry(frame_input, bg="#1a1a2e", fg="#ffffff")
entry_id.grid(row=1, column=1)

tk.Label(frame_input, text="Jumlah:", bg="#0f0f1a", fg="#ff00ff").grid(row=2, column=0)
entry_jumlah = tk.Entry(frame_input, bg="#1a1a2e", fg="#ffffff")
entry_jumlah.grid(row=2, column=1)

btn_pesan = tk.Button(root, text="🛒 Pesan", command=tambah_pesanan, bg="#ff00ff", fg="#000")
btn_pesan.pack(pady=3)

loading_label = tk.Label(root, text="", bg="#0f0f1a", fg="green")
loading_label.pack()

# Gambar makanan
gambar_label = tk.Label(root, bg="#0f0f1a")
gambar_label.pack(pady=5)

# Pesanan frame
frame_pesanan = tk.Frame(root)
frame_pesanan.pack(pady=5)

scroll_pesanan = tk.Scrollbar(frame_pesanan)
scroll_pesanan.pack(side=tk.RIGHT, fill=tk.Y)

text_pesanan = tk.Text(frame_pesanan, height=8, width=50, bg="#1a1a2e", fg="#00ffcc", font=("Courier New", 10), yscrollcommand=scroll_pesanan.set)
text_pesanan.pack(side=tk.LEFT)

scroll_pesanan.config(command=text_pesanan.yview)

# Tombol aksi
btn_lihat = tk.Button(root, text="👁️ Lihat Pesanan", command=lihat_pesanan, bg="#00ffff", fg="#000")
btn_lihat.pack(pady=3)

btn_simpan = tk.Button(root, text="💾 Simpan Riwayat", command=simpan_riwayat, bg="#00ff99", fg="#000")
btn_simpan.pack(pady=2)

btn_reset = tk.Button(root, text="🔄 Reset", command=reset_pesanan, bg="#ff4444", fg="#fff")
btn_reset.pack(pady=2)

btn_keluar = tk.Button(root, text="🚪 Keluar", command=on_exit, bg="#cccccc", fg="#000")
btn_keluar.pack(pady=5)

tampilkan_menu()
root.mainloop()
