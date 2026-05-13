"""Demo: Using FASTA parser with DNA Sequence Analyzer"""

from analyzer import read_fasta, gc_content, reverse_complement, codon_frequency

# Read sequences from FASTA file
sequences = read_fasta("sample.fasta")

print("DNA Sequences loaded from FASTA file:")
print("=" * 50)

# Analyze each sequence
for seq_id, sequence in sequences.items():
    print("\nSequence ID: {0}".format(seq_id))
    print("Length: {0} bp".format(len(sequence)))
    print("Sequence: {0}...".format(sequence[:50]))  # First 50 bases
    print("-" * 50)
    
    # Analyze
    gc = gc_content(sequence)
    codons = codon_frequency(sequence)
    
    print("GC Content: {0:.2f}%".format(gc))
    print("Codon count: {0}".format(len(codons)))
    print("Top 3 codons:")
    
    # Sort codons by frequency
    sorted_codons = sorted(codons.items(), key=lambda x: x[1], reverse=True)
    for codon, count in sorted_codons[:3]:
        print("  {0}: {1}".format(codon, count))

print("\n" + "=" * 50)
print("Analysis complete!")
