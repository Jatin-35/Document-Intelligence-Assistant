"use client"

import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { DocumentAssistantAPI } from "@/lib/api"
import type { UploadResponse } from "@/lib/types"

export function SummarizeButton({ uploadSuccess }: { uploadSuccess: UploadResponse | null }) {
  const [summary, setSummary] = useState("")
  const [loading, setLoading] = useState(false)

  // 🔄 Reset summary when a new doc_id appears
  useEffect(() => {
    setSummary("")
  }, [uploadSuccess?.doc_id])

  const handleSummarize = async () => {
    if (!uploadSuccess?.doc_id) {
      setSummary(" Please upload a document first.")
      return
    }

    setLoading(true)
    try {
      const result = await DocumentAssistantAPI.summarizeDocument(uploadSuccess.doc_id)
      setSummary(result.summary)
    } catch (err) {
      setSummary("Failed to summarize.")
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="text-center space-y-2">
      <Button variant="outline" 
        className="bg-indigo-500 text-white hover:bg-indigo-600 transition duration-200"
        onClick={handleSummarize} disabled={loading}>
        📄 Summarize Document
      </Button>
      {summary && (
        <div className="mt-4 bg-white p-4 rounded-md shadow text-left">
          <h2 className="text-lg font-semibold mb-2">Summary:</h2>
          <p className="text-gray-800 whitespace-pre-line">{summary}</p>
        </div>
      )}
    </div>
  )
}
