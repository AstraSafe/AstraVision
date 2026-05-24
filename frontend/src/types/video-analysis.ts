export type HealthCheckResponse = {
  status: string
  service?: string
  version?: string
  message?: string
}

export type VideoAnalysisInput = {
  filename?: string | null
  saved_path?: string | null
}

export type VideoAnalysisOutput = {
  filename?: string | null
  video_url?: string | null
  ready?: boolean
}

export type VideoAnalysisMetadata = {
  sample_frame_urls?: string[]
  overlay_sample_frame_urls?: string[]
  raw_sample_frame_urls?: string[]
  sample_frames_saved?: number
  frames_processed?: number
  frame_count?: number | null
  duration_seconds?: number | null
  fps?: number | null
  width?: number | null
  height?: number | null
  pipeline_status?: string
  detection_mode?: string
  warning?: string | null
  error?: string
  [key: string]: unknown
}

export type VideoAnalysisResponse = {
  analysis_id?: string | null
  status: string
  message?: string
  input?: VideoAnalysisInput
  output?: VideoAnalysisOutput
  metadata?: VideoAnalysisMetadata
}

export type NormalizedVideoAnalysisResponse = VideoAnalysisResponse & {
  output?: VideoAnalysisOutput
  metadata?: VideoAnalysisMetadata & {
    sample_frame_urls?: string[]
    overlay_sample_frame_urls?: string[]
  }
}
