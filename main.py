from ttkbootstrap import Window, Frame, Label, Button, Entry, END, Treeview, Scrollbar, VERTICAL, WARNING, \
    SUCCESS, DANGER, OUTLINE, INFO
from tkinter.filedialog import askopenfilename
from ttkbootstrap.dialogs import Messagebox
import patoolib
from rarfile import RarFile
from zipfile import ZipFile

# Create Window
page = Window(title="Extract Zip File", themename="darkly")

page.geometry(f"{1200}x{700}")
page.minsize(width=800, height=600)
page.grid_columnconfigure(0, weight=1)
page.grid_rowconfigure(0, weight=1)

# Global path_address
path_address = None

# Global Item Treeview
tree_view = []

# Create Frame
frame = Frame(page)
frame.grid_columnconfigure(1, weight=1)
frame.grid_rowconfigure(2, weight=1)
frame.grid(row=0, column=0, sticky="nsew")

# Create Path Label and Choice File and Information Button and TreeView
path_label = Label(frame, text="Path  :")
path_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

path_entry = Entry(frame)
path_entry.grid(row=0, column=1, padx=(0, 10), pady=(10, 10), sticky="ew")


def file_dialog_clicked():
    global path_address
    path_entry.delete(0, END)
    FILE_TYPE = [("ZipFile & RarFile", "*.zip;*.rar")]
    path_address = askopenfilename(filetypes=FILE_TYPE)
    path_entry.insert(0, path_address)


def file_information_clicked():
    global path_address
    global tree_view

    for item in tree_view:
        tabel.delete(item)
    tree_view.clear()

    row_number = 1

    if not path_address:
        Messagebox.show_error(title="Error", message="Please Select Your Zip or Rar File", alert=True)

    if path_address:
        if path_address.endswith(".rar"):
            with RarFile(path_address, mode="r") as rar_file:
                for item in rar_file.namelist():
                    info = rar_file.getinfo(item)
                    items = tabel.insert("", END, text=str(row_number), values=(
                        info.filename,
                        f"{int(info.file_size // 1024)} KB"
                    ))
                    row_number += 1
                    tree_view.append(items)

                tabel.column("#0", width=150, anchor="w")
                for column in columns:
                    tabel.column(column, width=300, anchor="center")

        if path_address.endswith(".zip"):
            with ZipFile(path_address, mode="r") as zip_file:
                for item in zip_file.namelist():
                    info = zip_file.getinfo(item)
                    items = tabel.insert("", END, text=str(row_number), values=(
                        info.filename,
                        f"{int(info.file_size // 1024)} KB"
                    ))
                    row_number += 1
                    tree_view.append(items)

                tabel.column("#0", width=150, anchor="w")
                for column in columns:
                    tabel.column(column, width=300, anchor="center")


file_dialog_button = Button(frame, text="File Dialog", command=file_dialog_clicked, bootstyle=WARNING + OUTLINE)
file_dialog_button.grid(row=0, column=2, padx=(0, 10), pady=(10, 10))

file_information_button = Button(frame, text="Information", command=file_information_clicked,
                                 bootstyle=OUTLINE + SUCCESS)
file_information_button.grid(row=0, column=3, padx=(0, 10), pady=(10, 10))

# ScrollBar & Treeview

y_scrollbar = Scrollbar(frame, orient=VERTICAL, bootstyle=INFO)
y_scrollbar.grid(row=2, column=2, padx=(0, 10), pady=(10, 10), sticky="ns")

columns = ("path", "size")

tabel = Treeview(frame, columns=columns, yscrollcommand=y_scrollbar.set, bootstyle=INFO)

y_scrollbar.config(command=tabel.yview)

tabel.heading("#0", text="NO")
tabel.heading("path", text="Path")
tabel.heading("size", text="Size")

tabel.grid(row=2, column=1, padx=(0, 10), pady=(10, 10), sticky="nsew")

# Extract Part

extract_label = Label(frame, text="Extract  :")
extract_label.grid(row=1, column=0, padx=(10, 10), pady=(10, 10))

extract_entry = Entry(frame)
extract_entry.grid(row=1, column=1, padx=(0, 10), pady=(10, 10), sticky="ew")


def extract_button_clicked():
    global path_address
    extract_path = extract_entry.get()

    if not path_address:
        Messagebox.show_error(title="Error", message="Please Select Your Zip or Rar File", alert=True)

    if path_address:
        if extract_path == "" or extract_path == " ":
            Messagebox.show_error(title="Error", message="Please Enter Your Name Address", alert=True)

        else:
            if path_address.endswith(".rar"):
                patoolib.extract_archive(path_address, outdir=extract_path)
            if path_address.endswith(".zip"):
                with ZipFile(path_address, mode="r") as zip_file:
                    zip_file.extractall(extract_path)


extract_button = Button(frame, text="Extract", bootstyle=OUTLINE + DANGER, command=extract_button_clicked)
extract_button.grid(row=1, column=2, padx=(0, 10), pady=(10, 10))

page.mainloop()
