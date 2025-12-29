#!/bin/bash
# Log deployment-related commands for audit trail

# Read the tool input from stdin
INPUT=$(cat)

# Extract command
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Check if it's a deployment-related command
if echo "$COMMAND" | grep -qE '(deploy|rollback|release)'; then
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    LOG_FILE="${HOME}/.claude/deploy-audit.log"

    # Ensure log directory exists
    mkdir -p "$(dirname "$LOG_FILE")"

    # Log the command
    echo "[$TIMESTAMP] Command: $COMMAND" >> "$LOG_FILE"

    # Also log exit code if available
    EXIT_CODE=$(echo "$INPUT" | jq -r '.tool_result.exit_code // empty')
    if [ -n "$EXIT_CODE" ]; then
        echo "[$TIMESTAMP] Exit Code: $EXIT_CODE" >> "$LOG_FILE"
    fi
fi

# Always exit 0 to not block the operation
exit 0
