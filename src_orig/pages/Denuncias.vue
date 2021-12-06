<template>
  <div class="content">
    <div class="md-layout">
      <div class="md-layout-item md-medium-size-100 md-size-66">
        <denuncias-form data-background-color="green"> </denuncias-form>
      </div>
    </div>
  </div>
</template>

<script>
import { DenunciasForm } from "@/components";

export default {
  components: {
    DenunciasForm,
  },
};
</script>
