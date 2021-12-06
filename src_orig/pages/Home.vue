<template>
  <div class="content">
    <div class="md-layout">
      <div class="md-layout-item">
        <md-card>
          <md-card-header data-background-color="green">
            <h4 class="title">Bienvenido</h4>
            <p class="category">Sistema de gestión de inundaciones</p>
          </md-card-header>

          <md-card-content>
          
              <h2>
                Ahora puede visualizar las zonas con peligro de inundacion,
                también puede ver los caminos de evacuacion y los puntos de
                encuentro mas cercanos. Puede realizar denuncias y ver las
                denuncias resueltas.
              </h2>
            
          </md-card-content>
        </md-card>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    dataBackgroundColor: {
      type: String,
      default: "",
    },
  },
};
</script>
