from flask import Flask, render_template, request, jsonify
from analyzer import (
    gc_content, 
    reverse_complement, 
    codon_frequency, 
    translate_to_protein,
    get_amino_acid_info,
    find_mutations
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze/single', methods=['POST'])
def analyze_single():
    data = request.json
    sequence = data.get('sequence', '').upper()
    analysis_types = data.get('analysis_types', [])
    
    if not sequence:
        return jsonify({'error': 'No sequence provided'}), 400
        
    results = {}
    
    try:
        if 'gc_content' in analysis_types:
            results['gc_content'] = round(gc_content(sequence), 2)
            
        if 'reverse_complement' in analysis_types:
            results['reverse_complement'] = str(reverse_complement(sequence))
            
        if 'codon_frequency' in analysis_types:
            results['codon_frequency'] = codon_frequency(sequence)
            
        if 'translation' in analysis_types:
            protein = translate_to_protein(sequence)
            results['translation'] = protein
            if protein:
                results['amino_acid_info'] = get_amino_acid_info(protein)
                
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze/compare', methods=['POST'])
def analyze_compare():
    data = request.json
    seq1 = data.get('seq1', '').upper()
    seq2 = data.get('seq2', '').upper()
    
    if not seq1 or not seq2:
        return jsonify({'error': 'Both sequences are required'}), 400
        
    try:
        mutations = find_mutations(seq1, seq2)
        return jsonify({
            'success': True, 
            'results': {
                'mutations': mutations,
                'total_mutations': len(mutations),
                'seq1_len': len(seq1),
                'seq2_len': len(seq2)
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
