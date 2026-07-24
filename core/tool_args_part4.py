BUILTIN_ARGS = {
    "exiftool": [
        ("image.jpg", "Read metadata"),
        ("-a -G1 image.jpg", "All metadata"),
        ("-all= image.jpg", "Remove all metadata"),
    ],
    "binwalk": [
        ("firmware.bin", "Scan file"),
        ("-e firmware.bin", "Extract files"),
        ("-Me firmware.bin", "Recursive extract"),
    ],
    "steghide": [
        ("embed -cf cover.jpg -ef secret.txt", "Embed file"),
        ("extract -sf stego.jpg", "Extract file"),
        ("embed -cf cover.jpg -ef secret.txt -p password", "With password"),
    ],
    "sherlock": [
        ("username", "Search username"),
        ("username --output results/ --csv", "Save results CSV"),
        ("username --site twitter,instagram,facebook", "Specific sites"),
    ],
    "theHarvester": [
        ("-d target.com -b google", "Google search"),
        ("-d target.com -b all", "All sources"),
        ("-d target.com -b linkedin", "LinkedIn search"),
        ("-d target.com -b google -f report.html", "Save HTML"),
    ],
    "amass": [
        ("enum -d target.com", "Basic enum"),
        ("enum -passive -d target.com", "Passive only"),
        ("enum -active -d target.com", "Active enum"),
    ],
    "subfinder": [
        ("-d target.com", "Basic subdomain"),
        ("-d target.com -silent", "Silent mode"),
        ("-d target.com -o subs.txt", "Save to file"),
    ],
}
