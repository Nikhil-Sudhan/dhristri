import { useState } from 'react'

export default function UploadPanel() {
  const [file, setFile] = useState<File | null>(null)
  const [videoId, setVideoId] = useState<string | null>(null)
  const [uploading, setUploading] = useState(false)

  const onUpload = async () => {
    if (!file) return
    setUploading(true)
    const form = new FormData()
    form.append('file', file)
    const res = await fetch('/api/upload', { method: 'POST', body: form })
    const data = await res.json()
    setVideoId(data.videoId)
    ;(window as any).__lastVideoId = data.videoId
    setUploading(false)
  }

  return (
    <div className="space-y-3">
      <input type="file" accept="video/*" onChange={e => setFile(e.target.files?.[0] || null)} className="block w-full text-sm" />
      <button onClick={onUpload} disabled={!file || uploading} className="px-3 py-2 rounded bg-gray-600 hover:bg-gray-500 disabled:opacity-50">
        {uploading ? 'Uploading…' : 'Upload'}
      </button>
      {videoId && <div className="text-sm text-gray-300">Video ID: {videoId}</div>}
    </div>
  )
}


