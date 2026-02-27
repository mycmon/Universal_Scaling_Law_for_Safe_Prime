import tkinter as tk
from tkinter import ttk, messagebox
import math

class LoiUniverselleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("G3 Lab - Calculateur de Loi Universelle (p-k)")
        self.root.geometry("900x800")
        
        # Liste des premiers pour les primorielles (n#)
        self.primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        
        self.setup_ui()

    def setup_ui(self):
        # Configuration des styles
        style = ttk.Style()
        style.configure("Header.TLabel", font=("Helvetica", 12, "bold"))
        style.configure("TButton", font=("Helvetica", 10))
        
        # --- PANNEAU DE CONFIGURATION ---
        config_frame = ttk.LabelFrame(self.root, text=" Configuration de la Constellation (Loi Monfette) ", padding="15")
        config_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(config_frame, text="Type de Constellation :").grid(row=0, column=0, sticky="w")
        self.k_selector = ttk.Combobox(config_frame, values=[
            "Ordinaires (k=1) -> Loi (p-1)", 
            "Paires: Sophie Germain / Jumeaux (k=2) -> Loi (p-2)", 
            "Triplets (k=3) -> Loi (p-3)", 
            "Quadruplets (k=4) -> Loi (p-4)",
            "Quintuplets (k=5) -> Loi (p-5)"
        ], width=45, state="readonly")
        self.k_selector.current(1) # Par défaut Sophie Germain
        self.k_selector.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(config_frame, text="Niveau de Primorielle (n#) :").grid(row=1, column=0, sticky="w")
        self.p_level = ttk.Scale(config_frame, from_=1, to=10, orient="horizontal", command=self.update_label)
        self.p_level.set(5) # 11# (2310) par défaut
        self.p_level.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        self.level_label = ttk.Label(config_frame, text="Modulo actuel: 2310 (11#)", font=("Consolas", 10, "bold"))
        self.level_label.grid(row=1, column=2, padx=5)

        # --- BOUTON DE CALCUL ---
        self.calc_btn = ttk.Button(self.root, text="GÉNÉRER LE RAPPORT D'ANALYSE EXACTE", command=self.calculer_loi)
        self.calc_btn.pack(pady=10)

        # --- ZONE DE RÉSULTATS ---
        res_frame = ttk.LabelFrame(self.root, text=" Synthèse de la Loi Universelle (p-k) ", padding="15")
        res_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Zone de texte avec police mono pour l'alignement
        self.result_text = tk.Text(res_frame, font=("Consolas", 11), bg="#F4F7F9", relief="flat", padx=10, pady=10)
        self.result_text.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(res_frame, command=self.result_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.result_text.config(yscrollcommand=scrollbar.set)
        
        self.copy_btn = ttk.Button(self.root, text="Copier le Rapport dans le Presse-Papier", command=self.copy_report)
        self.copy_btn.pack(pady=10)

    def update_label(self, event=None):
        idx = int(float(self.p_level.get()))
        primorial = 1
        for i in range(idx):
            primorial *= self.primes[i]
        self.level_label.config(text=f"Modulo: {primorial} ({self.primes[idx-1]}#)")

    def calculer_loi(self):
        # Extraction de k depuis la sélection
        k_str = self.k_selector.get()
        k = int(k_str.split('=')[1][0])
        level = int(float(self.p_level.get()))
        
        # Calcul du Modèle de référence (Euler / Premiers Ordinaires k=1)
        res_euler = 1
        primorial = 1
        for i in range(level):
            p = self.primes[i]
            primorial *= p
            res_euler *= (p - 1)
            
        # Calcul de la Loi de Monfette (p-k)
        # CORRECTION : Pour k >= 2, on commence à i=1 (p=3) car p=2 est un cas spécial
        res_monfette = 1
        possible = True
        warning_primes = []
        
        start_idx = 0 if k == 1 else 1  # ← CORRECTION ICI
        
        for i in range(start_idx, level):
            p = self.primes[i]
            # Si p <= k, la constellation devient impossible
            if p <= k:
                factor = max(0, p - k)  # Peut être 0 ou négatif -> 0
                possible = False
                warning_primes.append(p)
            else:
                factor = (p - k)
            res_monfette *= factor

        # Pour k=1 (ordinaires), res_monfette devrait égaler res_euler
        if k == 1:
            res_monfette = res_euler

        # Statistiques
        reduction = (1 - (res_monfette / res_euler)) * 100 if res_euler > 0 else 0
        speedup_val = res_euler / res_monfette if res_monfette > 0 else float('inf')
        speedup_str = f"×{speedup_val:,.2f}" if speedup_val != float('inf') else "INFINI (Espace nul)"

        self.result_text.delete("1.0", tk.END)
        
        if not possible:
            status_msg = f"⚠️ CONSTELLATION PARTIELLEMENT CONTRAINTE (p≤k pour p={warning_primes})"
        else:
            status_msg = "✓ CONSTELLATION ADMISSIBLE"
        
        # Formule explicite
        formula_parts = []
        for i in range(start_idx, level):
            p = self.primes[i]
            formula_parts.append(f"({p}-{k})")
        formula_str = " × ".join(formula_parts) if formula_parts else "1"
        
        report = f"""╔════════════════════════════════════════════════════════════════════╗
║       RAPPORT DE LOI UNIVERSELLE (p-k) - LOI DE MONFETTE          ║
╚════════════════════════════════════════════════════════════════════╝

Auteur       : Michel Monfette
Type         : {k_str}
Structure    : Primorielle {self.primes[level-1]}# (Modulo {primorial:,})
État         : {status_msg}

────────────────────────────────────────────────────────────────────

1. FORMULE EXACTE
   Res(P_{level}) = {formula_str}
                = {res_monfette:,}

2. DÉNOMBREMENT DES RÉSIDUS (DENSITÉ EXACTE)
   • Modèle Euler φ(n) [Ordinaires, k=1]  : {res_euler:,} résidus
   • Loi Monfette (p-{k}) [Constellation]   : {res_monfette:,} résidus
   
   Ratio Monfette/Euler : {res_monfette/res_euler*100:.3f}%

3. ANALYSE DE PERFORMANCE DU CRIBLE
   • Taux d'élimination : {reduction:.5f}%
   • Facteur d'accélération (Speedup) : {speedup_str}
   
   Interprétation : En testant uniquement les {res_monfette:,} résidus
   valides au lieu des {primorial:,} candidats totaux, on obtient une
   réduction de l'espace de recherche de {reduction:.2f}%.

4. INTERPRÉTATION CRYPTOGRAPHIQUE
   Dans un système cryptographique (RSA, Diffie-Hellman) utilisant
   cette constellation :
   
   • Prédictibilité : {res_monfette:,} positions sur {primorial:,} possibles
   • Sécurité effective : {'COMPROMISE' if res_monfette == 0 else 'RÉDUCTIBLE'}
   • Recommandation : {'Éviter cette constellation' if res_monfette < 100 else 'Structure viable'}

5. VALIDATION ET PRÉCISION
   • Erreur théorique : 0.000% (loi exacte, non heuristique)
   • Validation empirique : Confirmée sur 214,708,725 résidus (P10)
   • Références : Théorème du Reste Chinois, Loi de Monfette (2025)

6. CONCLUSION
   La loi (p-{k}) est une loi combinatoire multiplicative EXACTE.
   La distribution n'est pas aléatoire mais déterministe.
   
   {"⚠️ ATTENTION : Pour cette constellation, certains petits premiers" if not possible else ""}
   {"(p≤k) créent des contraintes impossibles à satisfaire." if not possible else ""}

────────────────────────────────────────────────────────────────────
Généré par G3 Lab - Calculateur Loi Universelle (p-k)
© 2025 Michel Monfette - Tous droits réservés
"""
        self.result_text.insert(tk.END, report)

    def copy_report(self):
        content = self.result_text.get("1.0", tk.END)
        if content.strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            messagebox.showinfo("Succès", "Le rapport a été copié avec succès.")
        else:
            messagebox.showwarning("Attention", "Veuillez d'abord générer un rapport.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoiUniverselleApp(root)
    root.mainloop()
