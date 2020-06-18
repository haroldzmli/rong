<template>
  <swiper class="swiper" :options="swiperOption">
    <swiper-slide>
      <div class="swiper-zoom-container">
        <img :src="jpg6">
      </div>
    </swiper-slide>
    <swiper-slide>
      <div class="swiper-zoom-container">
        <img :src="jpg7">
      </div>
    </swiper-slide>
    <swiper-slide>
      <div class="swiper-zoom-container">
        <img :src="jpg8">
      </div>
    </swiper-slide>
    <div slot="pagination" class="swiper-pagination swiper-pagination-white" />
    <div slot="button-prev" class="swiper-button-prev" />
    <div slot="button-next" class="swiper-button-next" />
  </swiper>
</template>

<script>
import { Swiper, SwiperSlide } from 'vue-awesome-swiper'
import 'swiper/css/swiper.css'
import jpg8 from '@/assets/images/example/8.jpg'
import jpg7 from '@/assets/images/example/7.jpg'
import jpg6 from '@/assets/images/example/6.jpg'

export default {
  name: 'SwiperExampleZoom',
  title: 'Zoom',
  components: {
    Swiper,
    SwiperSlide
  },
  data() {
    return {
      swiperOption: {
        zoom: true,
        pagination: {
          el: '.swiper-pagination'
        },
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev'
        }
      },
      jpg6: jpg6,
      jpg7: jpg7,
      jpg8: jpg8
    }
  }
}
</script>

<style lang="scss" scoped>
  /*@import './base.scss';*/

  .swiper {
    height: 800px;

    .swiper-slide {
      background: #444;
    }
  }
</style>
