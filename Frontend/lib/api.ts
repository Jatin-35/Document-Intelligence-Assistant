import { UploadResponse, QueryResponse } from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000"

export class DocumentAssistantAPI {
  static async uploadFile(file: File): Promise<UploadResponse> {
    const formData = new FormData()
    formData.append("file", file)

    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: "POST",
      body: formData,
    })

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`)
    }

    return response.json()
  }

  static async askQuestion(question: string , sessionId : string): Promise<QueryResponse> {
    const formData = new FormData()
    formData.append("question", question)
    formData.append("session_id", sessionId)

    const response = await fetch(`${API_BASE_URL}/ask`, {
      method: "POST",
      body: formData,
    })

    if (!response.ok) {
      throw new Error(`Query failed: ${response.statusText}`)
    }

    return response.json()
  }


  static async resetMemory(sessionId: string): Promise<{ status: string }> {
  const formData = new FormData()
  formData.append("session_id", sessionId)

  const response = await fetch(`${API_BASE_URL}/reset_memory`, {
    method: "POST",
    body: formData,
  })

  if (!response.ok) {
    throw new Error(`Reset failed: ${response.statusText}`)
  }

    return response.json()
  }


  static async summarizeDocument(sessionId: string): Promise<{ summary: string }> {
  const formData = new FormData()
  formData.append("session_id", sessionId)

  const response = await fetch(`${API_BASE_URL}/summarize`, {
    method: "POST",
    body: formData,
  })

  if (!response.ok) {
    throw new Error(`Summarization failed: ${response.statusText}`)
  }

  return response.json()
  }


}

export type { UploadResponse, QueryResponse } from "./types"
