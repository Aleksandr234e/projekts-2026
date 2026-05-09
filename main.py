import json
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

root = tk.Tk(screenName=None, baseName="Stark", className='Tk', useTk=1)
root.title("Personīgo finanšu sekotājs")
root.geometry()
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++JSON faila pielietošana++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def saglabat_faila():
    dati = {
        "Pārtika": listbox_food.get(0, tk.END),
        "Transports": listbox_transport.get(0, tk.END),
        "Izklaide": listbox_fun.get(0, tk.END),
        "Citi": listbox_else.get(0, tk.END),
        "Ienākumi": listbox_ienakumi.get(0, tk.END)

    }

    with open("budzets.json", "w", encoding="utf-8") as f:
        json.dump(dati, f, ensure_ascii=False, indent=4)

dati_saglabati = True  # ŠEIT ATZĪMĒJAM, KA SAGLABĀTS

def ieladet_failu():
    try:
        with open("budzets.json", "r", encoding="utf-8") as f:
            dati = json.load(f)

        listbox_food.delete(0, tk.END)
        listbox_transport.delete(0, tk.END)
        listbox_fun.delete(0, tk.END)
        listbox_else.delete(0,tk.END)
        listbox_ienakumi.delete(0, tk.END)

        for v in dati["Pārtika"]:
            listbox_food.insert(tk.END, v)
        for v in dati["Transports"]:
            listbox_transport.insert(tk.END, v)
        for v in dati["Izklaide"]:
            listbox_fun.insert(tk.END, v)
        for v in dati["Citi"]:
            listbox_else.insert(tk.END, v)
        for v in dati["Ienākumi"]:
            listbox_ienakumi.insert(tk.END, v)

    except FileNotFoundError:
        print("Fails nav atrasts")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++Riņķvejda diogramas radīšana un vejdošana++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def paradit_grafiku():
   # Saskaitām kategorijas
    try:
        sum_food = sum(float(i) for i in listbox_food.get(0, tk.END))
        sum_transport = sum(float(i) for i in listbox_transport.get(0, tk.END))
        sum_fun = sum(float(i) for i in listbox_fun.get(0, tk.END))
        sum_else = sum(float(i) for i in listbox_else.get(0, tk.END))
    except ValueError:
        return # ja sarakstā ir tukšas rindas
# kategorijas
    kategorijas = ["Pārtika", "Transports", "Izklaide", "Citi"]
    vertibas = [sum_food, sum_transport, sum_fun, sum_else]
    krasas = ["#ff9999", "#66b3ff", "#99ff99","#808000"]

 # Filtrējam ārā kategorijas ar 0 vērtību
    kategorijas, vertibas, krasas = zip(
        *[(k, v, c) for k, v, c in zip(kategorijas, vertibas, krasas) if v > 0]
    )

    # Ja visas kategorijas ir 0
    if not vertibas:
        messagebox.showinfo("Nav datu", "Nav neviena izdevuma, ko parādīt grafikā.")
        return


    # Jauns logs
    logs = tk.Toplevel()
    logs.title("Riņķveida grafiks")
    logs.geometry("500x600")
    # Izveido figūru
    fig, ax = plt.subplots(figsize=(5, 5))
    wedges, texts, autotexts = ax.pie(
        vertibas,
        labels = kategorijas,
        autopct = "%1.1f%%",
        colors = krasas
    )
    ax.set_title("Izdevumu sadalījums")

    # Leģenda blakus grafikam
    ax.legend(
        wedges,
        kategorijas,
        title="Kategorijas",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )

    # Parāda grafiku jaunajā logā ar GRID
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master = logs)
    canvas.draw()
    canvas.get_tk_widget().grid(row = 0, column = 0, padx = 10, pady = 10)

    # Aizvērt poga
    close_btn = tk.Button(logs, text="Aizvērt", command = logs.destroy)
    close_btn.grid(row = 1, column = 0, pady = 10)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++Programmas funkcionāls++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def summet():
    total = 0

    # Saskaita katras kategorijas summu
    for lb in (listbox_food, listbox_transport, listbox_fun, listbox_else):
        items = lb.get(0, tk.END)
        total += sum(float(i) for i in items)
        ienakumi = sum(float(i) for i in listbox_ienakumi.get(0, tk.END))

    rezultats_label.config(text=f"Kopējā summa kuru patereja: {total:.2f}€") #Izvada rezultātu ar diviem cipariem aiz komata.
    ienakumu_label.config(text=f"Kopējā summa kuru saņem: {ienakumi:.2f}€") #Izvada ienākumus, ja nav ievadīti ienākumi tad rezultāts būs 0.00€
    parplakimus_label.config(text=f"Kopējā summa kura palika: {ienakumi - total:.2f}€") #Izvada parplakumus, ja nav ievadīti ienākumi tad rezultāts būs negatīvs un parplakumi būs vienādi ar patēriņu.

def dellet_from_list(): #Pogas DELETE funkcionals, kurš ļauj dzēst no visam kategorijam bet ne no vienas.

    global dati_saglabati
    dati_saglabati = False

    # Pārtika
    selected = listbox_food.curselection()
    if selected:
        listbox_food.delete(selected[0])
        return

    # Transports
    selected = listbox_transport.curselection()
    if selected:
        listbox_transport.delete(selected[0])
        return

    # Izklaide
    selected = listbox_fun.curselection()
    if selected:
        listbox_fun.delete(selected[0])
        return

    # Citi
    selected = listbox_else.curselection()
    if selected:
        listbox_else.delete(selected[0])
        return
    
    # Ienākumi
    selected = listbox_ienakumi.curselection()
    if selected:
        listbox_ienakumi.delete(selected[0])
        return


def add_to_list():
    global dati_saglabati
    dati_saglabati = False

    value = entry.get().replace(",", ".")
    try:
        num = float(value)
    except ValueError:
        entry.delete(0, tk.END)
        return

    kategorija = kategorija_var.get()

    if kategorija == "Pārtika":
        listbox_food.insert(tk.END, value)

    elif kategorija == "Transports":
        listbox_transport.insert(tk.END, value)

    elif kategorija == "Izklaide":
        listbox_fun.insert(tk.END, value)

    elif kategorija == "Citi":
        listbox_else.insert(tk.END, value)

    elif kategorija == "Ienakumi":
        listbox_ienakumi.insert(tk.END, value)

    entry.delete(0, tk.END)




def validate(value_if_allowed):
    # Atļaujam tukšu lauku
    if value_if_allowed == "":
        error_label.config(text = "")
        return True

    # Automātiska komata => punkta nomaiņa
    value_if_allowed = value_if_allowed.replace(",", ".")

    try:
        float(value_if_allowed)
        error_label.config(text = "")  # nav kļūdas
        return True
    except ValueError:
        error_label.config(text = "Ievadiet tikai skaitļus!")
        return False


vcmd = (root.register(validate), "%P")

def quit_program():
    global dati_saglabati

    # Ja dati jau saglabāti → vienkārši aizveram
    if dati_saglabati:
        root.destroy()
        return

    # Ja NAV saglabāti → pajautājam
    atbilde = messagebox.askyesno(
        "Iziet",
        "Vai vēlaties saglabāt datus pirms aizvēršanas?"
    )

    if atbilde:
        saglabat_faila()

    root.destroy()




root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)

# Kategoriju izvēlne
kategorija_var = tk.StringVar(value="Pārtika")
kategorijas = ["Pārtika", "Transports", "Izklaide", "Citi", "Ienakumi"]


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++POGAS UN PAREJAIS++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

frame = tk.Frame(root, bd=3, relief="groove", padx=10, pady=10, bg="#f2f2f2")
frame.grid(row=1, column=0, padx=10, pady=10)

title_label = tk.Label(
    root,
    text="PERSONĪGO FINANŠU SEKOTĀJS",
    font=("Arial", 24, "bold"),
    fg="#003366",
    pady=10
)
title_label.grid(row=0, column=0, columnspan=10)

button_style = {
    "font": ("Arial", 11, "bold"),
    "bg": "#4da6ff",
    "fg": "white",
    "activebackground": "#1a75ff",
    "activeforeground": "white",
    "bd": 2,
    "relief": "raised",
    "padx": 5,
    "pady": 3
}

option_style = {
    "font": ("Arial", 11, "bold"),
    "bg": "#e6f2ff",
    "fg": "#003366",
    "activebackground": "#cce6ff",
    "activeforeground": "#003366",
    "highlightthickness": 1,
    "highlightbackground": "#4da6ff",
    "bd": 2
}

label_style = {
    "font": ("Arial", 12, "bold"),
    "bg": "#f2f2f2",
    "fg": "#003366",
    "pady": 5
}



entry = tk.Entry(frame, validate = "key", validatecommand = vcmd)
entry.grid(row = 0, column = 1, padx = 20, pady = 10)

ienakumi_lable = tk.Label(frame, text = "Ienākumi/Izdevumi==>", fg = "blue", font=("Arial", 12, "bold"))
ienakumi_lable.grid(row = 0, column = 0, padx = 5, pady = 5)

frame.columnconfigure(1, weight = 10)

faill_save = tk.Button(root, text = "Saglabāt failā", command = saglabat_faila, **button_style)
faill_save.grid(row = 2, column = 3)

daygram_showing = tk.Button(root, text = "Parādīt grafiku", command = paradit_grafiku, **button_style)
daygram_showing.grid(row = 2, column = 2)


#Izvejdo pogu ar kuru palidzību var pievienot
entry_bth1 = tk.Button(frame, text = "Add", command = add_to_list, **button_style)
entry_bth1.grid(row = 0, column = 2, padx = 1, pady = 1)
root.bind("<Return>", add_to_list)

#Izvejdo pogu ar kuru palidzību var dzēst no
entry_btn2 = tk.Button(frame, text = "Delete", command = dellet_from_list, **button_style)
entry_btn2.grid(row = 0, column = 3, padx = 1, pady = 1)
root.bind("<BackSpace>", dellet_from_list)

Button = tk.Button(root, text = "Quit", command = quit_program, **button_style)
Button.grid(row = 4, column = 3 , padx = 5, pady = 5)

error_label = tk.Label(root, text = "", fg = "red")
error_label.grid(row = 1, column = 0)

# Poga "Summa"
summa_btn = tk.Button(root, text = "Summa", command = summet, **button_style)
summa_btn.grid(row = 3, column = 3, padx = 5, pady = 5)

# Rezultāta teksts
rezultats_label = tk.Label(root, text="Kopējā summa kuru patērēja:", fg="green", font=("Arial", 12, "bold"))
rezultats_label.grid(row = 3, column = 0)

ienakumu_label = tk.Label(root, text = "Kopējā summa kuru saņem: ", fg = "blue", font=("Arial", 12, "bold"))
ienakumu_label.grid(row = 2, column = 0)

parplakimus_label = tk.Label(root, text = "Kopējā summa kura palika: ", fg = "red", font=("Arial", 12, "bold"))
parplakimus_label.grid(row = 4, column = 0)

# Listbox katrai kategorijai
tk.Label(frame, text="Pārtika", **label_style).grid(row=1, column=0)
listbox_food = tk.Listbox(frame, width = 15, height = 8)
listbox_food.grid(row = 2, column = 0, padx = 5, pady = 5)

tk.Label(frame, text="Transports", **label_style).grid(row=1, column=1)
listbox_transport = tk.Listbox(frame, width = 15, height = 8)
listbox_transport.grid(row = 2, column = 1, padx = 5, pady = 5)

tk.Label(frame, text="Izklaide", **label_style).grid(row=1, column=2)
listbox_fun = tk.Listbox(frame, width = 15, height = 8)
listbox_fun.grid(row = 2, column = 2, padx = 5, pady = 5)

tk.Label(frame, text="Citi", **label_style).grid(row=1, column=3)
listbox_else = tk.Listbox(frame, width = 15, height = 8)
listbox_else.grid(row = 2, column = 3, padx = 5, pady = 5)

#Ienakumu kategorija
tk.Label(frame, text="Ienākumi", **label_style).grid(row=1, column=4)
listbox_ienakumi = tk.Listbox(frame, width = 15, height = 8)
listbox_ienakumi.grid(row = 2, column = 4, padx = 5, pady = 5)

kategorija_menu = tk.OptionMenu(frame, kategorija_var, *kategorijas)
kategorija_menu.config(**option_style)
kategorija_menu.grid(row=0, column=4, padx=10, pady=5)

ieladet_failu()
root.mainloop()

