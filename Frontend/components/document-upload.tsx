"use client"

import type React from "react"
import { Upload, FileText, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import type { DocumentUploadProps } from "@/lib/types"



export function DocumentUpload({ file, isUploading, uploadSuccess, onFileChange, onUpload }: DocumentUploadProps) {
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    onFileChange(selectedFile || null)
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Upload className="h-5 w-5" />
          Upload Document
        </CardTitle>
        <CardDescription>Upload a document to analyze and ask questions about its content</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center gap-4">
          <Input type="file" onChange={handleFileChange} className="flex-1" accept=".pdf,.txt,.doc,.docx" />
          <Button onClick={onUpload} disabled={!file || isUploading} className="min-w-[100px]">
            {isUploading ? (
              <>
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                Uploading
              </>
            ) : (
              <>
                <Upload className="h-4 w-4 mr-2" />
                Upload
              </>
            )}
          </Button>
        </div>

        {uploadSuccess && (
          <Alert className="border-green-200 bg-green-50">
            <FileText className="h-4 w-4 text-green-600" />
            <AlertDescription className="text-green-800">
              <strong>Upload successful!</strong>
              Status : {uploadSuccess.status}
              <br />
              File: {uploadSuccess.file}
              <br />
              File Type : {uploadSuccess.filetype} 
              <br />
              Document ID : {uploadSuccess.doc_id} 
              <br />
              Chunks created: {uploadSuccess.chunks}
            </AlertDescription>
          </Alert>
        )}
      </CardContent>
    </Card>
  )
}
