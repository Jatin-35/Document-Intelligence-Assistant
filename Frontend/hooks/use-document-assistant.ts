"use client"

import { useState } from "react"
import { DocumentAssistantAPI } from "@/lib/api"
import type { DocumentAssistantState } from "@/lib/types"

export function useDocumentAssistant() {
  const [state, setState] = useState<DocumentAssistantState>({
    file: null,
    question: "",
    response: null,
    isUploading: false,
    isAsking: false,
    uploadSuccess: null,
    doc_id: null, // ✅ Add this here
    error: null,
  })

  const setFile = (file: File | null) => {
    setState((prev) => ({
      ...prev,
      file,
      uploadSuccess: null,
      doc_id: null, // ✅ Reset old doc_id when new file is picked
      response: null,
      summary: null,
      error: null,
    }))
  }

  const setQuestion = (question: string) => {
    setState((prev) => ({ ...prev, question }))
  }

  const clearError = () => {
    setState((prev) => ({ ...prev, error: null }))
  }

  const uploadFile = async () => {
    if (!state.file) {
      setState((prev) => ({
        ...prev,
        error: "Please select a file to upload",
      }))
      return
    }

    setState((prev) => ({
      ...prev,
      isUploading: true,
      error: null,
    }))

    try {
      const uploadSuccess = await DocumentAssistantAPI.uploadFile(state.file)
      setState((prev) => ({
        ...prev,
        uploadSuccess,
        doc_id: uploadSuccess.doc_id, // ✅ Set new doc_id
        question: "",
        response: null,
        isUploading: false,
      }))
    } catch (error) {
      setState((prev) => ({
        ...prev,
        error: "Failed to upload file. Please try again.",
        isUploading: false,
      }))
    }
  }

  const askQuestion = async () => {
    if (!state.question.trim()) {
      setState((prev) => ({
        ...prev,
        error: "Please enter a question",
      }))
      return
    }

    const sessionId = state.doc_id // ✅ Now directly from state
    if (!sessionId) {
      setState((prev) => ({
        ...prev,
        error: "No document found. Please upload a file first.",
      }))
      return
    }

    setState((prev) => ({
      ...prev,
      isAsking: true,
      error: null,
    }))

    try {
      const response = await DocumentAssistantAPI.askQuestion(state.question, sessionId)
      setState((prev) => ({
        ...prev,
        response,
        isAsking: false,
      }))
    } catch (error) {
      setState((prev) => ({
        ...prev,
        error: "Failed to get answer. Please try again.",
        isAsking: false,
      }))
    }
  }

  const summarizeDocument = async () => {
    const sessionId = state.doc_id // ✅ Always use this
    if (!sessionId) {
      setState((prev) => ({
        ...prev,
        error: "No document found. Please upload a file first.",
      }))
      return
    }

    setState((prev) => ({
      ...prev,
      isAsking: true,
      error: null,
    }))

    try {
      const response = await DocumentAssistantAPI.summarizeDocument(sessionId)
      setState((prev) => ({
        ...prev,
        response: {
          answer: response.summary,
          sources: [],
        },
        summary: response.summary, 
        isAsking: false,
      }))
    } catch (error) {
      setState((prev) => ({
        ...prev,
        error: "Failed to summarize the document. Please try again.",
        isAsking: false,
      }))
    }
  }

  return {
    ...state,
    setFile,
    setQuestion,
    clearError,
    uploadFile,
    askQuestion,
    summarizeDocument,
    summary: state.summary,
  }
}
