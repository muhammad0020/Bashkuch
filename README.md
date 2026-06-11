# Bashkuch (بشکوچ)

> **Bashkuch** is an enterprise-grade, secure, and strictly object-oriented password management system executed via a command-line interface. Inspired by the ancient Persian mythological guardian of treasures, this system is engineered to secure your digital assets through robust encryption and a decoupled architectural design.

---

## 🏛️ Core Architecture & Design Principles

Unlike basic scripts, Bashkuch is built upon solid software engineering principles designed for stability and scalability:
*   **Separation of Concerns:** Distinct isolation between the presentation layer (`menus`) and the underlying business logic (`account_manager`).
*   **Data Integrity & Constraints:** Dynamic caching and tracking of composite unique keys to eliminate record duplication and prevent state conflicts.
*   **State Persistence:** Automated and atomic state-saving mechanisms managing active and soft-deleted records.

---

## 🚀 Key Capabilities

*   **Cryptographic Security:** End-to-end local data encryption powered by `cryptography.fernet` symmetric keys.
*   **Lifecycle Management:** Comprehensive and validated operations (Create, Read, Update, Delete) for sensitive credentials.
*   **Resilience (Recycle Bin):** A dedicated soft-delete infrastructure allowing complete restoration of deleted data points.
*   **Rule-Based Generator:** Enforced password generation through dynamic character-type validation loops.
*   **System Integration:** Secure and automated interaction with the system clipboard for seamless credential deployment.

---

## 🛠️ Technical Specifications & Dependencies

| Dependency | Version | Purpose |
| :--- | :--- | :--- |
| **Python** | `3.8+` | Core Runtime Environment |
| **cryptography** | `46.0.7` | Symmetric Fernet Encryption Standard |
| **pyperclip** | `1.11.0` | Clipboard Integration & Cross-Platform Interoperability |
| **cffi** | `2.0.0` | Foreign Function Interface for C-core tasks |
| **pycparser** | `3.0` | C parser support for cryptographic backends |

---

## ⚙️ Deployment & Execution Guide

Follow these steps to deploy and execute the Bashkuch architecture in an isolated local environment:

### 1. Clone the Architecture
```bash
git clone https://github.com/muhammad0020/Bashkuch.git
cd Bashkuch
```

### 2. Environment Isolation
Initialize and activate an isolated virtual environment to prevent dependency drift:
*   **Windows:**
```cmd
    python -m venv venv
    venv\Scripts\activate
```
*   **Linux / macOS:**
```bash
    python3 -m venv venv
    source venv/bin/activate
```

### 3. Dependency Installation
Install the exact, verified product dependencies from the manifest:
```bash
pip install -r requirements.txt
```

### 4. System Launch
Execute the primary interface to start the application:
```bash
python app.py
```

---

## 🗺️ Product Roadmap

* [ ] Migration to a cross-platform graphical user interface (GUI).
* [ ] Implementation of secure, zero-knowledge cloud synchronization.
* [ ] Integration of advanced automated password strength and vulnerability audits.
* [ ] Refactor the password generation subsystem to leverage the `secrets` module for true cryptographic entropy.