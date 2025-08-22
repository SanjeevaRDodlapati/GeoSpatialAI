'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  ExclamationTriangleIcon, 
  MapPinIcon, 
  CalendarIcon,
  UserIcon,
  DocumentTextIcon,
  CameraIcon
} from '@heroicons/react/24/outline'

interface ConservationFormData {
  reportType: 'threat' | 'sighting' | 'research' | 'maintenance'
  location: {
    lat: number
    lng: number
    description: string
  }
  species?: string
  threatType?: string
  urgency: 'low' | 'medium' | 'high' | 'critical'
  description: string
  reporterName: string
  reporterRole: string
  photos?: File[]
  followUpRequired: boolean
  estimatedImpact: string
}

interface ConservationFormProps {
  onSubmit?: (data: ConservationFormData) => void
  initialData?: Partial<ConservationFormData>
}

export default function ConservationForm({ onSubmit, initialData }: ConservationFormProps) {
  const [formData, setFormData] = useState<ConservationFormData>({
    reportType: 'sighting',
    location: { lat: -18.7669, lng: 46.8691, description: '' }, // Madagascar center
    urgency: 'medium',
    description: '',
    reporterName: '',
    reporterRole: 'researcher',
    followUpRequired: false,
    estimatedImpact: 'medium',
    ...initialData
  })

  const [errors, setErrors] = useState<Record<string, string>>({})
  const [submitting, setSubmitting] = useState(false)
  const [currentStep, setCurrentStep] = useState(0)

  const steps = [
    { title: 'Report Type', icon: DocumentTextIcon },
    { title: 'Location', icon: MapPinIcon },
    { title: 'Details', icon: ExclamationTriangleIcon },
    { title: 'Reporter Info', icon: UserIcon }
  ]

  const urgencyColors = {
    low: 'bg-green-100 text-green-800 border-green-200',
    medium: 'bg-yellow-100 text-yellow-800 border-yellow-200', 
    high: 'bg-orange-100 text-orange-800 border-orange-200',
    critical: 'bg-red-100 text-red-800 border-red-200'
  }

  const handleInputChange = (field: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
    
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }))
    }
  }

  const handleLocationChange = (field: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      location: { ...prev.location, [field]: value }
    }))
  }

  const validateStep = (step: number): boolean => {
    const newErrors: Record<string, string> = {}
    
    switch (step) {
      case 0: // Report Type
        if (!formData.reportType) newErrors.reportType = 'Please select a report type'
        break
      case 1: // Location
        if (!formData.location.description) newErrors.locationDescription = 'Please describe the location'
        break
      case 2: // Details
        if (!formData.description) newErrors.description = 'Please provide a description'
        if (formData.reportType === 'threat' && !formData.threatType) {
          newErrors.threatType = 'Please specify the threat type'
        }
        break
      case 3: // Reporter Info
        if (!formData.reporterName) newErrors.reporterName = 'Reporter name is required'
        break
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleNext = () => {
    if (validateStep(currentStep)) {
      setCurrentStep(prev => Math.min(prev + 1, steps.length - 1))
    }
  }

  const handlePrevious = () => {
    setCurrentStep(prev => Math.max(prev - 1, 0))
  }

  const handleSubmit = async () => {
    if (!validateStep(currentStep)) return
    
    setSubmitting(true)
    
    // Simulate API submission
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    console.log('Submitting conservation report:', formData)
    onSubmit?.(formData)
    
    setSubmitting(false)
    
    // Reset form or show success message
    alert('Conservation report submitted successfully!')
  }

  const getCurrentLocation = () => {
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          handleLocationChange('lat', position.coords.latitude)
          handleLocationChange('lng', position.coords.longitude)
        },
        (error) => {
          console.error('Error getting location:', error)
          alert('Could not get current location. Please enter manually.')
        }
      )
    }
  }

  return (
    <div className="max-w-2xl mx-auto bg-white rounded-xl shadow-lg p-6">
      {/* Progress Indicator */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          {steps.map((step, index) => (
            <div key={index} className="flex flex-col items-center flex-1">
              <div className={`
                w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium
                ${index <= currentStep 
                  ? 'bg-emerald-600 text-white' 
                  : 'bg-gray-200 text-gray-500'
                }
              `}>
                {index < currentStep ? '✓' : index + 1}
              </div>
              <span className={`mt-2 text-xs font-medium ${
                index <= currentStep ? 'text-emerald-600' : 'text-gray-500'
              }`}>
                {step.title}
              </span>
              {index < steps.length - 1 && (
                <div className={`
                  absolute top-5 h-0.5 w-full transform translate-x-1/2
                  ${index < currentStep ? 'bg-emerald-600' : 'bg-gray-200'}
                `} style={{ left: `${(index + 0.5) * (100 / steps.length)}%`, width: `${100 / steps.length}%` }} />
              )}
            </div>
          ))}
        </div>
      </div>

      <motion.div
        key={currentStep}
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -20 }}
        transition={{ duration: 0.3 }}
      >
        {/* Step 0: Report Type */}
        {currentStep === 0 && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">What are you reporting?</h2>
            
            <div className="grid grid-cols-2 gap-4">
              {[
                { value: 'sighting', label: 'Species Sighting', emoji: '🦎', description: 'Wildlife observation or encounter' },
                { value: 'threat', label: 'Conservation Threat', emoji: '⚠️', description: 'Poaching, deforestation, or danger' },
                { value: 'research', label: 'Research Data', emoji: '🔬', description: 'Scientific observations or measurements' },
                { value: 'maintenance', label: 'Infrastructure Issue', emoji: '🔧', description: 'Equipment or facility problems' }
              ].map((option) => (
                <button
                  key={option.value}
                  onClick={() => handleInputChange('reportType', option.value)}
                  className={`
                    p-4 rounded-lg border-2 text-left transition-all hover:shadow-md
                    ${formData.reportType === option.value 
                      ? 'border-emerald-500 bg-emerald-50' 
                      : 'border-gray-200 hover:border-emerald-300'
                    }
                  `}
                >
                  <div className="text-2xl mb-2">{option.emoji}</div>
                  <div className="font-semibold text-gray-900">{option.label}</div>
                  <div className="text-sm text-gray-600">{option.description}</div>
                </button>
              ))}
            </div>
            
            {errors.reportType && (
              <p className="text-red-600 text-sm">{errors.reportType}</p>
            )}
          </div>
        )}

        {/* Step 1: Location */}
        {currentStep === 1 && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Where did this occur?</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Location Description *
                </label>
                <input
                  type="text"
                  value={formData.location.description}
                  onChange={(e) => handleLocationChange('description', e.target.value)}
                  placeholder="e.g., Andasibe-Mantadia National Park, near waterfall trail"
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 ${
                    errors.locationDescription ? 'border-red-500' : 'border-gray-300'
                  }`}
                />
                {errors.locationDescription && (
                  <p className="text-red-600 text-sm mt-1">{errors.locationDescription}</p>
                )}
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Latitude</label>
                  <input
                    type="number"
                    step="0.000001"
                    value={formData.location.lat}
                    onChange={(e) => handleLocationChange('lat', parseFloat(e.target.value))}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Longitude</label>
                  <input
                    type="number"
                    step="0.000001"
                    value={formData.location.lng}
                    onChange={(e) => handleLocationChange('lng', parseFloat(e.target.value))}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                  />
                </div>
              </div>
              
              <button
                onClick={getCurrentLocation}
                className="flex items-center space-x-2 text-emerald-600 hover:text-emerald-700 font-medium"
              >
                <MapPinIcon className="w-5 h-5" />
                <span>Use Current Location</span>
              </button>
            </div>
          </div>
        )}

        {/* Step 2: Details */}
        {currentStep === 2 && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Provide Details</h2>
            
            {formData.reportType === 'sighting' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Species (if known)</label>
                <select
                  value={formData.species || ''}
                  onChange={(e) => handleInputChange('species', e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                >
                  <option value="">Select species or leave blank</option>
                  <option value="lemur_catta">Ring-tailed Lemur (Lemur catta)</option>
                  <option value="indri_indri">Indri (Indri indri)</option>
                  <option value="eulemur_fulvus">Brown Lemur (Eulemur fulvus)</option>
                  <option value="propithecus_diadema">Diademed Sifaka (Propithecus diadema)</option>
                  <option value="microcebus_murinus">Gray Mouse Lemur (Microcebus murinus)</option>
                  <option value="brookesia_micra">Brookesia micra</option>
                  <option value="furcifer_pardalis">Panther Chameleon (Furcifer pardalis)</option>
                  <option value="other">Other (describe in details)</option>
                </select>
              </div>
            )}
            
            {formData.reportType === 'threat' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Threat Type *</label>
                <select
                  value={formData.threatType || ''}
                  onChange={(e) => handleInputChange('threatType', e.target.value)}
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 ${
                    errors.threatType ? 'border-red-500' : 'border-gray-300'
                  }`}
                >
                  <option value="">Select threat type</option>
                  <option value="poaching">Poaching/Illegal Hunting</option>
                  <option value="deforestation">Deforestation/Logging</option>
                  <option value="encroachment">Human Encroachment</option>
                  <option value="fire">Forest Fire</option>
                  <option value="pollution">Pollution</option>
                  <option value="infrastructure">Infrastructure Damage</option>
                  <option value="other">Other</option>
                </select>
                {errors.threatType && (
                  <p className="text-red-600 text-sm mt-1">{errors.threatType}</p>
                )}
              </div>
            )}
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Urgency Level</label>
              <div className="grid grid-cols-4 gap-2">
                {(['low', 'medium', 'high', 'critical'] as const).map((level) => (
                  <button
                    key={level}
                    onClick={() => handleInputChange('urgency', level)}
                    className={`
                      p-3 rounded-lg border text-sm font-medium transition-all
                      ${formData.urgency === level 
                        ? urgencyColors[level]
                        : 'border-gray-300 text-gray-700 hover:border-gray-400'
                      }
                    `}
                  >
                    {level.charAt(0).toUpperCase() + level.slice(1)}
                  </button>
                ))}
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description *
              </label>
              <textarea
                value={formData.description}
                onChange={(e) => handleInputChange('description', e.target.value)}
                rows={4}
                placeholder="Provide detailed information about your observation or report..."
                className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 ${
                  errors.description ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {errors.description && (
                <p className="text-red-600 text-sm mt-1">{errors.description}</p>
              )}
            </div>
            
            <div className="flex items-center space-x-3">
              <input
                type="checkbox"
                id="followUp"
                checked={formData.followUpRequired}
                onChange={(e) => handleInputChange('followUpRequired', e.target.checked)}
                className="w-4 h-4 text-emerald-600 border-gray-300 rounded focus:ring-emerald-500"
              />
              <label htmlFor="followUp" className="text-sm text-gray-700">
                This requires immediate follow-up action
              </label>
            </div>
          </div>
        )}

        {/* Step 3: Reporter Info */}
        {currentStep === 3 && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Reporter Information</h2>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Your Name *
              </label>
              <input
                type="text"
                value={formData.reporterName}
                onChange={(e) => handleInputChange('reporterName', e.target.value)}
                placeholder="Full name"
                className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 ${
                  errors.reporterName ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {errors.reporterName && (
                <p className="text-red-600 text-sm mt-1">{errors.reporterName}</p>
              )}
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Role</label>
              <select
                value={formData.reporterRole}
                onChange={(e) => handleInputChange('reporterRole', e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
              >
                <option value="researcher">Researcher</option>
                <option value="ranger">Park Ranger</option>
                <option value="guide">Tour Guide</option>
                <option value="local_community">Local Community Member</option>
                <option value="tourist">Tourist/Visitor</option>
                <option value="conservation_manager">Conservation Manager</option>
                <option value="other">Other</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Estimated Impact
              </label>
              <select
                value={formData.estimatedImpact}
                onChange={(e) => handleInputChange('estimatedImpact', e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
              >
                <option value="low">Low - Minimal conservation impact</option>
                <option value="medium">Medium - Moderate conservation significance</option>
                <option value="high">High - Significant conservation importance</option>
                <option value="critical">Critical - Immediate conservation attention needed</option>
              </select>
            </div>
          </div>
        )}
      </motion.div>

      {/* Navigation Buttons */}
      <div className="flex justify-between mt-8">
        <button
          onClick={handlePrevious}
          disabled={currentStep === 0}
          className={`
            px-6 py-3 rounded-lg font-medium transition-all
            ${currentStep === 0 
              ? 'bg-gray-100 text-gray-400 cursor-not-allowed' 
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }
          `}
        >
          Previous
        </button>
        
        {currentStep < steps.length - 1 ? (
          <button
            onClick={handleNext}
            className="bg-gradient-to-r from-emerald-600 to-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:shadow-lg transition-all"
          >
            Next Step
          </button>
        ) : (
          <button
            onClick={handleSubmit}
            disabled={submitting}
            className={`
              px-6 py-3 rounded-lg font-medium transition-all
              ${submitting 
                ? 'bg-gray-400 text-white cursor-not-allowed' 
                : 'bg-gradient-to-r from-emerald-600 to-blue-600 text-white hover:shadow-lg'
              }
            `}
          >
            {submitting ? (
              <div className="flex items-center space-x-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span>Submitting...</span>
              </div>
            ) : (
              'Submit Report'
            )}
          </button>
        )}
      </div>
    </div>
  )
}
