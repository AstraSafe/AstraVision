import {
  Activity,
  BarChart3,
  CircleCheck,
  FileText,
  LayoutDashboard,
  PlaySquare,
  UploadCloud,
} from "lucide-react"
import { NavLink, Outlet } from "react-router-dom"

import { ThemeToggle } from "@/components/theme/theme-toggle"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import futbotmxShield from "@/assets/escudo_futbotmx_2026_color.svg"

const navigationItems = [
  {
    label: "Panel",
    to: "/",
    icon: LayoutDashboard,
  },
  {
    label: "Análisis",
    to: "/analysis",
    icon: Activity,
  },
  {
    label: "Visor de partido",
    to: "/match-viewer",
    icon: PlaySquare,
  },
  {
    label: "Reportes",
    to: "/reports",
    icon: FileText,
  },
]

export function AppLayout() {
  return (
    <div className="min-h-svh bg-background text-foreground">
      <div className="grid min-h-svh lg:grid-cols-[260px_1fr]">
        <aside className="hidden h-svh border-r bg-sidebar/95 lg:sticky lg:top-0 lg:flex lg:flex-col lg:self-start">
          <div className="border-b px-5 py-5">
            <div className="flex items-center gap-3">
              <img
                src={futbotmxShield}
                alt="Escudo FutBotMX 2026"
                className="h-10 w-auto shrink-0 object-contain"
              />
              <div>
                <p className="text-sm font-semibold leading-none">AstraVision</p>
                <p className="mt-1 text-xs text-muted-foreground">FutBotMX · IA</p>
              </div>
            </div>
          </div>

          <nav className="flex min-h-0 flex-1 flex-col gap-1 overflow-y-auto px-3 py-4">
            {navigationItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.to === "/"}
                className={({ isActive }) =>
                  cn(
                    "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-muted hover:text-foreground",
                    isActive && "bg-muted text-foreground"
                  )
                }
              >
                <item.icon className="h-4 w-4" />
                {item.label}
              </NavLink>
            ))}
          </nav>

          <div className="border-t p-4">
            <div className="rounded-lg border bg-background p-3 shadow-sm">
              <div className="flex items-center justify-between gap-2">
                <span className="text-xs font-medium text-muted-foreground">Flujo</span>
                <Badge variant="outline">Listo</Badge>
              </div>
              <p className="mt-2 text-sm font-medium">Espacio de análisis de video</p>
              <p className="mt-1 text-xs text-muted-foreground">
                Preparado para carga, detección, métricas y reportes.
              </p>
            </div>
          </div>
        </aside>

        <div className="flex min-w-0 flex-col">
          <header className="sticky top-0 z-10 border-b bg-background/95 backdrop-blur">
            <div className="flex min-h-16 items-center justify-between gap-4 px-4 sm:px-6">
              <div>
                <p className="text-sm font-semibold leading-none">Consola AstraVision</p>
                <p className="mt-1 text-xs text-muted-foreground">
                  Panel de IA para inteligencia de partidos FutBotMX
                </p>
              </div>

              <div className="flex items-center gap-2">
                <div className="hidden items-center gap-2 md:flex">
                  <Badge variant="outline" className="gap-1.5">
                    <CircleCheck className="h-3 w-3" />
                    Sistema listo
                  </Badge>
                  <Button variant="outline" size="sm">
                    <UploadCloud className="h-4 w-4" />
                    Subir video
                  </Button>
                  <Button size="sm">
                    <BarChart3 className="h-4 w-4" />
                    Nuevo análisis
                  </Button>
                </div>
                <ThemeToggle />
              </div>
            </div>

            <nav className="flex gap-1 overflow-x-auto border-t px-4 py-2 lg:hidden">
              {navigationItems.map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  end={item.to === "/"}
                  className={({ isActive }) =>
                    cn(
                      "inline-flex shrink-0 items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-muted-foreground",
                      isActive ? "bg-muted text-foreground" : "hover:bg-muted"
                    )
                  }
                >
                  <item.icon className="h-4 w-4" />
                  {item.label}
                </NavLink>
              ))}
            </nav>
          </header>

          <main className="flex-1 px-4 py-6 sm:px-6 lg:px-8">
            <Outlet />
          </main>
        </div>
      </div>
    </div>
  )
}
