"""Unit tests for DNA Sequence Analyzer"""

from analyzer import gc_content, reverse_complement, codon_frequency, read_fasta, translate_to_protein, get_amino_acid_info, find_mutations, calculate_similarity, analyze_mutations, get_mutation_type

def test_gc_content():
    """Test GC content calculation"""
    # Test 1: 50% GC content
    assert round(gc_content("ATGC"), 2) == 50.0
    
    # Test 2: 100% GC content
    assert round(gc_content("GCGC"), 2) == 100.0
    
    # Test 3: 0% GC content
    assert round(gc_content("ATAT"), 2) == 0.0
    
    # Test 4: 66.67% GC content
    assert round(gc_content("ATGCGC"), 2) == 66.67
    
    print("PASSED: GC Content Tests")

def test_reverse_complement():
    """Test reverse complement calculation"""
    # Test 1: Simple sequence
    assert str(reverse_complement("ATGC")) == "GCAT"
    
    # Test 2: Another sequence
    assert str(reverse_complement("AAAA")) == "TTTT"
    
    # Test 3: Complex sequence
    assert str(reverse_complement("ATGCGTATGAAA")) == "TTTCATACGCAT"
    
    print("PASSED: Reverse Complement Tests")

def test_codon_frequency():
    """Test codon frequency calculation"""
    # Test 1: Simple sequence
    result = codon_frequency("ATGCGTATG")
    assert result == {"ATG": 2, "CGT": 1}
    
    # Test 2: Another sequence
    result = codon_frequency("ATGCGTATGAAA")
    assert result == {"ATG": 2, "CGT": 1, "AAA": 1}
    
    # Test 3: Single codon
    result = codon_frequency("ATG")
    assert result == {"ATG": 1}
    
    print("PASSED: Codon Frequency Tests")

def test_read_fasta():
    """Test FASTA file reading"""
    # Test 1: Read sample FASTA file
    sequences = read_fasta("sample.fasta")
    assert len(sequences) == 3
    assert "human_beta_globin" in sequences
    assert "mouse_beta_globin" in sequences
    assert "fruit_fly_hemoglobin" in sequences
    
    # Test 2: Check sequence content
    human_seq = sequences["human_beta_globin"]
    assert human_seq.startswith("ATGGTGCACC")
    assert len(human_seq) > 0
    
    # Test 3: Test nonexistent file
    empty_result = read_fasta("nonexistent.fasta")
    assert empty_result == {}
    
    print("PASSED: FASTA Parser Tests")

def test_translate_to_protein():
    """Test DNA to protein translation"""
    # Test 1: Simple sequence
    dna = "ATGGCTGAA"
    protein = translate_to_protein(dna)
    assert protein == "MAE"
    
    # Test 2: With stop codon
    dna = "ATGGCTTAA"  # TAA is stop codon
    protein = translate_to_protein(dna)
    assert protein == "MA*"
    
    # Test 3: Longer sequence
    dna = "ATGGTGCACCCTGACTCC"
    protein = translate_to_protein(dna)
    assert protein == "MVHPDS"
    
    print("PASSED: Translation Tests")

def test_get_amino_acid_info():
    """Test amino acid composition analysis"""
    # Test 1: Simple protein
    protein = "MVHPDT"
    composition = get_amino_acid_info(protein)
    assert composition['M'] == 1
    assert composition['V'] == 1
    assert composition['H'] == 1
    
    # Test 2: With repeats
    protein = "AAAAGG"
    composition = get_amino_acid_info(protein)
    assert composition['A'] == 4
    assert composition['G'] == 2
    
    print("PASSED: Amino Acid Info Tests")

def test_find_mutations():
    """Test mutation detection between two sequences"""
    # Test 1: Identical sequences
    seq1 = "ATGCGT"
    seq2 = "ATGCGT"
    assert find_mutations(seq1, seq2) == []
    
    # Test 2: Single mutation
    seq1 = "ATGCGT"
    seq2 = "ATGGGT"
    mutations = find_mutations(seq1, seq2)
    assert len(mutations) == 1
    assert mutations[0] == {'position': 3, 'seq1': 'C', 'seq2': 'G'}
    
    # Test 3: Multiple mutations
    seq1 = "ATGCGT"
    seq2 = "TTGAGT"
    mutations = find_mutations(seq1, seq2)
    assert len(mutations) == 2
    assert mutations[0] == {'position': 0, 'seq1': 'A', 'seq2': 'T'}
    assert mutations[1] == {'position': 3, 'seq1': 'C', 'seq2': 'A'}
    
    # Test 4: Different lengths
    seq1 = "ATGC"
    seq2 = "ATGCGT"
    assert find_mutations(seq1, seq2) == []
    
    print("PASSED: Mutation Detection Tests")

def test_calculate_similarity():
    """Test sequence similarity calculation"""
    # Test 1: Identical sequences
    assert round(calculate_similarity("ATGC", "ATGC"), 2) == 100.0
    
    # Test 2: Completely different
    assert round(calculate_similarity("ATGC", "CGTA"), 2) == 0.0
    
    # Test 3: 75% similar
    assert round(calculate_similarity("ATGC", "ATGA"), 2) == 75.0
    
    # Test 4: 50% similar
    assert round(calculate_similarity("ATGC", "TTTT"), 2) == 25.0
    
    print("PASSED: Similarity Calculation Tests")

def test_get_mutation_type():
    """Test mutation type classification"""
    # Transitions (purine to purine or pyrimidine to pyrimidine)
    assert get_mutation_type('A', 'G') == 'Transition'
    assert get_mutation_type('G', 'A') == 'Transition'
    assert get_mutation_type('C', 'T') == 'Transition'
    assert get_mutation_type('T', 'C') == 'Transition'
    
    # Transversions (purine to pyrimidine or vice versa)
    assert get_mutation_type('A', 'T') == 'Transversion'
    assert get_mutation_type('A', 'C') == 'Transversion'
    assert get_mutation_type('G', 'T') == 'Transversion'
    assert get_mutation_type('G', 'C') == 'Transversion'
    
    print("PASSED: Mutation Type Tests")

def test_analyze_mutations():
    """Test comprehensive mutation analysis"""
    # Test sickle cell mutation
    normal = "CTGAGGAGAAGTCTGCCGTT"
    sickle = "CTGTGGAGAAGTCTGCCGTT"
    
    analysis = analyze_mutations(normal, sickle)
    assert analysis['total_mutations'] == 1
    assert round(analysis['similarity_percent'], 2) == 95.0
    assert analysis['transversions'] == 1
    assert analysis['transitions'] == 0
    
    print("PASSED: Mutation Analysis Tests")

if __name__ == "__main__":
    test_gc_content()
    test_reverse_complement()
    test_codon_frequency()
    test_read_fasta()
    test_translate_to_protein()
    test_get_amino_acid_info()
    test_find_mutations()
    print("\nAll Tests Passed!")
