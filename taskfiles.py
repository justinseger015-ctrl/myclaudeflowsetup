#!/usr/bin/env python3
"""
Task Files Capture Utility
Captures neural enhancement task files and outputs their paths, names, and contents.
"""

import os
from pathlib import Path
from datetime import datetime

# Base directory
BASE_DIR = Path("/home/cabdru/claudeflowblueprint")

# List of task files to capture
FILES_TO_CAPTURE = [
    "docs2/neuralenhancement/specs/tasks/TASK-NEURAL-001.md",
    "docs2/neuralenhancement/specs/tasks/TASK-NEURAL-002.md",
    "docs2/neuralenhancement/specs/tasks/TASK-NEURAL-003.md",
    "docs2/neuralenhancement/specs/tasks/TASK-NEURAL-004.md",
    "docs2/neuralenhancement/specs/tasks/TASK-NEURAL-005.md",
    "docs2/neuralenhancement/specs/tasks/TASK-NEURAL-006.md",
    "docs2/neuralenhancement/specs/tasks/TASK-NEURAL-007.md",
    "docs2/neuralenhancement/specs/tasks/TASK-NEURAL-008.md",
    "docs2/neuralenhancement/specs/tasks/TASK-NEURAL-009.md",
    "docs2/neuralenhancement/specs/tasks/TASK-NEURAL-010.md",
    "docs2/neuralenhancement/specs/tasks/TASK-NEURAL-011.md",
    "docs2/neuralenhancement/specs/tasks/TASK-NEURAL-012.md",
    "docs2/neuralenhancement/specs/tasks/TASK-NEURAL-013.md",
    "docs2/neuralenhancement/specs/implementation-roadmap.md",
]

def capture_files():
    """Capture all specified task files and write to output file."""
    output_file = BASE_DIR / "task_files_output.txt"

    with open(output_file, 'w', encoding='utf-8') as out:
        # Write header
        out.write("=" * 80 + "\n")
        out.write("NEURAL ENHANCEMENT TASK FILES CAPTURE REPORT\n")
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
