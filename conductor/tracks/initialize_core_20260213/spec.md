# Specification: Initialize Core Infrastructure

## Goal
Set up the foundational infrastructure for ArtShield, including database tracking and the initial UI/UX framework, and implement a baseline protection flow.

## Scope
- **Backend:** SQLite database schema for tracking protected assets.
- **Frontend:** Integration of TanStack Query and shadcn/ui.
- **Protection Logic:** Basic metadata stripping and simple watermarking flow.
- **End-to-End:** A simple UI to upload an image, apply basic protection, and save the record to the database.