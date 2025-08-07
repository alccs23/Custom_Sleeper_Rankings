import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from fantasy_utils import get_draft_pick_names, get_filtered_fantasy_rankings

class FantasyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fantasy Football Best Available Players")
        self.geometry("800x600")

        self.draft_id_var = tk.StringVar()
        self.csv_path_var = tk.StringVar()
        self.format_var = tk.StringVar(value="Standard")

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Sleeper Draft ID:").pack(pady=(10, 0))
        ttk.Entry(self, textvariable=self.draft_id_var, width=50).pack()

        ttk.Label(self, text="Rankings CSV File:").pack(pady=(10, 0))
        file_frame = ttk.Frame(self)
        file_frame.pack()
        ttk.Entry(file_frame, textvariable=self.csv_path_var, width=50).pack(side=tk.LEFT)
        ttk.Button(file_frame, text="Browse", command=self.browse_file).pack(side=tk.LEFT, padx=5)

        ttk.Label(self, text="Rankings Format:").pack(pady=(10, 0))
        format_dropdown = ttk.OptionMenu(
            self, self.format_var, "Standard", "Standard", "BC"
        )
        format_dropdown.pack()

        ttk.Button(self, text="Get Best Available List", command=self.get_best_available).pack(pady=10)

        self.listbox = tk.Listbox(self, height=25, width=100)
        self.listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

    def browse_file(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if path:
            self.csv_path_var.set(path)

    def get_best_available(self):
        draft_id = self.draft_id_var.get().strip()
        csv_path = self.csv_path_var.get().strip()
        mode = self.format_var.get().strip().lower()

        if not draft_id or not csv_path:
            messagebox.showerror("Input Error", "Please enter both Draft ID and CSV file path.")
            return

        self.listbox.delete(0, tk.END)
        self.listbox.insert(tk.END, "Fetching draft picks...")

        try:
            drafted_names = get_draft_pick_names(draft_id)
            filtered_rankings = get_filtered_fantasy_rankings(csv_path, drafted_names, mode=mode)
            self.listbox.delete(0, tk.END)

            if not filtered_rankings:
                self.listbox.insert(tk.END, "No available players found or all players drafted.")
            else:
                for player in filtered_rankings:
                    self.listbox.insert(tk.END, player)
        except Exception as e:
            self.listbox.delete(0, tk.END)
            self.listbox.insert(tk.END, f"Error: {e}")

if __name__ == "__main__":
    app = FantasyApp()
    app.mainloop()

