<template>
    <div id="temporal_view"></div>
</template>

<script>
  /*
  Original source: https://www.echartsjs.com/examples/en/editor.html?c=area-simple
  Documentation for option: https://www.echartsjs.com/en/option.html#title
   */
  import * as echarts from "echarts";

  export default {
    name: "TemporalView",
    props:{
      temporalOverview: Object,
      loadingTimeSlider: Boolean
    },
    data() {
      return {
        // the DOM element
        timeSlider: null,
      }
    },
    watch:{
      temporalOverview: function() {
        this.renderTimeSlider();
      },
    },
    mounted:function(){
      this.initTimeSlider();
    },
    methods: {
      setPeriod(params) {
        let data = this.temporalOverview.date;

        // dataZoom can be triggered by the slider or the above click listener
        let periodStart = params.start? data[Math.ceil(data.length * params.start / 100)]: params.startValue;
        let periodEnd = params.end? data[Math.floor(data.length * params.end / 100)-1]: params.endValue;

        console.log(params);
        console.log(`emit message ${periodStart} to ${periodEnd}`);
        this.$emit('setPeriod', {periodStart: periodStart, periodEnd: periodEnd});
      },
      initTimeSlider() {
        this.timeSlider = echarts.init(document.getElementById('temporal_view'));
        this.timeSlider.showLoading();

        // click for 90 days context
        this.timeSlider.on('click', function (params) {
          let data = this.temporalOverview.date;
          let zoomSize = 45;  // days

          this.timeSlider.dispatchAction({
            type: 'dataZoom',
            dataZoomIndex: 0,
            startValue: data[Math.max(params.dataIndex - zoomSize, 0)],
            endValue: data[Math.min(params.dataIndex + zoomSize, data.length - 1)]
          });
        }, this);

        // obtain the time interval in the slider
        this.timeSlider.on('dataZoom', (params) => {this.setPeriod(params)}, this);
      },
      renderTimeSlider() {
        // draw time slider for transaction of 2014-2015
        let timeSliderOption = {
          // size of the chart, value is the padding to the direction
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
              end: 100,
              top: 'top',
              minValueSpan: 30  // at least one month
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
          toolbox: {
            top: 'top',
            right: 'right',
            feature: {
              restore: {
                title: ' ',
              }
            }
          },
          series: [
            {
              type: 'bar',
              animation: false,  // setting to false for better performance
              data: null
            }
          ]
        };

        // set the data
        timeSliderOption.xAxis.data = this.temporalOverview.date;
        timeSliderOption.series[0].data = this.temporalOverview.ap_txn_amount;
        this.timeSlider.setOption(timeSliderOption);
        this.timeSlider.hideLoading();
      }
    }
  }
</script>

<style scoped>

</style>