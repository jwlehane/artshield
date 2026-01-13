import { useState, useCallback } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Shield, Upload, CheckCircle, AlertCircle } from "lucide-react"
import { processImage, getStatus } from "@/lib/api"
import { toast } from "sonner"

function App() {
  const [isDragging, setIsDragging] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [progress, setProgress] = useState(0)
  const [statusMessage, setStatusMessage] = useState("")
  const [isComplete, setIsComplete] = useState(false)

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback(async (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    const files = e.dataTransfer.files
    if (files.length > 0) {
      await startProcessing(files)
    }
  }, [])

  const startProcessing = async (files: FileList | null) => {
    if (!files || files.length === 0) return

    setIsProcessing(true)
    setIsComplete(false)
    setProgress(0)
    setStatusMessage("Initializing...")

    try {
      // Start the task
      const taskId = await processImage(files)

      // Poll for status (Mock simulation loop for demo)
      let currentProgress = 0
      const interval = setInterval(async () => {
        currentProgress += 10

        // In real app, we'd use getStatus(taskId) here
        // For the smooth demo effect without complex mock state management:
        if (import.meta.env.VITE_MOCK_API === 'true') {
          setProgress(currentProgress)
          if (currentProgress < 50) setStatusMessage("Applying Mist Cloak...")
          else if (currentProgress < 80) setStatusMessage("Injecting Metadata...")
          else setStatusMessage("Finalizing Watermark...")

          if (currentProgress >= 100) {
            clearInterval(interval)
            setIsProcessing(false)
            setIsComplete(true)
            setStatusMessage("Protection Complete")
            toast.success("Your folder has been shielded!")
          }
        } else {
          try {
            const status = await getStatus(taskId)
            setProgress(status.progress)
            setStatusMessage(status.message)

            if (status.status === 'completed') {
              clearInterval(interval)
              setIsProcessing(false)
              setIsComplete(true)
              setStatusMessage("Protection Complete")
              toast.success("Your folder has been shielded!")
            } else if (status.status === 'failed') {
              clearInterval(interval)
              setIsProcessing(false)
              setStatusMessage(status.message)
              toast.error(`Processing failed: ${status.message}`)
            }
          } catch (e) {
             console.error("Error polling status:", e)
          }
        }

      }, 800)

    } catch (error) {
      console.error(error)
      toast.error("Failed to start processing")
      setIsProcessing(false)
    }
  }

  return (
    <div className="min-h-screen bg-neutral-50 flex flex-col items-center justify-center p-8 font-sans text-slate-800">
      <div className="max-w-2xl w-full space-y-8">
        <header className="text-center space-y-2">
          <h1 className="text-4xl font-bold tracking-tight text-slate-900 flex items-center justify-center gap-3">
            <Shield className="h-10 w-10 text-teal-600" />
            ArtShield
          </h1>
          <p className="text-slate-500">Democratizing defense for the independent artist.</p>
        </header>

        <Card className="w-full bg-white shadow-sm border-slate-200">
          <CardHeader>
            <CardTitle>Protect Your Work</CardTitle>
            <CardDescription>Drag and drop your images or folder here to apply Mist Cloak and Metadata protection.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">

            {!isProcessing && !isComplete && (
              <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={`border-2 border-dashed rounded-lg p-12 text-center transition-all cursor-pointer group ${isDragging ? 'border-teal-500 bg-teal-50' : 'border-slate-200 hover:bg-slate-50'
                  }`}
              >
                <div className="mx-auto h-12 w-12 text-slate-300 group-hover:text-slate-400 mb-4 flex items-center justify-center">
                  <Upload className="h-full w-full" />
                </div>
                <p className="text-sm text-slate-600 font-medium">Click or drag folder to upload</p>
                <p className="text-xs text-slate-400 mt-2">Supports PNG, JPG (Max 500MB)</p>
              </div>
            )}

            {(isProcessing || isComplete) && (
              <div className="py-8 space-y-4">
                <div className="flex justify-between text-sm font-medium text-slate-700">
                  <span>{statusMessage}</span>
                  <span>{progress}%</span>
                </div>
                <Progress value={progress} className="h-2 w-full" />

                {isComplete && (
                  <div className="mt-6 flex flex-col items-center text-teal-600 animate-in fade-in slide-in-from-bottom-2">
                    <CheckCircle className="h-12 w-12 mb-2" />
                    <p className="font-semibold text-lg">Shielding Complete</p>
                    <p className="text-sm text-slate-500 mb-4">Files saved to output folder.</p>
                    <Button onClick={() => { setIsComplete(false); setProgress(0); }} variant="outline">Protect More</Button>
                  </div>
                )}
              </div>
            )}

            {!isProcessing && !isComplete && (
              <div className="flex justify-end pt-2">
                <Button onClick={() => startProcessing(null)} className="bg-slate-900 hover:bg-slate-800 text-white">
                  Run Demo (Mock)
                </Button>
              </div>
            )}

          </CardContent>
        </Card>

        <footer className="text-center text-xs text-slate-400">
          ArtShield v1.0 • Local Execution • Privacy First
          {import.meta.env.VITE_MOCK_API === 'true' && <span className="ml-2 text-amber-500 font-semibold">• DEMO MODE</span>}
        </footer>
      </div>
    </div>
  )
}

export default App
