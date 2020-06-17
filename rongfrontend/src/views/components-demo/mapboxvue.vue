<!-- mapboxue 跳出大坑，就是 django的 static file server 不受 跨域限制-->
<template>
  <MglMap
    container="map-test"
    :zoom.sync="zoom"
    :center="center"
    :map-style="mapStyle"
  />
</template>

<script>
import Mapbox from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

import {
  MglMap
  // MglMarker,
  // MglGeojsonLayer
} from 'vue-mapbox'

export default {
  name: 'MapboxVue',
  components: {
    MglMap
    // MglMarker,
    // MglGeojsonLayer
  },
  data() {
    return {
      accessToken: 'some_token',
      mapStyle: 'http://192.168.3.13:8000/cstddataplat/api/v0.1/maps/vectorserver/json/china16.json/',
      center: [116.38, 39.91],
      zoom: 12
    }
  },
  created() {
    // We need to set mapbox-gl library here in order to use it in template
    this.mapbox = Mapbox
  },
  methods: {
    // onMapLoaded (event) {
    //   // in component
    //   this.map = event.map
    //   // or just to store if you want have access from other components
    //   this.$store.map = event.map
    // }
  }
}
</script>
