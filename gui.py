import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkcalendar import DateEntry
import os, json
import subprocess as sub
from datetime import datetime
import time
from shutil import copy
from pyembroidery import EmbPattern

from monogram import monogram


APPLICATION_FONT = "Courier"

platforms = {
    "mac": ("./fonts/", "./Monograms/")
}

readable = [
    'pes',
    'dst',
    'exp',
    'jef',
    'vp3',
    '10o',
    '100',
    'bro',
    'dat',
    'dsb',
    'dsz',
    'emd',
    'exy',
    'fxy',
    'gt',
    'hus',
    'inb',
    'jpx',
    'ksm',
    'max',
    'mit',
    'new',
    'pcd',
    'pcm',
    'pcq',
    'pcs',
    'pec',
    'phb',
    'phc',
    'sew',
    'shv',
    'stc',
    'stx',
    'tap',
    'tbf',
    'u01',
    'xxx',
    'zhs',
    'zxy',
    'gcode',
    'col',
    'edr',
    'inf',
    'pmv',
    'csv',
    'json'
]

writable = [
    'png',
    'pes',
    'svg',
    'dst',
    'exp',
    'jef',
    'vp3',
    'u01',
    'pec',
    'xxx',
    'gcode',
    'col',
    'edr',
    'inf',
    'pmv',
    'csv',
    'json',
    'txt'
]

class MonogramMagic():
    def __init__(self, parent):
        self.parent = parent
        self.platform = get_platform()
        self.font_dir = self.platform[0]
        self.fonts = sorted(os.listdir(self.font_dir))
        self.font_sizes = ["-"]

        self.label_font = (APPLICATION_FONT, 20)
        self.entry_font = (APPLICATION_FONT, 30)
        self.button_font = (APPLICATION_FONT, 12)

        self.cur_letter_search = ""
        self.cur_fonts_matching_search = []
        self.cur_match_index = 0
        self.notification_text = ""

        ### Start TK GUI
        self.parent.option_add("*TCombobox*Listbox*Font", self.entry_font)

        self.selected_font = tk.StringVar(self.parent)
        self.selected_font.set(self.fonts[0])

        self.selected_font_size = tk.StringVar(self.parent)
        self.selected_font_size.set("-")

        self.notification_text = tk.StringVar(self.parent)
        self.notification_text.set("")

        self.monogram_entry_label = tk.Label(self.parent, text="Monogram:")
        self.monogram_entry_label.config(font=self.label_font)
        self.monogram_entry_label.pack()

        self.monogram_entry = tk.Entry(self.parent, font=self.entry_font)
        self.monogram_entry.pack()

        self.font_select_label = tk.Label(self.parent, text="Font:")
        self.font_select_label.config(font=self.label_font)
        self.font_select_label.pack()

        self.font_select = ttk.Combobox(self.parent, textvariable=self.selected_font, values=self.fonts, width=50, font=self.label_font, state="readonly")
        self.font_select.bind('<<ComboboxSelected>>', self.set_sizes_for_selected_font)
        self.font_select.bind('<KeyRelease>', self.handle_font_search)
        self.font_select.pack()

        self.font_size_select_label = tk.Label(self.parent, text="Font Sizes:")
        self.font_size_select_label.config(font=self.label_font)
        self.font_size_select_label.pack()

        self.font_size_select = ttk.Combobox(self.parent, textvariable=self.selected_font_size, values=self.font_sizes, font=self.label_font, state="readonly")
        self.font_size_select.pack()

        self.spacer1 = tk.Label(self.parent, text="")
        self.spacer1.pack()

        self.create_file_butt = tk.Button(self.parent, command=self.run_monogram, text="Create File", height=4, width=20, pady=10, padx=10)
        self.create_file_butt.bind('<Return>', self.run_monogram)
        self.create_file_butt.config(font=self.button_font)
        self.create_file_butt.pack()

        self.show_success = tk.Label(self.parent, textvariable=self.notification_text, fg='#03AC13')
        self.show_success.config(font=self.label_font)
        self.show_success.pack()
        self.show_success.pack_forget()

        self.export_monograms_butt = tk.Button(self.parent, command=self.export_monograms, text="Export Monograms", height= 2, width=20, pady=10, padx=10)
        self.export_monograms_butt.config(font=self.button_font)
        self.export_monograms_butt.pack()

        self.spacer2 = tk.Label(self.parent, text="")
        self.spacer2.pack()

        self.update_butt = tk.Button(self.parent, command=self.run_update_script, text="Update Monogram Magic", height=1, width=50, pady=1, padx=1, fg="#DC143C")
        self.update_butt.config(font=self.button_font)
        self.update_butt.pack()

    def run_monogram(self, e=None):
        print("Font: " + self.selected_font.get())
        print("Monogram: " + self.monogram_entry.get())
        try:
            font_name, monogram_text, font_size = self.selected_font.get(), self.monogram_entry.get().replace(" ", ""), self.selected_font_size.get()
            res = monogram(font_name, monogram_text, font_size, self.platform)
            if res[0] == 'created':
                pat, filename = res[1], res[2]
                pat.write(filename)
                noti_text = f"File Saved: {monogram_text}-{font_name}-{font_size}"
            else:
                noti_text = f"File Exists: {monogram_text}-{font_name}-{font_size}"
            self.notification_text.set(noti_text)
            self.show_success.pack()
            self.parent.after(2100, self.show_success.pack_forget)
        except Exception as e:
            messagebox.showerror("Error", "Error in monogramming: {0}".format(e))

    def run_update_script(self):
        answer = tk.messagebox.askyesno("Update Monogram Magic", "Would you like to update Monogram Magic?")
        if answer:
            shell_var = "C:" in self.font_dir
            sub.call([os.path.join(platform[0], '..', 'updateAndBuild.sh'), os.path.join(platform[0], '..', 'gui.py')], shell=shell_var)
            tk.messagebox.showinfo("Update Successful", "Update was successful. Monogram Magic will close automatically after you click OK. Please restart to see updates.")
            self.parent.destroy()

    def set_sizes_for_selected_font(self, choice):
        self.selected_font_size.set('')
        self.font_size_select.set('')
        sizes = list()
        with open(os.path.join(self.font_dir, self.selected_font.get(), 'font_options.json')) as f:
            opt = json.load(f)
            sizes = list(opt["sizes"].values())
            self.font_size_select['values'] = sizes

    def handle_font_search(self, e):
        matches = [font for font in self.fonts if e.char.lower() == font[0].lower()]
        if self.cur_letter_search == e.char:
            if self.cur_match_index == len(matches) - 1:
                self.cur_match_index = 0
            else:
                self.cur_match_index += 1
        else:
            self.cur_match_index = 0
        self.cur_letter_search = e.char
        self.selected_font.set(matches[self.cur_match_index])
        self.set_sizes_for_selected_font(matches[self.cur_match_index])

    def export_monograms_to_folder(self):
        folder_selected = filedialog.askdirectory()
        oldest_export = datetime.combine(self.date_entry.get_date(), datetime.min.time())
        save_files = []
        for file in os.listdir(self.platform[1]):
            full_fp = os.path.join(self.platform[1], file)
            string_time = time.ctime(os.path.getmtime(full_fp))
            last_mod = datetime.strptime(string_time, "%a %b %d %H:%M:%S %Y")
            if last_mod <= self.today and last_mod >= oldest_export:
                save_files.append(file)
                copy(full_fp, folder_selected)
        self.export_window.destroy()
        self.notification_text.set(f"{len(save_files)} Files Copied to Folder: {folder_selected}")
        self.show_success.pack()
        self.parent.after(5000, self.show_success.pack_forget)

    def export_monograms(self):
        self.export_window = tk.Toplevel(self.parent)
        self.export_window.geometry('400x200')
        self.today = datetime.today()
        tk.Label(self.export_window, text="Select Oldest Export Date").pack()
        self.date_entry = DateEntry(self.export_window, selectmode='day', year=self.today.year, month=self.today.month, day=self.today.day, fg="black", bg="black")
        self.date_entry.pack(pady=10)
        tk.Button(self.export_window, text='Export Mongrams to Folder', command=self.export_monograms_to_folder).pack()


def get_platform():
    cwd = os.getcwd()
    if "Lori Odom" in cwd:
        return platforms["desktop_back"]
    if "Initially Yours" in cwd:
        return platforms["desktop_front"]
    if "colevick" in cwd:
        return platforms["mac"]
    elif "initi" in cwd:
        return platforms["new_lap"]
    else:
        return platforms["old_lap"]


class Converter():
    def __init__(self, parent):
        self.parent = parent

        self.label_font = (APPLICATION_FONT, 20)
        self.entry_font = (APPLICATION_FONT, 30)
        self.button_font = (APPLICATION_FONT, 12)

        ### Start TK GUI
        self.notification_text = tk.StringVar(self.parent)
        self.notification_text.set("")

        self.file_selected = tk.StringVar(self.parent)
        self.file_selected.set("")

        self.out_format_selected = tk.StringVar(self.parent)
        self.out_format_selected.set("")

        self.select_file_butt = tk.Button(self.parent, command=self.select_file, text="Select File to Convert", height=1, width=20, pady=10, padx=10)
        self.select_file_butt.config(font=self.button_font)
        self.select_file_butt.pack()

        self.show_selected = tk.Label(self.parent, textvariable=self.file_selected)
        self.show_selected.config(font=self.button_font)
        self.show_selected.pack()

        self.spacer2 = tk.Label(self.parent, text="")
        self.spacer2.pack()

        self.format_select_label = tk.Label(self.parent, text="Writable File Types:")
        self.format_select_label.config(font=self.label_font)
        self.format_select_label.pack()

        self.format_select = ttk.Combobox(self.parent, textvariable=self.out_format_selected, values=writable, width=25, font=self.label_font, state="readonly")
        self.format_select.pack()

        self.spacer1 = tk.Label(self.parent, text="")
        self.spacer1.pack()

        self.convert_butt = tk.Button(self.parent, command=self.convert, text="Convert", height=1, width=20, pady=10, padx=10)
        self.convert_butt.config(font=self.button_font)
        self.convert_butt.pack()

        self.show_success = tk.Label(self.parent, textvariable=self.notification_text, fg='#03AC13')
        self.show_success.config(font=self.button_font)
        self.show_success.pack()
        self.show_success.pack_forget()

    def select_file(self):
        f = filedialog.askopenfilename()
        self.file_selected.set(f)

    def convert(self):
        filename, extension = self.file_selected.get().split('.')
        if extension in readable:
            pattern = EmbPattern(self.file_selected.get())
            pattern.write(f"{filename}.{self.out_format_selected.get()}")
            self.notification_text.set(f"Wrote {filename}.{self.out_format_selected.get()}")
            self.show_success.pack()
            self.parent.after(5000, self.show_success.pack_forget)
        else:
            raise Exception("Cannot Read the {extension} filetype.")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x800")
    root.title("Monogram Magic")

    notebook = ttk.Notebook(root, width=800, height=800)
    notebook.pack(expand=True)

    f1 = tk.Frame(notebook, width=800, height=800, pady=25)
    f2 = tk.Frame(notebook, width=800, height=800, pady=25)

    mm = MonogramMagic(f1)
    f1.pack(fill="both", expand=True)

    converter = Converter(f2)
    f2.pack(fill="both", expand=True)

    notebook.add(f1, text="Monogram Magic")
    notebook.add(f2, text="File Converter")

    root.mainloop()

