import { useMemo, useRef, useState } from "react"
import { useMutation, useQuery } from "@tanstack/react-query"
import axios from "axios"
import {
  AlertCircle,
  CheckCircle2,
  FileVideo,
  ImageIcon,
  Loader2,
  ServerOff,
  UploadCloud,
} from "lucide-react"

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { API_BASE_URL } from "@/services/api-client"
import { analyzeVideo, healthCheck } from "@/services/video-analysis.service"
import type { NormalizedVideoAnalysisResponse } from "@/types/video-analysis"

const MAX_UPLOAD_SIZE_BYTES = 200 * 1024 * 1024
const ACCEPTED_VIDEO_EXTENSIONS = [".mp4", ".mov", ".avi", ".mkv", ".webm"]
const ACCEPTED_VIDEO_TYPES = [
  "video/mp4",
  "video/quicktime",
  "video/x-msvideo",
  "video/x-matroska",
  "video/webm",
]

export function VideoAnalysisPage() {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [validationError, setValidationError] = useState<string | null>(null)
  const [analysisResult, setAnalysisResult] =
    useState<NormalizedVideoAnalysisResponse | null>(null)

  const healthQuery = useQuery({
    queryKey: ["backend-health"],
    queryFn: healthCheck,
    retry: 1,
    refetchInterval: 30000,
  })

  const analysisMutation = useMutation({
    mutationFn: analyzeVideo,
    onSuccess: (data) => {
      setAnalysisResult(data)
      if (data.status === "error") {
        setValidationError(data.message ?? "El backend no pudo analizar el video.")
        return
      }
      setValidationError(null)
    },
    onError: (error) => {
      setValidationError(getUploadErrorMessage(error))
    },
  })

  const previewFrames = useMemo(() => {
    const metadata = analysisResult?.metadata
    return metadata?.overlay_sample_frame_urls?.length
      ? metadata.overlay_sample_frame_urls
      : metadata?.sample_frame_urls ?? []
  }, [analysisResult])

  const canAnalyze = Boolean(selectedFile) && !analysisMutation.isPending

  function handleFileChange(file?: File) {
    setAnalysisResult(null)

    if (!file) {
      setSelectedFile(null)
      setValidationError(null)
      return
    }

    const error = validateVideoFile(file)
    if (error) {
      setSelectedFile(null)
      setValidationError(error)
      return
    }

    setSelectedFile(file)
    setValidationError(null)
  }

  function handleAnalyze() {
    if (!selectedFile) {
      setValidationError("Selecciona un video antes de iniciar el análisis.")
      return
    }

    const error = validateVideoFile(selectedFile)
    if (error) {
      setValidationError(error)
      return
    }

    analysisMutation.mutate(selectedFile)
  }

  return (
    <div className="space-y-6">
      <section className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
        <div>
          <div className="flex flex-wrap items-center gap-2">
            <Badge variant="outline">Análisis de video</Badge>
            <BackendStatusBadge connected={healthQuery.isSuccess} checked={healthQuery.isFetched} />
          </div>
          <h1 className="mt-3 text-3xl font-semibold tracking-normal text-foreground">
            Sube e inspecciona videos del partido
          </h1>
          <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
            Envía clips FutBotMX al backend local para generar overlays, video
            procesado y frames de vista previa para la demo.
          </p>
        </div>
        <div className="rounded-lg border bg-muted/30 px-3 py-2 text-xs text-muted-foreground">
          API local: <span className="font-medium text-foreground">{API_BASE_URL}</span>
        </div>
      </section>

      <section className="grid gap-4 xl:grid-cols-[minmax(0,1fr)_380px]">
        <Card>
          <CardHeader>
            <CardTitle>Entrada de video</CardTitle>
            <CardDescription>
              Formatos aceptados: MP4, MOV, AVI, MKV y WEBM. Tamaño máximo: 200 MB.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div
              className="flex min-h-60 flex-col items-center justify-center rounded-lg border border-dashed bg-muted/30 p-8 text-center transition-colors hover:bg-muted/45"
              onDragOver={(event) => event.preventDefault()}
              onDrop={(event) => {
                event.preventDefault()
                handleFileChange(event.dataTransfer.files[0])
              }}
            >
              <input
                ref={fileInputRef}
                className="sr-only"
                type="file"
                accept={ACCEPTED_VIDEO_EXTENSIONS.join(",")}
                onChange={(event) => handleFileChange(event.target.files?.[0])}
              />
              <div className="flex size-14 items-center justify-center rounded-xl bg-background shadow-sm">
                <UploadCloud className="h-5 w-5 text-muted-foreground" />
              </div>
              <h2 className="mt-4 text-lg font-medium">Arrastra aquí el video FutBotMX</h2>
              <p className="mt-2 max-w-md text-sm text-muted-foreground">
                También puedes seleccionar un archivo desde tu equipo. El video se
                procesa sin compresión en el frontend.
              </p>
              <Button
                className="mt-5"
                variant="outline"
                onClick={() => fileInputRef.current?.click()}
                disabled={analysisMutation.isPending}
              >
                <FileVideo className="h-4 w-4" />
                Seleccionar video
              </Button>
            </div>

            {selectedFile ? <SelectedFileDetails file={selectedFile} /> : null}

            {validationError ? (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>No se pudo continuar</AlertTitle>
                <AlertDescription>{validationError}</AlertDescription>
              </Alert>
            ) : null}

            {analysisMutation.isPending ? (
              <div className="space-y-2 rounded-lg border bg-muted/30 p-3">
                <div className="flex items-center gap-2 text-sm font-medium">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Subiendo y analizando video...
                </div>
                <Progress value={65} />
              </div>
            ) : null}

            <Button className="w-full sm:w-auto" onClick={handleAnalyze} disabled={!canAnalyze}>
              {analysisMutation.isPending ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <UploadCloud className="h-4 w-4" />
              )}
              Analizar video
            </Button>
          </CardContent>
        </Card>

        <TechnicalSummary result={analysisResult} previewFrameCount={previewFrames.length} />
      </section>

      <section className="grid gap-4 xl:grid-cols-[minmax(0,1.1fr)_minmax(320px,0.9fr)]">
        <ProcessedVideo result={analysisResult} />
        <PreviewFrames frames={previewFrames} />
      </section>
    </div>
  )
}

function BackendStatusBadge({ connected, checked }: { connected: boolean; checked: boolean }) {
  if (!checked) {
    return <Badge variant="outline">Verificando backend</Badge>
  }

  return connected ? (
    <Badge variant="secondary" className="gap-1.5">
      <CheckCircle2 className="h-3 w-3" />
      Backend conectado
    </Badge>
  ) : (
    <Badge variant="destructive" className="gap-1.5">
      <ServerOff className="h-3 w-3" />
      Backend no disponible
    </Badge>
  )
}

function SelectedFileDetails({ file }: { file: File }) {
  return (
    <div className="grid gap-3 rounded-lg border p-3 text-sm sm:grid-cols-3">
      <div>
        <p className="text-xs text-muted-foreground">Archivo</p>
        <p className="mt-1 truncate font-medium">{file.name}</p>
      </div>
      <div>
        <p className="text-xs text-muted-foreground">Tamaño</p>
        <p className="mt-1 font-medium">{formatBytes(file.size)}</p>
      </div>
      <div>
        <p className="text-xs text-muted-foreground">Tipo</p>
        <p className="mt-1 truncate font-medium">{file.type || "video/desconocido"}</p>
      </div>
    </div>
  )
}

function ProcessedVideo({ result }: { result: NormalizedVideoAnalysisResponse | null }) {
  const videoUrl = result?.output?.video_url

  return (
    <Card>
      <CardHeader>
        <CardTitle>Video procesado</CardTitle>
        <CardDescription>Resultado generado por el pipeline local de OpenCV.</CardDescription>
      </CardHeader>
      <CardContent>
        {videoUrl ? (
          <div className="overflow-hidden rounded-lg border bg-black">
            <video className="aspect-video w-full" controls src={videoUrl}>
              Tu navegador no puede reproducir este video.
            </video>
          </div>
        ) : (
          <EmptyState
            icon={FileVideo}
            title="Sin video procesado"
            description="Cuando el backend devuelva output.video_url, aparecerá aquí."
          />
        )}
      </CardContent>
    </Card>
  )
}

function PreviewFrames({ frames }: { frames: string[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Frames de vista previa</CardTitle>
        <CardDescription>
          Se priorizan frames con overlay; si no existen, se usan los frames procesados.
        </CardDescription>
      </CardHeader>
      <CardContent>
        {frames.length > 0 ? (
          <div className="grid gap-3 sm:grid-cols-2">
            {frames.map((frameUrl, index) => (
              <a
                key={frameUrl}
                href={frameUrl}
                target="_blank"
                rel="noreferrer"
                className="group overflow-hidden rounded-lg border bg-muted"
              >
                <img
                  src={frameUrl}
                  alt={`Frame de vista previa ${index + 1}`}
                  className="aspect-video w-full object-cover transition-transform group-hover:scale-[1.02]"
                />
              </a>
            ))}
          </div>
        ) : (
          <EmptyState
            icon={ImageIcon}
            title="Sin frames de vista previa"
            description="El backend puede devolver metadata.overlay_sample_frame_urls o metadata.sample_frame_urls."
          />
        )}
      </CardContent>
    </Card>
  )
}

function TechnicalSummary({
  result,
  previewFrameCount,
}: {
  result: NormalizedVideoAnalysisResponse | null
  previewFrameCount: number
}) {
  const metadata = result?.metadata
  const usefulMetadata = metadata
    ? [
        ["Pipeline", metadata.pipeline_status],
        ["Frames procesados", metadata.frames_processed],
        ["Frames totales", metadata.frame_count],
        ["Duración", formatSeconds(metadata.duration_seconds)],
        ["FPS", formatNumber(metadata.fps)],
        ["Resolución", formatResolution(metadata.width, metadata.height)],
        ["Modo de detección", metadata.detection_mode],
        ["Advertencia", metadata.warning],
        ["Error", metadata.error],
      ].filter(([, value]) => value !== undefined && value !== null && value !== "")
        .map(([label, value]) => [String(label), String(value)] as const)
    : []

  return (
    <Card>
      <CardHeader>
        <CardTitle>Resumen técnico</CardTitle>
        <CardDescription>Datos principales de la respuesta del backend.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <SummaryRow label="Estado" value={result?.status ?? "Sin análisis"} />
        <SummaryRow label="Archivo" value={result?.input?.filename ?? "Pendiente"} />
        <SummaryRow
          label="Video procesado"
          value={result?.output?.video_url ?? "No disponible"}
          wrap
        />
        <SummaryRow label="Frames preview" value={previewFrameCount.toString()} />

        {result?.message ? (
          <Alert>
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Mensaje del backend</AlertTitle>
            <AlertDescription>{result.message}</AlertDescription>
          </Alert>
        ) : null}

        {usefulMetadata.length > 0 ? (
          <div className="space-y-2 border-t pt-4">
            {usefulMetadata.map(([label, value]) => (
              <SummaryRow key={label} label={label} value={String(value)} />
            ))}
          </div>
        ) : null}
      </CardContent>
    </Card>
  )
}

function SummaryRow({
  label,
  value,
  wrap = false,
}: {
  label: string
  value: string
  wrap?: boolean
}) {
  return (
    <div className="grid gap-1 text-sm">
      <p className="text-xs text-muted-foreground">{label}</p>
      <p className={wrap ? "break-all font-medium" : "truncate font-medium"}>{value}</p>
    </div>
  )
}

function EmptyState({
  icon: Icon,
  title,
  description,
}: {
  icon: typeof FileVideo
  title: string
  description: string
}) {
  return (
    <div className="flex min-h-48 flex-col items-center justify-center rounded-lg border bg-muted/30 p-6 text-center">
      <Icon className="h-5 w-5 text-muted-foreground" />
      <p className="mt-3 text-sm font-medium">{title}</p>
      <p className="mt-1 max-w-sm text-sm text-muted-foreground">{description}</p>
    </div>
  )
}

function validateVideoFile(file: File) {
  if (file.size > MAX_UPLOAD_SIZE_BYTES) {
    return `El archivo pesa ${formatBytes(file.size)}. El límite para esta demo es 200 MB.`
  }

  const lowerName = file.name.toLowerCase()
  const hasAcceptedExtension = ACCEPTED_VIDEO_EXTENSIONS.some((extension) =>
    lowerName.endsWith(extension)
  )
  const hasAcceptedType = file.type ? ACCEPTED_VIDEO_TYPES.includes(file.type) : false

  if (!hasAcceptedExtension && !hasAcceptedType) {
    return "Formato no soportado. Usa un video MP4, MOV, AVI, MKV o WEBM."
  }

  return null
}

function getUploadErrorMessage(error: unknown) {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail
    const message = error.response?.data?.message

    if (typeof detail === "string") {
      return detail
    }

    if (typeof message === "string") {
      return message
    }

    if (error.code === "ERR_NETWORK") {
      return "No se pudo conectar con el backend local. Verifica que esté encendido en http://127.0.0.1:8000."
    }
  }

  return "Ocurrió un error al subir o analizar el video. Intenta de nuevo."
}

function formatBytes(bytes: number) {
  if (bytes === 0) {
    return "0 B"
  }

  const units = ["B", "KB", "MB", "GB"]
  const unitIndex = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1)
  const value = bytes / 1024 ** unitIndex
  return `${value.toFixed(value >= 10 || unitIndex === 0 ? 0 : 1)} ${units[unitIndex]}`
}

function formatSeconds(value: unknown) {
  return typeof value === "number" ? `${value.toFixed(1)} s` : value
}

function formatNumber(value: unknown) {
  return typeof value === "number" ? value.toFixed(2) : value
}

function formatResolution(width: unknown, height: unknown) {
  if (typeof width === "number" && typeof height === "number") {
    return `${width} x ${height}`
  }

  return undefined
}
