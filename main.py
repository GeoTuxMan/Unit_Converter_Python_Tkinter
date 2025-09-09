import tkinter as tk
from tkinter import ttk

# Center window
def center(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    win.geometry(f"{width}x{height}+{x}+{y}")

# ---------------- INTRO ---------------- #
class Intro:
    def __init__(self, root):
        self.root = root
        self.root.title("Unit Converter - Intro")
        self.root.configure(bg="#008080")
        self.root.resizable(False, False)
        center(self.root, 400, 200)

        tk.Label(
            self.root,
            text="Welcome to Unit Converter!",
            font=("Arial", 16, "bold"),
            bg="#008080", fg="white"
        ).pack(pady=30)

        tk.Button(
            self.root,
            text="START",
            font=("Arial", 12, "bold"),
            bg="white", fg="black",
            command=self.open_converter
        ).pack(pady=20)

    def open_converter(self):
        self.root.withdraw()
        top = tk.Toplevel()
        Converter(top)

# ---------------- CONVERTER ---------------- #
class Converter:
    def __init__(self, win):
        self.win = win
        self.win.title("Unit Converter")
        self.win.resizable(False, False)
        center(self.win, 500, 400)

        # Dictionary
        self.conversions = {
            "Length": {
                "m": 1, "km": 1000, "cm": 0.01, "mm": 0.001
            },
            "Mass": {
                "kg": 1, "g": 0.001, "lb": 0.453592, "ton": 1000
            },
            "Speed": {
                "m/s": 1, "km/h": 1000/3600, "mph": 0.44704
            },
            "Time": {
                "sec": 1, "min": 60, "hour": 3600
            },
            "Temperature": None  # special
        }

        # categories
        tk.Label(self.win, text="Choose category:", font=("Arial", 12)).pack(pady=10)
        self.category = ttk.Combobox(self.win, values=list(self.conversions.keys()), state="readonly")
        self.category.current(0)
        self.category.pack(pady=5)
        self.category.bind("<<ComboboxSelected>>", self.update_units)

        # Units
        frame = tk.Frame(self.win)
        frame.pack(pady=15)

        self.from_val = tk.DoubleVar()
        tk.Entry(frame, textvariable=self.from_val, font=("Arial", 12), width=10).grid(row=0, column=0, padx=5)

        self.from_unit = ttk.Combobox(frame, state="readonly", width=10)
        self.from_unit.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="→", font=("Arial", 14, "bold")).grid(row=0, column=2, padx=5)

        self.to_unit = ttk.Combobox(frame, state="readonly", width=10)
        self.to_unit.grid(row=0, column=3, padx=5)

        # Buton Convert
        tk.Button(self.win, text="Convert", font=("Arial", 12, "bold"),
                  command=self.convert).pack(pady=10)

        # Result
        self.result_lbl = tk.Label(self.win, text="", font=("Arial", 14, "bold"), fg="blue")
        self.result_lbl.pack(pady=15)

        self.update_units()

    def update_units(self, event=None):
        category = self.category.get()
        if category == "Temperature":
            units = ["Celsius", "Fahrenheit", "Kelvin"]
        else:
            units = list(self.conversions[category].keys())

        self.from_unit["values"] = units
        self.to_unit["values"] = units
        self.from_unit.current(0)
        self.to_unit.current(1)

    def convert(self):
        category = self.category.get()
        val = self.from_val.get()
        from_u = self.from_unit.get()
        to_u = self.to_unit.get()

        if category == "Temperature":
            result = self.convert_temperature(val, from_u, to_u)
        else:
            base = val * self.conversions[category][from_u]
            result = base / self.conversions[category][to_u]

        self.result_lbl.config(text=f"{val} {from_u} = {result:.4f} {to_u}")

    def convert_temperature(self, val, from_u, to_u):
        # convert to Kelvin at base
        if from_u == "Celsius":
            k = val + 273.15
        elif from_u == "Fahrenheit":
            k = (val - 32) * 5/9 + 273.15
        else:  # Kelvin
            k = val

        if to_u == "Celsius":
            return k - 273.15
        elif to_u == "Fahrenheit":
            return (k - 273.15) * 9/5 + 32
        else:
            return k

# ---------------- MAIN ---------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = Intro(root)
    root.mainloop()
