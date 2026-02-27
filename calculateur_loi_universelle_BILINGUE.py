import tkinter as tk
from tkinter import ttk, messagebox
import math

class LoiUniverselleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("G3 Lab - Universal Law Calculator (p-k) / Calculateur de Loi Universelle (p-k)")
        self.root.geometry("1000x900")
        
        # Liste des premiers pour les primorielles (n#)
        self.primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        
        # Langue par défaut
        self.lang = "fr"  # "en" ou "fr"
        
        # Textes multilingues
        self.texts = {
            "en": {
                "title": "Universal Law Calculator (p-k) - Monfette Law",
                "config_title": " Constellation Configuration (Monfette Law) ",
                "constellation_type": "Constellation Type:",
                "primorial_level": "Primorial Level (n#):",
                "modulo_current": "Current Modulo:",
                "generate_btn": "GENERATE COMPLETE ANALYSIS REPORT",
                "synthesis_title": " Universal Law (p-k) Synthesis ",
                "copy_btn": "Copy Report to Clipboard",
                "success": "Success",
                "copy_success": "Report successfully copied.",
                "warning": "Warning",
                "generate_first": "Please generate a report first.",
                "k1": "Regular (k=1) -> Law (p-1)",
                "k2": "Pairs: Sophie Germain / Safe / Twin (k=2) -> Law (p-2)",
                "k3": "Triplets (k=3) -> Law (p-3)",
                "k4": "Quadruplets (k=4) -> Law (p-4)",
                "k5": "Quintuplets (k=5) -> Law (p-5)",
                "author": "Author",
                "type": "Type",
                "structure": "Structure",
                "state": "Status",
                "admissible": "✓ ADMISSIBLE CONSTELLATION",
                "constrained": "⚠️ CONSTRAINED CONSTELLATION",
                "formula_title": "1. EXACT FORMULA",
                "count_title": "2. RESIDUE COUNT (EXACT DENSITY)",
                "euler_model": "Euler φ(n) Model [Regular, k=1]",
                "monfette_model": "Monfette Law (p-{}) [Constellation]",
                "ratio": "Monfette/Euler Ratio",
                "performance_title": "3. SIEVE PERFORMANCE ANALYSIS",
                "elimination_rate": "Elimination Rate",
                "speedup": "Speedup Factor",
                "interpretation": "Interpretation: By testing only {} valid residues instead of {} total candidates, we achieve a search space reduction of {:.2f}%.",
                "crypto_title": "4. CRYPTOGRAPHIC INTERPRETATION",
                "crypto_text": "In a cryptographic system (RSA, Diffie-Hellman) using this constellation:",
                "predictability": "Predictability",
                "effective_security": "Effective Security",
                "recommendation": "Recommendation",
                "viable": "Viable structure",
                "avoid": "Avoid this constellation",
                "compromised": "COMPROMISED",
                "reducible": "REDUCIBLE",
                "validation_title": "5. VALIDATION AND PRECISION",
                "theoretical_error": "Theoretical error: 0.000% (exact law, not heuristic)",
                "empirical_validation": "Empirical validation: Confirmed on 214,708,725 residues (P₁₀)",
                "references": "References: Chinese Remainder Theorem, Monfette Law (2025)",
                "conclusion_title": "6. CONCLUSION",
                "conclusion_text": "The (p-{}) law is an EXACT multiplicative combinatorial law.\nThe distribution is not random but deterministic.",
                "comparison_title": "7. CONSTELLATION COMPARISON (Level P_{})",
                "comparison_header": "Type                          k    Residues            Ratio      Speedup",
                "comparison_obs": "Observations:",
                "comparison_obs1": "• Higher k values reduce search space more",
                "comparison_obs2": "• Speedup grows exponentially with k",
                "comparison_obs3": "• Quintuplets (k=5) offer >99% reduction",
                "convergence_title": "8. RATIO CONVERGENCE Res(Pₙ)/φ(Pₙ) FOR k={}",
                "trend": "Trend",
                "decrease": "Decrease",
                "increase": "Increase",
                "convergence": "convergence",
                "insufficient_data": "Insufficient data",
                "convergence_interp": "Interpretation:",
                "convergence_obs1": "• Ratio Res(Pₙ)/φ(Pₙ) converges to a finite constant",
                "convergence_obs2": "• This convergence relates to Hardy-Littlewood constants",
                "convergence_obs3": "• For k=2: converges to C₂ ≈ 0.66 (twin constant)",
                "asymptotic_title": "9. ASYMPTOTIC FORMULA",
                "asymptotic_text": "For n → ∞, the ratio converges to:",
                "asymptotic_formula": "Res_k(Pₙ)/φ(Pₙ) → ∏(p>k) [(p-k)/(p-1)] × [correction factors]",
                "current_measure": "Your current measure (P_{}, k={}): {:.3f}%",
                "near_convergence": "Near convergence",
                "partial_convergence": "Partial convergence",
                "footer": "Generated by G3 Lab - Universal Law Calculator (p-k)",
                "copyright": "© 2025 Michel Monfette - All Rights Reserved",
                "selected": "SELECTED",
                "residues": "residues",
                "positions": "positions",
                "on": "on",
                "possible": "possible",
                "lang_switch": "Français"
            },
            "fr": {
                "title": "Calculateur de Loi Universelle (p-k) - Loi de Monfette",
                "config_title": " Configuration de la Constellation (Loi Monfette) ",
                "constellation_type": "Type de Constellation :",
                "primorial_level": "Niveau de Primorielle (n#) :",
                "modulo_current": "Modulo actuel :",
                "generate_btn": "GÉNÉRER LE RAPPORT D'ANALYSE COMPLET",
                "synthesis_title": " Synthèse de la Loi Universelle (p-k) ",
                "copy_btn": "Copier le Rapport dans le Presse-Papier",
                "success": "Succès",
                "copy_success": "Le rapport a été copié avec succès.",
                "warning": "Attention",
                "generate_first": "Veuillez d'abord générer un rapport.",
                "k1": "Ordinaires (k=1) -> Loi (p-1)",
                "k2": "Paires: Sophie Germain / Sûrs / Jumeaux (k=2) -> Loi (p-2)",
                "k3": "Triplets (k=3) -> Loi (p-3)",
                "k4": "Quadruplets (k=4) -> Loi (p-4)",
                "k5": "Quintuplets (k=5) -> Loi (p-5)",
                "author": "Auteur",
                "type": "Type",
                "structure": "Structure",
                "state": "État",
                "admissible": "✓ CONSTELLATION ADMISSIBLE",
                "constrained": "⚠️ CONSTELLATION CONTRAINTE",
                "formula_title": "1. FORMULE EXACTE",
                "count_title": "2. DÉNOMBREMENT DES RÉSIDUS (DENSITÉ EXACTE)",
                "euler_model": "Modèle Euler φ(n) [Ordinaires, k=1]",
                "monfette_model": "Loi Monfette (p-{}) [Constellation]",
                "ratio": "Ratio Monfette/Euler",
                "performance_title": "3. ANALYSE DE PERFORMANCE DU CRIBLE",
                "elimination_rate": "Taux d'élimination",
                "speedup": "Facteur d'accélération (Speedup)",
                "interpretation": "Interprétation : En testant uniquement les {} résidus valides au lieu des {} candidats totaux, on obtient une réduction de l'espace de recherche de {:.2f}%.",
                "crypto_title": "4. INTERPRÉTATION CRYPTOGRAPHIQUE",
                "crypto_text": "Dans un système cryptographique (RSA, Diffie-Hellman) utilisant cette constellation :",
                "predictability": "Prédictibilité",
                "effective_security": "Sécurité effective",
                "recommendation": "Recommandation",
                "viable": "Structure viable",
                "avoid": "Éviter cette constellation",
                "compromised": "COMPROMISE",
                "reducible": "RÉDUCTIBLE",
                "validation_title": "5. VALIDATION ET PRÉCISION",
                "theoretical_error": "Erreur théorique : 0.000% (loi exacte, non heuristique)",
                "empirical_validation": "Validation empirique : Confirmée sur 214 708 725 résidus (P₁₀)",
                "references": "Références : Théorème du Reste Chinois, Loi de Monfette (2025)",
                "conclusion_title": "6. CONCLUSION",
                "conclusion_text": "La loi (p-{}) est une loi combinatoire multiplicative EXACTE.\nLa distribution n'est pas aléatoire mais déterministe.",
                "comparison_title": "7. COMPARAISON ENTRE CONSTELLATIONS (Niveau P_{})",
                "comparison_header": "Type                          k    Résidus            Ratio      Speedup",
                "comparison_obs": "Observations :",
                "comparison_obs1": "• Plus k augmente, plus l'espace de recherche se réduit",
                "comparison_obs2": "• Le speedup croît exponentiellement avec k",
                "comparison_obs3": "• Les quintuplets (k=5) offrent une réduction de >99%",
                "convergence_title": "8. CONVERGENCE DU RATIO Res(Pₙ)/φ(Pₙ) POUR k={}",
                "trend": "Tendance",
                "decrease": "Décroissance",
                "increase": "Croissance",
                "convergence": "convergence",
                "insufficient_data": "Données insuffisantes",
                "convergence_interp": "Interprétation :",
                "convergence_obs1": "• Le ratio Res(Pₙ)/φ(Pₙ) converge vers une constante finie",
                "convergence_obs2": "• Cette convergence est liée aux constantes de Hardy-Littlewood",
                "convergence_obs3": "• Pour k=2 : converge vers C₂ ≈ 0.66 (constante des jumeaux)",
                "asymptotic_title": "9. FORMULE ASYMPTOTIQUE",
                "asymptotic_text": "Pour n → ∞, le ratio converge vers :",
                "asymptotic_formula": "Res_k(Pₙ)/φ(Pₙ) → ∏(p>k) [(p-k)/(p-1)] × [facteurs correctifs]",
                "current_measure": "Votre mesure actuelle (P_{}, k={}) : {:.3f}%",
                "near_convergence": "Proche de la convergence",
                "partial_convergence": "Convergence partielle",
                "footer": "Généré par G3 Lab - Calculateur Loi Universelle (p-k)",
                "copyright": "© 2025 Michel Monfette - Tous droits réservés",
                "selected": "SÉLECTIONNÉ",
                "residues": "résidus",
                "positions": "positions",
                "on": "sur",
                "possible": "possibles",
                "lang_switch": "English"
            }
        }
        
        self.setup_ui()

    def t(self, key):
        return self.texts[self.lang].get(key, key)

    def switch_language(self):
        self.lang = "fr" if self.lang == "en" else "en"
        self.refresh_ui()

    def refresh_ui(self):
        self.root.title("G3 Lab - " + self.t("title"))
        self.config_frame.config(text=self.t("config_title"))
        self.const_label.config(text=self.t("constellation_type"))
        self.level_lbl.config(text=self.t("primorial_level"))
        self.calc_btn.config(text=self.t("generate_btn"))
        self.res_frame.config(text=self.t("synthesis_title"))
        self.copy_btn.config(text=self.t("copy_btn"))
        self.lang_btn.config(text=self.t("lang_switch"))
        self.k_selector.config(values=[self.t("k1"), self.t("k2"), self.t("k3"), self.t("k4"), self.t("k5")])
        self.update_label()

    def setup_ui(self):
        style = ttk.Style()
        style.configure("Header.TLabel", font=("Helvetica", 12, "bold"))
        
        self.lang_btn = ttk.Button(self.root, text=self.t("lang_switch"), command=self.switch_language, width=10)
        self.lang_btn.pack(anchor="ne", padx=20, pady=5)
        
        self.config_frame = ttk.LabelFrame(self.root, text=self.t("config_title"), padding="15")
        self.config_frame.pack(fill="x", padx=20, pady=10)

        self.const_label = ttk.Label(self.config_frame, text=self.t("constellation_type"))
        self.const_label.grid(row=0, column=0, sticky="w")
        
        self.k_selector = ttk.Combobox(self.config_frame, values=[
            self.t("k1"), self.t("k2"), self.t("k3"), self.t("k4"), self.t("k5")
        ], width=55, state="readonly")
        self.k_selector.current(1)
        self.k_selector.grid(row=0, column=1, padx=10, pady=5)

        self.level_lbl = ttk.Label(self.config_frame, text=self.t("primorial_level"))
        self.level_lbl.grid(row=1, column=0, sticky="w")
        
        # Création du label d'affichage AVANT l'appel à update_label par le Scale
        self.level_label = ttk.Label(self.config_frame, text="", font=("Consolas", 10, "bold"))
        self.level_label.grid(row=1, column=2, padx=5)

        self.p_level = ttk.Scale(self.config_frame, from_=5, to=10, orient="horizontal", command=self.update_label)
        self.p_level.set(10)
        self.p_level.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.calc_btn = ttk.Button(self.root, text=self.t("generate_btn"), command=self.calculer_loi)
        self.calc_btn.pack(pady=10)

        self.res_frame = ttk.LabelFrame(self.root, text=self.t("synthesis_title"), padding="15")
        self.res_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.result_text = tk.Text(self.res_frame, font=("Consolas", 10), bg="#F4F7F9", relief="flat", padx=10, pady=10)
        self.result_text.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(self.res_frame, command=self.result_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.result_text.config(yscrollcommand=scrollbar.set)
        
        self.copy_btn = ttk.Button(self.root, text=self.t("copy_btn"), command=self.copy_report)
        self.copy_btn.pack(pady=10)
        
        self.update_label()

    def update_label(self, event=None):
        idx = int(float(self.p_level.get()))
        primorial = 1
        for i in range(idx): primorial *= self.primes[i]
        # Vérification de sécurité pour éviter l'erreur d'init
        if hasattr(self, 'level_label'):
            self.level_label.config(text=f"{self.t('modulo_current')} {primorial:,} ({self.primes[idx-1]}#)")

    def calculer_residus_pour_k(self, level, k):
        res = 1
        start_idx = 0 if k == 1 else 1
        for i in range(start_idx, level):
            p = self.primes[i]
            res *= max(0, p - k)
        return res

    def calculer_loi(self):
        k_str = self.k_selector.get()
        k = int(k_str.split('=')[1][0])
        level = int(float(self.p_level.get()))
        
        res_euler = 1
        primorial = 1
        for i in range(level):
            primorial *= self.primes[i]
            res_euler *= (self.primes[i] - 1)
            
        res_monfette = self.calculer_residus_pour_k(level, k)
        reduction = (1 - (res_monfette / res_euler)) * 100 if res_euler > 0 else 0
        speedup_val = res_euler / res_monfette if res_monfette > 0 else float('inf')
        speedup_str = f"×{speedup_val:,.2f}" if speedup_val != float('inf') else "×∞"

        self.result_text.delete("1.0", tk.END)
        status_msg = self.t("admissible") if res_monfette > 0 else self.t("constrained")
        
        report = f"""╔════════════════════════════════════════════════════════════════════╗
║  {self.t('title').upper().center(66)}║
╚════════════════════════════════════════════════════════════════════╝

{self.t('author')}       : Michel Monfette
{self.t('type')}         : {k_str}
{self.t('structure')}    : Primorielle {self.primes[level-1]}# (Modulo {primorial:,})
{self.t('state')}         : {status_msg}

────────────────────────────────────────────────────────────────────

{self.t('formula_title')}
   Res(P_{level}) = {res_monfette:,} (Exact)

{self.t('count_title')}
   • {self.t('euler_model')}  : {res_euler:,} {self.t('residues')}
   • {self.t('monfette_model').format(k)}   : {res_monfette:,} {self.t('residues')}
   
   {self.t('ratio')} : {res_monfette/res_euler*100:.3f}%

{self.t('performance_title')}
   • {self.t('elimination_rate')} : {reduction:.5f}%
   • {self.t('speedup')} : {speedup_str}
   
   {self.t('interpretation').format(f"{res_monfette:,}", f"{primorial:,}", reduction)}

{self.t('crypto_title')}
   {self.t('crypto_text')}
   
   • {self.t('predictability')} : {res_monfette:,} {self.t('positions')} sur {primorial:,}
   • {self.t('effective_security')} : {self.t('compromised') if res_monfette == 0 else self.t('reducible')}

────────────────────────────────────────────────────────────────────

{self.t('comparison_title').format(level)}
   {self.t('comparison_header')}
   ───────────────────────────────────────────────────────────────────────\n"""
        
        for k_comp in range(1, 6):
            res_k = self.calculer_residus_pour_k(level, k_comp)
            rat = (res_k/res_euler*100) if res_euler > 0 else 0
            sp = res_euler/res_k if res_k > 0 else float('inf')
            mark = f" ◄ {self.t('selected')}" if k_comp == k else ""
            report += f"   k={k_comp:<26} {res_k:>15,}  {rat:>7.2f}%   {f'x{sp:.1f}' if sp!=float('inf') else 'x∞':>8}{mark}\n"
        
        report += f"\n{self.t('convergence_title').format(k)}\n"
        for lvl in range(5, level + 1):
            rk = self.calculer_residus_pour_k(lvl, k)
            re = 1
            for j in range(lvl): re *= (self.primes[j]-1)
            ratio_lvl = (rk/re*100)
            bar = "█" * int(ratio_lvl * 0.4)
            report += f"   P{lvl:<2} ({self.primes[lvl-1]:>2}#) {bar:<40} {ratio_lvl:>5.2f}%\n"

        report += f"\n{self.t('footer')}\n{self.t('copyright')}"
        self.result_text.insert(tk.END, report)

    def copy_report(self):
        content = self.result_text.get("1.0", tk.END)
        if content.strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            messagebox.showinfo(self.t("success"), self.t("copy_success"))

if __name__ == "__main__":
    root = tk.Tk()
    app = LoiUniverselleApp(root)
    root.mainloop()
