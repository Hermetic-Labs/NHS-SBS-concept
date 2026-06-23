# NHS SBS Healthcare AI Solutions (SBS10523) - Data Aggregation Audit

## 1. Framework Context (From Web & Documents)
*   **Framework Name:** NHS SBS Healthcare AI Solutions
*   **Reference:** SBS10523
*   **Total Estimated Value:** £900 million
*   **Framework Term:** 12 May 2027 to 11 May 2035
*   **Original/Extended Deadline:** 7 July 2026, 12:00 noon
*   **Target Lot:** Lot 7 (Advisory and Specialised Support)
*   **Buyer Goal:** Support adoption of AI across health and care systems (diagnostics, predictive analytics, robotics, efficiency, governance).

## 2. Existing Local Repository Assets
The following files in the `d:\Minimax\docs\` directory are relevant to this initiative and will be ingested or referenced by the portal:
1.  **`Bidder_Copy_Clarification_Qs_Healthcare_AI_SBS10525_BATCH 2_03_06_26.xlsx`**
    *   *Role:* The core dataset. Will be parsed into SQLite/JSON and embedded for semantic search.
2.  **`NHS-Lot7-Contract-Examples.md`**
    *   *Role:* Contains context on Hermetic Labs' capabilities (e.g., AI readiness, DPIA support, DTAC support). Will inform the "About" or "Capabilities" section of the portal to silently sell your Lot 7 expertise.
3.  **`NHS-Lot7-Free-Tasks.md`**
    *   *Role:* Administrative context.
4.  **`NHS-SBS-Lot7-Sprint-Task-List.md`**
    *   *Role:* Timeline and project management context.

## 3. UI / UX Direction
*   **Vibe:** Sleek, clinical, highly trusted. Merges NHS digital standards (accessible, clean, trusted blue/white aesthetics) with Hermetic Labs' premium, edge-native dark mode style (or a toggle between "Clinical Light" and "Hermetic Dark").
*   **Key Functionality:** 
    *   Frictionless Semantic Search across the Q&A dataset.
    *   **"Draft & Send" Workflow:** An interface to draft a question, use the local AI to refine it, and package it into an email to the procurement team.

## 4. Asset Collection Checklist (User Action Required)
Please drop the following assets into the `d:\Minimax\nhs_sbs_cq_portal\assets\` directory. I've structured the app to pull from there:

- [ ] **NHS SBS Logo** (Preferably a high-res SVG or PNG with a transparent background).
- [ ] **Hermetic Labs Logo** (For the "Powered by Hermetic Labs" discreet branding).
- [ ] **Brand Color Hex Codes** (If you want to deviate from the standard NHS Blue `#005EB8`).
- [ ] **Destination Email Address** (The exact NHS SBS procurement email address where the "Draft & Send" button should route the finalized questions).

---
*Note: This file and the associated directory structure form the foundation for the Clarification Question Portal Model. Once assets are gathered, we will begin the code execution phase to build the local LLM integration and the Electron/FastAPI frontend.*
