#!/usr/bin/env bash
# Rotina diária: tendências + stories do dia (instruções em ROTINA.md).
# O cron chama de hora em hora; roda uma vez por dia, a partir das 10h, e no máximo 2 tentativas.
# Assim, se o PC/WSL estava desligado às 10h, roda na primeira hora em que estiver ligado.
set -uo pipefail
cd /home/mucida/3d-instagram || exit 1
export TZ=America/Sao_Paulo
export PATH=/home/mucida/.nvm/versions/node/v23.3.0/bin:/home/mucida/miniconda3/bin:/usr/local/bin:/usr/bin:/bin
# Token de longa duração do `claude setup-token`, guardado fora do repo (chmod 600):
#   CLAUDE_CODE_OAUTH_TOKEN=...
[ -f "$HOME/.config/claude-rotina.env" ] && set -a && . "$HOME/.config/claude-rotina.env" && set +a
HOJE=$(date +%F)
[ -z "${FORCAR:-}" ] && [ "$(date +%H)" -lt 10 ] && exit 0
[ -f "diario/$HOJE.md" ] && exit 0
mkdir -p diario/logs
TENT="diario/logs/$HOJE.tentativas"
N=$(( $(cat "$TENT" 2>/dev/null || echo 0) + 1 ))
[ "$N" -gt 2 ] && exit 0
echo "$N" > "$TENT"
LOG="diario/logs/$HOJE.log"
exec 9>.tmp-rotina.lock; flock -n 9 || exit 0
echo "== tentativa $N · $(date '+%F %T')" >> "$LOG"
git pull -q --rebase >> "$LOG" 2>&1
claude -p "Hoje é $HOJE (America/Sao_Paulo). Leia ROTINA.md na raiz desta pasta e siga as instruções à risca para hoje. Responda em português do Brasil." \
  --model sonnet \
  --allowedTools "Read" "Write" "Edit" "Glob" "Grep" "WebSearch" "WebFetch" \
    "Bash(node:*)" "Bash(npm:*)" "Bash(npx:*)" "Bash(python3:*)" "Bash(ls:*)" "Bash(mkdir:*)" "Bash(cp:*)" "Bash(date:*)" \
    "Bash(git status:*)" "Bash(git add:*)" "Bash(git commit:*)" "Bash(git push:*)" "Bash(git log:*)" "Bash(git diff:*)" \
  >> "$LOG" 2>&1
RC=$?
echo "== fim $(date '+%T') · saída $RC" >> "$LOG"
