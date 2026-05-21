import { Activity, Bot, CircleDot, Radar, Trophy } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

const summaryCards = [
  {
    label: "Videos en cola",
    value: "12",
    detail: "Listos para detectar robots y balón",
    icon: Activity,
  },
  {
    label: "Trayectorias de robots",
    value: "248",
    detail: "Rastreadas en sesiones recientes",
    icon: Bot,
  },
  {
    label: "Eventos del balón",
    value: "86",
    detail: "Posesión, tiros y transiciones",
    icon: CircleDot,
  },
  {
    label: "Reportes generados",
    value: "7",
    detail: "Listos para revisión del analista",
    icon: Trophy,
  },
]

const pipelineStages = [
  ["Carga de video", 72, "En cola de ingesta"],
  ["Detección de robots", 58, "Modelo de visión preparado"],
  ["Rastreo del balón", 46, "Eventos por sincronizar"],
  ["Generación de reportes", 34, "Resumen táctico pendiente"],
] as const

export function DashboardPage() {
  return (
    <div className="space-y-6">
      <section className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div>
          <Badge variant="outline">FutBotMX · IA</Badge>
          <h1 className="mt-3 text-3xl font-semibold tracking-normal text-foreground">
            Panel de análisis del partido
          </h1>
          <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
            Monitorea la carga de videos, detecciones de robots y balón, métricas
            del partido y reportes generados por el flujo de AstraVision.
          </p>
        </div>
        <Badge className="w-fit" variant="secondary">
          Sistema listo
        </Badge>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {summaryCards.map((card) => (
          <Card key={card.label} className="overflow-hidden">
            <CardHeader>
              <div className="flex items-center justify-between gap-3">
                <CardTitle>{card.label}</CardTitle>
                <div className="flex size-8 items-center justify-center rounded-lg bg-muted">
                  <card.icon className="h-4 w-4 text-muted-foreground" />
                </div>
              </div>
              <CardDescription>{card.detail}</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-semibold">{card.value}</p>
              <div className="mt-4 h-1 rounded-full bg-muted">
                <div className="h-1 w-2/3 rounded-full bg-primary" />
              </div>
            </CardContent>
          </Card>
        ))}
      </section>

      <section className="grid gap-4 lg:grid-cols-[1.4fr_1fr]">
        <Card>
          <CardHeader>
            <CardTitle>Flujo de análisis</CardTitle>
            <CardDescription>
              Estado de demostración para ingesta, detección, rastreo y reportes.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-5">
            {pipelineStages.map(([label, value, status]) => (
              <div key={label} className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="font-medium">{label}</span>
                  <span className="text-muted-foreground">{value}%</span>
                </div>
                <Progress value={Number(value)} />
                <p className="text-xs text-muted-foreground">{status}</p>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Siguiente enfoque</CardTitle>
            <CardDescription>
              Prioridades visuales para la demo de análisis FutBotMX.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3 text-sm text-muted-foreground">
            {[
              "Subir videos y dejarlos en cola para procesamiento de IA.",
              "Visualizar robots detectados, ruta del balón y eventos del partido.",
              "Revisar métricas antes de exportar reportes para analistas.",
            ].map((item) => (
              <div key={item} className="flex gap-3 rounded-lg border p-3">
                <Radar className="mt-0.5 h-4 w-4 shrink-0 text-muted-foreground" />
                <p>{item}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      </section>
    </div>
  )
}
