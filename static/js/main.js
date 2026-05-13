document.addEventListener('DOMContentLoaded', () => {
    // Tab Switching Logic
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            const tabId = btn.getAttribute('data-tab');
            document.getElementById(`${tabId}-tab`).classList.add('active');
        });
    });

    // Example Sequences
    const p53Sample = "ATGGAGGAGCCGCAGTCAGATCCTAGCGTCGAGCCCCCTCTGAGTCAGGAAACATTTTCAGACCTATGGAAACTACTTCCTGAAAACAACGTTCTGTCCCCCTTGCCGTCCCAAGCAATGGATGATTTGATGCTGTCCCCGGACGATATTGAACAATGGTTCACTGAAGACCCAGGTCCAGATGAAGCTCCCAGAATGCCAGAGGCTGCTCCCCGCGTGGCCCCTGCACCAGCAGCTCCTACACCGGCGGCCCCTGCACCAGCCCCCTCCTGGCCCCTGTCATCTTCTGTCCCTTCCCAGAAAACCTACCAGGGCAGCTACGGTTTC";
    const brcaWT = "ATGGATTTATCTGCTCTTCGCGTTGAAGAAGTACAAAATGTCATTAATGCTATGCAGAAAATCTTAGAGTGTCCCATCTGTCTGGAGTTGATCAAGGAACCTGTCTCCACAAAGTGTGACCACATATTTTGCAAATTTTGCATGCTGAAACTTCTCAACCAGAAGAAAGGGCCTTCACAGTGTCCTTTATGTAAGAATGATATAACCAAAAGGAGCCTACAAGAAAGTACGAGATTTAGTCAACTTGTTGAAGAGCTATTGAAAATCATTTGTGCTTTTCAGCTTGACACAGGTTTGGAGTATGCAAACAGCTATAATTTTGCAAAAAAGGAAAATAACTCTCCTGAACATCTAAAA";
    const brcaMut = "ATGGATTTATCTGCTCTTCGCGTTGAAGAAGTACAAAATGTCATTAATGCTATGCAGAAAATCTTAGAGTGTCCCATCTGTCTGGAGTTGATCAAGGAACCTGTCTCCACAAAGTGTGACCACATATTTTGCAAATTTTGCATGCTGAAACTTCTCAACCAGAAGAAAGGGCCTTCACAGTGTCCTTTATGTAAGAATGATATAACCAAAAGGAGCCTACAAGAAAGTACGAGATTTAGTCAACTTGTTGAAGAGCTATTGAAAATCATTTGTGCTTTTCAGCTTGACACAGGTTTGGAGTGCAAACAGCTATAATTTTGCAAAAAAGGAAAATAACTCTCCTGAACATCTAAAA";

    document.getElementById('load-sample-single').addEventListener('click', () => {
        document.getElementById('sequence').value = p53Sample;
    });
    document.getElementById('load-sample-ref').addEventListener('click', () => {
        document.getElementById('seq1').value = brcaWT;
    });
    document.getElementById('load-sample-tgt').addEventListener('click', () => {
        document.getElementById('seq2').value = brcaMut;
    });

    // Helper to format alignment
    function formatAlignment(alignment) {
        let { ref, match, target } = alignment;
        let html = '<div class="alignment-view">';
        
        let refHtml = "";
        let matchHtml = "";
        let tgtHtml = "";

        for(let i = 0; i < ref.length; i++) {
            if(match[i] === '|') {
                refHtml += ref[i];
                matchHtml += '|';
                tgtHtml += target[i];
            } else if (ref[i] === '-') {
                refHtml += '-';
                matchHtml += ' ';
                tgtHtml += `<span class="mut-ins">${target[i]}</span>`;
            } else if (target[i] === '-') {
                refHtml += `<span class="mut-del">${ref[i]}</span>`;
                matchHtml += ' ';
                tgtHtml += '-';
            } else {
                refHtml += `<span class="mut-sub">${ref[i]}</span>`;
                matchHtml += ' ';
                tgtHtml += `<span class="mut-sub">${target[i]}</span>`;
            }

            // Line wrapping for long alignments
            if ((i + 1) % 80 === 0 || i === ref.length - 1) {
                html += `<div>${refHtml}</div>`;
                html += `<div>${matchHtml}</div>`;
                html += `<div>${tgtHtml}</div><br>`;
                refHtml = ""; matchHtml = ""; tgtHtml = "";
            }
        }
        
        html += '</div>';
        return html;
    }

    // Chart Instance variable
    let codonChart = null;

    // Export Functionality
    function downloadText(filename, text) {
        const blob = new Blob([text], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        window.URL.revokeObjectURL(url);
    }

    let lastSingleData = null;
    let lastCompareData = null;

    // Single Sequence Form Submit
    const singleForm = document.getElementById('single-form');
    const singleResults = document.getElementById('single-results');

    singleForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const sequence = document.getElementById('sequence').value;
        const checkboxes = document.querySelectorAll('input[name="analysis_type"]:checked');
        const analysis_types = Array.from(checkboxes).map(cb => cb.value);

        const btn = singleForm.querySelector('button');
        btn.classList.add('loading');
        btn.textContent = 'Analyzing...';

        try {
            const response = await fetch('/analyze/single', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ sequence, analysis_types })
            });

            const data = await response.json();
            
            singleResults.classList.remove('hidden');
            singleResults.innerHTML = '';

            if (data.error) {
                singleResults.innerHTML = `<div class="error-msg">${data.error}</div>`;
                return;
            }

            lastSingleData = data.results;
            const res = data.results;
            let html = '<h2>Analysis Results</h2>';

            if (res.gc_content !== undefined) {
                html += `
                <div class="result-card">
                    <h3>GC Content</h3>
                    <div class="result-value">${res.gc_content}%</div>
                </div>`;
            }

            if (res.primer_tm !== undefined) {
                html += `
                <div class="result-card">
                    <h3>Primer Melting Temp (Tm)</h3>
                    <div class="result-value">${res.primer_tm} °C</div>
                </div>`;
            }

            if (res.orf_finder) {
                html += `
                <div class="result-card">
                    <h3>Longest Open Reading Frame (ORF)</h3>
                    <div class="result-value">
                        <strong>Frame:</strong> ${res.orf_finder.frame} (${res.orf_finder.strand})<br>
                        <strong>Length:</strong> ${res.orf_finder.length} AAs<br>
                        <strong>Protein:</strong> <br>${res.orf_finder.protein}<br><br>
                        <strong>DNA:</strong> <br>${res.orf_finder.dna}
                    </div>
                </div>`;
            } else if (analysis_types.includes('orf_finder')) {
                html += `
                <div class="result-card">
                    <h3>Longest Open Reading Frame (ORF)</h3>
                    <div class="result-value">No valid ORF found.</div>
                </div>`;
            }

            if (res.reverse_complement) {
                html += `
                <div class="result-card">
                    <h3>Reverse Complement</h3>
                    <div class="result-value">${res.reverse_complement}</div>
                </div>`;
            }

            if (res.translation) {
                html += `
                <div class="result-card">
                    <h3>Protein Translation</h3>
                    <div class="result-value">${res.translation}</div>
                </div>`;
            }

            if (res.codon_frequency) {
                html += `
                <div class="result-card">
                    <h3>Codon Frequency</h3>
                    <canvas id="codonChartCanvas"></canvas>
                </div>`;
            }

            html += `
                <div class="export-controls">
                    <button id="btn-export-single" class="export-btn">Download .txt</button>
                </div>
            `;

            singleResults.innerHTML = html;

            // Initialize Chart if needed
            if (res.codon_frequency) {
                const ctx = document.getElementById('codonChartCanvas').getContext('2d');
                
                // Sort codons by frequency
                const sortedCodons = Object.entries(res.codon_frequency)
                    .sort((a, b) => b[1] - a[1]);
                
                const labels = sortedCodons.map(item => item[0]);
                const counts = sortedCodons.map(item => item[1]);

                if(codonChart) codonChart.destroy();

                codonChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Codon Count',
                            data: counts,
                            backgroundColor: 'rgba(88, 166, 255, 0.6)',
                            borderColor: 'rgba(88, 166, 255, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { display: false }
                        },
                        scales: {
                            y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.1)' } },
                            x: { grid: { display: false } }
                        }
                    }
                });
            }

            document.getElementById('btn-export-single').addEventListener('click', () => {
                downloadText('genescope_single_results.txt', JSON.stringify(lastSingleData, null, 2));
            });

        } catch (error) {
            singleResults.classList.remove('hidden');
            singleResults.innerHTML = `<div class="error-msg">An error occurred while connecting to the server.</div>`;
        } finally {
            btn.classList.remove('loading');
            btn.textContent = 'Analyze Sequence';
        }
    });

    // Compare Sequence Form Submit
    const compareForm = document.getElementById('compare-form');
    const compareResults = document.getElementById('compare-results');

    compareForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const seq1 = document.getElementById('seq1').value;
        const seq2 = document.getElementById('seq2').value;

        const btn = compareForm.querySelector('button');
        btn.classList.add('loading');
        btn.textContent = 'Comparing...';

        try {
            const response = await fetch('/analyze/compare', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ seq1, seq2 })
            });

            const data = await response.json();
            
            compareResults.classList.remove('hidden');
            compareResults.innerHTML = ''; 

            if (data.error) {
                compareResults.innerHTML = `<div class="error-msg">${data.error}</div>`;
                return;
            }

            const res = data.results;
            lastCompareData = res;

            let html = `<h2>Comparison Results</h2>
                        <p style="color: #8b949e; margin-bottom: 1rem;">
                            Seq1 Length: ${res.seq1_len} | Seq2 Length: ${res.seq2_len} | Total Mutations: ${res.total_mutations}
                        </p>`;

            if (res.alignment) {
                html += `
                <div class="result-card">
                    <h3>Needleman-Wunsch Alignment</h3>
                    ${formatAlignment(res.alignment)}
                </div>`;
            }

            if (res.mutations.length > 0) {
                html += `
                <div class="result-card">
                    <h3>Mutation Details</h3>
                    <table class="data-table">
                        <thead><tr><th>Pos</th><th>Ref</th><th>Target</th><th>Type</th><th>Effect (Frame 1)</th></tr></thead>
                        <tbody>
                            ${res.mutations.map(m => `
                                <tr>
                                    <td>${m.position}</td>
                                    <td class="${m.ref === '-' ? 'mut-ins' : (m.target === '-' ? 'mut-del' : 'mut-sub')}">${m.ref}</td>
                                    <td class="${m.ref === '-' ? 'mut-ins' : (m.target === '-' ? 'mut-del' : 'mut-sub')}">${m.target}</td>
                                    <td>${m.type}</td>
                                    <td>${m.effect}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>`;
            } else {
                html += `
                <div class="result-card">
                    <h3>No Mutations Detected</h3>
                    <p style="color: var(--success-color)">The sequences are identical.</p>
                </div>`;
            }

            html += `
                <div class="export-controls">
                    <button id="btn-export-compare" class="export-btn">Download .txt</button>
                </div>
            `;

            compareResults.innerHTML = html;

            document.getElementById('btn-export-compare').addEventListener('click', () => {
                downloadText('genescope_mutation_results.txt', JSON.stringify(lastCompareData, null, 2));
            });

        } catch (error) {
            compareResults.classList.remove('hidden');
            compareResults.innerHTML = `<div class="error-msg">An error occurred while connecting to the server.</div>`;
        } finally {
            btn.classList.remove('loading');
            btn.textContent = 'Compare Sequences (NW Alignment)';
        }
    });
});
