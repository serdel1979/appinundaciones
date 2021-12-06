<template>
  <div class="content">
    <div class="md-layout">
      <div class="md-layout-item">
        <md-card class="md-card-plain">
          <md-card-header data-background-color="green">
            <h4 class="title">Mapa</h4>
            <p class="category">Zonas de inundación</p>
          </md-card-header>
          <md-card-content>
            <div>
              <l-map
                :zoom="zoom"
                :center="center"
                style="height: 500px; width: 100%"
              >
                <l-polygon :lat-lngs="polygon.latlngs" :color="polygon.color">
                  <l-popup content="Polygon" />
                </l-polygon>
              </l-map>
            </div>
          </md-card-content>
        </md-card>
        <md-card class="md-card-plain">
          <md-card-header data-background-color="green">
            <h4 class="title">Detalle</h4>
            <p class="category">Descripción de las zonas</p>
          </md-card-header>
          <md-card-content>
            <h1>zonas:</h1>
            <ul v-if="zonas && zonas.length">
              <li v-for="(zona, index) in zonas" :key="index">
                <strong>{{ zona.name }}</strong>
              </li>
            </ul>
            <ul v-if="errors && errors.length">
              <li v-for="(error, index) in errors" :key="index">
                {{ error.message }}
              </li>
            </ul>
          </md-card-content>
        </md-card>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { LMap, LPolygon } from "vue2-leaflet";
export default {
  components: {
    LMap,
    LPolygon,
  },
  data() {
    return {
      zoom: 13,
      center: [-34.922883,-57.956317],

      polygon: {
        latlngs: [[
                   [-34.9263233179962,-57.93012826285298],
          [-34.93046548102748,-57.92247774276017],
          [-34.93851251419676,-57.927602147727995],
          [-34.93750667822358,-57.93813965653509],
          [-34.93543580061372,-57.94174839242791]
        ],[
        [-34.911598729026764,-57.9420016578851],
          [-34.91442360463918,-57.94516584229556],
          [-34.91509319053249,-57.94302236253363],
          [-34.913272741123905,-57.93996024858804]
        ]],

        color: "#ff00ff",
      },

      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zonas: [],
      errors: [],
    };
  },
  // Fetches posts when the component is created.
  created() {
    axios
      .get(
        "https://admin-grupo2.proyecto2021.linti.unlp.edu.ar/api/zonas-inundables"
      )
      .then((response) => {
        this.zonas = response.data.Zonas;
      })
      .catch((e) => {
        this.errors.push(e);
      });
  },
};
</script>
