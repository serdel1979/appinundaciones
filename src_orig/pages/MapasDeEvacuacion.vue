import { ChartCard, StatsCard } from '../components';

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
                Datos sobre evacuaciones y puntos de encuentro
              </h2>
              <Evacuaciones > </Evacuaciones>
              <PuntosDeEncuentro> </PuntosDeEncuentro>
              <chart-card></chart-card>
                <stats-card></stats-card>
          </md-card-content>

        </md-card>
      </div>
    </div>
  </div>
</template>


<script>
import { Evacuaciones, PuntosDeEncuentro, ChartCard, StatsCard } from "@/components";

export default {
  components: {
   Evacuaciones,
   PuntosDeEncuentro,
   ChartCard, 
   StatsCard
  },
  props: {
    dataBackgroundColor: {
      type: String,
      default: "",
    },
  },
};
</script>