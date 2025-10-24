#!/bin/bash
# Run tests without NO_COLOR/FORCE_COLOR warnings

# Set FORCE_COLOR to 0 to disable colored output and avoid warnings
export FORCE_COLOR=0

# Run the command passed as arguments
"$@"
