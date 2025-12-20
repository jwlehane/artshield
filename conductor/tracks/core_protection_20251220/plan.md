# Implementation Plan: Implement Core Protection Engine

## Phase 1: Foundation & Metadata (The Tag) [checkpoint: 4578cc5]
Goal: Establish the metadata injection system and basic engine structure.

- [x] Task: Define unified Protection Parameters and Result models in `backend/processor.py` [24c2b50]
- [x] Task: Write tests for Metadata Injection (JPEG/PNG) [112338a]
- [x] Task: Implement `The Tag` (Metadata Injection) for `NoAI`, Copyright, and Ownership [8713b80]
- [x] Task: Conductor - User Manual Verification 'Phase 1: Foundation & Metadata' (Protocol in workflow.md) [4578cc5]

## Phase 2: Adversarial Protection (The Cloak & The Poison)
Goal: Integrate adversarial models for style protection and poisoning.

- [x] Task: Write tests for Adversarial Noise application [67122fe]
- [x] Task: Implement `The Cloak` (Glaze-style style protection) logic [c2aa785]
- [x] Task: Implement `The Poison` (Nightshade-style data poisoning) logic [c2aa785]
- [ ] Task: Integrate Cloak/Poison into the unified processing engine
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Adversarial Protection' (Protocol in workflow.md)

## Phase 3: Integration & Performance
Goal: Optimize the engine and provide the API interface.

- [ ] Task: Write tests for the unified processing endpoint
- [ ] Task: Create FastAPI endpoints for triggering protection tasks
- [ ] Task: Implement local hardware detection for optimization (CPU vs GPU)
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Integration & Performance' (Protocol in workflow.md)
