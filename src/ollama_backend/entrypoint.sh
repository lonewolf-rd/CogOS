#!/bin/sh
set -e
ollama serve &
OLLAMA_PID=$!
(sleep 5 ollama pull gemma3:4b-it-q4_K_M || true) & wait "$OLLAMA_PID"
