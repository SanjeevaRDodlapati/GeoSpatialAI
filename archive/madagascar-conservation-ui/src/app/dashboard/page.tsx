'use client'

import { useState } from 'react'
import { Tab } from '@headlessui/react'
import { 
  ChartBarIcon, 
  GlobeAltIcon, 
  EyeIcon, 
  ShieldCheckIcon,
  MapIcon,
  BeakerIcon,
  CpuChipIcon,
  ArrowRightIcon,
  CloudArrowUpIcon,
  DocumentTextIcon,
  CameraIcon
} from '@heroicons/react/24/outline'
import ImageUploadInterface from '../components/ImageUploadInterface'
import ConservationForm from '../components/ConservationForm'

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(' ')
}

export default function InteractiveDashboard() {
  const [selectedTab, setSelectedTab] = useState(0)

  const tabs = [
    {
      name: '🏠 Dashboard',
      icon: GlobeAltIcon,
      component: DashboardTab
    },
    {
      name: '📷 Species ID',
      icon: CameraIcon, 
      component: SpeciesIdentificationTab
    },
    {
      name: '📝 Report',
      icon: DocumentTextIcon,
      component: ReportingTab
    },
    {
      name: '📊 Analytics',
      icon: ChartBarIcon,
      component: AnalyticsTab
    },
    {
      name: '🗺️ Live Map',
      icon: MapIcon,
      component: LiveMapTab
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#FFF3E0] via-white to-[#E8F5E8]">
      {/* Header */}
      <header className="bg-white/90 backdrop-blur border-b border-white/20 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-emerald-600 to-blue-600 rounded-lg flex items-center justify-center">
                <GlobeAltIcon className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gradient">Madagascar Conservation AI</h1>
                <p className="text-xs text-gray-600">Interactive Conservation Platform</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="hidden md:flex items-center space-x-2 text-sm">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-gray-600">System Online</span>
              </div>
              <button className="bg-gradient-to-r from-emerald-600 to-blue-600 text-white px-4 py-2 rounded-lg hover:shadow-lg transition-all">
                Emergency Alert
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Tab Navigation */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <Tab.Group selectedIndex={selectedTab} onChange={setSelectedTab}>
          <Tab.List className="flex space-x-1 rounded-xl bg-blue-900/20 p-1 mb-8">
            {tabs.map((tab, index) => (
              <Tab
                key={tab.name}
                className={({ selected }) =>
                  classNames(
                    'w-full rounded-lg py-3 px-4 text-sm font-medium leading-5 transition-all',
                    'ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2',
                    selected
                      ? 'bg-white text-emerald-700 shadow'
                      : 'text-emerald-600 hover:bg-white/[0.12] hover:text-emerald-800'
                  )
                }
              >
                <div className="flex items-center justify-center space-x-2">
                  <tab.icon className="w-5 h-5" />
                  <span className="hidden sm:block">{tab.name}</span>
                </div>
              </Tab>
            ))}
          </Tab.List>

          <Tab.Panels>
            {tabs.map((tab, index) => (
              <Tab.Panel key={index} className="focus:outline-none">
                <tab.component />
              </Tab.Panel>
            ))}
          </Tab.Panels>
        </Tab.Group>
      </div>
    </div>
  )
}

// Dashboard Tab Component
function DashboardTab() {
  const stats = [
    { label: "Species Detected Today", value: "47", change: "+12%", icon: "🦎" },
    { label: "Active Threats", value: "3", change: "-25%", icon: "⚠️" },
    { label: "Protected Areas", value: "23", change: "0%", icon: "🌳" },
    { label: "Researchers Online", value: "156", change: "+8%", icon: "👥" }
  ]

  const recentActivity = [
    { time: "2 min ago", event: "Lemur catta spotted in Andasibe", type: "sighting", priority: "normal" },
    { time: "15 min ago", event: "Deforestation alert in Zone 7", type: "threat", priority: "high" },
    { time: "1 hour ago", event: "New research data uploaded", type: "research", priority: "normal" },
    { time: "3 hours ago", event: "Camera trap maintenance completed", type: "maintenance", priority: "low" }
  ]

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-emerald-600 to-blue-600 rounded-xl p-6 text-white">
        <h2 className="text-2xl font-bold mb-2">Welcome to Madagascar Conservation AI</h2>
        <p className="text-emerald-100 mb-4">
          Real-time monitoring and intelligent conservation for Madagascar's unique ecosystems
        </p>
        <div className="flex space-x-4">
          <button className="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg transition-all">
            View Live Map
          </button>
          <button className="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg transition-all">
            Submit Report
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {stats.map((stat, index) => (
          <div key={index} className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">{stat.label}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                <p className={`text-sm ${stat.change.startsWith('+') ? 'text-green-600' : stat.change.startsWith('-') ? 'text-red-600' : 'text-gray-600'}`}>
                  {stat.change} from yesterday
                </p>
              </div>
              <div className="text-2xl">{stat.icon}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-100">
        <div className="p-6 border-b border-gray-100">
          <h3 className="text-lg font-semibold text-gray-900">Recent Activity</h3>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            {recentActivity.map((activity, index) => (
              <div key={index} className="flex items-center space-x-4 p-3 rounded-lg hover:bg-gray-50 transition-colors">
                <div className={`w-3 h-3 rounded-full ${
                  activity.priority === 'high' ? 'bg-red-500' :
                  activity.priority === 'normal' ? 'bg-yellow-500' : 'bg-green-500'
                }`}></div>
                <div className="flex-1">
                  <p className="text-sm text-gray-900">{activity.event}</p>
                  <p className="text-xs text-gray-500">{activity.time}</p>
                </div>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  activity.type === 'threat' ? 'bg-red-100 text-red-800' :
                  activity.type === 'sighting' ? 'bg-green-100 text-green-800' :
                  activity.type === 'research' ? 'bg-blue-100 text-blue-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {activity.type}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

// Species Identification Tab
function SpeciesIdentificationTab() {
  const [analysisResults, setAnalysisResults] = useState<any[]>([])

  const handleAnalysis = (result: any) => {
    setAnalysisResults(prev => [result, ...prev.slice(0, 4)]) // Keep last 5 results
  }

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">AI Species Identification</h2>
        <p className="text-gray-600">Upload images for instant species identification and conservation analysis</p>
      </div>

      <ImageUploadInterface onFileAnalysis={handleAnalysis} />

      {/* Recent Results */}
      {analysisResults.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Identifications</h3>
          <div className="space-y-3">
            {analysisResults.map((result, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900">🦎 {result.species}</p>
                  <p className="text-sm text-gray-600">{result.habitat} • {(result.confidence * 100).toFixed(1)}% confidence</p>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                  result.conservationStatus === 'Critically Endangered' ? 'bg-red-100 text-red-800' :
                  result.conservationStatus === 'Endangered' ? 'bg-orange-100 text-orange-800' :
                  'bg-yellow-100 text-yellow-800'
                }`}>
                  {result.conservationStatus}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

// Reporting Tab
function ReportingTab() {
  const handleReportSubmit = (data: any) => {
    console.log('Report submitted:', data)
    // Here you would typically send to your backend API
  }

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Conservation Reporting</h2>
        <p className="text-gray-600">Report species sightings, threats, research data, and maintenance issues</p>
      </div>

      <ConservationForm onSubmit={handleReportSubmit} />
    </div>
  )
}

// Analytics Tab
function AnalyticsTab() {
  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Conservation Analytics</h2>
        <p className="text-gray-600">Real-time insights and trends for Madagascar's conservation efforts</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Species Population Trends */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Species Population Trends</h3>
          <div className="space-y-4">
            {[
              { species: 'Lemur catta', trend: '+5.2%', status: 'stable' },
              { species: 'Indri indri', trend: '-2.1%', status: 'declining' },
              { species: 'Eulemur fulvus', trend: '+1.8%', status: 'improving' },
              { species: 'Propithecus diadema', trend: '-0.5%', status: 'stable' }
            ].map((item, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <span className="font-medium text-gray-900">{item.species}</span>
                <div className="flex items-center space-x-2">
                  <span className={`text-sm font-medium ${
                    item.trend.startsWith('+') ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {item.trend}
                  </span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    item.status === 'improving' ? 'bg-green-100 text-green-800' :
                    item.status === 'declining' ? 'bg-red-100 text-red-800' :
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    {item.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Threat Analysis */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Threat Analysis</h3>
          <div className="space-y-4">
            {[
              { threat: 'Deforestation', level: 'High', incidents: 23 },
              { threat: 'Poaching', level: 'Medium', incidents: 7 },
              { threat: 'Human Encroachment', level: 'Medium', incidents: 12 },
              { threat: 'Pollution', level: 'Low', incidents: 3 }
            ].map((item, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <span className="font-medium text-gray-900">{item.threat}</span>
                  <p className="text-sm text-gray-600">{item.incidents} incidents this month</p>
                </div>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  item.level === 'High' ? 'bg-red-100 text-red-800' :
                  item.level === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-green-100 text-green-800'
                }`}>
                  {item.level}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Conservation Impact Metrics */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Conservation Impact Metrics</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-800">94.2%</div>
            <div className="text-sm text-green-600">Ecosystem Health Score</div>
          </div>
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-2xl font-bold text-blue-800">156</div>
            <div className="text-sm text-blue-600">Active Conservation Projects</div>
          </div>
          <div className="text-center p-4 bg-purple-50 rounded-lg">
            <div className="text-2xl font-bold text-purple-800">87%</div>
            <div className="text-sm text-purple-600">Species Protection Success Rate</div>
          </div>
        </div>
      </div>
    </div>
  )
}

// Live Map Tab
function LiveMapTab() {
  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Live Conservation Map</h2>
        <p className="text-gray-600">Real-time species sightings, threats, and conservation activities across Madagascar</p>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Interactive Map</h3>
          <div className="flex space-x-2">
            <button className="px-3 py-1 text-sm bg-green-100 text-green-800 rounded-full">Species</button>
            <button className="px-3 py-1 text-sm bg-red-100 text-red-800 rounded-full">Threats</button>
            <button className="px-3 py-1 text-sm bg-blue-100 text-blue-800 rounded-full">Protected Areas</button>
          </div>
        </div>
        
        <div className="h-96 bg-gradient-to-br from-green-100 to-blue-100 rounded-lg flex items-center justify-center">
          <div className="text-center">
            <MapIcon className="w-16 h-16 text-green-600 mx-auto mb-4" />
            <p className="text-gray-600">Interactive Madagascar map will be integrated here</p>
            <p className="text-sm text-gray-500 mt-2">Real-time species locations, threat zones, and conservation data</p>
          </div>
        </div>

        {/* Map Legend */}
        <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-green-500 rounded-full"></div>
            <span className="text-sm text-gray-600">Species Sighting</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-red-500 rounded-full"></div>
            <span className="text-sm text-gray-600">Active Threat</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-blue-500 rounded-full"></div>
            <span className="text-sm text-gray-600">Protected Area</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-yellow-500 rounded-full"></div>
            <span className="text-sm text-gray-600">Research Station</span>
          </div>
        </div>
      </div>
    </div>
  )
}
