"use client"

import type React from "react"
import { MessageCircle, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

interface QuestionFormProps {
  question: string
  isAsking: boolean
  onQuestionChange: (question: string) => void
  onAsk: () => void
}

export function QuestionForm({ question, isAsking, onQuestionChange, onAsk }: QuestionFormProps) {
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !isAsking) {
      onAsk()
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <MessageCircle className="h-5 w-5" />
          Ask a Question
        </CardTitle>
        <CardDescription>Ask any question about the uploaded document content</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center gap-4">
          <Input
            type="text"
            placeholder="What would you like to know about the document?"
            value={question}
            onChange={(e) => onQuestionChange(e.target.value)}
            onKeyPress={handleKeyPress}
            className="flex-1"
          />
          <Button onClick={onAsk} disabled={!question.trim() || isAsking} className="min-w-[100px]">
            {isAsking ? (
              <>
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                Asking
              </>
            ) : (
              <>
                <MessageCircle className="h-4 w-4 mr-2" />
                Ask
              </>
            )}
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
