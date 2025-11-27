#!/usr/bin/env python3
"""
File Capture Utility
Captures specified files and outputs their paths, names, and contents to a single text file.
"""

import os
from pathlib import Path
from datetime import datetime

# Base directory
BASE_DIR = Path("/home/cabdru/claudeflowblueprint")

# List of files to capture
FILES_TO_CAPTURE = [
    "docs/specs/01-functional-specs/_index.md",
    "docs/specs/01-functional-specs/02-daa-initialization.md",
    "docs/specs/01-functional-specs/03-agent-lifecycle.md",
    "docs/specs/01-functional-specs/04-knowledge-sharing.md",
    "docs/specs/01-functional-specs/05-pattern-management.md",
    "docs/specs/01-functional-specs/06-meta-learning.md",
    "docs/specs/01-functional-specs/07-monitoring-health.md",
    "docs/specs/02-technical-specs/_index.md",
    "docs/specs/02-technical-specs/01-system-architecture.md",
    "docs/specs/02-technical-specs/02-api-design.md",
    "docs/specs/02-technical-specs/03-database-schema.md",
    "docs/specs/02-technical-specs/04-security-auth.md",
    "docs/specs/02-technical-specs/05-deployment-infrastructure.md",
    "docs/specs/02-technical-specs/06-integration-patterns.md",
    "docs/specs/04-context-templates/activeContext.md",
    "docs/specs/04-context-templates/decisionLog.md",
    "docs/specs/04-context-templates/progressTracking.md",
    "docs/specs/04-context-templates/sessionRestoration.md",
    "docs/specs/00-project-constitution.md",
    "docs/specs/03-task-specs.md",
    "docs/specs/VERIFICATION-REPORT.md",
    "docs2/neuralenhancement/NEURAL-ENHANCEMENT-FIXES-SUMMARY.md",
    "docs2/neuralenhancement/neural-enhancement-immediate.md",
    "docs2/neuralenhancement/neural-enhancement-short-term.md",
    "docs2/neuralenhancement/neural-pattern-expiry-checker.js",
]

def capture_files():
    """Capture all specified files and write to output file."""
    output_file = BASE_DIR / "captured_files_output.txt"

    with open(output_file, 'w', encoding='utf-8') as out:
        # Write header
        out.write("=" * 80 + "\n")
        out.write("FILE CAPTURE REPORT\n")
        out.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out.write(f"Total files to capture: {len(FILES_TO_CAPTURE)}\n")
        out.write("=" * 80 + "\n\n")

        captured_count = 0
        missing_count = 0

        for relative_path in FILES_TO_CAPTURE:
            file_path = BASE_DIR / relative_path

            out.write("\n" + "=" * 80 + "\n")
            out.write(f"FILE NAME: {file_path.name}\n")
            out.write(f"FILE PATH: {file_path}\n")
            out.write(f"RELATIVE PATH: {relative_path}\n")
            out.write("=" * 80 + "\n\n")

            if file_path.exists() and file_path.is_file():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    out.write("CONTENTS:\n")
                    out.write("-" * 80 + "\n")
                    out.write(content)
                    out.write("\n" + "-" * 80 + "\n")

                    captured_count += 1
                    print(f"✓ Captured: {relative_path}")

                except Exception as e:
                    out.write(f"ERROR READING FILE: {str(e)}\n")
                    print(f"✗ Error reading: {relative_path} - {str(e)}")
                    missing_count += 1
            else:
                out.write("FILE NOT FOUND OR NOT ACCESSIBLE\n")
                print(f"✗ Not found: {relative_path}")
                missing_count += 1

            out.write("\n")

        # Write summary
        out.write("\n" + "=" * 80 + "\n")
        out.write("SUMMARY\n")
        out.write("=" * 80 + "\n")
        out.write(f"Total files requested: {len(FILES_TO_CAPTURE)}\n")
        out.write(f"Successfully captured: {captured_count}\n")
        out.write(f"Missing or errors: {missing_count}\n")
        out.write("=" * 80 + "\n")

    print(f"\n{'=' * 80}")
    print(f"Capture complete!")
    print(f"Output file: {output_file}")
    print(f"Successfully captured: {captured_count}/{len(FILES_TO_CAPTURE)} files")
    print(f"{'=' * 80}")

    return output_file, captured_count, missing_count

if __name__ == "__main__":
    try:
        output_file, captured, missing = capture_files()
        exit(0 if missing == 0 else 1)
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        exit(1)
