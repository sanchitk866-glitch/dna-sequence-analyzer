"""Unit tests for DNA Sequence Analyzer"""

from analyzer import gc_content, reverse_complement, codon_frequency

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

if __name__ == "__main__":
    test_gc_content()
    test_reverse_complement()
    test_codon_frequency()
    print("\nAll Tests Passed!")
