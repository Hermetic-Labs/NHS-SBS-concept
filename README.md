# NHS SBS CQ Portal - Healthcare AI Solutions Framework (Lot 7)

> **⚠️ DEMONSTRATIVE PROTOTYPE**
> 
> This portal and its underlying architecture are provided for **demonstrative purposes only** as a practical example of consultancy and technical services for the **NHS SBS10523 Healthcare AI Solutions Framework (Lot 7) bid**. 
> 
> While the framework information is public, this specific repository is **not** intended for mass production deployment or active healthcare distribution. All code, AI logic, and interfaces herein are tailored to showcase rapid AI prototyping, offline RAG capabilities, and modern UI implementation for NHS evaluation.

---

## Overview

This project is a fully offline, air-gapped Retrieval-Augmented Generation (RAG) portal designed to instantly index and query Clarification Questions (CQs) and extensive framework literature regarding the £900m NHS SBS AI Solutions Framework.

## How to Run Locally (Windows)

The entire backend intelligence and frontend routing is designed to run locally without external dependencies (aside from standard Python libraries).

1. Clone or download this repository to your local machine.
2. Double-click the `start.bat` file in the root directory.
3. The batch script will automatically:
   - Establish the Python Virtual Environment (`venv`)
   - Install any missing pip requirements
   - Boot the local FastAPI server (`http://127.0.0.1:7778`)
   - Launch your default web browser directly into the portal.

## Notice for Apple / Mac Users

The automated startup script (`start.bat`) is currently configured for Windows environments. 

For the Apple crowd, to achieve native app-like execution without terminal commands, you may wrap this frontend web architecture in **Capacitor** (or Electron). Alternatively, you can run the backend manually via terminal:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python backend/main.py
```
*(Once the backend is running, simply open `frontend/index.html` in Safari/Chrome).*
