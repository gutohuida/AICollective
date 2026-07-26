#!/usr/bin/env bash
# Install the skills in this directory into every agent CLI found on this machine.
#
#   ./install.sh                 user-level, all detected agents
#   ./install.sh /path/to/repo   also installs <repo>/.agents/skills/
#
# Safe to re-run: it overwrites, so use it to re-sync after editing a skill here.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS=()
for d in "$SRC"/*/; do
  [ -f "$d/SKILL.md" ] && SKILLS+=("$(basename "$d")")
done

if [ ${#SKILLS[@]} -eq 0 ]; then
  echo "No skills found in $SRC" >&2
  exit 1
fi

installed=0

install_to() {
  local dest="$1" label="$2"
  mkdir -p "$dest"
  for s in "${SKILLS[@]}"; do
    rm -rf "$dest/$s"
    cp -r "$SRC/$s" "$dest/$s"
  done
  echo "  ✓ $label → $dest"
  installed=$((installed + 1))
}

echo "Installing: ${SKILLS[*]}"
echo

# Claude Code — user-level, applies to every project
[ -d "$HOME/.claude" ] && install_to "$HOME/.claude/skills" "Claude Code"

# Codex — user-level only; it has no project-level discovery
if [ -d "${CODEX_HOME:-$HOME/.codex}" ]; then
  install_to "${CODEX_HOME:-$HOME/.codex}/skills" "Codex"
fi

# Kimi — brand dir plus the generic .agents convention
[ -d "$HOME/.kimi-code" ] && install_to "$HOME/.kimi-code/skills" "Kimi"

# .agents/ is honored by Kimi and OpenCode at user level
if [ -d "$HOME/.kimi-code" ] || [ -d "$HOME/.config/opencode" ]; then
  install_to "$HOME/.agents/skills" "Kimi + OpenCode (generic)"
fi

# OpenCode — its own config dir
[ -d "$HOME/.config/opencode" ] && install_to "$HOME/.config/opencode/skill" "OpenCode"

# Optional project target: .agents/ reaches Kimi and OpenCode inside that repo
if [ $# -ge 1 ]; then
  proj="$1"
  if [ ! -d "$proj" ]; then
    echo "Project directory not found: $proj" >&2
    exit 1
  fi
  install_to "$proj/.agents/skills" "project (Kimi + OpenCode)"
  if git -C "$proj" check-ignore -q .agents/ 2>/dev/null; then
    echo
    echo "  note: .agents/ is gitignored in $proj — skills work locally but"
    echo "        won't be committed. Add '!.agents/skills/' to keep them tracked."
  fi
fi

echo
if [ $installed -eq 0 ]; then
  echo "No agent CLIs detected. Nothing installed."
  exit 1
fi
echo "Done — $installed location(s). Start a new session to pick them up."
