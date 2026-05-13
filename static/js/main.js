document.addEventListener('DOMContentLoaded', () => {
    // Tab Switching Logic
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            // Add active class to clicked
            btn.classList.add('active');
            const tabId = btn.getAttribute('data-tab');
            document.getElementById(`${tabId}-tab`).classList.add('active');
        });
    });

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
            singleResults.innerHTML = ''; // clear previous

            if (data.error) {
                singleResults.innerHTML = `<div class="error-msg">${data.error}</div>`;
                return;
            }

            // Render Results
            const res = data.results;
            let html = '<h2>Analysis Results</h2>';

            if (res.gc_content !== undefined) {
                html += `
                <div class="result-card">
                    <h3>GC Content</h3>
                    <div class="result-value">${res.gc_content}%</div>
                </div>`;
            }

            if (res.reverse_complement) {
                html += `
                <div class="result-card">
                    <h3>Reverse Complement</h3>
                    <div class="result-value">${res.reverse_complement}</div>
                </div>`;
            }

            if (res.codon_frequency) {
                html += `
                <div class="result-card">
                    <h3>Codon Frequency</h3>
                    <table class="data-table">
                        <thead><tr><th>Codon</th><th>Count</th></tr></thead>
                        <tbody>
                            ${Object.entries(res.codon_frequency).map(([codon, count]) => `
                                <tr><td>${codon}</td><td>${count}</td></tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>`;
            }

            if (res.translation) {
                html += `
                <div class="result-card">
                    <h3>Protein Translation</h3>
                    <div class="result-value">${res.translation}</div>
                </div>`;
            }

            singleResults.innerHTML = html;
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
            let html = `<h2>Comparison Results</h2>
                        <p style="color: #8b949e; margin-bottom: 1rem;">
                            Seq1 Length: ${res.seq1_len} | Seq2 Length: ${res.seq2_len} | Total Mutations: ${res.total_mutations}
                        </p>`;

            if (res.mutations.length > 0) {
                html += `
                <div class="result-card">
                    <h3>Mutations Detected</h3>
                    <table class="data-table">
                        <thead><tr><th>Position</th><th>Reference (Seq1)</th><th>Target (Seq2)</th></tr></thead>
                        <tbody>
                            ${res.mutations.map(m => `
                                <tr>
                                    <td>${m.position + 1}</td>
                                    <td style="color: var(--error-color)">${m.seq1}</td>
                                    <td style="color: var(--success-color)">${m.seq2}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>`;
            } else {
                html += `
                <div class="result-card">
                    <h3>No Mutations Detected</h3>
                    <p style="color: var(--success-color)">The sequences are identical up to the compared length.</p>
                </div>`;
            }

            compareResults.innerHTML = html;
        } catch (error) {
            compareResults.classList.remove('hidden');
            compareResults.innerHTML = `<div class="error-msg">An error occurred while connecting to the server.</div>`;
        } finally {
            btn.classList.remove('loading');
            btn.textContent = 'Compare Sequences';
        }
    });
});
