from flask import Flask, render_template, request, jsonify
from analyzer import (
    validate_sequence,
    gc_content, 
    reverse_complement, 
    codon_frequency, 
    translate_to_protein,
    get_amino_acid_info,
    calculate_tm,
    find_orfs,
    find_mutations
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze/single', methods=['POST'])
def analyze_single():
    data = request.json
    raw_sequence = data.get('sequence', '')
    analysis_types = data.get('analysis_types', [])
    
    if not raw_sequence:
        return jsonify({'error': 'No sequence provided'}), 400
        
    try:
        sequence = validate_sequence(raw_sequence)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

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
                
        if 'primer_tm' in analysis_types:
            results['primer_tm'] = calculate_tm(sequence)
            
        if 'orf_finder' in analysis_types:
            results['orf_finder'] = find_orfs(sequence)
                
        return jsonify({'success': True, 'results': results, 'clean_sequence': sequence})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze/compare', methods=['POST'])
def analyze_compare():
    data = request.json
    raw_seq1 = data.get('seq1', '')
    raw_seq2 = data.get('seq2', '')
    
    if not raw_seq1 or not raw_seq2:
        return jsonify({'error': 'Both sequences are required'}), 400
        
    try:
        seq1 = validate_sequence(raw_seq1)
        seq2 = validate_sequence(raw_seq2)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
        
    try:
        result = find_mutations(seq1, seq2)
        mutations = result["mutations"]
        
        return jsonify({
            'success': True, 
            'results': {
                'alignment': result["alignment"],
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
