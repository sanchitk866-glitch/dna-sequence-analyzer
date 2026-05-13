"""Demo: Mutation Detector - Compare DNA sequences"""

from analyzer import analyze_mutations, get_mutation_type

# Example sequences (real genetic variants)
print("Mutation Detector Demo")
print("=" * 70)

# Example 1: Sickle cell anemia mutation
seq1_normal = "CTGAGGAGAAGTCTGCCGTT"
seq1_sickle = "CTGTGGAGAAGTCTGCCGTT"

print("\nExample 1: Sickle Cell Anemia Mutation")
print("Normal:     {0}".format(seq1_normal))
print("Sickle:     {0}".format(seq1_sickle))
print("-" * 70)

analysis = analyze_mutations(seq1_normal, seq1_sickle)

print("Analysis:")
print("  Sequence 1 length: {0} bp".format(analysis['seq1_length']))
print("  Sequence 2 length: {0} bp".format(analysis['seq2_length']))
print("  Total mutations: {0}".format(analysis['total_mutations']))
print("  Similarity: {0:.2f}%".format(analysis['similarity_percent']))
print("  Transitions: {0}".format(analysis['transitions']))
print("  Transversions: {0}".format(analysis['transversions']))

print("\nMutation Details:")
for mutation in analysis['mutations']:
    pos = mutation['position']
    from_base = mutation['seq1']
    to_base = mutation['seq2']
    mut_type = get_mutation_type(from_base, to_base)
    print("  Position {0}: {1} -> {2} ({3})".format(pos, from_base, to_base, mut_type))

# Example 2: Multiple mutations
print("\n" + "=" * 70)
print("\nExample 2: Multiple Mutations")

seq2_original = "ATGCGATCGATCG"
seq2_mutated  = "ATGCGATCGTTCG"

print("Original:   {0}".format(seq2_original))
print("Mutated:    {0}".format(seq2_mutated))
print("-" * 70)

analysis2 = analyze_mutations(seq2_original, seq2_mutated)

print("Analysis:")
print("  Total mutations: {0}".format(analysis2['total_mutations']))
print("  Similarity: {0:.2f}%".format(analysis2['similarity_percent']))
print("  Transitions: {0}".format(analysis2['transitions']))
print("  Transversions: {0}".format(analysis2['transversions']))

print("\nMutation Details:")
for mutation in analysis2['mutations']:
    pos = mutation['position']
    from_base = mutation['seq1']
    to_base = mutation['seq2']
    mut_type = get_mutation_type(from_base, to_base)
    print("  Position {0}: {1} -> {2} ({3})".format(pos, from_base, to_base, mut_type))

# Example 3: Visualize alignment
print("\n" + "=" * 70)
print("\nExample 3: Sequence Alignment Visualization")

seq3_seq1 = "ATGCGATCGATCGATCG"
seq3_seq2 = "ATGCGATXGATCGATCG"  # X is a mutation

print("Seq1:  {0}".format(seq3_seq1))

# Create visual alignment
alignment = ""
for i in range(len(seq3_seq1)):
    if seq3_seq1[i] == seq3_seq2[i]:
        alignment += "|"
    else:
        alignment += "X"

print("Match: {0}".format(alignment))
print("Seq2:  {0}".format(seq3_seq2))

print("\n" + "=" * 70)
print("Mutation detection complete!")
