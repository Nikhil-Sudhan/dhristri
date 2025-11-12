import { useEffect, useState } from 'react'

type Slice = { startSec: number; endSec: number; summaryText: string }

export default function StatusPreview() {
  const [videoId, setVideoId] = useState<string | null>(null)
  const [status, setStatus] = useState<{ status: string; progress: number } | null>(null)
  const [slices, setSlices] = useState<Slice[]>([])

  useEffect(() => {
    // Placeholder: In a real app, videoId would be shared via context/state
    const id = (window as any).__lastVideoId as string | undefined
    if (id) setVideoId(id)
  }, [])

  useEffect(() => {
    if (!videoId) return
    const t = setInterval(async () => {
      const res = await fetch(`/api/status/${videoId}`)
      const data = await res.json()
      setStatus({ status: data.status, progress: data.progress })
      // Placeholder: slices would come from another endpoint or expanded status
    }, 2000)
    return () => clearInterval(t)
  }, [videoId])

  return (
    <div className="space-y-2">
      {!videoId && <div className="text-sm text-gray-400">Upload a video to begin.</div>}
      {videoId && (
        <div className="text-sm">Status: {status?.status || 'queued'} · {status?.progress ?? 0}%</div>
      )}
      <div className="space-y-1">
        {slices.map((s, i) => (
          <div key={i} className="text-sm text-gray-300">
            {s.startSec}-{s.endSec}s — {s.summaryText}
          </div>
        ))}
      </div>
    </div>
  )
}





