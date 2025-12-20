# Product Guidelines: ArtShield

## 1. User Experience (UX) Principles
-   **Empowerment & Agency:** Every interaction should reinforce the user's control. Language should be protective and affirmative (e.g., "Shield Activated" instead of "Processing Complete").
-   **"Apple-like" Minimalism:** The interface must remain uncluttered, friendly, and accessible. Complexity should be concealed behind elegant abstractions unless the user explicitly dives into details.
-   **Transparent Choice:** Always offer choice without overwhelming. Provide simple, honest defaults that prioritize protection, but maintain a clear path for customization and privacy enhancements.
-   **System Harmony:** The application must seamlessly respect the user's system preferences, including automatic switching between Light and Dark modes to feel like a native tool.

## 2. Visual Design & Aesthetic
-   **Clean & Focused:** Use ample whitespace and clear typography. The content (the artist's work) should be the hero; the UI is the frame.
-   **Trust Signals:** Use consistent, high-quality iconography to denote security and protection status.
-   **Responsive Feedback:** Provide immediate, clear feedback for all actions. For long-running tasks (like local model processing), use engaging "magic" animations rather than raw terminal logs, while still offering accurate time estimates.

## 3. Communication & Tone
-   **Voice:** The product voice is **Serious but Supportive**. We are the artist's digital bodyguard—professional, reliable, and staunchly on their side.
-   **Honest Defaults:** Default settings should always lean towards maximum privacy and protection.
-   **Consensual Data:** Be explicit and granular when asking for data. For example, when optimizing processing:
    -   *Option A:* Auto-detect system hardware (Ask permission to scan).
    -   *Option B:* Manual entry (User inputs specs).
    -   *Option C:* Skip & Select (User chooses "Low-end" or "High-end" profile based on self-assessment).
    -   *Improvement:* Ask separately for permission to share anonymous data to help the community/product.

## 4. Feature-Specific Guidelines
-   **Legal Shield:**
    -   This feature requires a dedicated, interactive experience.
    -   **Platform Awareness:** Ask users for their portfolio platform (Wix, Squarespace, WordPress, etc.) to provide tailored, copy-pasteable snippets and instructions.
    -   **Automation:** Where possible, offer to automate the insertion of legal language or generate platform-specific code.
-   **Hybrid Processing Engine:**
    -   **Local First:** Always attempt to assess local hardware first. If capable, recommend the local open-source model path.
    -   **Flexible Cloud:** Clearly present the "ArtShield Cloud" (Paid) and "Bring Your Own Key" (Gemini/Cloud APIs) options as alternatives for users with lower-end hardware, ensuring they understand the trade-offs (privacy vs. convenience).
