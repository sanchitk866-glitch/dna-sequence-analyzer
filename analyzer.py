import re
from Bio.Seq import Seq
from Bio.Align import PairwiseAligner

# Standard genetic code table (codon -> amino acid)
GENETIC_CODE = {
    'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
    'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
    'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
    'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
}

# Amino acid full names
AMINO_ACID_NAMES = {
    'A': 'Alanine', 'R': 'Arginine', 'N': 'Asparagine', 'D': 'Aspartic acid',
    'C': 'Cysteine', 'Q': 'Glutamine', 'E': 'Glutamic acid', 'G': 'Glycine',
    'H': 'Histidine', 'I': 'Isoleucine', 'L': 'Leucine', 'K': 'Lysine',
    'M': 'Methionine', 'F': 'Phenylalanine', 'P': 'Proline', 'S': 'Serine',
    'T': 'Threonine', 'W': 'Tryptophan', 'Y': 'Tyrosine', 'V': 'Valine',
    '*': 'Stop'
}

def validate_sequence(sequence):
    """Sanitizes sequence and validates it contains only ATGC."""
    seq = re.sub(r'[\s\d]', '', sequence.upper())
    seq = seq.replace('U', 'T')
    
    invalid_chars = set(seq) - set('ATGC')
    if invalid_chars:
        raise ValueError(f"Invalid characters detected: {', '.join(invalid_chars)}. Only A, T, G, C allowed.")
    
    return seq

def gc_content(sequence):
    """Calculate GC content percentage of a DNA sequence"""
    g_count = sequence.count("G")
    c_count = sequence.count("C")
    if len(sequence) == 0: return 0.0
    return (float(g_count + c_count) / len(sequence)) * 100

def reverse_complement(sequence):
    """Calculate reverse complement of a DNA sequence"""
    dna = Seq(sequence)
    return str(dna.reverse_complement())

def codon_frequency(sequence):
    """Calculate frequency of each codon in a DNA sequence"""
    codon_counts = {}
    for i in range(0, len(sequence), 3):
        codon = sequence[i:i+3]
        if len(codon) == 3:
            codon_counts[codon] = codon_counts.get(codon, 0) + 1
    return codon_counts

def translate_to_protein(sequence):
    """Translate DNA sequence to protein (amino acid sequence)"""
    protein = ""
    for i in range(0, len(sequence) - 2, 3):
        codon = sequence[i:i+3].upper()
        if codon in GENETIC_CODE:
            aa = GENETIC_CODE[codon]
            protein += aa
            if aa == '*': break
        else:
            protein += 'X'
    return protein

def get_amino_acid_info(protein_sequence):
    """Get amino acid composition and information"""
    aa_counts = {}
    for amino_acid in protein_sequence:
        aa_counts[amino_acid] = aa_counts.get(amino_acid, 0) + 1
    return aa_counts

def calculate_tm(sequence):
    """Calculate melting temperature (Tm) for a primer sequence."""
    a_count = sequence.count('A')
    t_count = sequence.count('T')
    g_count = sequence.count('G')
    c_count = sequence.count('C')
    return 2 * (a_count + t_count) + 4 * (g_count + c_count)

def find_orfs(sequence, min_protein_length=20):
    """Finds the longest Open Reading Frame (ORF) in all 6 frames."""
    longest_orf = {"length": 0, "dna": "", "protein": "", "frame": None, "strand": None}
    dna_seq = Seq(sequence)
    
    for strand, nuc in [(1, dna_seq), (-1, dna_seq.reverse_complement())]:
        for frame in range(3):
            length = len(nuc) - frame
            trans = str(nuc[frame:frame + length - (length % 3)].translate(to_stop=False))
            
            start_indices = [m.start() for m in re.finditer('M', trans)]
            for start in start_indices:
                stop = trans.find('*', start)
                if stop != -1:
                    prot_len = stop - start
                    if prot_len >= min_protein_length and prot_len > longest_orf["length"]:
                        prot_seq = trans[start:stop]
                        dna_start = frame + start * 3
                        dna_end = frame + stop * 3 + 3
                        dna_orf = str(nuc)[dna_start:dna_end]
                        longest_orf = {
                            "length": prot_len,
                            "dna": dna_orf,
                            "protein": prot_seq,
                            "frame": f"{'+' if strand == 1 else '-'}{frame + 1}",
                            "strand": "Forward" if strand == 1 else "Reverse Complement"
                        }
                        
    if longest_orf["length"] == 0:
        return None
    return longest_orf

def find_mutations(seq1, seq2):
    """Compare two sequences using Needleman-Wunsch alignment."""
    aligner = PairwiseAligner()
    aligner.mode = 'global'
    aligner.match_score = 2
    aligner.mismatch_score = -1
    aligner.open_gap_score = -2
    aligner.extend_gap_score = -0.5
    
    alignments = aligner.align(seq1, seq2)
    if not alignments:
        return {"alignment": None, "mutations": []}
        
    best_alignment = alignments[0]
    lines = str(best_alignment).strip().split('\n')
    if len(lines) >= 3:
        aligned_seq1 = lines[0]
        match_line = lines[1]
        aligned_seq2 = lines[2]
    else:
        return {"alignment": None, "mutations": []}

    mutations = []
    
    # For effect calculation, we assume seq1 is coding from frame 1
    for i in range(len(aligned_seq1)):
        c1 = aligned_seq1[i]
        c2 = aligned_seq2[i]
        match_char = match_line[i]
        
        if match_char != '|':
            if c1 == '-':
                mut_type = "Insertion"
                effect = "Frameshift"
            elif c2 == '-':
                mut_type = "Deletion"
                effect = "Frameshift"
            else:
                mut_type = "Substitution"
                codon_start = (i // 3) * 3
                if codon_start + 3 <= len(aligned_seq1) and '-' not in aligned_seq1[codon_start:codon_start+3]:
                    ref_codon = aligned_seq1[codon_start:codon_start+3]
                    tgt_codon = aligned_seq2[codon_start:codon_start+3]
                    if '-' not in tgt_codon:
                        ref_aa = GENETIC_CODE.get(ref_codon, 'X')
                        tgt_aa = GENETIC_CODE.get(tgt_codon, 'X')
                        if ref_aa == tgt_aa:
                            effect = "Silent"
                        elif tgt_aa == '*':
                            effect = "Nonsense"
                        else:
                            effect = f"Missense ({ref_aa} -> {tgt_aa})"
                    else:
                        effect = "In-frame indel or frameshift"
                else:
                    effect = "Unknown"
            
            mutations.append({
                "position": i + 1, # 1-based index for biologist users
                "ref": c1,
                "target": c2,
                "type": mut_type,
                "effect": effect
            })

    return {
        "alignment": {
            "ref": aligned_seq1,
            "match": match_line,
            "target": aligned_seq2
        },
        "mutations": mutations
    }
