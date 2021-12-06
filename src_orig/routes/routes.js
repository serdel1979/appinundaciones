import DashboardLayout from "@/pages/Layout/DashboardLayout.vue";

import CaminosEvacuacion from "@/pages/CaminosEvacuacion.vue";
import Dashboard from "@/pages/Home.vue";
import Denuncias from "@/pages/Denuncias.vue";
import TableList from "@/pages/TableList.vue";
import Typography from "@/pages/Typography.vue";
import ZonasInundables from "@/pages/ZonasInundables.vue";
import Maps from "@/pages/Maps.vue";
import Notifications from "@/pages/Notifications.vue";
import UpgradeToPRO from "@/pages/UpgradeToPRO.vue";

const routes = [
  {
    path: "/",
    component: DashboardLayout,
    redirect: "/dashboard",
    children: [
      {
        path: "dashboard",
        name: "Dashboard",
        component: Dashboard,
      },
      {
        path: "denuncias",
        name: "Denuncias",
        component: Denuncias,
      },
      {
        path: "table",
        name: "Table List",
        component: TableList,
      },
      {
        path: "typography",
        name: "Typography",
        component: Typography,
      },
      {
        path: "zonasInundables",
        name: "zonasInundables",
        component: ZonasInundables,
      },
      {
        path: "caminosEvacuacion",
        name: "caminosEvacuacion",
        component: CaminosEvacuacion,
      },
      {
        path: "maps",
        name: "Maps",
        meta: {
          hideFooter: true,
        },
        component: Maps,
      },
      {
        path: "notifications",
        name: "Notifications",
        component: Notifications,
      },
      {
        path: "upgrade",
        name: "Upgrade to PRO",
        component: UpgradeToPRO,
      },
      {
        path: "estadisticas",
        name: "Upgrade to PRO",
        component: UpgradeToPRO,
      },
    ],
  },
];

export default routes;
