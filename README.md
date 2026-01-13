# 🕵️‍♂️ ShadowForensic

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**ShadowForensic** is a professional, modular forensic tool designed for Windows Volume Shadow Copy Service (VSS) analysis and data recovery.

## 🚀 Features

-   🔍 **List:** Identify all existing Volume Shadow Copies on the system.
-   🆕 **Create:** Create new shadow copies for point-in-time analysis.
-   📂 **Mount:** Access shadow copies via symbolic links or named pipes.
-   🔋 **Recover:** Advanced file recovery with filters (large files, hidden files, metadata preservation).
-   💻 **Modern CLI:** Beautiful and intuitive interface powered by `Typer` and `Rich`.
-   🛠 **Modular API:** Can be integrated into larger forensic workflows.

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/ismailtsdln/ShadowForensic.git
cd ShadowForensic

# Install dependencies (Windows required for full functionality)
pip install .
```

## 🛠 Usage

```bash
# List all shadow copies
shadowforensic list

# Create a new shadow copy for drive C:
shadowforensic create C:

# Mount a shadow copy
shadowforensic mount {id} /mnt/shadow

# Recover files from a shadow copy
shadowforensic recover {id} --filter "*.docx" --output ./recovered
```

## 🛡 Security & Ethics

This tool is intended for forensic professionals and authorized security audits. Unauthorized use on systems you do not own or have explicit permission to test is prohibited.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
