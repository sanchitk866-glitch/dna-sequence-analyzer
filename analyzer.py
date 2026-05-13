from Bio.Seq import Seq

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

def gc_content(sequence):
    """Calculate GC content percentage of a DNA sequence"""
    g_count = sequence.count("G")
    c_count = sequence.count("C")
    
    gc_percentage = (float(g_count + c_count) / len(sequence)) * 100
    
    return gc_percentage

def reverse_complement(sequence):
    """Calculate reverse complement of a DNA sequence"""
    dna = Seq(sequence)
    return dna.reverse_complement()
def codon_frequency(sequence):
    """Calculate frequency of each codon in a DNA sequence"""
    codon_counts = {}

    for i in range(0, len(sequence), 3):
        codon = sequence[i:i+3]

        if len(codon) == 3:
            if codon in codon_counts:
                codon_counts[codon] += 1
            else:
                codon_counts[codon] = 1

    return codon_counts

def read_fasta(filename):
    """Read DNA sequences from a FASTA file
    
    Returns a dictionary with sequence IDs as keys and sequences as values
    """
    sequences = {}
    current_id = None
    current_seq = ""
    
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                
                if not line:
                    continue
                
                if line.startswith('>'):
                    # Save previous sequence if exists
                    if current_id is not None:
                        sequences[current_id] = current_seq
                    
                    # New sequence header
                    current_id = line[1:]  # Remove '>' character
                    current_seq = ""
                else:
                    # Add to current sequence
                    current_seq += line
            
            # Don't forget the last sequence
            if current_id is not None:
                sequences[current_id] = current_seq
        
        return sequences
    
    except IOError:
        print("Error: File not found!")
        return {}

def translate_to_protein(sequence):
    """Translate DNA sequence to protein (amino acid sequence)
    
    Converts a DNA sequence into amino acids using the genetic code.
    Stops at stop codon (*).
    """
    protein = ""
    
    # Process sequence in triplets (codons)
    for i in range(0, len(sequence) - 2, 3):
        codon = sequence[i:i+3].upper()
        
        # Check if codon is valid
        if codon in GENETIC_CODE:
            amino_acid = GENETIC_CODE[codon]
            protein += amino_acid
            
            # Stop if we hit a stop codon
            if amino_acid == '*':
                break
        else:
            # Unknown codon
            protein += 'X'
    
    return protein

def get_amino_acid_info(protein_sequence):
    """Get amino acid composition and information
    
    Returns a dictionary with counts of each amino acid.
    """
    aa_counts = {}
    
    for amino_acid in protein_sequence:
        if amino_acid in aa_counts:
            aa_counts[amino_acid] += 1
        else:
            aa_counts[amino_acid] = 1
    
    return aa_counts

def find_mutations(seq1, seq2):
    """Compare two sequences and find differences (mutations).
    
    Returns a list of dictionaries containing the position, original character,
    and mutated character for each difference.
    """
    mutations = []
    
    # Compare up to the length of the shorter sequence
    min_len = min(len(seq1), len(seq2))
    
    for i in range(min_len):
        if seq1[i] != seq2[i]:
            mutations.append({
                'position': i,
                'seq1': seq1[i],
                'seq2': seq2[i]
            })
            
    return mutations
