"""Demo: Protein Translation from DNA sequences"""

from analyzer import read_fasta, translate_to_protein, get_amino_acid_info, AMINO_ACID_NAMES

# Read sequences from FASTA file
sequences = read_fasta("sample.fasta")

print("Protein Translation from DNA")
print("=" * 60)

# Translate each sequence
for seq_id, sequence in sequences.items():
    print("\nSequence: {0}".format(seq_id))
    print("DNA length: {0} bp".format(len(sequence)))
    
    # Translate to protein
    protein = translate_to_protein(sequence)
    
    print("Protein length: {0} amino acids".format(len(protein)))
    print("Protein sequence: {0}".format(protein))
    print("-" * 60)
    
    # Amino acid composition
    aa_info = get_amino_acid_info(protein)
    
    print("Amino acid composition:")
    for aa, count in sorted(aa_info.items()):
        full_name = AMINO_ACID_NAMES.get(aa, "Unknown")
        print("  {0} ({1}): {2}".format(aa, full_name, count))

print("\n" + "=" * 60)
print("Translation complete!")
