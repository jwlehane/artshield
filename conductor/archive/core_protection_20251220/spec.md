# Track Spec: Implement Core Protection Engine (The Cloak & The Tag)

## Overview
This track focuses on the foundational backend logic of ArtShield. It implements the two primary protection mechanisms: "The Cloak" (adversarial style protection) and "The Tag" (comprehensive metadata injection).

## Objectives
- Integrate adversarial protection techniques (Glaze/Nightshade concepts) into the backend.
- Create a robust metadata injection system for `NoAI` tags, copyright, and ownership info.
- Ensure all processing happens locally and securely.

## Requirements

### 1. The Cloak (Adversarial Protection)
- **Feature:** Apply adversarial noise to images to disrupt AI style mimicry (Glaze-style) and data poisoning (Nightshade-style).
- **Implementation:**
    - Use PyTorch to run protection models.
    - Support different intensity levels (Low, Medium, High).
    - Provide a way to process images locally on CPU or GPU.

### 2. The Tag (Metadata Injection)
- **Feature:** Inject persistent metadata into image files (JPEG, PNG).
- **Implementation:**
    - Include `NoAI` tags (XMP/Exif).
    - Include `Copyright` assertions.
    - Include `Ownership` information (Artist name, contact, website).
    - Ensure tags are as persistent as possible after common social media stripping.

### 3. Core Engine Integration
- **Feature:** A unified processing function that accepts an image and a set of protection parameters.
- **Output:** A protected image saved to a user-specified location.

## Success Criteria
- Backend tests confirm adversarial noise is applied.
- Metadata injection is verified via standard tools (exiftool, etc.).
- Processing completes within reasonable timeframes on standard consumer hardware.
