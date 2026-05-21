import { BrainCircuit, Film, UploadCloud } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

export function VideoAnalysisPage() {
  return (
    <div className="space-y-6">
      <section>
        <Badge variant="outline">Análisis de video</Badge>
        <h1 className="mt-3 text-3xl font-semibold tracking-normal text-foreground">
          Sube e inspecciona videos del partido
        </h1>
        <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
          Prepara videos FutBotMX para detección de robots, rastreo del balón,
          extracción de eventos y revisión del analista.
        </p>
      </section>

      <section className="grid gap-4 lg:grid-cols-[1.2fr_1fr]">
        <Card className="min-h-[340px]">
          <CardHeader>
            <CardTitle>Entrada de video</CardTitle>
            <CardDescription>
              Área de carga preparada para la futura ingesta de partidos.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex min-h-56 flex-col items-center justify-center rounded-lg border border-dashed bg-muted/30 p-8 text-center">
              <div className="flex size-14 items-center justify-center rounded-xl bg-background shadow-sm">
                <UploadCloud className="h-5 w-5 text-muted-foreground" />
              </div>
              <h2 className="mt-4 text-lg font-medium">Arrastra aquí el video FutBotMX</h2>
              <p className="mt-2 max-w-md text-sm text-muted-foreground">
                La carga y el procesamiento con backend aún no están conectados.
                Esta pantalla reserva el flujo de trabajo para la demo.
              </p>
              <Button className="mt-5" variant="outline">
                <Film className="h-4 w-4" />
                Seleccionar video
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Preparación de IA</CardTitle>
            <CardDescription>
              Etapas previstas para la función de análisis.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {[
              "Muestreo de cuadros",
              "Detección de robots",
              "Rastreo del balón",
              "Línea de tiempo de eventos",
            ].map((step) => (
              <div key={step} className="flex items-center gap-3 rounded-lg border p-3">
                <BrainCircuit className="h-4 w-4 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">{step}</p>
                  <p className="text-xs text-muted-foreground">Base visual preparada</p>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </section>
    </div>
  )
}
