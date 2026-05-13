from analyzer import gc_content, reverse_complement

dna_sequence = "ATGCGC"

gc_result = gc_content(dna_sequence)
reverse_result = reverse_complement(dna_sequence)

print("GC Content: {0:.2f}%".format(gc_result))
print("Reverse Complement: {0}".format(reverse_result))