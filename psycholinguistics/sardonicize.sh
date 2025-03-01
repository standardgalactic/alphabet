#!/usr/bin/env bash
set -Eeuo pipefail

# Number of lines per chunk
CHUNK_LINES=100

SUMMARY_COMMAND=("ollama" "run" "vanilj/phi-4")
CRITIQUE_COMMAND=("ollama" "run" "vanilj/phi-4")
SARDONIC_COMMAND=("ollama" "run" "vanilj/phi-4")
PROGRESS_FILE="progress.log"

main_dir="$(pwd)"
touch "$main_dir/$PROGRESS_FILE"

log() {
    local message="[${USER:-$(whoami)}@$(hostname)] [$(date '+%Y-%m-%d %H:%M:%S')] $*"
    echo "$message"
    echo "$message" | tee -a "$main_dir/$PROGRESS_FILE"
}

is_processed() {
    local file_path="$1"
    grep -Fxq "$file_path" "$main_dir/$PROGRESS_FILE"
}

mark_processed() {
    local file_path="$1"
    echo "$file_path" >> "$main_dir/$PROGRESS_FILE"
}

cleanup_tempdirs() {
    if [[ -n "${TEMP_DIRS_CREATED:-}" ]]; then
        for tmpd in $TEMP_DIRS_CREATED; do
            [[ -d "$tmpd" ]] && rm -rf "$tmpd"
            log "Cleaned up temporary directory: $tmpd"
        done
    fi
}
trap cleanup_tempdirs EXIT

log "Script started."

process_files_in_directory() {
    local dir="$1"
    log "Processing directory: $dir"

    shopt -s nullglob
    local all_files=("$dir"/*.txt)
    shopt -u nullglob

    [[ ${#all_files[@]} -eq 0 ]] && {
        log "No files found in $dir"
        return
    }

    for file in "${all_files[@]}"; do
        [[ -f "$file" && ! -L "$file" ]] || continue

        if ! is_processed "$file"; then
            local file_name="$(basename "$file")"
            log "Processing file: $file"

            local sanitized_name
            sanitized_name="$(echo "$file_name" | tr -d '[:space:]')"
            local temp_dir
            temp_dir="$(mktemp -d "$dir/tmp_${sanitized_name}_XXXXXX")"
            TEMP_DIRS_CREATED="${TEMP_DIRS_CREATED:-} $temp_dir"
            log "Created temporary directory: $temp_dir"

            local preprocessed_file="$temp_dir/preprocessed.txt"
            cp "$file" "$preprocessed_file"

            split -l "$CHUNK_LINES" -- "$preprocessed_file" "$temp_dir/chunk_"
            log "Split $file into chunks of $CHUNK_LINES lines each."

            local summary_file="$dir/${file_name%.txt}-overview.txt"
            local critique_file="$dir/${file_name%.txt}-critique.txt"
            local sardonic_file="$dir/${file_name%.txt}-sardonic.txt"
            touch "$summary_file" "$critique_file" "$sardonic_file"
            log "Summaries will go to $summary_file"
            log "Critiques will go to $critique_file"
            log "Sardonic reviews will go to $sardonic_file"

            for chunk_file in "$temp_dir"/chunk_*; do
                [[ -f "$chunk_file" ]] || continue
                local chunk_name="$(basename "$chunk_file")"
                log "Processing chunk: $chunk_name"

                # Summarize
                {
                    echo "Summarize the following text from \"$file_name\"."
                    echo "Focus on main ideas, ignoring extraneous details."
                    echo "---------------"
                    cat "$chunk_file"
                } | "${SUMMARY_COMMAND[@]}" 2>>"$main_dir/$PROGRESS_FILE" | tee -a "$summary_file"

                # Critique
                {
                    echo "Critique the following text from \"$file_name\"."
                    echo "Identify contradictions, confusions, and provide counterarguments."
                    echo "---------------"
                    cat "$chunk_file"
                } | "${CRITIQUE_COMMAND[@]}" 2>>"$main_dir/$PROGRESS_FILE" | tee -a "$critique_file"

                # Sardonic review
                {
                    echo "Provide a sardonic, clickbaity, sarcastic, biting review for the following text from \"$file_name\"."
                    echo "---------------"
                    cat "$chunk_file"
                } | "${SARDONIC_COMMAND[@]}" 2>>"$main_dir/$PROGRESS_FILE" | tee -a "$sardonic_file"

                log "Chunk $chunk_name processed."
            done

            mark_processed "$file"
            log "Marked $file as processed."
        fi
    done
}

process_files_in_directory "$main_dir"

process_subdirectories() {
    local parent_dir=$1

    for dir in "$parent_dir"/*/; do
        if [ -d "$dir" ]; then
            process_files_in_directory "$dir"
            process_subdirectories "$dir"
        fi
    done
}

process_subdirectories "$main_dir"

log "Script completed."
