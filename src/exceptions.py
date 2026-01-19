"""
Exceções customizadas para o CoverageSummarizer.
"""


class CoverageError(Exception):
    """Erro quando cobertura não atinge 100% após max tentativas."""
    pass
