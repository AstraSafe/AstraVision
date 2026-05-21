import {
  BarChart3,
  Bot,
  BrainCircuit,
  CircleDot,
  FileText,
  LineChart,
  Play,
  Radar,
  Sparkles,
  UploadCloud,
  Video,
} from "lucide-react"

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

const heroBadges = [
  "FutBotMX",
  "Visión computacional",
  "IA aplicada",
  "Hackathon",
]

const summaryCards = [
  {
    label: "Videos analizados",
    value: "24",
    detail: "Partidos procesados para la demo",
    progress: 82,
    icon: Video,
  },
  {
    label: "Detecciones de robots",
    value: "1,248",
    detail: "Instancias identificadas por frame",
    progress: 74,
    icon: Bot,
  },
  {
    label: "Eventos del balón",
    value: "386",
    detail: "Pases, tiros y cambios de posesión",
    progress: 66,
    icon: CircleDot,
  },
  {
    label: "Reportes generados",
    value: "18",
    detail: "Resumen listos para compartir",
    progress: 58,
    icon: FileText,
  },
]

const workflowSteps = [
  {
    step: "1",
    title: "Sube un video de partido",
    description: "Carga la grabación del encuentro FutBotMX para iniciar el análisis.",
    icon: UploadCloud,
  },
  {
    step: "2",
    title: "Detecta robots y balón",
    description: "La visión computacional localiza elementos clave en la cancha.",
    icon: BrainCircuit,
  },
  {
    step: "3",
    title: "Rastrea trayectorias",
    description: "AstraVision reconstruye movimiento, dirección y zonas de actividad.",
    icon: LineChart,
  },
  {
    step: "4",
    title: "Genera métricas y reportes",
    description: "Convierte detecciones en indicadores claros para evaluar el partido.",
    icon: BarChart3,
  },
]

const benefits = [
  {
    title: "Detección visual clara",
    description:
      "Overlays simples ayudan a identificar robots, balón y puntos relevantes sin perder contexto del partido.",
    icon: Radar,
  },
  {
    title: "Métricas útiles",
    description:
      "Indicadores de actividad, trayectorias y eventos convierten el video en información accionable.",
    icon: BarChart3,
  },
  {
    title: "Presentación rápida",
    description:
      "Una pantalla lista para explicar el flujo completo del proyecto ante jueces y equipos técnicos.",
    icon: Sparkles,
  },
]

export function DashboardPage() {
  return (
    <div className="mx-auto flex max-w-7xl flex-col gap-6">
      <section className="grid gap-6 lg:grid-cols-[1.05fr_0.95fr] lg:items-stretch">
        <Card className="border-foreground/10 bg-card">
          <CardContent className="flex min-h-[390px] flex-col justify-between gap-8 p-6 sm:p-8">
            <div className="space-y-6">
              <div className="flex flex-wrap gap-2">
                {heroBadges.map((badge) => (
                  <Badge key={badge} variant="outline" className="bg-background/70">
                    {badge}
                  </Badge>
                ))}
              </div>

              <div className="max-w-3xl space-y-4">
                <div className="flex items-center gap-3">
                  <div className="flex size-11 items-center justify-center rounded-lg bg-primary text-primary-foreground shadow-sm">
                    <Bot className="h-5 w-5" />
                  </div>
                  <p className="text-sm font-medium text-muted-foreground">
                    Plataforma de inteligencia deportiva
                  </p>
                </div>
                <div>
                  <h1 className="text-4xl font-semibold tracking-normal text-foreground sm:text-5xl lg:text-6xl">
                    AstraVision
                  </h1>
                  <p className="mt-4 max-w-2xl text-lg font-medium text-foreground sm:text-xl">
                    Análisis inteligente de partidos FutBotMX con visión computacional
                  </p>
                  <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground sm:text-base">
                    Sube videos de partidos, detecta robots y balón, visualiza
                    trayectorias y convierte cada jugada en métricas listas para
                    reportes.
                  </p>
                </div>
              </div>
            </div>

            <div className="flex flex-col gap-3 sm:flex-row">
              <Button size="lg" className="sm:w-fit">
                <UploadCloud className="h-4 w-4" />
                Subir video
              </Button>
              <Button size="lg" variant="outline" className="sm:w-fit">
                <Play className="h-4 w-4" />
                Ver demo
              </Button>
            </div>
          </CardContent>
        </Card>

        <AnalysisPreview />
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {summaryCards.map((card) => (
          <Card key={card.label} className="bg-card">
            <CardHeader>
              <div className="flex items-start justify-between gap-3">
                <div>
                  <CardTitle>{card.label}</CardTitle>
                  <CardDescription className="mt-1">{card.detail}</CardDescription>
                </div>
                <div className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-muted">
                  <card.icon className="h-4 w-4 text-muted-foreground" />
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-3xl font-semibold tracking-normal">{card.value}</p>
              <Progress value={card.progress} />
            </CardContent>
          </Card>
        ))}
      </section>

      <section className="grid gap-6 xl:grid-cols-[1fr_0.85fr]">
        <Card>
          <CardHeader>
            <Badge variant="outline" className="w-fit">
              Flujo de análisis
            </Badge>
            <CardTitle className="text-2xl">
              ¿Cómo funciona AstraVision?
            </CardTitle>
            <CardDescription>
              Un proceso claro para transformar video de partido en inteligencia
              deportiva lista para presentar.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-2">
              {workflowSteps.map((item) => (
                <div key={item.step} className="rounded-lg border bg-background p-4">
                  <div className="flex items-start gap-3">
                    <div className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-primary text-sm font-semibold text-primary-foreground">
                      {item.step}
                    </div>
                    <div className="min-w-0 space-y-2">
                      <div className="flex items-center gap-2">
                        <item.icon className="h-4 w-4 text-muted-foreground" />
                        <h3 className="text-sm font-semibold">{item.title}</h3>
                      </div>
                      <p className="text-sm leading-6 text-muted-foreground">
                        {item.description}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Beneficios</CardTitle>
            <CardDescription>
              Ventajas pensadas para una demo breve, visual y convincente.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {benefits.map((benefit) => (
              <div key={benefit.title} className="rounded-lg border bg-background p-4">
                <div className="flex gap-3">
                  <div className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-muted">
                    <benefit.icon className="h-4 w-4 text-muted-foreground" />
                  </div>
                  <div className="space-y-1">
                    <h3 className="text-sm font-semibold">{benefit.title}</h3>
                    <p className="text-sm leading-6 text-muted-foreground">
                      {benefit.description}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </section>
    </div>
  )
}

function AnalysisPreview() {
  return (
    <Card className="bg-card">
      <CardHeader>
        <div className="flex items-center justify-between gap-3">
          <div>
            <CardTitle>Vista previa del análisis</CardTitle>
            <CardDescription>
              Simulación visual de detecciones y trayectorias sobre la cancha.
            </CardDescription>
          </div>
          <Badge variant="secondary" className="hidden sm:inline-flex">
            Demo
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="relative aspect-[16/10] min-h-[280px] overflow-hidden rounded-lg border bg-slate-950 text-white shadow-inner">
          <div className="absolute inset-0 bg-[linear-gradient(90deg,rgba(148,163,184,0.16)_1px,transparent_1px),linear-gradient(180deg,rgba(148,163,184,0.16)_1px,transparent_1px)] bg-[size:42px_42px]" />
          <div className="absolute inset-x-8 top-1/2 h-px bg-slate-500/50" />
          <div className="absolute inset-y-8 left-1/2 w-px bg-slate-500/50" />
          <div className="absolute left-[14%] top-[18%] h-[64%] w-[72%] rounded-[32px] border border-slate-500/50" />
          <div className="absolute left-1/2 top-1/2 size-24 -translate-x-1/2 -translate-y-1/2 rounded-full border border-slate-500/50" />

          <div className="absolute left-[19%] top-[25%] h-24 w-36 rounded-full border border-dashed border-cyan-300/70" />
          <div className="absolute bottom-[18%] right-[16%] h-20 w-44 rounded-full border border-dashed border-amber-300/70" />
          <div className="absolute left-[28%] top-[64%] h-1 w-[38%] -rotate-12 rounded-full bg-cyan-300/70" />
          <div className="absolute left-[43%] top-[42%] h-1 w-[28%] rotate-[22deg] rounded-full bg-amber-300/80" />

          <DetectionMarker
            className="left-[25%] top-[34%]"
            label="Robot A"
            tone="cyan"
          />
          <DetectionMarker
            className="right-[22%] top-[57%]"
            label="Robot B"
            tone="amber"
          />
          <DetectionMarker
            className="left-[52%] top-[47%]"
            label="Balón"
            tone="white"
          />

          <div className="absolute bottom-4 left-4 right-4 flex flex-wrap items-center justify-between gap-3 rounded-lg border border-white/10 bg-slate-950/75 px-3 py-2 text-xs text-slate-200 backdrop-blur">
            <span>Frame 01:24</span>
            <span>Confianza promedio 94%</span>
            <span>3 objetos detectados</span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

function DetectionMarker({
  className,
  label,
  tone,
}: {
  className: string
  label: string
  tone: "amber" | "cyan" | "white"
}) {
  const toneClasses = {
    amber: "border-amber-300 bg-amber-300 text-slate-950",
    cyan: "border-cyan-300 bg-cyan-300 text-slate-950",
    white: "border-white bg-white text-slate-950",
  }

  return (
    <div className={`absolute ${className}`}>
      <div
        className={`size-4 rounded-full border-2 shadow-sm ${toneClasses[tone]}`}
      />
      <div className="mt-2 rounded-md border border-white/10 bg-slate-900/90 px-2 py-1 text-xs font-medium text-white shadow-sm">
        {label}
      </div>
    </div>
  )
}
