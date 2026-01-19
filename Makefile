.PHONY: evidence help

help:
	@echo "Comandos disponíveis:"
	@echo "  make evidence  - Gera evidências de execução em /EVIDENCIAS/"

evidence:
	@echo "Gerando evidências..."
	@mkdir -p /app/EVIDENCIAS
	@python src/generate_evidence.py
	@echo "✅ Evidências geradas com sucesso em /app/EVIDENCIAS/"
