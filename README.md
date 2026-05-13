# DNA Sequence Analyzer

A beginner bioinformatics project built using Python and Biopython. Analyze DNA sequences with three key functions.

## Features

- **GC Content Calculation** - Calculate the percentage of G and C bases in a DNA sequence
- **Reverse Complement Generator** - Generate the reverse complement of a DNA sequence
- **Codon Frequency Analyzer** - Count the frequency of each codon in a DNA sequence

## Installation

### Prerequisites
- Python 2.7 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/sanchitk866-glitch/dna-sequence-analyzer.git
cd dna-sequence-analyzer
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Mac/Linux:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Example

```python
from analyzer import gc_content, reverse_complement, codon_frequency

dna = "ATGCGTATGAAA"

# Calculate GC content
gc = gc_content(dna)
print("GC Content: {0:.2f}%".format(gc))  # Output: 33.33%

# Get reverse complement
rev_comp = reverse_complement(dna)
print("Reverse Complement: {0}".format(rev_comp))  # Output: TTTCATACGCAT

# Count codon frequency
codons = codon_frequency(dna)
print("Codon Frequency: {0}".format(codons))  # Output: {'ATG': 2, 'AAA': 1, 'CGT': 1}
```

### Run Main Program

```bash
python main.py
```

### Run Tests

```bash
python test_analyzer.py
```

## Functions

### gc_content(sequence)
Calculates the GC content (percentage of G and C bases) in a DNA sequence.

**Parameters:**
- `sequence` (str): DNA sequence string (e.g., "ATGC")

**Returns:**
- (float): GC content percentage (0-100)

**Example:**
```python
gc_content("ATGCGC")  # Returns 66.67
```

### reverse_complement(sequence)
Generates the reverse complement of a DNA sequence.

**Parameters:**
- `sequence` (str): DNA sequence string

**Returns:**
- (Seq): Reverse complement sequence

**Example:**
```python
reverse_complement("ATGC")  # Returns GCAT
```

### codon_frequency(sequence)
Counts the frequency of each codon (3-base group) in a DNA sequence.

**Parameters:**
- `sequence` (str): DNA sequence string

**Returns:**
- (dict): Dictionary of codon frequencies

**Example:**
```python
codon_frequency("ATGCGTATG")  # Returns {'ATG': 2, 'CGT': 1}
```

## Project Structure

```
dna-sequence-analyzer/
│
├── .venv/                  # Virtual environment
├── main.py                 # Main program
├── analyzer.py             # Analysis functions
├── test_analyzer.py        # Unit tests
├── requirements.txt        # Project dependencies
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## Technologies Used

- **Python** - Programming language
- **Biopython** - Bioinformatics library for DNA manipulation
- **VS Code** - Code editor

## Biology Background

### GC Content
GC content refers to the percentage of Guanine (G) and Cytosine (C) bases in a DNA sequence. Higher GC content means the DNA is more stable and resistant to heat.

### Reverse Complement
In DNA, bases pair as: A↔T and G↔C. The reverse complement is used to find the complementary strand of DNA.

### Codons
A codon is a sequence of three DNA bases that encode a specific amino acid. Codon frequency analysis helps understand gene expression patterns.

## Future Improvements

- Add FASTA file support for reading DNA sequences
- RNA transcription function
- Protein translation from DNA
- Mutation detection
- Web interface using Flask
- GUI using Tkinter

## Learning Outcomes

By completing this project, you'll learn:
- Python functions and modules
- Working with strings and dictionaries
- Using external libraries (Biopython)
- Unit testing with pytest
- Git version control
- Basic bioinformatics concepts

## License

This project is open source and available under the MIT License.

## Author

Built as a beginner bioinformatics learning project.
