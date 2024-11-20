import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk
## membuat library untuk membuat GUI di python (tkinter)
# message box untuk menampilkan pesan dialog
def create_database():
    conn = sqlite3.connect('nilai_siswa_.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS nilai_siswa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_siswa TEXT NOT NULL,
        biologi INTEGER,
        fisika INTEGER,
        inggris INTEGER,
        prediksi_fakultas TEXT
        )
    ''')
    conn.commit()
    conn.close()
## membuat database dari table nama siswa dan pembuatan interface GUI
def fetch_data():
    conn = sqlite3.connect('nilai_siswa_.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM nilai_siswa')
    rows = cursor.fetchall()
    conn.close()
    return rows
# membuat frame utama untuk padding , menggunakan stringVar.
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa_.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))
    conn.commit()
    conn.close()
# membuat dictionary fakultas dan nilai
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa_.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()
    conn.close()
    # memanggil fungsi untuk memperbarui data

def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa_.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()
#memanggil fungsi untuk menghapus data
def calculate_prediction(biologi, fisika, inggris):
#memanggil fungsi untuk menghitung prediksi fakultas
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak diketahui"

def submit():
    try:
        #mengambil data dari input GUI
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())
    # validasi input
        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")
        #hitung prediksi fakultas
        prediksi = calculate_prediction(biologi, fisika, inggris)
        # menyimpan data ke database
        save_to_database(nama, biologi, fisika, inggris, prediksi)
        # menampilkan pesan sukses
        messagebox.showinfo("Sukses", f"Data Berhasil disimpan!\nPrediksi fakultas: {prediksi}")
        clear_inputs()
        populate_table()
    # menampilkan pesan error jika input tidak valid
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")

def update():
    try:
    # memperbarui data base
    # mengecek data apakah sudah sesuai 
        if not selected_record_id.get():
            raise ValueError("Pilih data dari tabel untuk di-update.")

        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")
        
        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)
        messagebox.showinfo("Sukses", "Data Berhasil diperbarui!")
        clear_inputs()
        populate_table()
# menampilkan pesan error jika kesalahan
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

def delete():
    try:
        # Memastikan bahwa ada data yang dipilih untuk dihapus.
        #Menghapus data berdasarkan ID dari database.
        # Menampilkan pesan keberhasilan jika penghapusan berhasil.
        # Membersihkan input dan memperbarui tabel setelah data dihapus.
        if not selected_record_id.get():
            raise ValueError("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())
        # Panggil fungsi untuk menghapus data dari database
        delete_database(record_id)
        messagebox.showinfo("Sukses", "Data Berhasil dihapus!")
        # menghapus input an
        clear_inputs()
        populate_table()

    except ValueError as e:
         # Tampilkan pesan kesalahan jika terjadi error
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk membersihkan semua input
def clear_inputs():
    nama_var.set("") # Reset input untuk nama
    biologi_var.set("") # Reset input untuk nilai Biologi
    fisika_var.set("") # Reset input untuk nilai Fisika
    inggris_var.set("") # Reset input untuk nilai Bahasa Inggris
    selected_record_id.set("") # Reset ID data yang dipilih

# Fungsi untuk mengisi ulang tabel dengan data
def populate_table():

    # Hapus semua data yang ada di tabel
    for row in tree.get_children():
        tree.delete(row)
    # Ambil data terbaru dan tambahkan ke tabel
    for row in fetch_data():
        tree.insert('', 'end', values=row)

# Fungsi untuk mengisi input form berdasarkan data yang dipilih dari tabel
def fill_inputs_from_table(event):
    try:
        # Ambil ID item yang dipilih di tabel
        selected_item = tree.selection()[0]
        selected_row = tree.item(selected_item)['values']

        selected_record_id.set(selected_row[0])
        # Isi variabel input dengan data dari tabel
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid")

create_database()

root = Tk()
root.title("Prediksi Fakultas Siswa")

nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()

   # Label dan Entry untuk Nama Siswa
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Bahasa Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

#tombol add
Button(root, text="Add", command=submit, bg='green', fg='white').grid(row=4, column=0, pady=10)
# tombol update
Button(root, text="Update", command=update, bg='blue', fg='white').grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete, bg='red', fg='white').grid(row=4, column=2, pady=10)

columns = ('id', 'nama_siswa', 'biologi', 'fisika', 'inggris', 'prediksi_fakultas')
tree = ttk.Treeview(root, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center')

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

populate_table()

root.mainloop()