export interface Source {
  text: string
  confidence: number
}

export interface QueryResponse {
  session_id : string
  question : string
  answer: string
  sources: Source[]
}

export interface UploadResponse {
  status : string
  file: string
  filetype : string
  doc_id : string
  chunks: number
}

export interface DocumentUploadProps {
  file: File | null
  isUploading: boolean
  uploadSuccess: UploadResponse | null
  onFileChange: (file: File | null) => void
  onUpload: () => void
}

export interface DocumentAssistantState {
  file: File | null
  question: string
  response: QueryResponse | null
  doc_id: string | null
  isUploading: boolean
  isAsking: boolean
  uploadSuccess: UploadResponse | null
  error: string | null
  summary?: string | null
}
