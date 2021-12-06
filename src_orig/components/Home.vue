
<template>
  <v-app>
    <v-main>
      <Menu />

      <Carousel />
      <ServiciosDestacados />
      <Newsletter />

      <router-view>
        <v-content> </v-content>
      </router-view>

      <Footer />
    </v-main>
  </v-app>
</template>

<script>
import Menu from "./Menu";
import Carousel from "./Home/Carousel";
import ServiciosDestacados from "./Home/ServiciosDestacados";
import Newsletter from "./Home/Newsletter";
import Footer from "./Footer";

export default {
  name: "Home",

  watch: {
    $route: {
      immediate: true,
      handler(to) {
        document.title = to.meta.title || "Home - Mi Proyecto";
      },
    },
  },

  components: {
    Menu,
    Carousel,
    ServiciosDestacados,
    Newsletter,
    Footer,
  },

  data: () => ({
    //
  }),
};
</script>
