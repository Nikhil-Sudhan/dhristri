import UploadPanel from './components/UploadPanel'
import StatusPreview from './components/StatusPreview'
import ChatPanel from './components/ChatPanel'

export default function App() {
  return (
    <div className="min-h-screen bg-[#121212] text-gray-100">
      <div className="max-w-7xl mx-auto p-4 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-4">
          <div className="bg-[#1E1E1E] rounded-lg p-4 shadow">
            <h2 className="text-lg font-semibold mb-2">Upload Video</h2>
            <UploadPanel />
          </div>
          <div className="bg-[#1E1E1E] rounded-lg p-4 shadow">
            <h2 className="text-lg font-semibold mb-2">Processing Status & Preview</h2>
            <StatusPreview />
          </div>
        </div>
        <div className="bg-[#2A2A2A] rounded-lg p-4 shadow min-h-[60vh]">
          <h2 className="text-lg font-semibold mb-2">Chat</h2>
          <ChatPanel />
        </div>
      </div>
    </div>
  )
}





