<template>
    <div id="temporal_view"></div>
</template>

<script>
  /*
  Source: https://www.echartsjs.com/examples/en/editor.html?c=area-simple
   */
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
          grid: {
            left: '40',
            right: '40',
            top: '30',
            bottom: '25',
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            axisLabel: {
              // shows only the first of month
              interval: function (index, value) {
                return value.slice(-2) === '01';
              },
              // shows the name of month
              formatter: function (value) {
                const MONTH = [
                  'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
                ];
                return MONTH[parseInt(value.slice(5,7))-1] + value.slice(2,4);
              },
              showMinLabel: true,
              showMaxLabel: true,
            },
            axisTick: {
              alignWithLabel: true,
              // shows only the first of month
              interval: function (index, value) {
                return value.slice(-2) === '01';
              },
            },
            data: null,
          },
          yAxis: {
            type: 'value',
            boundaryGap: false,
            min: 0
          },
          dataZoom: [
            {
              type: 'slider',
              show: true,
              xAxisIndex: 0,
              filterMode: 'filter',
              start: 0,
              end: 49.9,
              top: 'top',
              minValueSpan: 30  // at least one month
              // maxValueSpan: 364,  // at most one year
            },
            {
              type: 'slider',
              show: true,
              yAxisIndex: 0,
              filterMode: 'empty',
              left: 'right',
              start: 0,
              end: 100
            }
          ],
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'cross',
            },
            formatter: function (params) {
              return params[0].value.toFixed(2) + ' million';
            },
          },
          series: [
            {
              type: 'bar',
              animation: false,
              data: null
            }
          ]
        };
      },
      renderTimeSlider() {
        // set the data
        this.timeSliderOption['xAxis']['data'] = this.affiliatedPartyTimeList.date;
        this.timeSliderOption['series'][0]['data'] = this.affiliatedPartyTimeList.ap_txn_amount;
        this.timeSlider.setOption(this.timeSliderOption);
        this.timeSlider.hideLoading();

        // click for 90 days context
        this.timeSlider.on('click', function (params) {
          let data = this.affiliatedPartyTimeList.date;
          let zoomSize = 45;  // days
          this.timeSlider.dispatchAction({
            type: 'dataZoom',
            dataZoomIndex: 0,
            startValue: data[Math.max(params.dataIndex - zoomSize, 0)],
            endValue: data[Math.min(params.dataIndex + zoomSize, data.length - 1)]
          });
        }, this);
      }
    }
  }
</script>

<style scoped>

</style>