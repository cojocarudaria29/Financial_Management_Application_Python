import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import  Label, Button, messagebox, Toplevel, ttk, filedialog, Menu
from tkinter import colorchooser
import matplotlib.pyplot as plt

# Nume fișier pentru a stoca datele financiare
NUME_FISIER = "date_financiare.csv"


# Verifică dacă fișierul există; dacă nu, îl creează cu anteturi
def initializeaza_fisierul():
    if not os.path.exists(NUME_FISIER):
        with open(NUME_FISIER, mode='w', newline='') as fisier:
            writer = csv.writer(fisier)
            writer.writerow(["Data", "Tip", "Categorie", "Suma", "Descriere"])


# Funcții pentru operații

def adauga_tranzactie_gui():
    def salveaza():
        tip = tip_var.get()
        categorie = categorie_entry.get().strip()
        suma = suma_entry.get().strip()
        descriere = descriere_entry.get().strip()

        if not suma.replace('.', '', 1).isdigit():
            messagebox.showerror("Eroare", "Introdu o sumă validă.")
            return

        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(NUME_FISIER, mode='a', newline='') as fisier:
            writer = csv.writer(fisier)
            writer.writerow([data, tip, categorie, suma, descriere])

        messagebox.showinfo("Succes", "Tranzacția a fost adăugată cu succes!")
        adauga_fereastra.destroy()

    adauga_fereastra = tk.Toplevel(root)
    adauga_fereastra.title("Adaugă Tranzacție")
    adauga_fereastra.geometry("400x300")

    tk.Label(adauga_fereastra, text="Tip:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
    tip_var = tk.StringVar(value="Venit")
    tk.OptionMenu(adauga_fereastra, tip_var, "Venit", "Cheltuiala").grid(row=0, column=1, padx=10, pady=10)

    tk.Label(adauga_fereastra, text="Categorie:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
    categorie_entry = tk.Entry(adauga_fereastra, font=("Arial", 12))
    categorie_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(adauga_fereastra, text="Sumă:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10)
    suma_entry = tk.Entry(adauga_fereastra, font=("Arial", 12))
    suma_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(adauga_fereastra, text="Descriere:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10)
    descriere_entry = tk.Entry(adauga_fereastra, font=("Arial", 12))
    descriere_entry.grid(row=3, column=1, padx=10, pady=10)

    tk.Button(adauga_fereastra, text="Salvează", font=("Arial", 12), bg="#4CAF50", fg="white", command=salveaza).grid(row=4, column=0, columnspan=2, pady=20)


def vizualizeaza_tranzactii_gui():
    def aplica_filtre():
        # Preluăm valorile din câmpurile de introducere
        data_start = data_start_entry.get().strip()
        data_end = data_end_entry.get().strip()
        categorie_filtru = categorie_filtru_entry.get().strip().lower()

        tranzactii_filtrate = []

        for tranzactie in tranzactii[1:]:  # Ignorăm antetul
            data_tranzactie = tranzactie[0]
            categorie_tranzactie = tranzactie[2].strip().lower()  # Normalizăm șirurile
            include = True

            # Filtru după dată
            if data_start and data_end:
                try:
                    data_start_dt = datetime.strptime(data_start, "%Y-%m-%d")
                    data_end_dt = datetime.strptime(data_end, "%Y-%m-%d")
                    data_tranzactie_dt = datetime.strptime(data_tranzactie.split()[0], "%Y-%m-%d")  # Ignorăm ora
                    if not (data_start_dt <= data_tranzactie_dt <= data_end_dt):
                        include = False
                except ValueError:
                    messagebox.showerror("Eroare", "Formatul datelor trebuie să fie YYYY-MM-DD.")
                    return

            # Filtru după categorie
            if categorie_filtru and categorie_filtru not in categorie_tranzactie:
                include = False

            # Adaugă tranzacția dacă toate filtrele trec
            if include:
                tranzactii_filtrate.append(tranzactie)

        # Șterge toate elementele din tabelul existent
        for item in tree.get_children():
            tree.delete(item)

        # Adaugă tranzacțiile filtrate în tabel
        for tranzactie in tranzactii_filtrate:
            tree.insert("", "end", values=tranzactie)

    vizualizare_fereastra = tk.Toplevel(root)
    vizualizare_fereastra.title("Tranzacții")
    vizualizare_fereastra.geometry("800x500")
    vizualizare_fereastra.configure(bg="#ede7f6")

    with open(NUME_FISIER, mode='r') as fisier:
        reader = csv.reader(fisier)
        tranzactii = list(reader)

    if len(tranzactii) <= 1:
        tk.Label(vizualizare_fereastra, text="Nu există tranzacții de afișat.", font=("Arial", 12), bg="#ede7f6").pack(padx=20, pady=20)
    else:
        filtre_frame = tk.Frame(vizualizare_fereastra, bg="#ede7f6")
        filtre_frame.pack(padx=10, pady=10)

        tk.Label(filtre_frame, text="Data start (YYYY-MM-DD):", font=("Arial", 10), bg="#ede7f6").grid(row=0, column=0, padx=5)
        data_start_entry = tk.Entry(filtre_frame, font=("Arial", 10))
        data_start_entry.grid(row=0, column=1, padx=5)

        tk.Label(filtre_frame, text="Data end (YYYY-MM-DD):", font=("Arial", 10), bg="#ede7f6").grid(row=0, column=2, padx=5)
        data_end_entry = tk.Entry(filtre_frame, font=("Arial", 10))
        data_end_entry.grid(row=0, column=3, padx=5)

        tk.Label(filtre_frame, text="Categorie:", font=("Arial", 10), bg="#ede7f6").grid(row=0, column=4, padx=5)
        categorie_filtru_entry = tk.Entry(filtre_frame, font=("Arial", 10))
        categorie_filtru_entry.grid(row=0, column=5, padx=5)

        tk.Button(filtre_frame, text="Aplică filtre", font=("Arial", 10), bg="#4CAF50", fg="white", command=aplica_filtre).grid(row=0, column=6, padx=5)

        tree = ttk.Treeview(vizualizare_fereastra, columns=("Data", "Tip", "Categorie", "Suma", "Descriere"),show="headings")
        tree.heading("Data", text="Data")
        tree.heading("Tip", text="Tip")
        tree.heading("Categorie", text="Categorie")
        tree.heading("Suma", text="Sumă")
        tree.heading("Descriere", text="Descriere")

        for tranzactie in tranzactii[1:]:
            tree.insert("", "end", values=tranzactie)

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

def rezumat_gui():
    venituri, cheltuieli = 0, 0
    categorii = {}

    with open(NUME_FISIER, mode='r') as fisier:
        reader = csv.reader(fisier)
        next(reader)  # Sar antetul
        for linie in reader:
            suma = float(linie[3])
            if linie[1] == "Venit":
                venituri += suma
            elif linie[1] == "Cheltuiala":
                cheltuieli += suma
                categorii[linie[2]] = categorii.get(linie[2], 0) + suma

    rezumat_fereastra = tk.Toplevel(root)
    rezumat_fereastra.title("Rezumat Financiar")
    rezumat_fereastra.geometry("400x300")

    tk.Label(rezumat_fereastra, text=f"Total Venituri: {venituri:.2f} RON", font=("Arial", 12)).pack(padx=10, pady=5)
    tk.Label(rezumat_fereastra, text=f"Total Cheltuieli: {cheltuieli:.2f} RON", font=("Arial", 12)).pack(padx=10,pady=5)
    tk.Label(rezumat_fereastra, text=f"Balanță Netă: {venituri - cheltuieli:.2f} RON", font=("Arial", 12)).pack(padx=10, pady=5)

    def afiseaza_grafic():
        if not categorii:
            messagebox.showinfo("Info", "Nu există cheltuieli pentru grafic.")
            return

        etichete = categorii.keys()
        valori = categorii.values()
        plt.figure(figsize=(8, 6))
        plt.pie(valori, labels=etichete, autopct='%1.1f%%', startangle=140)
        plt.title("Distribuția Cheltuielilor pe Categorii")
        plt.show()

    tk.Button(rezumat_fereastra, text="Afișează Grafic", font=("Arial", 12), bg="#4CAF50", fg="white",command=afiseaza_grafic).pack(pady=10)


def exporta_csv_gui():
    fisier_export = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not fisier_export:
        return

    with open(NUME_FISIER, mode='r') as fisier:
        date = fisier.readlines()

    with open(fisier_export, mode='w') as fisier:
        fisier.writelines(date)

    messagebox.showinfo("Succes", f"Datele au fost exportate cu succes în {fisier_export}")


def economii_lunare():
    """Calculează economiile lunare pe baza veniturilor și cheltuielilor lunare."""

    def afiseaza_economii():
        luna_curenta = datetime.now().strftime("%Y-%m")
        venituri_lunare = 0
        cheltuieli_lunare = 0

        with open(NUME_FISIER, mode='r') as fisier:
            reader = csv.reader(fisier)
            next(reader)  # Sar antetul
            for linie in reader:
                data = linie[0].split()[0]  # Data în format YYYY-MM-DD
                if data.startswith(luna_curenta):
                    suma = float(linie[3])
                    if linie[1] == "Venit":
                        venituri_lunare += suma
                    elif linie[1] == "Cheltuiala":
                        cheltuieli_lunare += suma

        economii = venituri_lunare - cheltuieli_lunare

        rezultat_label["text"] = (f"Economii pentru luna {luna_curenta}: {economii:.2f} RON\n"f"Venituri: {venituri_lunare:.2f} RON, Cheltuieli: {cheltuieli_lunare:.2f} RON")

    economii_fereastra = Toplevel()
    economii_fereastra.title("Economii Lunare")
    economii_fereastra.geometry("400x200")

    Label(economii_fereastra, text="Economii lunare calculate pentru luna curentă:", font=("Arial", 12)).pack(pady=10)

    rezultat_label = Label(economii_fereastra, text="", font=("Arial", 12), fg="#4CAF50")
    rezultat_label.pack(pady=10)

    Button(economii_fereastra, text="Calculează Economii", font=("Arial", 12), bg="#4CAF50", fg="white", command=afiseaza_economii).pack(pady=5)
    Button(economii_fereastra, text="Închide", font=("Arial", 12), command=economii_fereastra.destroy).pack(pady=5)
def modifica_culoare():
    culoare = colorchooser.askcolor(title="Alege culoarea de fundal")
    if culoare[1]:
        root.configure(bg=culoare[1])
# Interfața principală
initializeaza_fisierul()
root = tk.Tk()
root.title("Gestiune Financiară Personală")
root.geometry("500x400")
root.configure(bg="#f0f0f0")

# Elemente principale ale interfeței
frame_butoane = tk.Frame(root, bg="#f0f0f0")
frame_butoane.pack(pady=20)

# Setare fundal general și culori pentru butoane
root.configure(bg="#d1c4e9")  # Mov deschis

meniu = Menu(root)
root.config(menu=meniu)
meniu.add_command(label="Schimbă Culoare Fundal", command=modifica_culoare)

# Elemente principale ale interfeței
tk.Label(root, text="Aplicație de Gestiune Financiară", font=("Arial", 16, "bold"), bg="#d1c4e9", fg="#4a148c").pack(pady=10)  # Mov închis

tk.Button(frame_butoane, text="Adaugă Tranzacție", font=("Arial", 12), bg="#7e57c2", fg="white", command=adauga_tranzactie_gui, width=25).pack(pady=5)
tk.Button(frame_butoane, text="Vizualizează Tranzacții", font=("Arial", 12), bg="#7e57c2", fg="white", command=vizualizeaza_tranzactii_gui, width=25).pack(pady=5)
tk.Button(frame_butoane, text="Rezumat Financiar", font=("Arial", 12), bg="#7e57c2", fg="white", command=rezumat_gui, width=25).pack(pady=5)
tk.Button(frame_butoane, text="Exportă Tranzacții", font=("Arial", 12), bg="#7e57c2", fg="white", command=exporta_csv_gui, width=25).pack(pady=5)
tk.Button(frame_butoane, text="Economii Lunare", font=("Arial", 12), bg="#7e57c2", fg="white", command=economii_lunare, width=25).pack(pady=5)
tk.Button(frame_butoane, text="Ieșire", font=("Arial", 12), bg="#ab47bc", fg="white", command=root.quit, width=25).pack(pady=5)  # Mov mai deschis pentru ieșire

root.mainloop()