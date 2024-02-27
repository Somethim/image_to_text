import tkinter as tk
from tkinter import ttk
from extract_text import EXTRACTED_WORDS, extract_text_from_images
import os
from tkinter import filedialog


def open_file_dialog():
    file_paths = filedialog.askopenfilenames(initialdir=os.path.expanduser('~'),
                                             filetypes=[("Image files", "*.png *.jpg *.jpeg *.tiff *.bmp *.gif")])
    return file_paths


def save_file_dialog():
    output_file_path = filedialog.asksaveasfilename(initialdir=os.path.expanduser('~'), defaultextension=".txt",
                                                    filetypes=[("Text files", "*.txt")], initialfile='extracted_text')
    return output_file_path


class TextExtractorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.extract_button = tk.Button(self.root, text="Extract Text", command=self.extract_text)
        self.progress_bar = ttk.Progressbar(self.root, length=200)
        self.text_preview = tk.Text(self.root)
        self.save_button = tk.Button(self.root, text="Save Text", command=self.save_text)
        self.modal_window = None

    def update_progress_bar(self, progress):
        self.progress_bar['value'] = progress
        self.root.update_idletasks()

    def create_modal_window(self):
        self.modal_window = tk.Toplevel(self.root)
        self.modal_window.transient(self.root)
        self.modal_window.overrideredirect(True)
        self.modal_window.grab_set()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 200
        window_height = 100
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.modal_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        self.modal_window.wait_visibility()
        self.modal_window.wm_attributes('-alpha', 0.5)
        extracting_label = tk.Label(self.modal_window, text="Extracting...", fg="white")
        extracting_label.pack()

    def disable_widgets(self):
        for child in self.root.winfo_children():
            if isinstance(child, (tk.Button, tk.Entry, tk.Text)):
                child.config(state='disabled')

    def enable_widgets(self):
        for child in self.root.winfo_children():
            if isinstance(child, (tk.Button, tk.Entry, tk.Text)):
                child.config(state='normal')

    def clear_text_preview(self):
        self.text_preview.delete('1.0', tk.END)

    def insert_extracted_words(self):
        self.text_preview.insert(tk.END, '\n'.join(EXTRACTED_WORDS))

    def extract_text(self):
        file_paths = open_file_dialog()
        if file_paths:
            self.create_modal_window()
            self.disable_widgets()
            extract_text_from_images(file_paths, self.update_progress_bar)
            self.enable_widgets()
            self.modal_window.destroy()
            self.clear_text_preview()
            self.insert_extracted_words()

    def save_text(self):
        output_file_path = save_file_dialog()
        if output_file_path:
            with open(output_file_path, 'w') as file:
                for sentence in EXTRACTED_WORDS:
                    file.write(sentence + '\n')
        EXTRACTED_WORDS.clear()
        self.text_preview.delete('1.0', tk.END)

    def run(self):
        self.progress_bar.pack()
        self.extract_button.pack()
        self.text_preview.pack()
        self.save_button.pack()
        self.root.mainloop()
