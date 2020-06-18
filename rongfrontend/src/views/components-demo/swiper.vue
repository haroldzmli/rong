<template>
  <div id="swiper">
    <div id="container">
      <swiper ref="mySwiper" :options="swiperOptions">
        <swiper-slide class="swiper-slide games"><Mapbox
          access-token="pk.eyJ1IjoibGlqaWFuZ2ppYW5namlhbmciLCJhIjoiY2s2b2czbmltMG14cDNkbXpldjhkd3c3ZiJ9.zBaMzJo2X2UVPyFTtd5hEQ"
          :map-options="{
            // style: 'mapbox://styles/mapbox/streets-v11',
            //  center: [-96, 37.8],
            // zoom: 3,
            style: 'http://192.168.3.13:8000/cstddataplat/api/v0.1/maps/vectorserver/json/china16.json/',
            center: center,
            minZoom: 9.5,
            maxZoom: 13.5,
            zoom: 12
          }"
          :geolocate-control="{
            show: true,
            position: 'top-left',
          }"
          @map-load="loaded"
          @map-zoomend="zoomend"
          @map-click:points="clicked"
          @geolocate-error="geolocateError"
          @geolocate-geolocate="geolocate"
        /></swiper-slide>
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
import Mapbox from 'mapbox-gl-vue'

export default {
  name: 'Carrousel',
  components: {
    Swiper,
    SwiperSlide,
    Mapbox
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
      },
      accessToken: 'some_token',
      mapStyle: 'http://192.168.3.13:8000/cstddataplat/api/v0.1/maps/vectorserver/json/china16.json/',
      center: [116.38, 39.91],
      zoom: 12
    }
  },
  methods: {
    loaded(map) {
      map.addLayer({
        id: 'points',
        type: 'symbol',
        source: {
          type: 'geojson',
          data: {
            type: 'FeatureCollection',
            features: [
              {
                type: 'Feature',
                geometry: {
                  type: 'Point',
                  coordinates: [116.38, 39.91]
                },
                properties: {
                  title: 'Mapbox DC',
                  icon: 'monument'
                }
              },
              {
                type: 'Feature',
                geometry: {
                  type: 'Point',
                  coordinates: [116.381, 39.92]
                },
                properties: {
                  title: 'Mapbox SF',
                  icon: 'harbor'
                }
              }
            ]
          }
        },
        layout: {
          'icon-image': '{icon}-15',
          'text-field': '{title}',
          'text-font': ['YaHeiRegular'],
          'text-offset': [0, 0.6],
          'text-anchor': 'top'
        }
      })
    },
    zoomend(map, e) {
      console.log('Map zoomed')
    },
    clicked(map, e) {
      const title = e.features[0].properties.title
      console.log(title)
    },
    geolocateError(control, positionError) {
      console.log(positionError)
    },
    geolocate(control, position) {
      console.log(
        `User position: ${position.coords.latitude}, ${position.coords.longitude}`
      )
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
