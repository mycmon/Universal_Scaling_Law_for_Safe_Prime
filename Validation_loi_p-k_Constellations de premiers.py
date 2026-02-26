import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from math import gcd
from functools import reduce
import openpyxl
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

# ==========================
# 1. Primes de base (primoriaux)
# ==========================

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

def primorial(n):
    """Produit des n premiers nombres premiers."""
    return reduce(lambda a, b: a * b, PRIMES[:n], 1)

# ==========================
# 2. Coeur de la loi (p-k)
# ==========================

def valid_residue_count(M, offsets):
    """
    Compte le nombre de résidus r mod M tels que
    pour tout offset c dans offsets, r + c est copremier avec M.
    """
    count = 0
    for r in range(M):
        ok = True
        for c in offsets:
            if gcd(r + c, M) != 1:
                ok = False
                break
        if ok:
            count += 1
    return count

def validate_law_pk(max_level, offsets):
    """
    Valide la loi Res(P_n * p_{n+1}) ≈ Res(P_n) * (p_{n+1} - k)
    Retourne une liste de dictionnaires.
    """
    results = []
    k = len(offsets)

    for n in range(2, max_level):
        Pn = primorial(n)
        p_next = PRIMES[n]
        Pn_next = Pn * p_next

        res_n = valid_residue_count(Pn, offsets)
        res_n1 = valid_residue_count(Pn_next, offsets)

        predicted = res_n * (p_next - k)

        if predicted != 0:
            rel_err = (res_n1 - predicted) / predicted
        else:
            rel_err = 0.0

        results.append({
            "n": n,
            "Pn": Pn,
            "p_next": p_next,
            "Pn_next": Pn_next,
            "res_n": res_n,
            "res_n1": res_n1,
            "predicted": predicted,
            "rel_err": rel_err
        })

    return results

# ==========================
# 3. Constellations prédéfinies
# ==========================

PRESETS = {
    "Jumeaux (0,2)": [0, 2],
    "Cousins (0,4)": [0, 4],
    "Sexy (0,6)": [0, 6],
    "Triplet (0,2,6)": [0, 2, 6],
    "Quadruplet (0,2,6,8)": [0, 2, 6, 8],
    "Quintuplet (0,2,6,8,12)": [0, 2, 6, 8, 12],  # exemple classique
}

# ==========================
# 4. GUI
# ==========================

class LawPKApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PMDT – Validation de la loi (p-k) et constellations")
        self.geometry("1300x750")

        self.results = []          # résultats du mode simple
        self.auto_results = {}     # résultats auto k
        self.compare_results = {}  # résultats comparatifs

        self.create_widgets()

    # ---------- Widgets principaux ----------

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Onglet 1 : Mode simple (une constellation)
        self.tab_simple = ttk.Frame(notebook)
        notebook.add(self.tab_simple, text="Constellation simple")

        # Onglet 2 : Analyse auto k=1..6
        self.tab_auto = ttk.Frame(notebook)
        notebook.add(self.tab_auto, text="Analyse auto k=1..6")

        # Onglet 3 : Analyse complète + graphiques
        self.tab_full = ttk.Frame(notebook)
        notebook.add(self.tab_full, text="Analyse complète + Graphiques")

        # Onglet 4 : Tableau comparatif
        self.tab_compare = ttk.Frame(notebook)
        notebook.add(self.tab_compare, text="Comparatif constellations")

        self.build_tab_simple()
        self.build_tab_auto()
        self.build_tab_full()
        self.build_tab_compare()

    # ---------- Onglet 1 : Constellation simple ----------

    def build_tab_simple(self):
        frame = self.tab_simple

        config_frame = ttk.LabelFrame(frame, text="Paramètres")
        config_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        ttk.Label(config_frame, text="Offsets (ex: 0,2 pour jumeaux) :").grid(row=0, column=0, sticky="w")
        self.offsets_entry = ttk.Entry(config_frame, width=40)
        self.offsets_entry.grid(row=0, column=1, sticky="w", padx=5)
        self.offsets_entry.insert(0, "0,2")

        ttk.Label(config_frame, text="Niveau primorial max (2..7) :").grid(row=1, column=0, sticky="w")
        self.level_spin = ttk.Spinbox(config_frame, from_=2, to=7, width=5)
        self.level_spin.grid(row=1, column=1, sticky="w", padx=5)
        self.level_spin.delete(0, tk.END)
        self.level_spin.insert(0, "6")

        ttk.Label(config_frame, text="Début (N) :").grid(row=2, column=0, sticky="w")
        self.start_entry = ttk.Entry(config_frame, width=20)
        self.start_entry.grid(row=2, column=1, sticky="w", padx=5)
        self.start_entry.insert(0, "800000000")

        ttk.Label(config_frame, text="Fin (N+H) :").grid(row=3, column=0, sticky="w")
        self.end_entry = ttk.Entry(config_frame, width=20)
        self.end_entry.grid(row=3, column=1, sticky="w", padx=5)
        self.end_entry.insert(0, "800500000")

        presets_frame = ttk.LabelFrame(frame, text="Constellations rapides")
        presets_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        for name, offs in PRESETS.items():
            ttk.Button(
                presets_frame,
                text=name,
                command=lambda o=offs: self.set_offsets(o)
            ).pack(side=tk.LEFT, padx=5)

        action_frame = ttk.Frame(frame)
        action_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        ttk.Button(action_frame, text="Valider la loi (p-k)", command=self.run_validation).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Exporter vers Excel", command=self.export_excel_simple).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Reset", command=self.reset_simple).pack(side=tk.LEFT, padx=5)

        results_frame = ttk.LabelFrame(frame, text="Résultats")
        results_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.text_simple = tk.Text(results_frame, wrap="none", font=("Consolas", 10))
        self.text_simple.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_y = ttk.Scrollbar(results_frame, orient="vertical", command=self.text_simple.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_simple.configure(yscrollcommand=scrollbar_y.set)

    def set_offsets(self, offsets):
        self.offsets_entry.delete(0, tk.END)
        self.offsets_entry.insert(0, ",".join(str(x) for x in offsets))

    def parse_offsets(self):
        s = self.offsets_entry.get().strip()
        if not s:
            raise ValueError("Veuillez entrer au moins un offset.")
        try:
            offsets = [int(x.strip()) for x in s.split(",")]
        except Exception:
            raise ValueError("Offsets invalides. Format : 0,2 ou 0,2,6.")
        return offsets

    def reset_simple(self):
        self.offsets_entry.delete(0, tk.END)
        self.offsets_entry.insert(0, "0,2")
        self.level_spin.delete(0, tk.END)
        self.level_spin.insert(0, "6")
        self.start_entry.delete(0, tk.END)
        self.start_entry.insert(0, "800000000")
        self.end_entry.delete(0, tk.END)
        self.end_entry.insert(0, "800500000")
        self.text_simple.delete("1.0", tk.END)
        self.results = []

    def run_validation(self):
        try:
            offsets = self.parse_offsets()
            max_level = int(self.level_spin.get())
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            return

        self.results = validate_law_pk(max_level, offsets)
        k = len(offsets)

        self.text_simple.delete("1.0", tk.END)
        self.text_simple.insert(tk.END, f"Validation de la loi (p-k) avec k = {k}, offsets = {offsets}\n\n")
        self.text_simple.insert(tk.END, f"{'n':>2}  {'Pn':>10}  {'p_{n+1}':>7}  {'Res(Pn)':>10}  {'Res(Pn*p)':>12}  {'Prédiction':>12}  {'Erreur rel.':>11}\n")
        self.text_simple.insert(tk.END, "-"*90 + "\n")

        for row in self.results:
            self.text_simple.insert(
                tk.END,
                f"{row['n']:>2}  {row['Pn']:>10}  {row['p_next']:>7}  {row['res_n']:>10}  {row['res_n1']:>12}  {row['predicted']:>12}  {row['rel_err']*100:>10.3f}%\n"
            )

    def export_excel_simple(self):
        if not self.results:
            messagebox.showerror("Erreur", "Aucun résultat à exporter.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if not file_path:
            return

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Loi_p_k_simple"

        headers = ["n", "Pn", "p_next", "Res(Pn)", "Res(Pn*p)", "Prédiction", "Erreur relative"]
        ws.append(headers)

        for row in self.results:
            ws.append([
                row["n"],
                row["Pn"],
                row["p_next"],
                row["res_n"],
                row["res_n1"],
                row["predicted"],
                row["rel_err"]
            ])

        wb.save(file_path)
        messagebox.showinfo("Succès", "Exportation Excel réussie (mode simple).")

    # ---------- Onglet 2 : Analyse auto k=1..6 ----------

    def build_tab_auto(self):
        frame = self.tab_auto

        config_frame = ttk.LabelFrame(frame, text="Paramètres auto k")
        config_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        ttk.Label(config_frame, text="Niveau primorial max (2..7) :").grid(row=0, column=0, sticky="w")
        self.auto_level_spin = ttk.Spinbox(config_frame, from_=2, to=7, width=5)
        self.auto_level_spin.grid(row=0, column=1, sticky="w", padx=5)
        self.auto_level_spin.delete(0, tk.END)
        self.auto_level_spin.insert(0, "6")

        ttk.Button(config_frame, text="Lancer analyse auto k=1..6", command=self.run_auto_k).grid(row=1, column=0, columnspan=2, pady=10)

        results_frame = ttk.LabelFrame(frame, text="Résultats auto k")
        results_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.text_auto = tk.Text(results_frame, wrap="none", font=("Consolas", 10))
        self.text_auto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_y = ttk.Scrollbar(results_frame, orient="vertical", command=self.text_auto.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_auto.configure(yscrollcommand=scrollbar_y.set)

    def run_auto_k(self):
        try:
            max_level = int(self.auto_level_spin.get())
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            return

        self.auto_results = {}
        self.text_auto.delete("1.0", tk.END)
        self.text_auto.insert(tk.END, "Analyse auto de la loi (p-k) pour k = 1..6\n\n")

        for k in range(1, 7):
            # offsets fictifs : [0,1,...,k-1] juste pour tester la loi (p-k)
            offsets = list(range(k))
            res = validate_law_pk(max_level, offsets)
            self.auto_results[k] = res

            self.text_auto.insert(tk.END, f"--- k = {k}, offsets = {offsets} ---\n")
            self.text_auto.insert(tk.END, f"{'n':>2}  {'Pn':>10}  {'p_{n+1}':>7}  {'Res(Pn)':>10}  {'Res(Pn*p)':>12}  {'Prédiction':>12}  {'Erreur rel.':>11}\n")
            self.text_auto.insert(tk.END, "-"*90 + "\n")
            for row in res:
                self.text_auto.insert(
                    tk.END,
                    f"{row['n']:>2}  {row['Pn']:>10}  {row['p_next']:>7}  {row['res_n']:>10}  {row['res_n1']:>12}  {row['predicted']:>12}  {row['rel_err']*100:>10.3f}%\n"
                )
            self.text_auto.insert(tk.END, "\n")

    # ---------- Onglet 3 : Analyse complète + Graphiques ----------

    def build_tab_full(self):
        frame = self.tab_full

        top_frame = ttk.LabelFrame(frame, text="Analyse complète et graphiques")
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        ttk.Label(top_frame, text="Niveau primorial max (2..7) :").grid(row=0, column=0, sticky="w")
        self.full_level_spin = ttk.Spinbox(top_frame, from_=2, to=7, width=5)
        self.full_level_spin.grid(row=0, column=1, sticky="w", padx=5)
        self.full_level_spin.delete(0, tk.END)
        self.full_level_spin.insert(0, "6")

        ttk.Button(top_frame, text="Analyser k=1..6 et tracer", command=self.run_full_analysis).grid(row=1, column=0, columnspan=2, pady=10)

        # Figure matplotlib
        fig = Figure(figsize=(7, 4), dpi=100)
        self.ax_line = fig.add_subplot(1, 2, 1)
        self.ax_3d = fig.add_subplot(1, 2, 2, projection='3d')

        self.canvas = FigureCanvasTkAgg(fig, master=frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def run_full_analysis(self):
        try:
            max_level = int(self.full_level_spin.get())
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            return

        # On réutilise auto_results pour k=1..6
        self.auto_results = {}
        for k in range(1, 7):
            offsets = list(range(k))
            res = validate_law_pk(max_level, offsets)
            self.auto_results[k] = res

        # Préparation des données pour graphiques
        ks = []
        ns = []
        errs = []

        for k, rows in self.auto_results.items():
            for row in rows:
                ks.append(k)
                ns.append(row["n"])
                errs.append(abs(row["rel_err"]))

        # Graphique 1 : courbe erreur max par k
        self.ax_line.clear()
        max_err_by_k = []
        for k in range(1, 7):
            rows = self.auto_results[k]
            max_err = max(abs(r["rel_err"]) for r in rows) if rows else 0.0
            max_err_by_k.append(max_err * 100)
        self.ax_line.plot(range(1, 7), max_err_by_k, marker="o")
        self.ax_line.set_xlabel("k")
        self.ax_line.set_ylabel("Erreur relative max (%)")
        self.ax_line.set_title("Erreur max de la loi (p-k) selon k")

        # Graphique 2 : 3D (n, k, |erreur|)
        self.ax_3d.clear()
        self.ax_3d.scatter(ns, ks, [e * 100 for e in errs], c=[e * 100 for e in errs], cmap="viridis")
        self.ax_3d.set_xlabel("n (niveau primorial)")
        self.ax_3d.set_ylabel("k")
        self.ax_3d.set_zlabel("|Erreur| (%)")
        self.ax_3d.set_title("Erreur relative de la loi (p-k)")

        self.canvas.draw()

    # ---------- Onglet 4 : Comparatif constellations ----------

    def build_tab_compare(self):
        frame = self.tab_compare

        config_frame = ttk.LabelFrame(frame, text="Comparatif constellations classiques")
        config_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        ttk.Label(config_frame, text="Niveau primorial max (2..7) :").grid(row=0, column=0, sticky="w")
        self.comp_level_spin = ttk.Spinbox(config_frame, from_=2, to=7, width=5)
        self.comp_level_spin.grid(row=0, column=1, sticky="w", padx=5)
        self.comp_level_spin.delete(0, tk.END)
        self.comp_level_spin.insert(0, "6")

        ttk.Button(config_frame, text="Générer tableau comparatif", command=self.run_compare).grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(config_frame, text="Exporter vers Excel", command=self.export_excel_compare).grid(row=2, column=0, columnspan=2, pady=5)

        results_frame = ttk.LabelFrame(frame, text="Tableau comparatif")
        results_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.text_compare = tk.Text(results_frame, wrap="none", font=("Consolas", 10))
        self.text_compare.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_y = ttk.Scrollbar(results_frame, orient="vertical", command=self.text_compare.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_compare.configure(yscrollcommand=scrollbar_y.set)

    def run_compare(self):
        try:
            max_level = int(self.comp_level_spin.get())
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            return

        self.compare_results = {}
        self.text_compare.delete("1.0", tk.END)

        self.text_compare.insert(tk.END, "Comparatif des constellations classiques (loi (p-k))\n\n")
        header = f"{'Nom':<20} {'k':>2}  {'Offsets':<20} {'Max err %':>10}\n"
        self.text_compare.insert(tk.END, header)
        self.text_compare.insert(tk.END, "-" * 70 + "\n")

        for name, offsets in PRESETS.items():
            res = validate_law_pk(max_level, offsets)
            self.compare_results[name] = {
                "offsets": offsets,
                "rows": res
            }
            max_err = max(abs(r["rel_err"]) for r in res) * 100 if res else 0.0
            line = f"{name:<20} {len(offsets):>2}  {str(offsets):<20} {max_err:>10.3f}\n"
            self.text_compare.insert(tk.END, line)

    def export_excel_compare(self):
        if not self.compare_results:
            messagebox.showerror("Erreur", "Aucun résultat comparatif à exporter.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if not file_path:
            return

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Comparatif_constellations"

        headers = ["Nom", "k", "Offsets", "n", "Pn", "p_next", "Res(Pn)", "Res(Pn*p)", "Prédiction", "Erreur relative"]
        ws.append(headers)

        for name, data in self.compare_results.items():
            offsets = data["offsets"]
            rows = data["rows"]
            k = len(offsets)
            for row in rows:
                ws.append([
                    name,
                    k,
                    str(offsets),
                    row["n"],
                    row["Pn"],
                    row["p_next"],
                    row["res_n"],
                    row["res_n1"],
                    row["predicted"],
                    row["rel_err"]
                ])

        wb.save(file_path)
        messagebox.showinfo("Succès", "Exportation Excel réussie (comparatif).")

# ==========================
# 5. Lancement
# ==========================

if __name__ == "__main__":
    app = LawPKApp()
    app.mainloop()
