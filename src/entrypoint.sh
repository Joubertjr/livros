#!/bin/bash
set -e

MODE="${1:-web}"

echo "===================================="
echo "CoverageSummarizer - Starting..."
echo "Mode: $MODE"
echo "===================================="

if [ "$MODE" = "web" ]; then
    echo "🌐 Starting Web UI server..."
    echo "📍 Access at: http://localhost:8000"
    echo "📚 API Docs at: http://localhost:8000/api/docs"
    echo ""
    exec uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload

elif [ "$MODE" = "cli" ]; then
    echo "💻 CLI Mode - Container ready for commands"
    echo "Run: docker exec -it book_summarizer python src/main.py --help"
    echo ""
    # Keep container alive for CLI commands
    exec tail -f /dev/null

else
    echo "🔧 Custom command mode"
    exec "$@"
fi
