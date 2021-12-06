
<template>

  <v-carousel v-model="model" height="auto" class="mt-3" hide-delimiters>
    <v-carousel-item
      v-for="(item,i) in items"
      :key="i"
      :src="item.src"
    >
    </v-carousel-item>
  </v-carousel>

</template>


<script>
  export default {
    name: 'Carousel',

    data: () => ({

      items: [
          {
            src: 'https://blog.nubecolectiva.com/wp-content/uploads/2020/10/bbbimg_destacada_blog_devs-950x305.png',
          },
          {
            src: 'https://blog.nubecolectiva.com/wp-content/uploads/2020/09/2img_destacada_blog_devs-1-950x305.png',
          },
          {
            src: 'https://blog.nubecolectiva.com/wp-content/uploads/2020/09/aimg_destacada_blog_devs-2-950x305.png',
          },
          {
            src: 'https://blog.nubecolectiva.com/wp-content/uploads/2020/09/img_destacada_blog_devs-4-950x305.png',
          },
      ],

      model: 0,
      colors: [
        'primary',
        'secondary',
        'yellow darken-2',
        'red',
        'orange',
      ],     

    })

  }
</script>
