<template>
    <div id="calendar_view"></div>
</template>

<script>
  import * as echarts from "echarts";

  export default {
    name: 'CalendarView',
    props: {
      calendarData: Array,
      loadingCalendar: Boolean,
    },
    data() {
      return {
        // the DOM element
        calendar: null,
      }
    },
    watch: {
      calendarData: function () {
        this.renderCalendar();
      },
    },
    mounted: function () {
      this.initCalendar();
      this.renderCalendar();
    },
    methods: {
      initCalendar() {
        this.calendar = echarts.init(document.getElementById('calendar_view'));
      },
      renderCalendar() {
        if (this.calendarData === undefined || this.calendarData.length === 0) return;
        let src_data = this.calendarData[0];
        let dst_data = this.calendarData[1];

        let date_start = src_data['date'][0];
        let date_end = src_data['date'][src_data['date'].length-1];

        let heatmap = 'profit';
        let heatmap_max = Math.max(...src_data[heatmap]);
        let heatmap_min = Math.min(...src_data[heatmap]);

        let scatter = 'ap_profit';
        let scatter_max = Math.max(...src_data[scatter]);
        let scatter_min = Math.min(...src_data[scatter]);


        this.calendar.setOption({
          dataset: [
            {source: src_data},
            {source: dst_data}
          ],
          tooltip: {},
          calendar: {
            top: 60,
            bottom: 10,
            left: 30,
            right: '50%',
            range: [date_start, date_end],
            itemStyle: {borderWidth: 0.5},
            yearLabel: {show: false}
          },
          visualMap: [
            {
              seriesIndex: 0,
              min: heatmap_min,
              max: heatmap_max,
              calculable: true,
              dimension: heatmap,
              type: 'continuous',
              orient: 'horizontal',
              top: 'top',
              left: 'left',
              right: '50%',
              inRange: {
                color: ['#a6611a', '#dfc27d', '#f5f5f5', '#80cdc1', '#018571'],
              },
            },
            {
              seriesIndex: 1,
              show: false,
              min: scatter_min,
              max: scatter_max,
              dimension: scatter,
              type: 'continuous',
              orient: 'horizontal',
              inRange: {
                color: ['#d7191c', '#fdae61', '#ffffbf', '#a6d96a', '#1a9641'],
                symbolSize: [0, 10]
              },
            }
          ],
          series: [
            {
              type: 'heatmap',
              coordinateSystem: 'calendar',
              datasetIndex: 0,
              encode: {
                tooltip: [1,2,3,4,5,6,7,8]
              }
            },
            {
              type: 'scatter',
              coordinateSystem: 'calendar',
              datasetIndex: 0,
              encode: {}
            }
          ]
        });
      }
    }
  }
</script>

<style scoped>
</style>