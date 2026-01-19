// CoverageSummarizer Web UI - JavaScript

// Global state
let currentFile = null;
let currentSessionId = null;
let eventSource = null;
let lastProgressUpdate = Date.now();
let keepaliveCount = 0;
let progressUpdateTimer = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
});

function setupEventListeners() {
    // File upload
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');

    dropZone.addEventListener('dragover', handleDragOver);
    dropZone.addEventListener('dragleave', handleDragLeave);
    dropZone.addEventListener('drop', handleDrop);
    
    // File input change event
    if (fileInput) {
        fileInput.addEventListener('change', handleFileSelect);
    }

    // Text input character count
    const textInput = document.getElementById('text-input');
    textInput.addEventListener('input', updateCharCount);
}

// Tab Switching
function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        if (btn.dataset.tab === tabName) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        if (content.id === `${tabName}-tab`) {
            content.classList.add('active');
        } else {
            content.classList.remove('active');
        }
    });

    // Clear the other input
    if (tabName === 'file') {
        document.getElementById('text-input').value = '';
        updateCharCount();
    } else {
        clearFile();
    }
}

// File Upload Handlers
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFile(file) {
    // Validate file type
    const validTypes = ['.pdf', '.txt'];
    const extension = '.' + file.name.split('.').pop().toLowerCase();

    if (!validTypes.includes(extension)) {
        alert('Por favor, selecione um arquivo PDF ou TXT.');
        return;
    }

    // Store file
    currentFile = file;

    // Show file info
    document.getElementById('file-name').textContent = `📄 ${file.name} (${formatFileSize(file.size)})`;
    document.getElementById('drop-zone').style.display = 'none';
    document.getElementById('file-info').style.display = 'block';
}

function clearFile() {
    currentFile = null;
    document.getElementById('file-input').value = '';
    document.getElementById('drop-zone').style.display = 'block';
    document.getElementById('file-info').style.display = 'none';
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

// Text Input
function updateCharCount() {
    const text = document.getElementById('text-input').value;
    document.getElementById('char-count').textContent = `${text.length} caracteres`;
}

// Form Submission
async function submitForm() {
    const activeTab = document.querySelector('.tab-content.active').id;
    const text = document.getElementById('text-input').value;
    const exportMd = document.getElementById('export-md').checked;
    const exportPdf = document.getElementById('export-pdf').checked;

    // Validate input
    if (activeTab === 'file-tab' && !currentFile) {
        alert('Por favor, selecione um arquivo.');
        return;
    }

    if (activeTab === 'text-tab' && !text.trim()) {
        alert('Por favor, insira algum texto.');
        return;
    }

    // Validate export formats
    if (!exportMd && !exportPdf) {
        alert('Por favor, selecione pelo menos um formato de exportação.');
        return;
    }

    // Prepare form data
    const formData = new FormData();

    if (activeTab === 'file-tab') {
        formData.append('file', currentFile);
    } else {
        formData.append('text', text);
    }

    // Export formats
    const formats = [];
    if (exportMd) formats.push('md');
    if (exportPdf) formats.push('pdf');
    formData.append('export_formats', formats.join(','));

    // Disable submit button
    const submitBtn = document.getElementById('submit-btn');
    submitBtn.disabled = true;
    submitBtn.textContent = '⏳ Processando...';

    try {
        // Submit to API
        const response = await fetch('/api/summarize', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao processar solicitação');
        }

        const data = await response.json();
        currentSessionId = data.session_id;

        // Hide input section, show progress
        document.getElementById('input-section').style.display = 'none';
        document.getElementById('progress-section').style.display = 'block';

        // Connect to progress stream
        connectProgressStream(currentSessionId);

    } catch (error) {
        alert('Erro: ' + error.message);
        submitBtn.disabled = false;
        submitBtn.textContent = '✨ Gerar Resumos';
    }
}

// Progress Tracking (SSE)
function connectProgressStream(sessionId) {
    console.log('Connecting to progress stream:', sessionId);

    if (eventSource) {
        eventSource.close();
    }

    eventSource = new EventSource(`/api/progress/${sessionId}`);

    eventSource.onopen = () => {
        console.log('SSE connection opened');
    };

    eventSource.onmessage = (event) => {
        console.log('SSE message received:', event.data);

        // UX Rule: "UX deve comunicar atividade contínua perceptível mesmo quando o percentual não muda."
        // Keepalive indica que backend está ativo - mostrar feedback visual
        if (event.data.startsWith(':')) {
            console.log('Keepalive received, ignoring');
            keepaliveCount++;
            // Atualizar indicador visual de atividade contínua
            updateActivityIndicator(true);
            return;
        }

        try {
            // Remove "data: " prefix if present
            let jsonData = event.data;
            if (jsonData.startsWith('data: ')) {
                jsonData = jsonData.substring(6); // Remove "data: "
            }

            const data = JSON.parse(jsonData);
            console.log('Parsed data:', data);
            updateProgress(data.percentage, data.message);

            if (data.complete) {
                console.log('Processing complete');
                eventSource.close();
                if (data.error) {
                    showError(data.message);
                } else {
                    fetchResults(sessionId);
                }
            }
        } catch (e) {
            console.error('Error parsing SSE data:', e, event.data);
        }
    };

    eventSource.onerror = (error) => {
        console.error('SSE Error:', error);
        console.log('SSE readyState:', eventSource.readyState);
        eventSource.close();

        // Try to fetch results anyway
        setTimeout(() => fetchResults(sessionId), 1000);
    };
}

function updateProgress(percentage, message) {
    console.log(`Updating progress: ${percentage}% - ${message}`);

    const progressBar = document.getElementById('progress-bar');
    const progressMessage = document.getElementById('progress-message');
    const progressPercentage = document.getElementById('progress-percentage');

    console.log('Progress elements:', {
        progressBar: progressBar,
        progressMessage: progressMessage,
        progressPercentage: progressPercentage
    });

    lastProgressUpdate = Date.now();
    keepaliveCount = 0; // Reset quando há atualização real

    if (progressBar) {
        progressBar.style.width = `${percentage}%`;
        console.log('Progress bar width set to:', progressBar.style.width);
    }
    if (progressMessage) {
        progressMessage.textContent = message;
    }
    if (progressPercentage) {
        progressPercentage.textContent = `${percentage}%`;
    }
    
    // Atualizar indicador de atividade
    updateActivityIndicator(false);
}

// UX Rule: "UX deve comunicar atividade contínua perceptível mesmo quando o percentual não muda."
function updateActivityIndicator(isKeepalive) {
    const progressMessage = document.getElementById('progress-message');
    if (!progressMessage) return;
    
    const timeSinceLastUpdate = Date.now() - lastProgressUpdate;
    const isLongRunning = timeSinceLastUpdate > 10000; // Mais de 10 segundos sem atualização
    
    if (isKeepalive && isLongRunning) {
        // Adicionar indicador visual de atividade contínua
        const baseMessage = progressMessage.textContent || 'Processando...';
        if (!baseMessage.includes('⏳')) {
            progressMessage.textContent = `${baseMessage} ⏳ (sistema ativo...)`;
            progressMessage.style.animation = 'pulse 2s infinite';
        }
    } else if (!isLongRunning) {
        // Remover indicador quando há atualização recente
        progressMessage.style.animation = '';
    }
}

// Fetch Results
async function fetchResults(sessionId) {
    try {
        const response = await fetch(`/api/result/${sessionId}`);

        if (!response.ok) {
            throw new Error('Erro ao obter resultados');
        }

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        console.error('Error fetching results:', error);
        showError('Erro ao carregar resultados: ' + error.message);
    }
}

// Display Results
function displayResults(data) {
    console.log('displayResults called with data:', data);

    // Check status first - this is the canonical contract
    const status = data.status || (data.coverage_report && data.coverage_report.passed ? 'PASS' : 'FAIL');
    
    // Display result banner first (coverage is the main visual element)
    displayResultBanner(data, status);
    
    // Display coverage section (always show if available)
    displayCoverageSection(data);

    // Only show summary if status == PASS
    if (status === 'PASS') {
        // Detect format: chapter-based vs simple
        if (data.summaries && data.summaries.estrutura === 'capitulos') {
            console.log('Chapter-based format detected');
            displayChapterResults(data);
        } else {
            console.log('Simple format detected');
            displaySimpleResults(data);
        }
    } else {
        // Status FAIL - show error message, no summary
        displayFailureMessage(data);
    }
}

// Display Result Banner - Coverage is the main visual element
function displayResultBanner(data, status) {
    const bannerSection = document.getElementById('result-banner-section');
    const banner = document.getElementById('result-banner');
    
    if (!bannerSection || !banner) return;
    
    const report = data.coverage_report;
    const coverage = report ? (report.overall_coverage_percentage || 0) : 0;
    const passed = status === 'PASS';
    
    if (passed && coverage === 100) {
        banner.className = 'result-banner pass';
        banner.innerHTML = `
            <div class="result-banner-title">
                ✅ Coverage: 100% — VERIFIED
            </div>
            <div class="result-banner-subtitle">
                All critical items covered | Summary available
            </div>
        `;
    } else {
        banner.className = 'result-banner fail';
        banner.innerHTML = `
            <div class="result-banner-title">
                ❌ Coverage Failed — Missing critical items
            </div>
            <div class="result-banner-subtitle">
                Coverage: ${coverage.toFixed(1)}% | Summary not available
            </div>
        `;
    }
    
    bannerSection.style.display = 'block';
}

// Display Coverage Section
function displayCoverageSection(data) {
    const coverageSection = document.getElementById('coverage-section');
    const coverageContent = document.getElementById('coverage-content');
    
    if (!coverageSection || !coverageContent) return;
    
    if (!data.coverage_report) {
        coverageSection.style.display = 'none';
        return;
    }
    
    const report = data.coverage_report;
    const summary = report.summary || {};
    const addendumMetrics = data.addendum_metrics || {};
    
    let html = `
        <div class="coverage-metrics">
            <div class="coverage-metric-item">
                <span class="metric-label">Overall Coverage</span>
                <span class="metric-value">${(report.overall_coverage_percentage || 0).toFixed(1)}%</span>
            </div>
            <div class="coverage-metric-item">
                <span class="metric-label">Total Chapters</span>
                <span class="metric-value">${summary.total_chapters || 0}</span>
            </div>
            <div class="coverage-metric-item">
                <span class="metric-label">Chapters using Addendum</span>
                <span class="metric-value">${addendumMetrics.chapters_using_addendum || 0}</span>
            </div>
            <div class="coverage-metric-item">
                <span class="metric-label">Total Addendums Used</span>
                <span class="metric-value">${addendumMetrics.total_addendums_used || 0}</span>
            </div>
        </div>
    `;
    
    // Per-chapter status
    if (report.chapters && report.chapters.length > 0) {
        html += '<div class="per-chapter-coverage"><h4>Per-Chapter Status</h4><ul>';
        report.chapters.forEach(ch => {
            const audit = ch.audit_result || {};
            const passed = audit.passed !== undefined ? audit.passed : true;
            const addendumCount = audit.addendum_count || 0;
            const regenerationCount = audit.regeneration_count || 0;
            
            html += `
                <li class="chapter-status-item">
                    <strong>Chapter ${ch.chapter_number}:</strong>
                    <span class="status-badge ${passed ? 'status-pass' : 'status-fail'}">${passed ? 'PASS' : 'FAIL'}</span>
                    ${addendumCount > 0 ? `<span class="addendum-badge">Addendum: ${addendumCount}</span>` : ''}
                    ${regenerationCount > 0 ? `<span class="regeneration-badge">Regenerations: ${regenerationCount}</span>` : ''}
                </li>
            `;
        });
        html += '</ul></div>';
    }
    
    coverageContent.innerHTML = html;
    coverageSection.style.display = 'block';
}

// Display Failure Message
function displayFailureMessage(data) {
    // Hide summary sections
    document.getElementById('chapter-results-section').style.display = 'none';
    document.getElementById('results-section').style.display = 'none';
    document.getElementById('final-summary-section').style.display = 'none';
    
    // Show error message
    const progressSection = document.getElementById('progress-section');
    if (progressSection) {
        progressSection.style.display = 'block';
        progressSection.innerHTML = `
            <div class="section" style="background: #fee; border: 2px solid #fcc;">
                <h2 style="color: #c00;">❌ Coverage Validation Failed</h2>
                <p>Summary is not available because coverage validation failed.</p>
                ${data.errors && data.errors.length > 0 ? `<ul>${data.errors.map(e => `<li>${e}</li>`).join('')}</ul>` : ''}
                <button class="btn btn-primary" onclick="resetForm()">Try Again</button>
            </div>
        `;
    }
}

// Display Reliability Section
function displayReliabilitySection(data) {
    const reliabilitySection = document.getElementById('reliability-section');
    const reliabilityContent = document.getElementById('reliability-content');
    
    if (!reliabilitySection || !reliabilityContent) return;
    
    // Early return if no coverage_report
    if (!data.coverage_report) {
        reliabilitySection.style.display = 'none';
        return;
    }
    
    const addendumMetrics = data.addendum_metrics || {};
    const totalAddendums = addendumMetrics.total_addendums_used || 0;
    const chaptersWithAddendum = addendumMetrics.chapters_using_addendum || 0;
    
    let html = `
        <div class="reliability-item">
            <span class="reliability-item-icon">✔</span>
            <span class="reliability-item-text">Auditoria automática aplicada</span>
        </div>
        <div class="reliability-item">
            <span class="reliability-item-icon">✔</span>
            <span class="reliability-item-text">Itens críticos verificados</span>
        </div>
        <div class="reliability-item">
            <span class="reliability-item-icon">✔</span>
            <span class="reliability-item-text">Regeneração automática ativada</span>
        </div>
    `;
    
    if (totalAddendums > 0) {
        html += `
            <div class="reliability-item">
                <span class="reliability-item-icon">⚠</span>
                <span class="reliability-item-text">Addendum usado em ${chaptersWithAddendum} capítulo${chaptersWithAddendum !== 1 ? 's' : ''}</span>
            </div>
        `;
    }
    
    // Badge
    if (totalAddendums > 0) {
        html += `
            <div class="reliability-badge reinforcement">
                🔧 Reforço Automático Aplicado
            </div>
        `;
    } else {
        html += `
            <div class="reliability-badge direct">
                ✨ Resumo direto (sem reforços)
            </div>
        `;
    }
    
    reliabilityContent.innerHTML = html;
    reliabilitySection.style.display = 'block';
}

// Display Simple Results (original format)
function displaySimpleResults(data) {
    // Hide progress, show simple results
    document.getElementById('progress-section').style.display = 'none';
    document.getElementById('chapter-results-section').style.display = 'none';
    document.getElementById('final-summary-section').style.display = 'none';
    document.getElementById('reliability-section').style.display = 'none';
    document.getElementById('observability-section').style.display = 'none';
    document.getElementById('results-section').style.display = 'block';

    const summaries = data.summaries;

    // Populate summary cards
    document.getElementById('short-summary').innerHTML = formatSummary(summaries.curto);
    document.getElementById('medium-summary').innerHTML = formatSummary(summaries.medio);
    document.getElementById('long-summary').innerHTML = formatSummary(summaries.longo);
    document.getElementById('bullets-summary').innerHTML = formatSummary(summaries.bullets);

    // Quality report
    if (summaries.validation_report) {
        const reportCard = document.getElementById('quality-report');
        const reportContent = document.getElementById('quality-content');
        reportContent.innerHTML = `<pre>${summaries.validation_report}</pre>`;
        reportCard.style.display = 'block';
    }

    // Download links
    if (data.exported_files && Object.keys(data.exported_files).length > 0) {
        displayDownloadLinks(data.exported_files);
    }

    // Scroll to results
    document.getElementById('results-section').scrollIntoView({ behavior: 'smooth' });
}

// Display Chapter-Based Results (new format)
function displayChapterResults(data) {
    console.log('Displaying chapter-based results');
    console.log('Full data:', data);
    console.log('Summaries:', data.summaries);
    console.log('Capitulos array:', data.summaries.capitulos);
    console.log('Number of chapters:', data.summaries.capitulos ? data.summaries.capitulos.length : 0);

    // Hide progress and simple results, show chapter results
    document.getElementById('progress-section').style.display = 'none';
    document.getElementById('results-section').style.display = 'none';
    document.getElementById('chapter-results-section').style.display = 'block';

    const summaries = data.summaries;

    // Display executive summary
    const executiveSummary = document.getElementById('executive-summary');
    executiveSummary.innerHTML = `<p>${summaries.resumo_executivo.medio}</p>`;

    // Display chapter TOC
    const toc = document.getElementById('chapter-toc');
    if (summaries.capitulos && summaries.capitulos.length > 0) {
        toc.innerHTML = summaries.capitulos.map((cap, i) => {
            const palavrasOriginal = cap.palavras || 0;
            const palavrasResumo = cap.palavras_resumo || 0;
            const porcentagem = palavrasOriginal > 0 
                ? ((palavrasResumo / palavrasOriginal) * 100).toFixed(2).replace('.', ',')
                : '0,00';
            
            // UX Rule: "Métrica correta mas semanticamente ambígua é FAIL de UX."
            // Quando palavrasOriginal é 0, não exibir métrica confusa
            const metricText = palavrasOriginal > 0 
                ? `Original - ${palavrasOriginal.toLocaleString()} palavras | Resumo - ${palavrasResumo.toLocaleString()} palavras | % resumo/original ${porcentagem}%`
                : `Resumo - ${palavrasResumo.toLocaleString()} palavras`;
            
            return `
            <a href="#chapter-${i}" class="chapter-link">
                📖 Capítulo ${cap.numero}: ${cap.titulo}
                <span style="color: var(--text-secondary); font-size: 0.875rem;">
                    ${metricText}
                </span>
            </a>
        `;
        }).join('');
    }

            // Display chapter cards
    const chaptersContainer = document.getElementById('chapters-container');
    if (summaries.capitulos && summaries.capitulos.length > 0) {
        // Buscar dados de addendum do coverage_report se disponível
        const chapterMetrics = {};
        if (data.coverage_report && data.coverage_report.chapters) {
            data.coverage_report.chapters.forEach(ch => {
                chapterMetrics[ch.chapter_number] = ch.audit_result;
            });
        }
        
        chaptersContainer.innerHTML = summaries.capitulos.map((cap, i) => {
            const metrics = chapterMetrics[cap.numero] || {};
            const addendumCount = metrics.addendum_count || 0;
            const regenerationCount = metrics.regeneration_count || 0;
            const passed = metrics.passed !== undefined ? metrics.passed : true;
            
            let html = `
                <div class="chapter-card" id="chapter-${i}">
                    <div class="chapter-header">
                        <h3>Capítulo ${cap.numero}: ${cap.titulo}</h3>
                        <span class="chapter-meta">
                            ${(cap.palavras || 0) > 0 
                                ? `Original - ${(cap.palavras || 0).toLocaleString()} palavras | Resumo - ${(cap.palavras_resumo || 0).toLocaleString()} palavras | % resumo/original ${((cap.palavras_resumo / cap.palavras) * 100).toFixed(2).replace('.', ',')}%`
                                : `Resumo - ${(cap.palavras_resumo || 0).toLocaleString()} palavras`}
                            ${cap.paginas && cap.paginas.length > 0 ? ` | Páginas: ${cap.paginas.join(', ')}` : ''}
                            ${addendumCount > 0 ? ` <span class="addendum-badge chapter-badge-tooltip" data-tooltip="Sistema aplicou reforço automático para garantir cobertura completa">📝 Addendum: ${addendumCount}</span>` : ''}
                            ${regenerationCount > 0 ? ` <span class="regeneration-badge chapter-badge-tooltip" data-tooltip="Número de tentativas até obter resumo válido">🔄 Regenerações: ${regenerationCount}</span>` : ''}
                            <span class="status-badge ${passed ? 'status-pass' : 'status-fail'} chapter-badge-tooltip" data-tooltip="${passed ? 'Resumo passou na auditoria automática' : 'Resumo não passou na auditoria automática'}">${passed ? '✅ PASS' : '❌ FAIL'}</span>
                        </span>
                    </div>
                    <div class="chapter-body">
                        <div class="chapter-summary">
                            ${formatSummary(cap.resumo)}
                        </div>
            `;

            // Points-chave
            if (cap.pontos_chave && cap.pontos_chave.length > 0) {
                html += `
                    <div class="chapter-points">
                        <h4>🔑 Pontos-Chave</h4>
                        <ul>
                            ${cap.pontos_chave.map(p => `<li>${p}</li>`).join('')}
                        </ul>
                    </div>
                `;
            }

            // Citações
            if (cap.citacoes && cap.citacoes.length > 0) {
                html += `
                    <div class="chapter-quotes">
                        <h4>💬 Citações</h4>
                        ${cap.citacoes.map(q => `<blockquote>"${q}"</blockquote>`).join('')}
                    </div>
                `;
            }

            // Exemplos
            if (cap.exemplos && cap.exemplos.length > 0) {
                html += `
                    <div class="chapter-examples">
                        <h4>🔬 Exemplos Mencionados</h4>
                        <ul>
                            ${cap.exemplos.map(ex => `<li>${ex}</li>`).join('')}
                        </ul>
                    </div>
                `;
            }

            html += `
                    </div>
                </div>
            `;

            return html;
        }).join('');
    }

    // Download links for chapter-based format
    if (data.exported_files && Object.keys(data.exported_files).length > 0) {
        const downloadSection = document.getElementById('chapter-download-section');
        const downloadLinks = document.getElementById('chapter-download-links');

        let linksHTML = '';
        for (const [format, filepath] of Object.entries(data.exported_files)) {
            const filename = filepath.split('/').pop();
            const icon = format === 'markdown' ? '📄' : '📕';
            const label = format === 'markdown' ? 'Markdown' : 'PDF';

            linksHTML += `
                <a href="/api/download/${filename}"
                   download="${filename}"
                   class="download-link">
                    ${icon} Download ${label}
                </a>
            `;
        }

        downloadLinks.innerHTML = linksHTML;
        downloadSection.style.display = 'block';
    }

    // Display reliability section
    displayReliabilitySection(data);
    
    // Display final summary
    displayFinalSummary(data);
    
    // Display observability metrics (with defensive check inside)
    displayObservabilityMetrics(data);
    
    // Scroll to results
    document.getElementById('chapter-results-section').scrollIntoView({ behavior: 'smooth' });
}

function formatSummary(text) {
    if (!text) return '<p class="text-secondary">Não disponível</p>';

    // Remove technical markers ([[RS:capX:hash|chunks:Y]]) before formatting
    // UX Rule: "Usuário final nunca deve ver artefatos internos de engenharia."
    text = text.replace(/\[\[RS:cap\d+:[a-f0-9]+\|chunks:[^\]]+\]\]/g, '');
    text = text.replace(/\[\[RS:[^\]]+\]\]/g, ''); // Catch any other RS markers

    // Convert line breaks to paragraphs
    const paragraphs = text.split('\n\n').map(p => {
        p = p.trim();
        if (p.startsWith('•') || p.startsWith('-')) {
            return `<li>${p.substring(1).trim()}</li>`;
        }
        return `<p>${p}</p>`;
    });

    // Wrap list items in ul
    let formatted = paragraphs.join('\n');
    formatted = formatted.replace(/(<li>.*<\/li>(\n<li>.*<\/li>)*)/g, '<ul>$1</ul>');

    return formatted;
}

function displayDownloadLinks(exportedFiles) {
    const downloadSection = document.getElementById('download-section');
    const downloadLinks = document.getElementById('download-links');

    let linksHTML = '';

    for (const [format, filepath] of Object.entries(exportedFiles)) {
        const filename = filepath.split('/').pop();
        const icon = format === 'markdown' ? '📄' : '📕';
        const label = format === 'markdown' ? 'Markdown' : 'PDF';

        linksHTML += `
            <a href="/api/download/${filename}"
               download="${filename}"
               class="download-link">
                ${icon} Download ${label}
            </a>
        `;
    }

    downloadLinks.innerHTML = linksHTML;
    downloadSection.style.display = 'block';
}

// Card Toggle
function toggleCard(cardId) {
    const content = document.getElementById(`${cardId}-summary`);
    const header = content.previousElementSibling;

    if (content.classList.contains('collapsed')) {
        content.classList.remove('collapsed');
        content.classList.add('expanded');
        header.classList.add('expanded');
    } else {
        content.classList.remove('expanded');
        content.classList.add('collapsed');
        header.classList.remove('expanded');
    }
}

// Error Display
function showError(message) {
    document.getElementById('progress-section').style.display = 'none';
    document.getElementById('results-section').style.display = 'block';

    const resultsSection = document.getElementById('results-section');
    resultsSection.innerHTML = `
        <div class="section" style="background: #fee; border: 2px solid #fcc;">
            <h2 style="color: #c00;">❌ Erro</h2>
            <p>${message}</p>
            <button class="btn btn-primary" onclick="resetForm()">Tentar Novamente</button>
        </div>
    `;
}

// Display Final Summary
function displayFinalSummary(data) {
    const finalSection = document.getElementById('final-summary-section');
    const finalContent = document.getElementById('final-summary-content');
    
    if (!finalSection || !finalContent) return;
    
    // Early return if no summaries
    if (!data.summaries || !data.summaries.capitulos || data.summaries.capitulos.length === 0) {
        finalSection.style.display = 'none';
        return;
    }
    
    // Store final summary text globally for copy/export
    window.finalSummaryText = '';
    
    // Concatenate all chapter summaries
    const chapters = data.summaries.capitulos;
    let fullText = '';
    
    chapters.forEach((cap, index) => {
        fullText += `# Capítulo ${cap.numero}: ${cap.titulo}\n\n`;
        fullText += cap.resumo || '';
        fullText += '\n\n';
        
        if (cap.pontos_chave && cap.pontos_chave.length > 0) {
            fullText += '## Pontos-Chave\n\n';
            cap.pontos_chave.forEach(p => {
                fullText += `- ${p}\n`;
            });
            fullText += '\n';
        }
    });
    
    window.finalSummaryText = fullText;
    
    // Render formatted HTML
    let html = '';
    chapters.forEach((cap, index) => {
        html += `<div class="final-chapter">`;
        html += `<h2>Capítulo ${cap.numero}: ${cap.titulo}</h2>`;
        html += formatSummary(cap.resumo || '');
        
        if (cap.pontos_chave && cap.pontos_chave.length > 0) {
            html += `<h3>Pontos-Chave</h3><ul>`;
            cap.pontos_chave.forEach(p => {
                html += `<li>${p}</li>`;
            });
            html += `</ul>`;
        }
        
        html += `</div>`;
        if (index < chapters.length - 1) {
            html += `<hr style="margin: 2rem 0; border: 1px solid var(--border);">`;
        }
    });
    
    finalContent.innerHTML = html;
    finalSection.style.display = 'block';
}

// Copy Final Summary
function copyFinalSummary() {
    if (!window.finalSummaryText) {
        alert('Nenhum resumo disponível para copiar.');
        return;
    }
    
    navigator.clipboard.writeText(window.finalSummaryText).then(() => {
        alert('Resumo copiado para a área de transferência!');
    }).catch(err => {
        console.error('Erro ao copiar:', err);
        alert('Erro ao copiar resumo. Tente novamente.');
    });
}

// Export Final Summary
function exportFinalSummary(format) {
    if (!window.finalSummaryText) {
        alert('Nenhum resumo disponível para exportar.');
        return;
    }
    
    if (format === 'md') {
        const blob = new Blob([window.finalSummaryText], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'resumo-final.md';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    } else if (format === 'pdf') {
        alert('Exportação PDF será implementada em breve. Por enquanto, use a exportação Markdown.');
    }
}

// Display Observability Metrics
function displayObservabilityMetrics(data) {
    if (!data.coverage_report) {
        document.getElementById('observability-section').style.display = 'none';
        return;
    }
    
    const report = data.coverage_report;
    const summary = report.summary || {};
    
    // Overall metrics - improved visual format with cards
    const metricsContainer = document.getElementById('metrics-cards-container');
    if (metricsContainer) {
        const overallCoverage = report.overall_coverage_percentage || 0;
        const totalChapters = summary.total_chapters || 0;
        const chapters100 = summary.chapters_with_100_percent || 0;
        const chaptersAddendum = summary.chapters_using_addendum || 0;
        const totalAddendums = summary.total_addendums_used || 0;
        const avgAddendums = (summary.avg_addendums_per_chapter || 0).toFixed(2);
        
        metricsContainer.innerHTML = `
            <div class="metric-card">
                <span class="metric-card-icon">📊</span>
                <div class="metric-card-content">
                    <div class="metric-card-label">Cobertura Geral</div>
                    <div class="metric-card-value">${overallCoverage.toFixed(1)}%</div>
                </div>
            </div>
            <div class="metric-card">
                <span class="metric-card-icon">📚</span>
                <div class="metric-card-content">
                    <div class="metric-card-label">Capítulos Processados</div>
                    <div class="metric-card-value">${totalChapters}</div>
                </div>
            </div>
            <div class="metric-card">
                <span class="metric-card-icon">✅</span>
                <div class="metric-card-content">
                    <div class="metric-card-label">Capítulos com 100%</div>
                    <div class="metric-card-value">${chapters100}</div>
                </div>
            </div>
            <div class="metric-card">
                <span class="metric-card-icon">🔧</span>
                <div class="metric-card-content">
                    <div class="metric-card-label">Capítulos com Addendum</div>
                    <div class="metric-card-value">${chaptersAddendum}</div>
                </div>
            </div>
            <div class="metric-card">
                <span class="metric-card-icon">📝</span>
                <div class="metric-card-content">
                    <div class="metric-card-label">Total de Addendums</div>
                    <div class="metric-card-value">${totalAddendums}</div>
                </div>
            </div>
            <div class="metric-card">
                <span class="metric-card-icon">📈</span>
                <div class="metric-card-content">
                    <div class="metric-card-label">Média Addendums/Capítulo</div>
                    <div class="metric-card-value">${avgAddendums}</div>
                </div>
            </div>
        `;
    }
    
    // Per-chapter metrics
    const chapterMetricsContainer = document.getElementById('chapter-metrics');
    if (report.chapters && report.chapters.length > 0) {
        chapterMetricsContainer.innerHTML = report.chapters.map(ch => {
            const audit = ch.audit_result || {};
            const passed = audit.passed !== undefined ? audit.passed : true;
            const addendumCount = audit.addendum_count || 0;
            const regenerationCount = audit.regeneration_count || 0;
            const missingMarkers = audit.missing_markers || [];
            
            return `
                <div class="chapter-metric">
                    <div class="metric-header">
                        <strong>Capítulo ${ch.chapter_number}: ${ch.chapter_title || 'Sem título'}</strong>
                        <span class="status-badge ${passed ? 'status-pass' : 'status-fail'}">${passed ? '✅ PASS' : '❌ FAIL'}</span>
                    </div>
                    <div class="metric-details">
                        <span class="metric-item">Regenerações: <strong>${regenerationCount}</strong></span>
                        <span class="metric-item">Addendums: <strong>${addendumCount}</strong></span>
                        <span class="metric-item">Cobertura: <strong>${ch.chunk_coverage_percentage || 0}%</strong></span>
                        ${missingMarkers.length > 0 ? `<span class="metric-warning">⚠️ ${missingMarkers.length} marcadores faltando</span>` : ''}
                    </div>
                </div>
            `;
        }).join('');
    } else {
        chapterMetricsContainer.innerHTML = '<p class="text-secondary">Nenhuma métrica disponível</p>';
    }
    
    // Show section
    document.getElementById('observability-section').style.display = 'block';
}

// Reset Form
function resetForm() {
    // Clear form
    clearFile();
    document.getElementById('text-input').value = '';
    updateCharCount();

    // Reset checkboxes
    document.getElementById('export-md').checked = true;
    document.getElementById('export-pdf').checked = false;

    // Reset state
    currentFile = null;
    currentSessionId = null;

    if (eventSource) {
        eventSource.close();
        eventSource = null;
    }

    // Reset UI
    document.getElementById('submit-btn').disabled = false;
    document.getElementById('submit-btn').textContent = '✨ Gerar Resumos';
    document.getElementById('input-section').style.display = 'block';
    document.getElementById('progress-section').style.display = 'none';
    document.getElementById('results-section').style.display = 'none';
    document.getElementById('chapter-results-section').style.display = 'none';
    document.getElementById('result-banner-section').style.display = 'none';
    document.getElementById('coverage-section').style.display = 'none';
    document.getElementById('reliability-section').style.display = 'none';
    document.getElementById('final-summary-section').style.display = 'none';
    document.getElementById('observability-section').style.display = 'none';
    
    // Clear global state
    window.finalSummaryText = '';

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
