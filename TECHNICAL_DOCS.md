# Technical Documentation: Madhav Drafting Hub (Integrated System)

## Overview
This document outlines the technical specifications for the `Madhav_Drafting_Hub.html` application, which consolidates multiple legal document templates into a single interface.

## 1. Registered Rent Agreement (Hard Locked)
*   **Status**: Finalized.
*   **Key Features**: Clause distribution (1-10, 11-19, Annexure), Multi-party support (2 Lessors/Lessees), Annexure table, Witness details.
*   **Layout**: Strictly Pagination-controlled (3 Pages).

## 2. TM-48 Trademark Authorization (Hard Locked)
*   **Status**: **FINAL / HARD LOCKED** (Dec 2025).
*   **Source Truth**: Exact replication of "THE TRADE MARKS ACT.docx".
*   **Locked Specifications**:
    *   **Header**: "FORM TM-48", "THE TRADE MARKS ACT, 1999".
    *   **Attorney Code**: "48171" (Fixed).
    *   **Text Body**: Pre-defined legal authorization text (Section 145/Rule 21).
    *   **Variables**:
        *   Applicant Name
        *   Father's Name
        *   Designation (Dropdown: Proprietor, Partner, Director, Authorized Signatory)
        *   Company/Proprietorship Name
        *   Applicant Address
        *   Stamp Paper Number (Top-Center)
    *   **Spacing**: Zero-margin rendering for variables within text flow ("No space needed").
    *   **Signature Block**: Adjusted vertical spacing for stamp/sign relative to "For [Company]".
*   **File State**: Backup created as `Madhav_Drafting_Hub_Locked_TM48.html`.

## File Versioning
*   `Madhav_Drafting_Hub.html`: **Active Production File**.
*   `Madhav_Drafting_Hub_Locked_TM48.html`: Backup after TM-48 finalization.
*   `Madhav_Drafting_Hub_Locked_2025_12_29.html`: Hard Lock after Logo Embedding & GNIDA Registry Integ.
*   `RentAgreement_Final.html`: Legacy standalone file (Reference only).

