#!/bin/bash

# GitHub repository URL (hardcoded for Sophy)
repo_url="https://github.com/bastiaandehaan/Sophy.git"
repo_name="Sophy"

# Output file
output_file="${repo_name}_context.md"

# Remove the output file if it already exists
rm -f "$output_file"

# Function to process each file
process_file() {
    local file="$1"
    echo "Processing file: $file"
    echo "Path: $file" >> "$output_file"
    echo "" >> "$output_file"

    # Determine the file extension
    extension="${file##*.}"

    # Set the appropriate language for the code block
    case "$extension" in
        toml) language="toml" ;;
        md) language="" ;;  # Markdown heeft geen specifieke highlighting
        R) language="r" ;;
        Rmd) language="r" ;;
        py) language="python" ;;  # Toegevoegd voor Python-bestanden
        json) language="json" ;;  # Toegevoegd voor JSON-bestanden
        yml) language="yaml" ;;   # Toegevoegd voor YAML-bestanden
        txt) language="plaintext" ;;  # Toegevoegd voor tekstbestanden
        *) language="plaintext" ;;
    esac

    echo "\`\`\`$language" >> "$output_file"
    cat "$file" >> "$output_file"
    echo "\`\`\`" >> "$output_file"
    echo "" >> "$output_file"
    echo "-----------" >> "$output_file"
    echo "" >> "$output_file"
}

# Check if required tools are installed
for tool in git fd; do
    if ! command -v $tool &> /dev/null; then
        echo "Error: $tool is not installed. Please install $tool and try again."
        exit 1
    fi
done

# Create a temporary directory for cloning
temp_dir=$(mktemp -d)

# Clone the repository
echo "Cloning repository..."
git clone "$repo_url" "$temp_dir"

# Change to the cloned repository directory
cd "$temp_dir"

# Find files using fd, sort them by depth, then process each file
fd -H -t f -e py -e md -e json -e yml -e txt | sort -n -t'/' -k'1' | while read -r file; do
    process_file "$file"
done

# Move the output file to the original directory
mv "$output_file" "$OLDPWD"

# Change back to the original directory
cd "$OLDPWD"

# Clean up: remove the temporary directory
rm -rf "$temp_dir"

echo "Repository contents have been processed and combined into $output_file"
