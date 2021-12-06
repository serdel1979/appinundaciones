<template>
  <div class="wrapper" :class="{ 'nav-open': $sidebar.showSidebar }">
    <notifications></notifications>

    <side-bar
      :sidebar-item-color="sidebarBackground"
      :sidebar-background-image="sidebarBackgroundImage"
    >
      <mobile-menu slot="content"></mobile-menu>
      <sidebar-link to="/dashboard">
        <md-icon>home</md-icon>
        <p>Home</p>
      </sidebar-link>
      <sidebar-link to="/caminosEvacuacion">
        <md-icon>location_ons</md-icon>
        <p>Evacuacion</p>
      </sidebar-link>
      <sidebar-link to="/table">
        <md-icon>location_ons</md-icon>
        <p>Puntos de encuentro</p>
      </sidebar-link>
      <sidebar-link to="/ZonasInundables">
        <md-icon>location_ons</md-icon>
        <p>Zonas inundables</p>
      </sidebar-link>
      <sidebar-link to="/denuncias">
        <md-icon>report</md-icon>
        <p>Denunciar</p>
      </sidebar-link>
      <sidebar-link to="/maps">
        <md-icon>location_on</md-icon>
        <p>Localizar denuncias</p>
      </sidebar-link>
      <sidebar-link to="/estadisticas">
        <md-icon>dashboard</md-icon>
        <p>Estadísticas</p>
      </sidebar-link>
      
    </side-bar>

    <div class="main-panel">
      <top-navbar></top-navbar>

      <fixed-plugin
        :color.sync="sidebarBackground"
        :image.sync="sidebarBackgroundImage"
      >
      </fixed-plugin>

      <dashboard-content> </dashboard-content>

      <content-footer v-if="!$route.meta.hideFooter"></content-footer>
    </div>
  </div>
</template>

<script>
import TopNavbar from "./TopNavbar.vue";
import ContentFooter from "./ContentFooter.vue";
import DashboardContent from "./Content.vue";
import MobileMenu from "@/pages/Layout/MobileMenu.vue";
import FixedPlugin from "./Extra/FixedPlugin.vue";

export default {
  components: {
    TopNavbar,
    DashboardContent,
    ContentFooter,
    MobileMenu,
    FixedPlugin,
  },
  data() {
    return {
      sidebarBackground: "green",
      sidebarBackgroundImage: require("@/assets/img/sidebar-2.jpg"),
    };
  },
};
</script>
