'use client'

import { useState, useCallback, useRef } from 'react'
import { CloudArrowUpIcon, PhotoIcon, DocumentIcon, XMarkIcon } from '@heroicons/react/24/outline'
import { motion, AnimatePresence } from 'framer-motion'

interface UploadedFile {
  id: string
  file: File
  preview?: string
  type: 'image' | 'document'
  analysis?: {
    species?: string
    confidence?: number
    conservationStatus?: string
    habitat?: string
  }
}

interface ImageUploadProps {
  onFileAnalysis?: (analysis: any) => void
  maxFiles?: number
  acceptedTypes?: string[]
}

export default function ImageUploadInterface({ 
  onFileAnalysis, 
  maxFiles = 5,
  acceptedTypes = ['.jpg', '.jpeg', '.png', '.bmp', '.pdf', '.doc', '.docx']
}: ImageUploadProps) {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([])
  const [dragActive, setDragActive] = useState(false)
  const [analyzing, setAnalyzing] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  // Simulate AI analysis (replace with actual API call)
  const analyzeFile = async (file: File): Promise<any> => {
    setAnalyzing(true)
    
    // Mock species identification for images
    if (file.type.startsWith('image/')) {
      await new Promise(resolve => setTimeout(resolve, 2000)) // Simulate processing
      
      const mockSpecies = [
        { species: 'Lemur catta', confidence: 0.95, conservationStatus: 'Endangered', habitat: 'Spiny Forest' },
        { species: 'Indri indri', confidence: 0.89, conservationStatus: 'Critically Endangered', habitat: 'Rainforest' },
        { species: 'Eulemur fulvus', confidence: 0.82, conservationStatus: 'Near Threatened', habitat: 'Deciduous Forest' },
        { species: 'Brookesia micra', confidence: 0.91, conservationStatus: 'Near Threatened', habitat: 'Dry Forest' }
      ]
      
      const result = mockSpecies[Math.floor(Math.random() * mockSpecies.length)]
      setAnalyzing(false)
      return result
    }
    
    setAnalyzing(false)
    return { documentType: 'Research Paper', relevance: 'High' }
  }

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }, [])

  const handleDrop = useCallback(async (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    const files = Array.from(e.dataTransfer.files)
    await processFiles(files)
  }, [])

  const handleFileSelect = useCallback(async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    await processFiles(files)
  }, [])

  const processFiles = async (files: File[]) => {
    if (uploadedFiles.length + files.length > maxFiles) {
      alert(`Maximum ${maxFiles} files allowed`)
      return
    }

    for (const file of files) {
      const fileType = file.type.startsWith('image/') ? 'image' : 'document'
      const preview = fileType === 'image' ? URL.createObjectURL(file) : undefined
      
      const uploadedFile: UploadedFile = {
        id: Date.now().toString() + Math.random().toString(36),
        file,
        preview,
        type: fileType
      }

      setUploadedFiles(prev => [...prev, uploadedFile])

      // Analyze the file
      try {
        const analysis = await analyzeFile(file)
        setUploadedFiles(prev => 
          prev.map(f => 
            f.id === uploadedFile.id 
              ? { ...f, analysis } 
              : f
          )
        )
        onFileAnalysis?.(analysis)
      } catch (error) {
        console.error('Analysis failed:', error)
      }
    }
  }

  const removeFile = (id: string) => {
    setUploadedFiles(prev => {
      const file = prev.find(f => f.id === id)
      if (file?.preview) {
        URL.revokeObjectURL(file.preview)
      }
      return prev.filter(f => f.id !== id)
    })
  }

  const openFileDialog = () => {
    fileInputRef.current?.click()
  }

  return (
    <div className="w-full max-w-4xl mx-auto p-6">
      {/* Upload Area */}
      <motion.div
        className={`
          relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300
          ${dragActive 
            ? 'border-emerald-500 bg-emerald-50' 
            : 'border-gray-300 hover:border-emerald-400 hover:bg-emerald-25'
          }
        `}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept={acceptedTypes.join(',')}
          onChange={handleFileSelect}
          className="hidden"
        />
        
        <div className="space-y-4">
          <div className="mx-auto w-16 h-16 bg-gradient-to-br from-emerald-100 to-blue-100 rounded-full flex items-center justify-center">
            <CloudArrowUpIcon className="w-8 h-8 text-emerald-600" />
          </div>
          
          <div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Upload Images or Documents
            </h3>
            <p className="text-gray-600 mb-4">
              Drag and drop files here, or click to select files
            </p>
            <p className="text-sm text-gray-500">
              Supports: Images (JPG, PNG), Documents (PDF, DOC) - Max {maxFiles} files
            </p>
          </div>
          
          <button
            onClick={openFileDialog}
            className="bg-gradient-to-r from-emerald-600 to-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:shadow-lg transition-all"
          >
            Select Files
          </button>
        </div>
      </motion.div>

      {/* Processing Indicator */}
      <AnimatePresence>
        {analyzing && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="mt-6 bg-gradient-to-r from-emerald-100 to-blue-100 rounded-lg p-4"
          >
            <div className="flex items-center space-x-3">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-emerald-600"></div>
              <div>
                <p className="font-medium text-emerald-800">Analyzing with Madagascar AI...</p>
                <p className="text-sm text-emerald-600">Species identification and habitat analysis in progress</p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Uploaded Files Display */}
      {uploadedFiles.length > 0 && (
        <div className="mt-6">
          <h4 className="text-lg font-semibold text-gray-900 mb-4">
            Uploaded Files ({uploadedFiles.length}/{maxFiles})
          </h4>
          
          <div className="grid gap-4">
            <AnimatePresence>
              {uploadedFiles.map((uploadedFile) => (
                <motion.div
                  key={uploadedFile.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="bg-white rounded-lg border border-gray-200 p-4 shadow-sm"
                >
                  <div className="flex items-start space-x-4">
                    {/* File Preview */}
                    <div className="flex-shrink-0">
                      {uploadedFile.type === 'image' && uploadedFile.preview ? (
                        <img
                          src={uploadedFile.preview}
                          alt="Preview"
                          className="w-16 h-16 object-cover rounded-lg"
                        />
                      ) : (
                        <div className="w-16 h-16 bg-gray-100 rounded-lg flex items-center justify-center">
                          <DocumentIcon className="w-8 h-8 text-gray-500" />
                        </div>
                      )}
                    </div>
                    
                    {/* File Info */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <h5 className="text-sm font-medium text-gray-900 truncate">
                          {uploadedFile.file.name}
                        </h5>
                        <button
                          onClick={() => removeFile(uploadedFile.id)}
                          className="text-gray-400 hover:text-red-500 transition-colors"
                        >
                          <XMarkIcon className="w-5 h-5" />
                        </button>
                      </div>
                      
                      <p className="text-sm text-gray-500 mb-2">
                        {(uploadedFile.file.size / 1024 / 1024).toFixed(2)} MB • {uploadedFile.file.type}
                      </p>
                      
                      {/* Analysis Results */}
                      {uploadedFile.analysis && (
                        <div className="bg-gradient-to-r from-emerald-50 to-blue-50 rounded-lg p-3 mt-2">
                          {uploadedFile.type === 'image' && (
                            <div className="space-y-1">
                              <div className="flex items-center justify-between">
                                <span className="text-sm font-medium text-emerald-800">
                                  🦎 {uploadedFile.analysis.species}
                                </span>
                                <span className="text-sm text-emerald-600">
                                  {(uploadedFile.analysis.confidence! * 100).toFixed(1)}% confidence
                                </span>
                              </div>
                              <div className="flex items-center space-x-4 text-xs text-gray-600">
                                <span>📍 {uploadedFile.analysis.habitat}</span>
                                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                  uploadedFile.analysis.conservationStatus === 'Critically Endangered' 
                                    ? 'bg-red-100 text-red-800'
                                    : uploadedFile.analysis.conservationStatus === 'Endangered'
                                    ? 'bg-orange-100 text-orange-800' 
                                    : 'bg-yellow-100 text-yellow-800'
                                }`}>
                                  {uploadedFile.analysis.conservationStatus}
                                </span>
                              </div>
                            </div>
                          )}
                          
                          {uploadedFile.type === 'document' && (
                            <div className="text-sm text-blue-800">
                              📄 Document processed successfully
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        </div>
      )}
      
      {/* Action Buttons */}
      {uploadedFiles.length > 0 && (
        <div className="mt-6 flex space-x-4">
          <button className="bg-gradient-to-r from-emerald-600 to-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:shadow-lg transition-all">
            Generate Conservation Report
          </button>
          <button className="border-2 border-emerald-600 text-emerald-600 px-6 py-3 rounded-lg font-medium hover:bg-emerald-50 transition-all">
            Save to Research Database
          </button>
          <button className="border-2 border-blue-600 text-blue-600 px-6 py-3 rounded-lg font-medium hover:bg-blue-50 transition-all">
            Share with Team
          </button>
        </div>
      )}
    </div>
  )
}
