# Implementation Plan: Implement Core Protection Engine

## Phase 1: Foundation & Metadata (The Tag)
Goal: Establish the metadata injection system and basic engine structure.

- [x] Task: Define unified Protection Parameters and Result models in backend/processor.py [24c2b50]
- [ ] Task: Write tests for Metadata Injection (JPEG/PNG)
- [ ] Task: Implement `The Tag` (Metadata Injection) for `NoAI`, Copyright, and Ownership
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Foundation & Metadata' (Protocol in workflow.md)

## Phase 2: Adversarial Protection (The Cloak & The Poison)
Goal: Integrate adversarial models for style protection and poisoning.

- [ ] Task: Write tests for Adversarial Noise application
- [ ] Task: Implement `The Cloak` (Glaze-style style protection) logic
- [ ] Task: Implement `The Poison` (Nightshade-style data poisoning) logic
- [ ] Task: Integrate Cloak/Poison into the unified processing engine
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Adversarial Protection' (Protocol in workflow.md)

## Phase 3: Integration & Performance
Goal: Optimize the engine and provide the API interface.

- [ ] Task: Write tests for the unified processing endpoint
- [ ] Task: Create FastAPI endpoints for triggering protection tasks
- [ ] Task: Implement local hardware detection for optimization (CPU vs GPU)
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Integration & Performance' (Protocol in workflow.md)
