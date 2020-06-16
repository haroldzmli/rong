<template>
  <div id="swiper">
    <div id="container">
      <swiper ref="mySwiper" :options="swiperOptions">
        <swiper-slide class="swiper-slide games"><p>slide one</p></swiper-slide>
        <swiper-slide class="swiper-slide games"><p>2</p></swiper-slide>
        <swiper-slide class="swiper-slide games"><p>3</p></swiper-slide>
        <swiper-slide class="swiper-slide games"><p>4</p></swiper-slide>
      </swiper>
      <!--       <div class="swiper-pagination" slot="pagination"></div>-->
      <div slot="navigation" class="swiper-button-prev" />
      <div slot="navigation" class="swiper-button-next" />
    </div>
  </div>
</template>

<script>
// https://github.com/surmon-china/vue-awesome-swiper
// https://swiperjs.com/get-started/
// https://github.com/surmon-china/
import { Swiper, SwiperSlide } from 'vue-awesome-swiper'
import 'swiper/css/swiper.css'

export default {
  name: 'Carrousel',
  components: {
    Swiper,
    SwiperSlide
  },
  data() {
    return {
      swiperOptions: {
        notNextTick: true,
        // watchSlidesProgress: true,
        // slidesPerView: 'auto',
        centeredSlides: true,
        loop: true,
        // loopedSlides: 5,
        autoplay: true,
        // pagination: {
        //   el: '.swiper-pagination'
        // },
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev'
        }
      }
    }
  }
}
</script>

<style type="text/scss" lang="scss">
  html {
    background: rgba(0,0,0,.5);
  }
  #swiper {
    position: relative;
    width: 100%;
    height: 500px;
    min-width: 1200px;
    background: #d3d6a2;
    #container {
      width: 60%;
      height: 300px;
      margin: 0 auto;
      position: relative;
      top: 50%;
      transform: translateY(-50%);
    }
    .swiper-slide {
      width: 500px;
      height: 300px;
      &:nth-child(odd) {
        background: #876843;
      }
      &:nth-child(even) {
        background: #234356;
      }
      p {
        line-height: 98px;
        padding-top: 0;
        text-align: center;
        color: #636363;
        font-size: 1.1em;
        margin: 0;
      }
    }
  }
</style>
