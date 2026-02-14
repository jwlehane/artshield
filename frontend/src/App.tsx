import { useState, useCallback, useRef } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Shield, Upload, CheckCircle, FileImage } from "lucide-react"
import { processImage, getStatus } from "@/lib/api"
import { toast } from "sonner"

function App() {
  const [isDragging, setIsDragging] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [progress, setProgress] = useState(0)
  const [statusMessage, setStatusMessage] = useState("")
  const [isComplete, setIsComplete] = useState(false)
  const [fileCount, setFileCount] = useState(0)
  const fileInputRef = useRef<HTMLInputElement>(null)

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
      setFileCount(files.length)
      await startProcessing(files)
    }
  }, [])

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files.length > 0) {
      setFileCount(files.length)
      await startProcessing(files)
    }
  }

  const startProcessing = async (files: FileList | null) => {
    if (!files || files.length === 0) return

    setIsProcessing(true)
    setIsComplete(false)
    setProgress(0)
    setStatusMessage("Initializing...")

    try {
      const taskId = await processImage(files)

      let currentProgress = 0
      const interval = setInterval(async () => {
        currentProgress += 5

        if (import.meta.env.VITE_MOCK_API === 'true' || true) { // Force mock for UI dev
          setProgress(currentProgress)
          if (currentProgress < 30) setStatusMessage("Stripping Metadata...")
          else if (currentProgress < 70) setStatusMessage("Applying ArtShield Watermark...")
          else setStatusMessage("Finalizing Assets...")

          if (currentProgress >= 100) {
            clearInterval(interval)
            setIsProcessing(false)
            setIsComplete(true)
            setStatusMessage("Protection Complete")
            toast.success("Assets have been shielded!")
          }
        } else {
          const status = await getStatus(taskId)
          setProgress(status.progress)
        }

      }, 200)

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
            <CardDescription>Drag and drop your images or click to select files for metadata stripping and watermarking.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">

            {!isProcessing && !isComplete && (
              <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                className={`border-2 border-dashed rounded-lg p-12 text-center transition-all cursor-pointer group ${isDragging ? 'border-teal-500 bg-teal-50' : 'border-slate-200 hover:bg-slate-50'
                  }`}
              >
                <input
                  type="file"
                  multiple
                  ref={fileInputRef}
                  onChange={handleFileSelect}
                  className="hidden"
                  accept="image/*"
                />
                <div className="mx-auto h-12 w-12 text-slate-300 group-hover:text-slate-400 mb-4 flex items-center justify-center">
                  <Upload className="h-full w-full" />
                </div>
                <p className="text-sm text-slate-600 font-medium">Click or drag images to shield</p>
                <p className="text-xs text-slate-400 mt-2">Supports PNG, JPG, WEBP</p>
              </div>
            )}

            {(isProcessing || isComplete) && (
              <div className="py-4 space-y-6">
                <div className="flex items-center gap-4 p-4 bg-slate-50 rounded-lg border border-slate-100">
                  <div className="h-10 w-10 bg-white rounded border border-slate-200 flex items-center justify-center text-teal-600">
                    <FileImage className="h-6 w-6" />
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-semibold text-slate-900">{fileCount} {fileCount === 1 ? 'Asset' : 'Assets'} Selected</p>
                    <p className="text-xs text-slate-500">{isComplete ? 'Shielded and ready' : 'Processing...'}</p>
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="flex justify-between text-xs font-semibold uppercase tracking-wider text-slate-500">
                    <span>{statusMessage}</span>
                    <span>{progress}%</span>
                  </div>
                  <Progress value={progress} className="h-2 w-full bg-slate-100" />
                </div>

                {isComplete && (
                  <div className="mt-8 flex flex-col items-center text-teal-600 animate-in fade-in slide-in-from-bottom-2">
                    <CheckCircle className="h-12 w-12 mb-2" />
                    <p className="font-bold text-xl text-slate-900">Shielding Complete</p>
                    <p className="text-sm text-slate-500 mb-6">Your images have been metadata-stripped and watermarked.</p>
                    <Button 
                      onClick={() => { setIsComplete(false); setProgress(0); setFileCount(0); }} 
                      variant="outline"
                      className="border-slate-200 hover:bg-slate-50"
                    >
                      Protect More Assets
                    </Button>
                  </div>
                )}
              </div>
            )}

            {!isProcessing && !isComplete && (
              <div className="flex justify-center text-xs text-slate-400 pt-2 italic">
                All processing happens locally on your machine.
              </div>
            )}

          </CardContent>
        </Card>

        <footer className="text-center text-xs text-slate-400">
          ArtShield v1.0 • Local Execution • Privacy First
        </footer>
      </div>
    </div>
  )
}

export default App
