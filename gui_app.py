import customtkinter as ctk
import json
from analyzer import (
    gc_content, 
    reverse_complement, 
    codon_frequency, 
    translate_to_protein,
    get_amino_acid_info,
    find_mutations
)

class GeneScopeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GeneScope - DNA Sequence Analyzer")
        self.geometry("900x700")
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self.header_label = ctk.CTkLabel(self, text="GeneScope Analyzer", font=ctk.CTkFont(family="Inter", size=24, weight="bold"))
        self.header_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Tabview
        self.tabview = ctk.CTkTabview(self, width=860, height=600)
        self.tabview.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        self.tabview.add("Single Sequence")
        self.tabview.add("Mutation Detector")

        # Configure tab grids
        self.tabview.tab("Single Sequence").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Single Sequence").grid_rowconfigure(4, weight=1)
        
        self.tabview.tab("Mutation Detector").grid_columnconfigure((0, 1), weight=1)
        self.tabview.tab("Mutation Detector").grid_rowconfigure(4, weight=1)

        self.setup_single_sequence_tab()
        self.setup_mutation_detector_tab()

    def setup_single_sequence_tab(self):
        tab = self.tabview.tab("Single Sequence")

        # Input
        self.seq_label = ctk.CTkLabel(tab, text="DNA Sequence:", font=ctk.CTkFont(weight="bold"))
        self.seq_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
        
        self.seq_textbox = ctk.CTkTextbox(tab, height=100)
        self.seq_textbox.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="ew")

        # Options
        self.options_frame = ctk.CTkFrame(tab)
        self.options_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
        self.opt_gc = ctk.CTkCheckBox(self.options_frame, text="GC Content")
        self.opt_gc.grid(row=0, column=0, padx=20, pady=10)
        self.opt_gc.select()
        
        self.opt_rev = ctk.CTkCheckBox(self.options_frame, text="Reverse Complement")
        self.opt_rev.grid(row=0, column=1, padx=20, pady=10)
        self.opt_rev.select()
        
        self.opt_codon = ctk.CTkCheckBox(self.options_frame, text="Codon Frequency")
        self.opt_codon.grid(row=0, column=2, padx=20, pady=10)
        
        self.opt_trans = ctk.CTkCheckBox(self.options_frame, text="Translate to Protein")
        self.opt_trans.grid(row=0, column=3, padx=20, pady=10)

        # Button
        self.analyze_btn = ctk.CTkButton(tab, text="Analyze Sequence", command=self.analyze_single)
        self.analyze_btn.grid(row=3, column=0, padx=10, pady=10)

        # Output
        self.res_label = ctk.CTkLabel(tab, text="Results:", font=ctk.CTkFont(weight="bold"))
        self.res_label.grid(row=4, column=0, sticky="w", padx=10, pady=(10, 0))
        
        self.res_textbox = ctk.CTkTextbox(tab, height=250, state="disabled")
        self.res_textbox.grid(row=5, column=0, padx=10, pady=(5, 10), sticky="nsew")

    def setup_mutation_detector_tab(self):
        tab = self.tabview.tab("Mutation Detector")

        # Input 1
        self.ref_label = ctk.CTkLabel(tab, text="Reference Sequence:", font=ctk.CTkFont(weight="bold"))
        self.ref_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
        
        self.ref_textbox = ctk.CTkTextbox(tab, height=100)
        self.ref_textbox.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="ew")

        # Input 2
        self.tgt_label = ctk.CTkLabel(tab, text="Target Sequence:", font=ctk.CTkFont(weight="bold"))
        self.tgt_label.grid(row=0, column=1, sticky="w", padx=10, pady=(10, 0))
        
        self.tgt_textbox = ctk.CTkTextbox(tab, height=100)
        self.tgt_textbox.grid(row=1, column=1, padx=10, pady=(5, 10), sticky="ew")

        # Button
        self.compare_btn = ctk.CTkButton(tab, text="Compare Sequences", command=self.compare_sequences)
        self.compare_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Output
        self.mut_label = ctk.CTkLabel(tab, text="Comparison Results:", font=ctk.CTkFont(weight="bold"))
        self.mut_label.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 0))
        
        self.mut_textbox = ctk.CTkTextbox(tab, height=300, state="disabled", font=("Courier New", 12))
        self.mut_textbox.grid(row=4, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="nsew")

    def write_result(self, textbox, text):
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.insert("0.0", text)
        textbox.configure(state="disabled")

    def analyze_single(self):
        sequence = self.seq_textbox.get("1.0", "end-1c").strip().upper()
        if not sequence:
            self.write_result(self.res_textbox, "Error: No sequence provided.")
            return

        results = []
        try:
            if self.opt_gc.get():
                results.append(f"GC Content: {round(gc_content(sequence), 2)}%")
            if self.opt_rev.get():
                results.append(f"Reverse Complement:\n{reverse_complement(sequence)}\n")
            if self.opt_codon.get():
                freq = codon_frequency(sequence)
                freq_str = "\n".join([f"  {k}: {v}" for k, v in freq.items()])
                results.append(f"Codon Frequency:\n{freq_str}\n")
            if self.opt_trans.get():
                prot = translate_to_protein(sequence)
                results.append(f"Protein Translation:\n{prot}\n")

            self.write_result(self.res_textbox, "\n\n".join(results))
        except Exception as e:
            self.write_result(self.res_textbox, f"Error: {str(e)}")

    def compare_sequences(self):
        seq1 = self.ref_textbox.get("1.0", "end-1c").strip().upper()
        seq2 = self.tgt_textbox.get("1.0", "end-1c").strip().upper()

        if not seq1 or not seq2:
            self.write_result(self.mut_textbox, "Error: Both sequences are required.")
            return

        try:
            mutations = find_mutations(seq1, seq2)
            header = f"Seq1 Length: {len(seq1)} | Seq2 Length: {len(seq2)} | Total Mutations: {len(mutations)}\n"
            header += "-" * 50 + "\n\n"
            
            if mutations:
                lines = [f"{'Pos':<6} | {'Ref':<5} | {'Target':<6}"]
                lines.append("-" * 25)
                for m in mutations:
                    lines.append(f"{m['position'] + 1:<6} | {m['seq1']:<5} | {m['seq2']:<6}")
                self.write_result(self.mut_textbox, header + "\n".join(lines))
            else:
                self.write_result(self.mut_textbox, header + "No mutations detected. The sequences are identical up to the compared length.")
        except Exception as e:
            self.write_result(self.mut_textbox, f"Error: {str(e)}")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = GeneScopeApp()
    app.mainloop()
