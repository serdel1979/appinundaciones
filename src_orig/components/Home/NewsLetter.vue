
<template>
  <v-container class="mt-10">
    <div class="mt-6 text-center">
      <h2>Newsletter</h2>
    </div>

    <v-row align="center" justify="center">
      <v-form
        ref="form"
        v-model="valid"
        lazy-validation
        :class="{
          '': $vuetify.breakpoint.smAndDown,
          ancho: $vuetify.breakpoint.mdAndUp,
        }"
      >
        <v-text-field
          v-model="email"
          :rules="emailRules"
          label="E-mail"
          required
        >
          <template v-slot:append>
            <v-btn depressed :disabled="!valid" color="success" class="ml-10">
              Aceptar
            </v-btn>
          </template>
        </v-text-field>
      </v-form>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Newsletter",

  data: () => ({
    valid: true,
    email: "",
    emailRules: [
      (v) => !!v || "Ingresa tu Email",
      (v) => /.+@.+\..+/.test(v) || "Ingresa un Email válido",
    ],
  }),
};
</script>

<style scoped>
.ancho {
  width: 600px;
}
</style>
