export interface ProcessingStatus {
    id: string;
    status: 'pending' | 'processing' | 'completed' | 'failed';
    progress: number;
    message: string;
}

const MOCK_DELAY_MS = 2000;
const TAILNET_IP = '100.104.161.54';

export async function processImage(files: FileList | null): Promise<string> {
    if (import.meta.env.VITE_MOCK_API === 'true') {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve("mock-task-id-" + Math.random().toString(36).substr(2, 9));
            }, 500);
        });
    }

    const formData = new FormData();
    if (files) {
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }
    }

    const res = await fetch(`http://${window.location.hostname}:8999/api/process`, {
        method: 'POST',
        body: formData
    });
    const data = await res.json();
    return data.id;
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

    const res = await fetch(`http://${window.location.hostname}:8999/api/status/${taskId}`);
    return res.json();
}
