import sqlite3
import tkinter as tk
from tkinter import messagebox

def buat_tabel():
   
    conn = sqlite3.connect('file.db')
    cursor = conn.cursor()


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Person (
            person_id INTEGER PRIMARY KEY,
            nama_depan TEXT,
            nama_belakang TEXT
        )
    ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employee (
            employee_id INTEGER PRIMARY KEY,
            jabatan TEXT,
            person_id INTEGER,
            FOREIGN KEY (person_id) REFERENCES Person(person_id)
        )
    ''')


    conn.commit()
    conn.close()

def masukkan_data(nama_depan, nama_belakang, jabatan):
    try:

        conn = sqlite3.connect('file.db')
        cursor = conn.cursor()


        cursor.execute('INSERT INTO Person (nama_depan, nama_belakang) VALUES (?, ?)', (nama_depan, nama_belakang))
        person_id = cursor.lastrowid  # Mendapatkan ID terakhir yang dimasukkan

        cursor.execute('INSERT INTO Employee (jabatan, person_id) VALUES (?, ?)', (jabatan, person_id))

        
        conn.commit()
        conn.close()

        messagebox.showinfo("Sukses", "Data berhasil ditambahkan!")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

def main():

    root = tk.Tk()
    root.title("Aplikasi GUI SQL")


    tk.Label(root, text="Nama Depan:").grid(row=0, column=0)
    tk.Label(root, text="Nama Belakang:").grid(row=1, column=0)
    tk.Label(root, text="Jabatan:").grid(row=2, column=0)

    nama_depan_entry = tk.Entry(root)
    nama_belakang_entry = tk.Entry(root)
    jabatan_entry = tk.Entry(root)

    nama_depan_entry.grid(row=0, column=1)
    nama_belakang_entry.grid(row=1, column=1)
    jabatan_entry.grid(row=2, column=1)

    submit_button = tk.Button(root, text="Tambah Data", command=lambda: masukkan_data(
        nama_depan_entry.get(),
        nama_belakang_entry.get(),
        jabatan_entry.get()
    ))
    submit_button.grid(row=3, column=0, columnspan=2)


    buat_tabel()


    root.mainloop()

if __name__ == "__main__":
    main()
