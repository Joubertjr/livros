// History Management Functions
// F7: Carregar histórico de resumos

/**
 * Determina status do resumo baseado no coverage_report.
 * 
 * Clean Code: Extrai lógica de determinação de status para função separada.
 * 
 * @param {Object|null} coverageReport - Relatório de cobertura
 * @returns {string} - 'PASS' ou 'FAIL'
 */
function _determineStatusFromCoverage(coverageReport) {
    if (!coverageReport) {
        return 'PASS';  // Assumir PASS se não houver relatório
    }
    
    if (coverageReport.passed === false || coverageReport.overall_coverage_percentage < 100.0) {
        return 'FAIL';
    }
    
    return 'PASS';
}

async function loadHistory() {
    try {
        const response = await fetch('/api/summaries');
        const data = await response.json();
        
        const historyList = document.getElementById('history-list');
        const historyLoading = document.getElementById('history-loading');
        const historyEmpty = document.getElementById('history-empty');
        
        if (!historyList || !historyLoading || !historyEmpty) {
            console.warn('Elementos de histórico não encontrados no DOM');
            return;
        }
        
        historyLoading.style.display = 'none';
        
        if (data.summaries && data.summaries.length > 0) {
            historyList.style.display = 'block';
            historyEmpty.style.display = 'none';
            
            // Renderizar lista usando componentes do Design System
            historyList.innerHTML = data.summaries.map(summary => {
                const date = new Date(summary.created_at);
                const dateStr = date.toLocaleString('pt-BR');
                
                return `
                    <div class="card" style="margin-bottom: var(--spacing-lg);">
                        <div class="card-content">
                            <h3 style="font-size: var(--font-size-xl); margin-bottom: var(--spacing-md);">
                                ${summary.title || 'Resumo sem título'}
                            </h3>
                            <div style="display: flex; gap: var(--spacing-md); flex-wrap: wrap; margin-bottom: var(--spacing-md);">
                                <span class="badge badge-status-info">${summary.pipeline_type}</span>
                                <span style="color: var(--color-text-secondary); font-size: var(--font-size-sm);">
                                    📅 ${dateStr}
                                </span>
                            </div>
                            <div style="margin-bottom: var(--spacing-md);">
                                <p style="color: var(--color-text-secondary); font-size: var(--font-size-sm);">
                                    📊 ${summary.total_words_input || 0} palavras → ${summary.total_words_output || 0} palavras
                                    ${summary.processing_time ? ` | ⏱️ ${summary.processing_time.toFixed(1)}s` : ''}
                                </p>
                            </div>
                            <div style="display: flex; gap: var(--spacing-md);">
                                <button class="btn btn-primary" onclick="viewSummary('${summary.summary_id}')">
                                    👁️ Ver Detalhes
                                </button>
                                <button class="btn btn-secondary" onclick="submitFeedbackForSummary('${summary.summary_id}')">
                                    💬 Feedback
                                </button>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
        } else {
            historyList.style.display = 'none';
            historyEmpty.style.display = 'block';
        }
    } catch (error) {
        console.error('Erro ao carregar histórico:', error);
        const historyLoading = document.getElementById('history-loading');
        if (historyLoading) {
            historyLoading.innerHTML = 
                '<p style="color: var(--color-error);">Erro ao carregar histórico. Tente novamente.</p>';
        }
    }
}

// F7: Ver detalhes de um resumo
async function viewSummary(summaryId) {
    try {
        const response = await fetch(`/api/summaries/${summaryId}`);
        if (!response.ok) {
            throw new Error('Erro ao carregar resumo');
        }
        
        const data = await response.json();
        
        // Determinar status do coverage_report
        const status = _determineStatusFromCoverage(data.summary.coverage_report);
        
        // Exibir resumo usando displayResults
        if (data.summary && data.summary.summaries) {
            displayResults({
                session_id: data.summary.summary_id,
                status: status,
                errors: [],
                exported_files: data.summary.exported_files || {},
                coverage_report: data.summary.coverage_report,
                addendum_metrics: data.summary.addendum_metrics,
                summaries: data.summary.summaries
            });
            
            // Scroll para resultados
            setTimeout(() => {
                const resultsSection = document.getElementById('chapter-results-section') || 
                                     document.getElementById('results-section');
                if (resultsSection) {
                    resultsSection.scrollIntoView({ behavior: 'smooth' });
                }
            }, 100);
        } else {
            alert('Resumo não encontrado ou formato inválido');
        }
    } catch (error) {
        console.error('Erro ao visualizar resumo:', error);
        alert('Erro ao carregar resumo: ' + error.message);
    }
}

// F7: Submeter feedback para um resumo
async function submitFeedbackForSummary(summaryId) {
    const feedbackType = prompt('Tipo de feedback:\n1. dúvida\n2. erro\n3. sugestão\n4. elogio\n\nDigite o número ou o nome:');
    if (!feedbackType) return;
    
    const message = prompt('Mensagem do feedback:');
    if (!message) return;
    
    try {
        const formData = new FormData();
        formData.append('feedback_type', feedbackType);
        formData.append('message', message);
        
        const response = await fetch(`/api/summaries/${summaryId}/feedback`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Erro ao enviar feedback');
        }
        
        const data = await response.json();
        alert('Feedback registrado com sucesso!');
    } catch (error) {
        console.error('Erro ao enviar feedback:', error);
        alert('Erro ao enviar feedback: ' + error.message);
    }
}
