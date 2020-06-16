<template>
  <MglMap
    container="map-test"
    :center.sync="center"
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
  name: 'VueMapBox',
  components: {
    MglMap
    // MglMarker,
    // MglGeojsonLayer
  },
  data() {
    return {
      accessToken: 'some_token',
      mapStyle: 'http://192.168.3.13:8000/mapstatic/china16.json',
      center: [30, 30],
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

