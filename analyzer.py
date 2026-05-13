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