<p align="center">
  <img src="logo.png" width="250" alt="ShadowForensic Logo">
</p>

<h1 align="center">🕵️‍♂️ ShadowForensic</h1>

<p align="center">
  <strong>Professional Windows Volume Shadow Copy (VSS) Analysis & Data Recovery Toolkit</strong>
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python Version"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://github.com/ismailtsdln/ShadowForensic/actions"><img src="https://github.com/ismailtsdln/ShadowForensic/actions/workflows/ci.yml/badge.svg" alt="CI Status"></a>
</p>

---

## 📖 Overview

**ShadowForensic** is a state-of-the-art forensic tool designed to streamline the investigation of Windows Volume Shadow Copies. Built for Digital Forensics and Incident Response (DFIR) professionals, it provides a modular, reliable, and high-performance framework to interact with the Volume Shadow Copy Service (VSS).

Unlike traditional scripts, ShadowForensic offers a robust CLI experience, multi-threaded recovery capabilities, and deep integration with Windows system calls for maximum efficiency.

## ✨ Key Features

- **🔍 Advanced Listing:** Detailed enumeration of all shadow copies, including creation dates and device objects.
- **🆕 Live Creation:** Instantly create new shadow copies for point-in-time forensic snapshots.
- **📁 GlobalRoot Mounting:** Securely mount shadow copies using symbolic links to bypass standard access restrictions.
- **🚀 Turbo Recovery:** Multi-threaded file extraction engine with customizable filters (extensions, sizes, etc.).
- **🎨 Premium UI/UX:** A beautiful, colorized CLI interface with progress indicators and structured data tables.
- **🛡️ Forensic Integrity:** Preserves original file metadata (timestamps) during the recovery process.

## 🛠 Installation

### Prerequisites
- **Windows OS** (Required for VSS interaction)
- **Python 3.10+**
- **Administrator Privileges** (Required for mounting and VSS operations)

### Setup
```bash
# Clone the repository
git clone https://github.com/ismailtsdln/ShadowForensic.git
cd ShadowForensic

# Install the library and its dependencies
pip install .
```

## 🚀 Quick Start

### 1. List All Available Shadow Copies
```bash
shadowforensic list
```

### 2. Create a Point-in-Time Snapshot
```bash
shadowforensic create C:
```

### 3. Mount a Copy for Manual Inspection
```bash
shadowforensic mount {SHADOW_ID} C:\mnt\investigation_vss
```

### 4. Perform Advanced File Recovery
```bash
# Recover all JPEG and PDF files from a specific shadow copy
shadowforensic recover {SHADOW_ID} --filter "*.jpg" --filter "*.pdf" --output ./evidence_dump
```

## 🏗 Modular Architecture

ShadowForensic is built with extensibility in mind. You can use its core modules directly in your Python projects:

```python
from shadowforensic.vss.wrapper import VSSWrapper
from shadowforensic.core.scanner import FileScanner, RecoveryOptions

vss = VSSWrapper()
copies = vss.list_shadow_copies()

# High-performance scanning
options = RecoveryOptions(filters=["*.docx"])
scanner = FileScanner(source_path="C:\\mnt\\shadow", target_path="./recovered", options=options)
scanner.run()
```

## 🛡️ Security & Ethics

This tool is designed for **forensic professionals, incident responders, and authorized auditors**. Unauthorized use of this tool for accessing data on systems you do not own or have explicit permission to test is a violation of law and ethics. Use responsibly.

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

<p align="center">
  Developed with ❤️ by <a href="https://github.com/ismailtsdln">Ismail Tasdelen</a>
</p>
