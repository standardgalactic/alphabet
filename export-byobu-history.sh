#!/usr/bin/env bash
set -euo pipefail

# export-byobu-history.sh
#
# Export the complete retained tmux/Byobu scrollback history
# for every pane on the current tmux server.
#
# - One text file per pane
# - Joins terminal-wrapped lines (-J)
# - Captures from oldest retained history to current screen
# - Creates a timestamped output directory

timestamp=$(date '+%Y%m%d-%H%M%S')
out="${1:-$HOME/byobu-history-$timestamp}"

mkdir -p "$out"

echo "Exporting Byobu/tmux pane histories..."
echo "Destination: $out"
echo

count=0

tmux list-panes -a \
    -F '#{session_name}|#{window_index}|#{window_name}|#{pane_index}|#{pane_id}|#{pane_current_path}' |
while IFS='|' read -r session window window_name pane pane_id cwd; do

    # Make names filesystem-safe.
    safe_session=$(printf '%s' "$session" |
        sed 's/[^[:alnum:]_.-]/_/g')

    safe_name=$(printf '%s' "$window_name" |
        sed 's/[^[:alnum:]_.-]/_/g')

    filename=$(printf '%s/session-%s_window-%s_%s_pane-%s_%s.txt' \
        "$out" \
        "$safe_session" \
        "$window" \
        "$safe_name" \
        "$pane" \
        "${pane_id#%}")

    echo "[$pane_id] $session:$window.$pane"
    echo "    $cwd"
    echo " -> $filename"

    {
        printf 'TMUX/BYOBU HISTORY EXPORT\n'
        printf '=========================\n'
        printf 'Exported: %s\n' "$(date --iso-8601=seconds)"
        printf 'Session:  %s\n' "$session"
        printf 'Window:   %s (%s)\n' "$window" "$window_name"
        printf 'Pane:     %s (%s)\n' "$pane" "$pane_id"
        printf 'Path:     %s\n' "$cwd"
        printf '\n'
        printf '%s\n\n' '------------------------------------------------------------'

        tmux capture-pane \
            -p \
            -J \
            -S - \
            -E - \
            -t "$pane_id"

    } > "$filename"

    count=$((count + 1))
done

echo
echo "Export complete."
echo
du -sh "$out"
echo
find "$out" -maxdepth 1 -type f -printf '%f\n' | sort
