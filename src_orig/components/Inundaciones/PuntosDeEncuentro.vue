
<template>
  <v-item-group class="mt-6">
    <v-container>
      <v-row>
        <!-- Servicio 1 -->
        <v-card class="mx-auto" max-width="344">
          <v-img src="img/serv1.jpg" height="200px"></v-img>

          <v-card-title class="justify-center"> Servicio 1 </v-card-title>

          <v-card-subtitle class="alinearjustificado">
            orem ipsum dolor sit amet, consectetur adipiscing elit. Fusce sit
            amet tellus sed ante tempus mattis.
          </v-card-subtitle>

          <v-btn class="ml-3 mb-3" color="primary"> Leer más ... </v-btn>
        </v-card>

        <!-- Servicio 2 -->
        <v-card class="mx-auto" max-width="344">
          <v-img src="img/serv2.jpg" height="200px"></v-img>

          <v-card-title class="justify-center"> Servicio 2 </v-card-title>

          <v-card-subtitle class="alinearjustificado">
            orem ipsum dolor sit amet, consectetur adipiscing elit. Fusce sit
            amet tellus sed ante tempus mattis.
          </v-card-subtitle>

          <v-btn class="ml-3 mb-3" color="primary"> Leer más ... </v-btn>
        </v-card>

        <!-- Servicio 3 -->
        <v-card class="mx-auto" max-width="344">
          <v-img src="img/serv3.jpg" height="200px"></v-img>

          <v-card-title class="justify-center"> Servicio 3 </v-card-title>

          <v-card-subtitle class="alinearjustificado">
            orem ipsum dolor sit amet, consectetur adipiscing elit. Fusce sit
            amet tellus sed ante tempus mattis.
          </v-card-subtitle>

          <v-btn class="ml-3 mb-3" color="primary"> Leer más ... </v-btn>
        </v-card>
      </v-row>
    </v-container>
  </v-item-group>
</template>


<script>
export default {
  name: "PuntosDeEncuentro",
   props: {
    dataBackgroundColor: {
      type: String,
      default: "",
    },
  },
};
</script>
 
<style scope>
.alinearjustificado {
  text-align: justify;
}
</style>