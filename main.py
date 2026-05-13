from analyzer import (
    gc_content,
    reverse_complement,
    codon_frequency
)

dna_sequence = "ATGCGTATGAAA"

gc_result = gc_content(dna_sequence)
reverse_result = reverse_complement(dna_sequence)
codon_result = codon_frequency(dna_sequence)

print("GC Content: {0:.2f}%".format(gc_result))
print("Reverse Complement: {0}".format(reverse_result))
print("Codon Frequency: {0}".format(codon_result))