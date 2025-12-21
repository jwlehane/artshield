export interface ProcessingStatus {
    id: string;
    status: 'pending' | 'processing' | 'completed' | 'failed';
    progress: number;
    message: string;
}


const API_BASE = "http://localhost:8999/api";

export async function processImage(files: FileList | null): Promise<string> {
    if (!files || files.length === 0) {
        throw new Error("No files selected");
    }

    if (import.meta.env.VITE_MOCK_API === 'true') {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve("mock-task-id-" + Math.random().toString(36).substr(2, 9));
            }, 500);
        });
    }

    const formData = new FormData();
    formData.append('file', files[0]);
    // TODO: Add support for intensity and protection type selection in UI
    formData.append('protection_type', 'cloak_and_tag');
    formData.append('intensity', 'medium');

    const res = await fetch(`${API_BASE}/process`, {
        method: 'POST',
        body: formData,
    });

    if (!res.ok) {
        const error = await res.json();
        throw new Error(error.detail || "Failed to start processing");
    }

    const data = await res.json();
    return data.task_id;
}

export async function getStatus(taskId: string): Promise<ProcessingStatus> {
    if (import.meta.env.VITE_MOCK_API === 'true') {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    id: taskId,
                    status: 'processing',
                    progress: 45,
                    message: "Applying Mist Cloak (Mock)..."
                });
            }, 300);
        });
    }

    const res = await fetch(`${API_BASE}/status/${taskId}`);
    if (!res.ok) {
        throw new Error("Failed to fetch task status");
    }
    return res.json();
}
