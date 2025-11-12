import { useState } from 'react'

type Msg = { role: 'user' | 'ai'; text: string; clipUrl?: string | null }

export default function ChatPanel() {
  const [videoId, setVideoId] = useState<string | null>(null)
  const [msgs, setMsgs] = useState<Msg[]>([])
  const [input, setInput] = useState('')

  const ask = async () => {
    if (!videoId) {
      const id = (window as any).__lastVideoId as string | undefined
      if (id) setVideoId(id)
    }
    const message = input.trim()
    if (!message) return
    setMsgs(m => [...m, { role: 'user', text: message }])
    setInput('')
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ videoId: (videoId || (window as any).__lastVideoId || null), message })
    })
    const data = await res.json()
    setMsgs(m => [...m, { role: 'ai', text: data.answerText || '…', clipUrl: data.clipUrl }])
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto space-y-2 pr-1">
        {msgs.map((m, i) => (
          <div key={i} className={m.role === 'user' ? 'bg-gray-300 text-black rounded p-2 self-end max-w-[85%]' : 'bg-[#1E1E1E] text-gray-100 rounded p-2 self-start max-w-[85%]'}>
            <div className="text-sm whitespace-pre-wrap">{m.text}</div>
            {m.clipUrl && (
              <video controls className="mt-2 w-full rounded">
                <source src={m.clipUrl} type="video/mp4" />
              </video>
            )}
          </div>
        ))}
      </div>
      <div className="mt-2 flex gap-2">
        <input value={input} onChange={e => setInput(e.target.value)} placeholder="Ask a question…" className="flex-1 rounded bg-[#1E1E1E] text-gray-100 px-3 py-2 outline-none" />
        <button onClick={ask} className="px-3 py-2 rounded bg-gray-600 hover:bg-gray-500">Send</button>
      </div>
    </div>
  )
}



