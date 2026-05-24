import { apiClient, toAbsoluteApiUrl } from "@/services/api-client"
import type {
  HealthCheckResponse,
  NormalizedVideoAnalysisResponse,
  VideoAnalysisResponse,
} from "@/types/video-analysis"

export async function healthCheck() {
  const response = await apiClient.get<HealthCheckResponse>("/health")
  return response.data
}

export async function analyzeVideo(file: File) {
  const formData = new FormData()
  formData.append("file", file)

  const response = await apiClient.post<VideoAnalysisResponse>("/videos/analyze", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  })

  return normalizeVideoAnalysisResponse(response.data)
}

function normalizeVideoAnalysisResponse(
  data: VideoAnalysisResponse
): NormalizedVideoAnalysisResponse {
  return {
    ...data,
    output: data.output
      ? {
          ...data.output,
          video_url: toAbsoluteApiUrl(data.output.video_url),
        }
      : data.output,
    metadata: data.metadata
      ? {
          ...data.metadata,
          sample_frame_urls: normalizeUrlList(data.metadata.sample_frame_urls),
          overlay_sample_frame_urls: data.metadata.overlay_sample_frame_urls
            ? normalizeUrlList(data.metadata.overlay_sample_frame_urls)
            : undefined,
        }
      : data.metadata,
  }
}

function normalizeUrlList(urls?: string[]) {
  return urls?.map(toAbsoluteApiUrl).filter((url): url is string => Boolean(url))
}
