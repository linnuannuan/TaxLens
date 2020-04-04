<template>
    <div id="temporal_view"></div>
</template>

<script>
  /*
  Source: https://www.echartsjs.com/examples/en/editor.html?c=area-simple
   */
  // import * as d3 from "d3";
  // import * as lodash from "lodash";
  import * as echarts from "echarts";
  import EventService from "../utils/event-service";

  export default {
    name: "TemporalView",
    props:{
      affiliatedPartyTimeList: Object,
      loadingTimeSlider: Boolean
    },
    data() {
      return {
        timeSlider: null,
        timeSliderOption: {},
      }
    },
    watch:{
      affiliatedPartyTimeList: function() {
        this.renderTimeSlider();
      },
    },
    mounted:function(){
      this.initTimeSlider();
    },
    methods: {
      handleView(id) {
        EventService.emitSuspiciousGroupSelected(id);
      },
      initTimeSlider() {
        this.timeSlider = echarts.init(document.getElementById('temporal_view'));
        this.timeSlider.showLoading();
        // draw time slider for transaction of 2014-2015
        this.timeSliderOption = {
          tooltip: {
            trigger: 'axis',
            position: function (pt) {
              return [pt[0], '10%'];
            }
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            axisLabel: {
              interval: function(index, value) {
                return value.slice(-2) === '01';
              },
              formatter: function (value) {
                return echarts.format.formatTime('MM-yyyy', value);
              },
              rotate: 45
            },
            axisTick: {
              interval: function(index, value) {
                return value.slice(-2) === '01';
              },
              alignWithLabel: true
            },
            data: null
          },
          yAxis: {
            type: 'value',
            boundaryGap: false,
            min: 0,
          },
          dataZoom: [
            {
              type: 'slider',
              show: true,
              xAxisIndex: [0],
              filterMode: 'filter',
              start: 0,
              end: 50
            },
            {
              type: 'slider',
              show: true,
              yAxisIndex: [0],
              filterMode: 'empty',
              left: '93%',
              start: 0,
              end: 100
            },
            {
              type: 'inside',
              xAxisIndex: [0],
              start: 0,
              end: 50
            }
          ],
          series: [
            {
              name: 'Txn amount (mil)',
              type: 'bar',
              data: null
            }
          ]
        };
      },
      renderTimeSlider() {
        // render time slider
        this.timeSliderOption['xAxis']['data'] = this.affiliatedPartyTimeList.date;
        this.timeSliderOption['series'][0]['data'] = this.affiliatedPartyTimeList.ap_txn_amount;

        this.timeSlider.setOption(this.timeSliderOption);
        this.timeSlider.hideLoading()
      }
    }
  }
</script>

<style scoped>

</style>