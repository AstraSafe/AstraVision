import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react"

type Theme = "light" | "dark"

type ThemeProviderContext = {
  theme: Theme
  setTheme: (theme: Theme) => void
  toggleTheme: () => void
}

const THEME_STORAGE_KEY = "astravision-theme"

const ThemeContext = createContext<ThemeProviderContext | undefined>(undefined)

function getStoredTheme(): Theme | null {
  try {
    if (typeof window === "undefined") {
      return null
    }

    const storedTheme = window.localStorage.getItem(THEME_STORAGE_KEY)

    if (storedTheme === "light" || storedTheme === "dark") {
      return storedTheme
    }
  } catch {
    return null
  }

  return null
}

function getSystemTheme(): Theme {
  if (
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-color-scheme: dark)").matches
  ) {
    return "dark"
  }

  return "light"
}

function persistTheme(theme: Theme) {
  try {
    window.localStorage.setItem(THEME_STORAGE_KEY, theme)
  } catch {
    // localStorage can be unavailable in private or restricted contexts.
  }
}

function applyTheme(theme: Theme) {
  if (typeof document === "undefined") {
    return
  }

  document.documentElement.classList.toggle("dark", theme === "dark")
}

type ThemeProviderProps = {
  children: ReactNode
}

export function ThemeProvider({ children }: ThemeProviderProps) {
  const [theme, setThemeState] = useState<Theme>(() => getStoredTheme() ?? getSystemTheme())

  useEffect(() => {
    applyTheme(theme)
  }, [theme])

  const value = useMemo<ThemeProviderContext>(() => {
    const setTheme = (nextTheme: Theme) => {
      setThemeState(nextTheme)
      persistTheme(nextTheme)
    }

    return {
      theme,
      setTheme,
      toggleTheme: () => {
        setTheme(theme === "dark" ? "light" : "dark")
      },
    }
  }, [theme])

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
}

export function useTheme() {
  const context = useContext(ThemeContext)

  if (!context) {
    throw new Error("useTheme debe usarse dentro de ThemeProvider")
  }

  return context
}
