export interface ProcessingStatus {
    id: string;
    status: 'pending' | 'processing' | 'completed' | 'failed';
    progress: number;
    message: string;
}

const MOCK_DELAY_MS = 2000;

export async function processImage(files: FileList | null): Promise<string> {
    if (import.meta.env.VITE_MOCK_API === 'true') {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve("mock-task-id-" + Math.random().toString(36).substr(2, 9));
            }, 500);
        });
    }

    // Real API call would go here
    // const formData = new FormData();
    // ...
    // const res = await fetch('http://localhost:8999/api/process', ...);
    // return res.json().id;
    throw new Error("Real API not implemented yet");
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

    const res = await fetch(`http://localhost:8999/api/status/${taskId}`);
    return res.json();
}
