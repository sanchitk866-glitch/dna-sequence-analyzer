from analyzer import gc_content

dna_sequence = "ATGCGC"

result = gc_content(dna_sequence)

print("GC Content: {:.2f}%".format(result))
