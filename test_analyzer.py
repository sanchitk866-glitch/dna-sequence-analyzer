"""Unit tests for DNA Sequence Analyzer"""

from analyzer import gc_content, reverse_complement, codon_frequency, read_fasta, translate_to_protein, get_amino_acid_info

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

if __name__ == "__main__":
    test_gc_content()
    test_reverse_complement()
    test_codon_frequency()
    test_read_fasta()
    test_translate_to_protein()
    test_get_amino_acid_info()
    print("\nAll Tests Passed!")
