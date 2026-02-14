# ArtShield Tech Stack

## Frontend
- **Framework:** React (TypeScript) via Vite
- **Styling:** Tailwind CSS
- **UI Components:** Radix UI & shadcn/ui (for a professional "Studio" aesthetic)
- **State Management:** TanStack Query (for robust handling of image processing states)
- **Icons:** Lucide React

## Backend
- **Framework:** FastAPI (Python)
- **Database:** SQLite (for local asset tracking and success metrics)
- **Image Processing:**
    - **PyTorch:** For adversarial poisoning/shielding logic
    - **Pillow:** For image manipulation and down-sampling
    - **Piexif:** For metadata management and stripping

## Infrastructure & Tools
- **Deployment:** GitHub Actions (CI/CD)
- **Environment:** Local-first execution with optional cloud-processing bridge