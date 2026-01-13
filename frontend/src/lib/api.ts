export interface ProcessingStatus {
    id: string;
    status: 'pending' | 'processing' | 'completed' | 'failed';
    progress: number;
    message: string;
}

const API_BASE_URL = 'http://localhost:8999';

export async function processImage(files: FileList | null): Promise<string> {
    if (import.meta.env.VITE_MOCK_API === 'true') {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve("mock-task-id-" + Math.random().toString(36).substr(2, 9));
            }, 500);
        });
    }

    if (!files || files.length === 0) {
        throw new Error("No files provided");
    }

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
    }

    const res = await fetch(`${API_BASE_URL}/api/process`, {
        method: 'POST',
        body: formData,
    });

    if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || `Failed to process image: ${res.statusText}`);
    }

    const data = await res.json();
    return data.id;
}

export async function getStatus(taskId: string): Promise<ProcessingStatus> {
    if (import.meta.env.VITE_MOCK_API === 'true') {
        // Simulate progress based on time or random
        return new Promise((resolve) => {
            setTimeout(() => {
                // Determine mock state - for a simple demo, we can just return random progress
                // In a real mock, we might store state in localStorage
                resolve({
                    id: taskId,
                    status: 'processing',
                    progress: 45, // Static for now, or could increment
                    message: "Applying Mist Cloak (Mock)..."
                });
            }, 300);
        });
    }

    const res = await fetch(`${API_BASE_URL}/api/status/${taskId}`);
    if (!res.ok) {
        throw new Error(`Failed to get status: ${res.statusText}`);
    }
    return res.json();
}
