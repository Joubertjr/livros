.PHONY: evidence help sync-metodo

help:
	@echo "Comandos disponíveis:"
	@echo "  make evidence      - Gera evidências de execução em /EVIDENCIAS/"
	@echo "  make sync-metodo   - Sincroniza pasta METODO/ do repositório endfirst-ecosystem"

evidence:
	@echo "Gerando evidências..."
	@mkdir -p /app/EVIDENCIAS
	@python src/generate_evidence.py
	@echo "✅ Evidências geradas com sucesso em /app/EVIDENCIAS/"

sync-metodo:
	@echo "Sincronizando pasta METODO/ do repositório remoto..."
	@python scripts/sync_metodo.py
	@echo "✅ Sincronização concluída!"
