#!/usr/bin/env bash
set -euo pipefail

# export-byobu-metadata.sh
#
# Export metadata about every pane in the current tmux/Byobu server.
# Does NOT capture pane contents.

timestamp=$(date '+%Y%m%d-%H%M%S')
out="${1:-$HOME/byobu-metadata-$timestamp}"

mkdir -p "$out"

summary="$out/panes.tsv"
report="$out/panes.txt"

# Machine-readable TSV
printf 'session\twindow\twindow_name\tpane\tpane_id\tactive\tcommand\tstart_command\thistory_size\tcwd\n' \
    > "$summary"

tmux list-panes -a \
    -F '#{session_name}|#{window_index}|#{window_name}|#{pane_index}|#{pane_id}|#{pane_active}|#{pane_current_command}|#{pane_start_command}|#{history_size}|#{pane_current_path}' |
while IFS='|' read -r session window name pane id active command start history cwd; do

    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
        "$session" \
        "$window" \
        "$name" \
        "$pane" \
        "$id" \
        "$active" \
        "$command" \
        "$start" \
        "$history" \
        "$cwd" \
        >> "$summary"
done

# Human-readable report
{
    echo "BYOBU/TMUX PANE METADATA"
    echo "========================"
    echo "Captured: $(date --iso-8601=seconds)"
    echo

    tmux list-panes -a \
        -F 'Session:       #{session_name}
Window:        #{window_index}
Window name:   #{window_name}
Pane:          #{pane_index}
Pane ID:       #{pane_id}
Active:        #{pane_active}
Command:       #{pane_current_command}
Start command: #{pane_start_command}
History size:  #{history_size}
Path:          #{pane_current_path}
----------------------------------------'
} > "$report"

echo "Byobu/tmux metadata exported."
echo
echo "Human-readable:"
echo "  $report"
echo
echo "Machine-readable:"
echo "  $summary"
echo

column -t -s $'\t' "$summary" 2>/dev/null || cat "$summary"
