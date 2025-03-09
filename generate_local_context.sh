#!/bin/bash

# Lokale map van de Sophy-repository (pas dit aan naar jouw projectpad)
local_dir="C:/Users/basti/PycharmProjects/Sophy"  # Windows-pad met forward slashes
repo_name="Sophy"
output_file="${repo_name}_local_context.md"  # Aangepast naar _local_context.md

# Verwijder het uitvoerbestand als het al bestaat
rm -f "$output_file"

# Functie om elk bestand te verwerken
process_file() {
    local file="$1"
    echo "Processing file: $file"
    echo "Path: $file" >> "$output_file"
    echo "" >> "$output_file"

    # Bepaal de bestandsextensie
    extension="${file##*.}"

    # Stel de juiste taal in voor het codeblok
    case "$extension" in
        toml) language="toml" ;;
        md) language="" ;;
        R) language="r" ;;
        Rmd) language="r" ;;
        py) language="python" ;;
        json) language="json" ;;
        yml) language="yaml" ;;
        txt) language="plaintext" ;;
        *) language="plaintext" ;;
    esac

    echo "\`\`\`$language" >> "$output_file"
    cat "$file" >> "$output_file" 2>/dev/null || type "$file" >> "$output_file"  # Fallback voor Windows
    echo "\`\`\`" >> "$output_file"
    echo "" >> "$output_file"
    echo "-----------" >> "$output_file"
    echo "" >> "$output_file"
}

# Controleer of vereiste tools zijn geïnstalleerd
for tool in fd; do  # Verwijder 'git' omdat we niet meer clonen
    if ! command -v "$tool" &> /dev/null; then
        echo "Error: $tool is not installed. Please install $tool (e.g., via Chocolatey) and try again."
        exit 1
    fi
done

# Controleer of de lokale map bestaat
if [ ! -d "$local_dir" ]; then
    echo "Error: De lokale map $local_dir bestaat niet. Pas local_dir aan naar het juiste pad."
    exit 1
fi

# Verwerk bestanden in de lokale map
cd "$local_dir"
fd -H -t f -e py -e md -e json -e yml -e txt | sort -n -t'/' -k'1' | while read -r file; do
    process_file "$file"
done

# Verplaats het uitvoerbestand naar de oorspronkelijke directory
mv "$output_file" "$OLDPWD"

# Keer terug naar de oorspronkelijke directory
cd "$OLDPWD"

echo "Lokale repository inhoud is verwerkt en gecombineerd in $output_file"