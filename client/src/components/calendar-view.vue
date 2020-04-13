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

        let date_start  = src_data['date'][0];
        let date_end    = src_data['date'][src_data['date'].length-1];

        let heatmap = 'profit';
        let heatmap_max_src = Math.max(...src_data[heatmap]);
        let heatmap_min_src = Math.min(...src_data[heatmap]);
        let heatmap_max_dst = Math.max(...dst_data[heatmap]);
        let heatmap_min_dst = Math.min(...dst_data[heatmap]);

        let scatter = 'ap_profit';
        let scatter_max_src = Math.max(...src_data[scatter]);
        let scatter_min_src = Math.min(...src_data[scatter]);
        let scatter_max_dst = Math.max(...dst_data[scatter]);
        let scatter_min_dst = Math.min(...dst_data[scatter]);


        this.calendar.setOption({
          dataset: [
            {source: src_data},
            {source: dst_data}
          ],
          tooltip: {},
          calendar: [
            {
              top: 60,
              bottom: 10,
              left: '5%',
              right: '55%',
              range: [date_start, date_end],
              itemStyle: {borderWidth: 0.5},
              yearLabel: {show: false}
            },
            {
              top: 60,
              bottom: 10,
              left: '55%',
              right: '5%',
              range: [date_start, date_end],
              itemStyle: {borderWidth: 0.5},
              yearLabel: {show: false}
            }
          ],
          visualMap: [
            // left calendar
            {
              seriesIndex: 0,
              min: heatmap_min_src,
              max: heatmap_max_src,
              calculable: true,
              dimension: heatmap,
              type: 'continuous',
              orient: 'horizontal',
              top: 'top',
              left: 'left',
              inRange: {
                color: ['#a6611a', '#dfc27d', '#f5f5f5', '#80cdc1', '#018571'],
              },
            },
            {
              seriesIndex: 1,
              show: false,
              min: scatter_min_src,
              max: scatter_max_src,
              dimension: scatter,
              type: 'continuous',
              orient: 'horizontal',
              inRange: {
                color: ['#d7191c', '#fdae61', '#ffffbf', '#a6d96a', '#1a9641'],
                symbolSize: [0, 10]
              },
            },
            // right calendar
            {
              seriesIndex: 2,
              min: heatmap_min_dst,
              max: heatmap_max_dst,
              calculable: true,
              dimension: heatmap,
              type: 'continuous',
              orient: 'horizontal',
              top: 'top',
              right: 'right',
              inRange: {
                color: ['#a6611a', '#dfc27d', '#f5f5f5', '#80cdc1', '#018571'],
              },
            },
            {
              seriesIndex: 3,
              show: false,
              min: scatter_min_dst,
              max: scatter_max_dst,
              dimension: scatter,
              type: 'continuous',
              orient: 'horizontal',
              inRange: {
                color: ['#d7191c', '#fdae61', '#ffffbf', '#a6d96a', '#1a9641'],
                symbolSize: [0, 10]
              },
            },
          ],
          series: [
            // left calendar
            {
              type: 'heatmap',
              coordinateSystem: 'calendar',
              datasetIndex: 0,
              calendarIndex: 0,
              encode: {
                tooltip: [1,2,3,4,5,6,7,8]
              }
            },
            {
              type: 'scatter',
              coordinateSystem: 'calendar',
              datasetIndex: 0,
              calendarIndex: 0,
              encode: {}
            },
            // right calendar
            {
              type: 'heatmap',
              coordinateSystem: 'calendar',
              datasetIndex: 1,
              calendarIndex: 1,
              encode: {
                tooltip: [1,2,3,4,5,6,7,8]
              }
            },
            {
              type: 'scatter',
              coordinateSystem: 'calendar',
              datasetIndex: 1,
              calendarIndex: 1,
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