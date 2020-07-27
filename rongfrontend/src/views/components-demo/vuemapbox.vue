<template>
  <div id="app" style="position:absolute; z-index:2; left:10px; top:10px; right:100px">
    <Mapbox
      access-token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTk1MjkyMzk5LCJleHAiOjE1OTc4ODQzOTksInVzZXJfaWQiOjF9.IulCkLFv4GtBf6BXfRozgyMHbA0GEEUhx5br-5qDtVo"
      :map-options="{
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
      :fullscreen-control="{
        show: true,
        position: 'top-left',
      }"
      @map-init="initialized"
      @map-load="loaded"
      @map-mousemove="mousemove"
      @map-zoomend="zoomend"
      @map-click:points="clicked"
      @geolocate-error="geolocateError"
      @geolocate-geolocate="geolocate"
    />
    <div style="position:absolute; z-index:2; left:10px; top:10px; right:100px">{{ printData }}</div>
  </div>
</template>

<script>
import Mapbox from 'mapbox-gl-vue'
import MapboxDraw from 'mapbox-gl-draw'
// import MapboxDraw from 'mapbox-gl-draw'

export default {
  components: { Mapbox },
  data() {
    return {
      accessToken: 'some_token',
      mapStyle: 'http://192.168.3.13:8000/cstddataplat/api/v0.1/maps/vectorserver/json/china16.json/',
      center: [116.38, 39.91],
      zoom: 12,
      printData: null
    }
  },
  methods: {
    initialized(map) {
      const draw = new MapboxDraw(
        { displayControlsDefault: true }
      )
      //   { displayControlsDefault: false,
      //     controls: {
      //       polygon: true,
      //       trash: true
      //     }
      //   }

      map.addControl(draw, 'top-left')
    },

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
    mousemove(map, e) {
      this.printData = '比例尺：' + JSON.stringify(map.getZoom()) + '    屏幕坐标：' + JSON.stringify(e.point) + '    地图坐标：' + JSON.stringify(e.lngLat)
    //  console.log(this.printData)
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
	#map { position: absolute; top: 30px; bottom: 30px; left: 200px; width: 100%; }
</style>
