<template>
  <div id="app">
    <Mapbox
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
    />
  </div>
</template>

<script>
import Mapbox from 'mapbox-gl-vue'

export default {
  components: { Mapbox },
  data() {
    return {
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

<style>
#map {
  width: 100%;
  height: 800px;
}
</style>
