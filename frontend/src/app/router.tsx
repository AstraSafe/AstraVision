import { createBrowserRouter, RouterProvider } from "react-router-dom"

import { AppLayout } from "@/components/layout/app-layout"
import { DashboardPage } from "@/pages/dashboard-page"
import { MatchViewerPage } from "@/pages/match-viewer-page"
import { ReportsPage } from "@/pages/reports-page"
import { VideoAnalysisPage } from "@/pages/video-analysis-page"

const router = createBrowserRouter([
  {
    element: <AppLayout />,
    children: [
      {
        path: "/",
        element: <DashboardPage />,
      },
      {
        path: "/analysis",
        element: <VideoAnalysisPage />,
      },
      {
        path: "/match-viewer",
        element: <MatchViewerPage />,
      },
      {
        path: "/reports",
        element: <ReportsPage />,
      },
    ],
  },
])

export function AppRouter() {
  return <RouterProvider router={router} />
}
