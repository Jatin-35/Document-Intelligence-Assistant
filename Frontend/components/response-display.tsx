"use client"

import { FileText } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import type { QueryResponse } from "@/lib/types"

interface ResponseDisplayProps {
  response: QueryResponse
}

export function ResponseDisplay({ response }: ResponseDisplayProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Answer</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="prose max-w-none">
          <p className="text-gray-800 leading-relaxed">{response.answer}</p>
        </div>

        <Separator />

        <div>
          <h4 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <FileText className="h-4 w-4" />
            Context Chunks
          </h4>
          <div className="space-y-4">
            {response.sources.map((chunk, idx) => (
              <Card key={idx} className="border-l-4 border-l-blue-500">
                <CardContent className="pt-4">
                  <div className="flex items-start justify-between gap-4 mb-2">
                    <Badge className="text-lg" variant="secondary">
                      Chunk {idx + 1}
                    </Badge>
                    <Badge
                      className="text-lg"
                      variant={
                        chunk.confidence > 80 ? "default" : chunk.confidence > 60 ? "secondary" : "outline"
                      }
                    >
                     {chunk.confidence.toFixed(1)}% confidence
                     </Badge>
                  </div>

                  <p className="text-gray-700 leading-relaxed">{chunk.text}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
