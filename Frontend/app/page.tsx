"use client"

import { Brain } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { DocumentUpload } from "@/components/document-upload"
import { QuestionForm } from "@/components/question-form"
import { ResponseDisplay } from "@/components/response-display"
import { useDocumentAssistant } from "@/hooks/use-document-assistant"
import { ResetMemoryButton } from "@/components/reset-memory-button"
import { SummarizeButton } from "@/components/summarize-button"

export default function DocumentAssistant() {
  const {
    file,
    question,
    response,
    isUploading,
    isAsking,
    uploadSuccess,
    error,
    setFile,
    setQuestion,
    clearError,
    uploadFile,
    askQuestion,
  } = useDocumentAssistant()

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <div className="flex items-center justify-center gap-2">
            <Brain className="h-8 w-8 text-blue-600" />
            <h1 className="text-3xl font-bold text-gray-900">Document Assistant</h1>
          </div>
          <p className="text-gray-600">Upload documents and ask intelligent questions about their content</p>
        </div>

        {/* Upload Section */}
        <DocumentUpload
          file={file}
          isUploading={isUploading}
          uploadSuccess={uploadSuccess}
          onFileChange={setFile}
          onUpload={uploadFile}
        />

        {/* Question Section */}
        <QuestionForm question={question} isAsking={isAsking} onQuestionChange={setQuestion} onAsk={askQuestion} />

        <div className="flex flex-wrap justify-center gap-4 mt-4">
             <SummarizeButton uploadSuccess={uploadSuccess} />
        </div>



        {/* Error Alert */}
        {error && (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Response Section */}
        {response && <ResponseDisplay response={response} />}

      </div>
    </div>
  )
}
