#!/bin/bash

# Set working directory to the directory where the script is located
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# Run pytest targeting the nested tests folder
pytest tests