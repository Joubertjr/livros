# ORDEM DO CEO — DEMANDA-000

Produto: Book Summarizer

Executor técnico: Cursor

Método: ENDFIRST

Pré-condição absoluta: Docker

⸻

🔒 END (imutável)

Uma pessoa externa consegue clonar o repositório, executar docker compose up, acessar uma UI ou CLI, enviar um livro (texto ou arquivo) e receber resumos (curto / médio / longo + bullets + insights + referências), passando por um Quality Gate automático e exportando o resultado (MD/PDF), sem instalar nada no host fora do Docker.

Se não roda em Docker, não existe execução.

⸻

🎯 Princípios inegociáveis
	•	END vem antes de HOW
	•	Sem Docker = ❌ execução inválida
	•	Sem card = ❌ Cursor não trabalha
	•	Sem acceptance no Git = ❌ não libera execução
	•	Sistema não depende de atenção, percepção ou metacognição humana

⸻

✅ Critérios de Aceitação

CA-00 — Docker é gating absoluto
	•	docker compose up --build sobe o sistema em máquina limpa
	•	Um único comando de primeira execução
	•	❌ Proibido exigir Node, Python ou qualquer setup no host

⸻

CA-01 — Entrada mínima funcional
	•	Sistema aceita texto colado OU arquivo
	•	Entrada acontece via UI ou CLI (decisão posterior)
	•	Nenhum prompt manual é escrito pelo usuário

⸻

CA-02 — Tipos de resumo

O sistema entrega automaticamente:
	•	Resumo curto
	•	Resumo médio
	•	Resumo longo
	•	Bullet points
	•	Insights principais
	•	Referências a trechos do texto

⸻

CA-03 — Pipeline determinístico
	•	Usuário escolhe resultado, não técnica
	•	❌ Usuário não escreve prompt
	•	❌ Usuário não escolhe método de sumarização

⸻

CA-04 — Quality Gate automático
	•	Sistema valida se o resumo atende critérios mínimos
	•	Se falhar:
	•	tenta regenerar automaticamente ou
	•	falha explicitamente com motivo rastreável
	•	❌ Proibido depender de revisão humana

⸻

CA-05 — Rastreabilidade
	•	Cada saída referencia trechos do livro
	•	Não existe resumo "solto" ou não justificável

⸻

CA-06 — Export
	•	Exportação para:
	•	Markdown
	•	PDF
	•	Arquivos salvos em volume Docker

⸻

CA-07 — Evidência reproduzível
	•	Existe comando dentro do container:

docker compose exec app make evidence


	•	Evidências são geradas automaticamente em /EVIDENCIAS/
	•	Evidências versionadas no Git

⸻

🧱 Arquitetura (restrição, não sugestão)
	•	Tudo funciona dentro do Docker
	•	Stack é livre, desde que cumpra END e CA
	•	Pode ser 1 serviço ou múltiplos
	•	Secrets via .env (não comitar)

❌ Discussão de stack antes da DEMANDA existir é proibida

⸻

📦 Incrementos (todos com Docker desde o início)

INCR-1 — Fundação Docker + Hello Flow

END:
docker compose up sobe sistema
UI/CLI responde
Texto enviado gera "stub summary"

⸻

INCR-2 — Pipeline de sumarização v1

END:
Dentro do Docker gera:
	•	curto / médio / longo
	•	bullets

⸻

INCR-3 — Rastreabilidade

END:
Cada saída aponta para trechos do texto

⸻

INCR-4 — Quality Gate

END:
Entrega bloqueada se falhar
Regeneração ou falha explícita

⸻

INCR-5 — Export

END:
Export MD/PDF salvo em volume

⸻

INCR-6 — Evidência automática

END:
make evidence gera tudo em /EVIDENCIAS/

⸻

🛠️ O QUE O cursor DEVE FAZER (e só isso)
	1.	Criar
/DEMANDAS/DEMANDA-000_BOOK_SUMMARIZER.md
	2.	Criar
/DEMANDAS/DEMANDA-000_ACCEPTANCE.md
(com CA-00..CA-07 acima)
	3.	Criar GitHub Project Book Summarizer
	4.	Criar cards:
	•	INCR-1 … INCR-6
	5.	Não executar nada
	6.	Trazer commit para validação do CEO antes do push

⸻

🔒 Leis ativas
	•	OD-009 — Processo > Disciplina
	•	OD-010 — Resultado é entidade primária
	•	OD-011 (estendida) — Metacognição fora do caminho crítico

Frase canônica:

"Sem Docker, não existe execução. Sem card, não existe trabalho."

⸻

❓ Decisões que o CEO ainda vai tomar (não agora)

Responder apenas com A/B/C quando solicitado:
	1.	Interface do MVP
	•	(A) Web UI
	•	(B) CLI
	2.	Entrada mínima
	•	(A) Texto
	•	(B) EPUB
	•	(C) PDF sem OCR
	3.	Provider inicial
	•	(A) OpenAI
	•	(B) Anthropic
	•	(C) Gemini

⸻

Se quiser, no próximo passo eu simulo o output esperado do INCR-1 para você validar se o END está exatamente onde você quer — antes de qualquer código existir.
