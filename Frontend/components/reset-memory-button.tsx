
"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { DocumentAssistantAPI } from "@/lib/api"

export function ResetMemoryButton({ sessionId = "default" }: { sessionId?: string }) {
  const [resetMessage, setResetMessage] = useState("")

  const handleReset = async () => {
    try {
      const result = await DocumentAssistantAPI.resetMemory(sessionId)
      setResetMessage(result.status)
      console.log("Memory reset:", result.status)
    } catch (err) {
      setResetMessage("Failed to reset memory.")
      console.error(err)
    }
  }

  return (
    <div className="text-center space-y-2">
      <Button  variant="secondary"
            className="bg-indigo-500 text-white hover:bg-indigo-600 transition duration-200"
             onClick={handleReset}>
        🔄 Reset Chat Memory
      </Button>
      {resetMessage && (
        <p className="text-sm text-green-700">{resetMessage}</p>
      )}
    </div>
  )
}
