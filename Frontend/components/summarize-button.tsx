"use client"

import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { DocumentAssistantAPI } from "@/lib/api"
import type { UploadResponse } from "@/lib/types"

export function SummarizeButton({ uploadSuccess }: { uploadSuccess: UploadResponse | null }) {
  const [summaryLines, setSummaryLines] = useState<string[]>([])
  const [loading, setLoading] = useState(false)

  // Reset summary when a new document is uploaded
  useEffect(() => {
    setSummaryLines([])
  }, [uploadSuccess?.doc_id])

  const handleSummarize = async () => {
    if (!uploadSuccess?.doc_id) {
      setSummaryLines(["Please upload a document first."])
      return
    }

    setLoading(true)
    try {
      const result = await DocumentAssistantAPI.summarizeDocument(uploadSuccess.doc_id)
      const lines = result.summary.split("\n").filter(line => line.trim())
      setSummaryLines(lines)
    } catch (err) {
      setSummaryLines(["Failed to summarize."])
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const renderSummaryLine = (line: string, index: number) => {
    const match = line.match(/^\s*[-•]?\s*\*\*(.+?)\*\*[:：]?\s*(.*)/)
    if (match) {
      const [, title, rest] = match
      return (
        <li key={index}>
          <strong>{title}</strong>{rest ? `: ${rest}` : ""}
        </li>
      )
    }
    return <li key={index}>{line.replace(/\*/g, "")}</li>
  }

  return (
    <div className="text-center space-y-2">
      <Button
        variant="outline"
        className="bg-indigo-500 text-white hover:bg-indigo-600 transition duration-200"
        onClick={handleSummarize}
        disabled={loading}
      >
        📄 Summarize Document
      </Button>

      {summaryLines.length > 0 && (
        <div className="mt-4 bg-white p-4 rounded-md shadow text-left">
          <h2 className="text-lg font-semibold mb-2">Summary:</h2>
          <ul className="text-gray-800 list-disc pl-5 space-y-1">
            {summaryLines.map((line, index) => renderSummaryLine(line, index))}
          </ul>
        </div>
      )}
    </div>
  )
}
