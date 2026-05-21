import { Download, FileText, LineChart, Share2 } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

const reportSections = [
  "Resumen del partido",
  "Rendimiento de robots",
  "Posesión del balón",
  "Línea de tiempo de eventos",
]

export function ReportsPage() {
  return (
    <div className="space-y-6">
      <section className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div>
          <Badge variant="outline">Reportes</Badge>
          <h1 className="mt-3 text-3xl font-semibold tracking-normal text-foreground">
            Genera salidas listas para analistas
          </h1>
          <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
            Organiza la inteligencia del partido en reportes FutBotMX revisables
            cuando los resultados del análisis estén disponibles.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button variant="outline">
            <Share2 className="h-4 w-4" />
            Compartir
          </Button>
          <Button>
            <Download className="h-4 w-4" />
            Exportar
          </Button>
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-[1fr_1fr]">
        <Card>
          <CardHeader>
            <CardTitle>Estructura del reporte</CardTitle>
            <CardDescription>
              Módulos preparados para futuros reportes generados.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {reportSections.map((section) => (
              <div key={section} className="flex items-center gap-3 rounded-lg border p-3">
                <FileText className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm font-medium">{section}</span>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Resumen de métricas</CardTitle>
            <CardDescription>
              Área reservada para gráficas, tendencias y comparativos de equipos.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex min-h-64 flex-col items-center justify-center rounded-lg border border-dashed bg-muted/30 p-8 text-center">
              <div className="flex size-14 items-center justify-center rounded-xl bg-background shadow-sm">
                <LineChart className="h-5 w-5 text-muted-foreground" />
              </div>
              <h2 className="mt-4 text-lg font-medium">Las gráficas aparecerán aquí</h2>
              <p className="mt-2 max-w-sm text-sm text-muted-foreground">
                Recharts ya está disponible para futuras visualizaciones de métricas.
              </p>
            </div>
          </CardContent>
        </Card>
      </section>
    </div>
  )
}
