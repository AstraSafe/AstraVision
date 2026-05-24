import axios from "axios"

export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") ?? "http://127.0.0.1:8000"

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
})

export function toAbsoluteApiUrl(url?: string | null) {
  if (!url) {
    return url
  }

  try {
    return new URL(url, API_BASE_URL).toString()
  } catch {
    return url
  }
}
