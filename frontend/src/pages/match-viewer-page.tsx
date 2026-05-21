import { CircleDot, Crosshair, Maximize2, Play } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

export function MatchViewerPage() {
  return (
    <div className="space-y-6">
      <section>
        <Badge variant="outline">Visor de partido</Badge>
        <h1 className="mt-3 text-3xl font-semibold tracking-normal text-foreground">
          Revisa detecciones sobre la cancha
        </h1>
        <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
          Visualiza posiciones de robots, movimiento del balón y capas de eventos
          cuando los datos de análisis estén conectados.
        </p>
      </section>

      <section className="grid gap-4 xl:grid-cols-[1.5fr_0.8fr]">
        <Card>
          <CardHeader>
            <div className="flex items-start justify-between gap-4">
              <div>
                <CardTitle>Reproducción de cancha</CardTitle>
                <CardDescription>
                  Lienzo preparado para video sincronizado y detecciones.
                </CardDescription>
              </div>
              <Button variant="outline" size="icon" aria-label="Expandir visor">
                <Maximize2 className="h-4 w-4" />
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="aspect-video rounded-lg border bg-muted/30 p-4">
              <div className="relative h-full overflow-hidden rounded-md border border-dashed bg-background/70">
                <div className="absolute inset-x-0 top-1/2 border-t border-dashed border-muted-foreground/20" />
                <div className="absolute inset-y-0 left-1/2 border-l border-dashed border-muted-foreground/20" />
                <div className="absolute left-[18%] top-[35%] flex items-center gap-2 rounded-full bg-background px-2 py-1 text-xs shadow-sm">
                  <Crosshair className="h-3 w-3" />
                  Robot A
                </div>
                <div className="absolute right-[22%] top-[48%] flex items-center gap-2 rounded-full bg-background px-2 py-1 text-xs shadow-sm">
                  <Crosshair className="h-3 w-3" />
                  Robot B
                </div>
                <div className="absolute left-[49%] top-[42%] flex size-7 items-center justify-center rounded-full bg-primary text-primary-foreground shadow-sm">
                  <CircleDot className="h-4 w-4" />
                </div>
                <div className="flex h-full items-center justify-center">
                  <Button>
                    <Play className="h-4 w-4" />
                    Vista previa
                  </Button>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Capas de detección</CardTitle>
            <CardDescription>
              Superposiciones previstas para el visor interactivo del partido.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {["Robots", "Trayectoria del balón", "Zonas de posesión", "Marcadores de eventos"].map(
              (layer) => (
                <div key={layer} className="flex items-center justify-between rounded-lg border p-3">
                  <span className="text-sm font-medium">{layer}</span>
                  <Badge variant="outline">Capa</Badge>
                </div>
              )
            )}
          </CardContent>
        </Card>
      </section>
    </div>
  )
}
