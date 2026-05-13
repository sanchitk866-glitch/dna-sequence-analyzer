from Bio.Seq import Seq

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