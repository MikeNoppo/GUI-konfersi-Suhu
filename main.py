import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib import pyplot as plt
import csv
from theme import Theme

class SuhuConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Konversi Suhu Interaktif")
        self.theme = Theme(self.root)
        self.history = []
        self.filtered_history = []
        self.create_widgets()

    def create_widgets(self):
        # Label untuk input suhu
        label_input = ttk.Label(self.root, text="Masukkan Suhu:")
        label_input.grid(column=0, row=0, padx=10, pady=5, sticky='W')

        # Entry input
        self.entry_input = tk.Entry(self.root)
        self.entry_input.grid(column=1, row=0, padx=10, pady=5, sticky='EW')

        # Widget Slider
        self.slider_input = ttk.Scale(self.root, from_=-273, to=1000, orient='horizontal', command=self.update_slider_value)
        self.slider_input.grid(column=2, row=0, padx=5, pady=5)

        # Combo box untuk jenis konversi
        self.conversion_combobox = ttk.Combobox(self.root, values=[
            "Celsius ke Fahrenheit",
            "Fahrenheit ke Celsius",
            "Celsius ke Kelvin",
            "Kelvin ke Celsius",
            "Fahrenheit ke Kelvin",
            "Kelvin ke Fahrenheit",
            "Celsius ke Rankine",
            "Celsius ke Reaumur"
        ])
        self.conversion_combobox.grid(column=0, row=1, columnspan=3, padx=10, pady=5, sticky='EW')
        self.conversion_combobox.current(0)

        # Tombol konversi
        button_convert = ttk.Button(self.root, text="Konversi", command=self.convert_temperature)
        button_convert.grid(column=0, row=2, padx=10, pady=5)

        # Tombol Plot Graph
        button_graph = ttk.Button(self.root, text="Plot Graph", command=self.plot_graph)
        button_graph.grid(column=1, row=2, padx=10, pady=5)

        # Tambahkan tombol untuk mengubah tema
        button_change_color = ttk.Button(self.root, text="Change Colors", command=self.theme.open_color_picker)
        button_change_color.grid(column=2, row=2, padx=10, pady=5)

        # Tombol Ekspor CSV
        button_csv = ttk.Button(self.root, text="Export to CSV", command=self.export_to_csv)
        button_csv.grid(column=0, row=3, padx=10, pady=5)

        # Tombol Bantuan
        button_help = ttk.Button(self.root, text="Show Help", command=self.show_help)
        button_help.grid(column=1, row=3, padx=10, pady=5)

        # Label hasil
        self.label_result = ttk.Label(self.root, text="Hasil: ")
        self.label_result.grid(column=0, row=4, columnspan=3, padx=10, pady=5)

        # Textbox untuk penjelasan perhitungan
        self.text_explanation = tk.Text(self.root, height=7, width=70, state=tk.DISABLED, wrap='word')
        self.text_explanation.grid(column=0, row=5, columnspan=3, padx=10, pady=5, sticky='EW')

        # Entry untuk pencarian
        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(column=0, row=6, padx=10, pady=5, sticky='EW')
        button_search = ttk.Button(self.root, text="Search", command=self.apply_filter)
        button_search.grid(column=1, row=6, padx=5, pady=5)

        # Box untuk riwayat
        self.listbox_history = tk.Listbox(self.root, height=5)
        self.listbox_history.grid(column=0, row=7, columnspan=3, padx=10, pady=5, sticky='EW')

        # Grid konfigurasi
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(6, weight=1)

        self.apply_theme()

    def update_slider_value(self, value):
        self.entry_input.delete(0, tk.END)
        self.entry_input.insert(0, str(round(float(value), 2)))

    def apply_filter(self):
        search_term = self.search_entry.get().lower()
        self.filtered_history = [entry for entry in self.history if search_term in entry.lower()]
        self.update_listbox(self.filtered_history)

    def convert_temperature(self):
        temp_input = self.validate_input()
        if temp_input is None:
            return

        conversion_type = self.conversion_combobox.get()
        if conversion_type == "Celsius ke Fahrenheit":
            result, explanation = self.celsius_to_fahrenheit(temp_input)
        elif conversion_type == "Fahrenheit ke Celsius":
            result, explanation = self.fahrenheit_to_celsius(temp_input)
        
        # (Sebagian besar sama...)

        self.label_result.config(text=f"Hasil: {result:.2f}")
        self.text_explanation.config(state=tk.NORMAL)
        self.text_explanation.delete(1.0, tk.END)
        self.text_explanation.insert(tk.END, explanation)
        self.text_explanation.config(state=tk.DISABLED)

        history_entry = f"{temp_input} {conversion_type.split()[0]} = {result:.2f} {conversion_type.split()[-1]}"
        self.update_history(history_entry)

    def update_history(self, conversion_result):
        self.history.append(conversion_result)
        self.update_listbox(self.history)

    def update_listbox(self, entries):
        self.listbox_history.delete(0, tk.END)
        for item in entries:
            self.listbox_history.insert(tk.END, item)

    def apply_theme(self):
        self.theme.apply_to_widgets(self.entry_input, self.text_explanation)

    def show_help(self):
        messagebox.showinfo("Bantuan", "Masukkan suhu secara langsung di entry atau gunakan slider, pilih jenis konversi, lalu klik 'Konversi'.\n"
                                       "Gunakan 'Plot Graph' untuk melihat grafik suhu.\n"
                                       "Gunakan 'Export to CSV' untuk menyimpan riwayat konversi.\n"
                                       "Gunakan kotak teks pencarian untuk menyaring riwayat.")

    def export_to_csv(self):
        data = self.history
        if not data:
            messagebox.showerror("Export Error", "Tidak ada data untuk diekspor.")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension='.csv',
                                                 filetypes=[('CSV files', '*.csv'), ('All Files', '*.*')],
                                                 title="Save File As")
        if file_path:
            try:
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Input Suhu', 'Unit Dari', 'Output Suhu', 'Unit Ke'])
                    for row in data:
                        writer.writerow(row.split())
                messagebox.showinfo("Export Success", "Riwayat berhasil diekspor.")
            except Exception as e:
                messagebox.showerror("Export Error", f"Gagal mengekspor data: {e}")

    def plot_graph(self):
        if not self.history:
            messagebox.showwarning("No Data", "Tidak ada data di riwayat untuk dipetakan.")
            return

        temps = [float(item.split()[0]) for item in self.history]
        plt.plot(temps, label='Converted Temperatures', marker='o')
        plt.title('Temperature Conversion History')
        plt.xlabel('Conversion Number')
        plt.ylabel('Temperature')
        plt.legend()
        plt.grid(True)
        plt.show()

    def validate_input(self):
        try:
            temp_input = float(self.entry_input.get())
            return temp_input
        except ValueError:
            messagebox.showerror("Input Error", "Silakan masukkan nilai numerik yang valid.")
            return None

    def convert_temperature(self):
        temp_input = self.validate_input()
        if temp_input is None:
            return

        conversion_type = self.conversion_combobox.get()
        if conversion_type == "Celsius ke Fahrenheit":
            result, explanation = self.celsius_to_fahrenheit(temp_input)
        elif conversion_type == "Fahrenheit ke Celsius":
            result, explanation = self.fahrenheit_to_celsius(temp_input)
        elif conversion_type == "Celsius ke Kelvin":
            result, explanation = self.celsius_to_kelvin(temp_input)
        elif conversion_type == "Kelvin ke Celsius":
            result, explanation = self.kelvin_to_celsius(temp_input)
        elif conversion_type == "Fahrenheit ke Kelvin":
            result, explanation = self.fahrenheit_to_kelvin(temp_input)
        elif conversion_type == "Kelvin ke Fahrenheit":
            result, explanation = self.kelvin_to_fahrenheit(temp_input)
        elif conversion_type == "Celsius ke Rankine":
            result, explanation = self.celsius_to_rankine(temp_input)
        elif conversion_type == "Celsius ke Reaumur":
            result, explanation = self.celsius_to_reaumur(temp_input)
        else:
            result = "Pilihan tidak valid."
            explanation = ""

        self.label_result.config(text=f"Hasil: {result:.2f}")
        self.text_explanation.config(state=tk.NORMAL)
        self.text_explanation.delete(1.0, tk.END)
        self.text_explanation.insert(tk.END, explanation)
        self.text_explanation.config(state=tk.DISABLED)

        self.update_history(f"{temp_input} {conversion_type.split()[0]} = {result:.2f} {conversion_type.split()[-1]}")

    def update_history(self, conversion_result):
        self.history.append(conversion_result)
        self.listbox_history.delete(0, tk.END)
        for item in self.history:
            self.listbox_history.insert(tk.END, item)

    def celsius_to_fahrenheit(self, celsius):
        fahrenheit = (celsius * 9/5) + 32
        explanation = (
            f"Rumus: (C × 9/5) + 32\n"
            f"Langkah 1: {celsius} × 9/5 = {celsius * 9/5}\n"
            f"Langkah 2: {celsius * 9/5} + 32 = {fahrenheit:.2f}"
        )
        return fahrenheit, explanation

    def fahrenheit_to_celsius(self, fahrenheit):
        celsius = (fahrenheit - 32) * 5/9
        explanation = (
            f"Rumus: (F - 32) × 5/9\n"
            f"Langkah 1: {fahrenheit} - 32 = {fahrenheit - 32}\n"
            f"Langkah 2: ({fahrenheit - 32}) × 5/9 = {celsius:.2f}"
        )
        return celsius, explanation

    def celsius_to_kelvin(self, celsius):
        kelvin = celsius + 273.15
        explanation = (
            f"Rumus: C + 273.15\n"
            f"Langkah 1: {celsius} + 273.15 = {kelvin:.2f}"
        )
        return kelvin, explanation

    def kelvin_to_celsius(self, kelvin):
        celsius = kelvin - 273.15
        explanation = (
            f"Rumus: K - 273.15\n"
            f"Langkah 1: {kelvin} - 273.15 = {celsius:.2f}"
        )
        return celsius, explanation

    def fahrenheit_to_kelvin(self, fahrenheit):
        celsius = (fahrenheit - 32) * 5/9
        kelvin = celsius + 273.15
        explanation = (
            f"Rumus: (F - 32) × 5/9 + 273.15\n"
            f"Langkah 1: (F - 32) × 5/9 = {celsius:.2f}\n"
            f"Langkah 2: {celsius:.2f} + 273.15 = {kelvin:.2f}"
        )
        return kelvin, explanation

    def kelvin_to_fahrenheit(self, kelvin):
        celsius = kelvin - 273.15
        fahrenheit = (celsius * 9/5) + 32
        explanation = (
            f"Rumus: (K - 273.15) × 9/5 + 32\n"
            f"Langkah 1: K - 273.15 = {celsius:.2f}\n"
            f"Langkah 2: ({celsius:.2f}) × 9/5 + 32 = {fahrenheit:.2f}"
        )
        return fahrenheit, explanation

    def celsius_to_rankine(self, celsius):
        rankine = (celsius + 273.15) * 9/5
        explanation = (
            f"Rumus: (C + 273.15) × 9/5\n"
            f"Langkah 1: C + 273.15 = {celsius + 273.15}\n"
            f"Langkah 2: ({celsius + 273.15}) × 9/5 = {rankine:.2f}"
        )
        return rankine, explanation

    def celsius_to_reaumur(self, celsius):
        reaumur = celsius * 4/5
        explanation = (
            f"Rumus: C × 4/5\n"
            f"Langkah 1: {celsius} × 4/5 = {reaumur:.2f}"
        )
        return reaumur, explanation

if __name__ == "__main__":
    root = tk.Tk()
    app = SuhuConverterApp(root)
    root.mainloop()