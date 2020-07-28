<template>
  <div id="app">
    <Mapbox
      access-token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTk1MjkyMzk5LCJl
      eHAiOjE1OTc4ODQzOTksInVzZXJfaWQiOjF9.IulCkLFv4GtBf6BXfRozgyMHbA0GEEUhx5br-5qDtVo"
      :map-options="{
        style: 'http://192.168.3.13:8000/cstddataplat/api/v0.1/maps/vectorserver/json/china16.json/',
        center: [116.38, 39.91],
        minZoom: 9.5,
        maxZoom: 13.5,
        zoom: 12
      }"
      :geolocate-control="{
        show: true,
        position: 'top-left',
      }"
      :scale-control="{
        show: true,
        position: 'top-left',
      }"
      :fullscreen-control="{
        show: true,
        position: 'top-left',
      }"

      @map-init="mapInitialized"
      @map-load="loaded"
      @map-mousemove="mousemove"
      @map-zoomend="zoomend"
      @map-click:points="clicked"
      @geolocate-error="geolocateError"
      @geolocate-geolocate="geolocate"
    />
    <!--      <p :class="$style.red">-->
    <!--    This should be red-->
    <!--  </p>-->
    <el-button type="primary" icon="el-icon-upload" class="updateDataset" @click="imagecropperShow=true">
      保存数据
    </el-button>
  </div>
<!--<div class="calculation-box">-->
<!--<p>Draw a polygon using the draw tools.</p>-->
<!--<div id="calculated-area"></div>-->
<!--</div>-->
</template>

<script>
import Mapbox from 'mapbox-gl-vue'
/* eslint-disable */
import MapboxDraw from "mapbox-gl-draw";
import map from 'mapbox-gl'
import 'mapbox-gl-draw/dist/mapbox-gl-draw.css'
import 'mapbox-gl/dist/mapbox-gl.css'

export default {
  components: { Mapbox },
  methods: {
    mapInitialized(map) {
      const Draw = new MapboxDraw(
          {
              displayControlsDefault: false,
              controls: {
                  polygon: true,
                  trash: true
              }}
      )
      map.addControl(Draw)
var markerHeight = 50, markerRadius = 10, linearOffset = 25;
var popupOffsets = {
'top-left': [100, 100],
'top-right': [100, 100],
};
        var popup = new mapboxgl.Popup({ offset: popupOffsets , className: 'my-class',closeOnClick: false })
// .setLngLat([116.38, 39.91])
.setHTML('<h1>Hello World!</h1>')
.addTo(map);
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
      //console.log(this.printData)
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
<!--<style module>-->
<!--.red {-->
<!--  color: red;-->
<!--}-->
<!--.bold {-->
<!--  font-weight: bold;-->
<!--}-->
<!--</style>-->
<style scoped>
#map {
  width: 100%;
  height: 700px;
}
.updateDataset {
            position: absolute;
            top:140px;
            left:10px;
            z-index:100;
            background-color:white;
            color:black;
            padding:6px;
            border-radius:4px;

}
  .calculation-box {
height: 75px;
width: 150px;
position: absolute;
bottom: 40px;
left: 10px;
background-color: rgba(255, 255, 255, 0.9);
padding: 15px;
text-align: center;
}

p {
font-family: 'Open Sans';
margin: 0;
font-size: 13px;
}
</style>
