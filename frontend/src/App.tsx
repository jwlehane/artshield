import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Shield } from "lucide-react"

function App() {
  return (
    <div className="min-h-screen bg-neutral-50 flex flex-col items-center justify-center p-8 font-sans text-slate-800">
      <div className="max-w-2xl w-full space-y-8">
        <header className="text-center space-y-2">
          <h1 className="text-4xl font-bold tracking-tight text-slate-900">ArtShield</h1>
          <p className="text-slate-500">Democratizing defense for the independent artist.</p>
        </header>

        <Card className="w-full bg-white shadow-sm border-slate-200">
          <CardHeader>
            <CardTitle>Protect Your Work</CardTitle>
            <CardDescription>Drag and drop your images or folder here to apply Mist Cloak and Metadata protection.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="border-2 border-dashed border-slate-200 rounded-lg p-12 text-center hover:bg-slate-50 transition-colors cursor-pointer group">
              <div className="mx-auto h-12 w-12 text-slate-300 group-hover:text-slate-400 mb-4 flex items-center justify-center">
                <Shield className="h-full w-full" />
              </div>
              <p className="text-sm text-slate-600">Click or drag folder to upload</p>
            </div>

            <div className="flex justify-end pt-4">
              <Button className="bg-slate-900 hover:bg-slate-800 text-white">Shield Art</Button>
            </div>
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
