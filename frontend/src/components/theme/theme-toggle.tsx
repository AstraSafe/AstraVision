import { Moon, Sun } from "lucide-react"

import { Button } from "@/components/ui/button"
import { useTheme } from "./theme-provider"

export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme()
  const isDark = theme === "dark"

  return (
    <Button
      type="button"
      variant="outline"
      size="icon-sm"
      aria-label="Cambiar tema"
      title="Cambiar tema"
      onClick={toggleTheme}
      className="bg-background/80 transition-transform duration-300 ease-out hover:scale-[1.2]"
    >
      {isDark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
      <span className="sr-only">Cambiar tema</span>
    </Button>
  )
}
