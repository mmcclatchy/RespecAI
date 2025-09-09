#!/bin/bash

# Research-Advisor Archive Scanner
# Quick archive assessment for gap analysis and context gathering

# Get archive directory from settings.json with environment variable override
if [[ -x ~/.claude/scripts/read-settings.sh ]]; then
    ARCHIVE_DIR=$(~/.claude/scripts/read-settings.sh archive-dir)
else
    ARCHIVE_DIR="${CLAUDE_RESEARCH_ARCHIVE_DIR:-$HOME/.claude/best-practices}"
fi

# Function to scan archives for research-advisor context
scan_archives_for_context() {
    local topic_query="$1"
    
    echo "Research Archive Scan for: $topic_query"
    echo "======================================="
    echo ""
    
    local found_relevant=0
    
    for file in $ARCHIVE_DIR/*.md; do
        if [[ -f "$file" ]]; then
            local basename=$(basename "$file" .md)
            local head_content=$(head -20 "$file")
            
            # Check if archive is relevant to query
            if echo "$head_content" | grep -qi "$topic_query"; then
                echo "📄 RELEVANT: $basename"
                echo "────────────────────────────────────"
                
                # Show metadata summary
                echo "$head_content" | head -15
                echo ""
                echo "⚡ Quick Assessment:"
                echo "   Contains: $(echo "$head_content" | grep -i "$topic_query" | wc -l) matches for '$topic_query'"
                echo "   File: $file"
                echo ""
                
                ((found_relevant++))
            fi
        fi
    done
    
    if [[ $found_relevant -eq 0 ]]; then
        echo "No relevant archives found for: $topic_query"
        echo ""
        echo "Available archive topics:"
        for file in $ARCHIVE_DIR/*.md; do
            if [[ -f "$file" ]]; then
                local topic=$(head -1 "$file" | sed 's/# Research Archive: //')
                echo "  - $topic"
            fi
        done
    else
        echo "Found $found_relevant relevant archives for context."
        echo ""
        echo "research-advisor can now:"
        echo "1. Use these summaries to identify knowledge gaps"
        echo "2. Access full content via file paths for detailed analysis"
        echo "3. Reference package versions for relevance assessment"
    fi
}

# Usage
if [[ $# -eq 0 ]]; then
    echo "Usage: $0 TOPIC"
    echo ""
    echo "Scan research archives for topic relevance"
    echo "Examples:"
    echo "  $0 fastapi        # Find FastAPI-related archives"
    echo "  $0 authentication # Find authentication patterns"
    echo "  $0 htmx           # Find HTMX integration archives"
    exit 1
fi

scan_archives_for_context "$1"