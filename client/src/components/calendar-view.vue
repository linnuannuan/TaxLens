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

        // layout
        let src_data = this.calendarData[0]['source'];
        let dst_data = this.calendarData[1]['source'];

        let date_start  = src_data['date'][0];
        let date_end    = src_data['date'][src_data['date'].length-1];

        let heatmap = 'profit';
        let heatmap_max_src = Math.max(...src_data[heatmap]);
        let heatmap_min_src = Math.min(...src_data[heatmap]);
        let heatmap_max_dst = Math.max(...dst_data[heatmap]);
        let heatmap_min_dst = Math.min(...dst_data[heatmap]);

        // min-max configuration for scatter plots, adding ones to make sure zeros are eliminated
        let scatter = 'ap_profit';
        let scatter_max_src = Math.max(...src_data[scatter], 1);
        let scatter_min_src = Math.min(...src_data[scatter], -1);
        let scatter_max_dst = Math.max(...dst_data[scatter], 1);
        let scatter_min_dst = Math.min(...dst_data[scatter], -1);

        // layout parameters
        let calendarPadding = 80;

        this.calendar.setOption({
          dataset: this.calendarData,
          tooltip: {},
          calendar: [
            {
              top: calendarPadding,
              bottom: calendarPadding,
              left: '5%',
              right: '52.5%',
              range: [date_start, date_end],
              itemStyle: {borderWidth: 0.5},
              yearLabel: {show: false}
            },
            {
              top: calendarPadding,
              bottom: calendarPadding,
              left: '52.5%',
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
              type: 'continuous',
              min: heatmap_min_src,
              max: heatmap_max_src,
              dimension: heatmap,
              orient: 'horizontal',
              bottom: 'bottom',
              left: 'left',
              calculable: true,
              padding: 10,
              itemWidth: 10,
              itemHeight: 250,
              text: ['Profit', 'Loss'],
              inRange: {
                color: ['#a6611a', '#dfc27d', '#f5f5f5', '#80cdc1', '#018571'],
                opacity: 0.75
              },
              formatter: (value) => {return ~~(value/1000) + 'k'},
            },
            {
              seriesIndex: 1,
              show: false,
              type: 'continuous',
              min: scatter_min_src,
              max: 0,
              orient: 'horizontal',
              inRange: {
                color: ['#d7191c', '#fdae61', '#ffffbf', '#a6d96a', '#1a9641'],
                symbolSize: [20, 0]
              },
            },
            {
              seriesIndex: 2,
              show: false,
              type: 'continuous',
              min: 0,
              max: scatter_max_src,
              orient: 'horizontal',
              inRange: {
                color: ['#d7191c', '#fdae61', '#ffffbf', '#a6d96a', '#1a9641'],
                symbolSize: [0, 20]
              },
            },
            // right calendar
            {
              seriesIndex: 3,
              type: 'continuous',
              min: heatmap_min_dst,
              max: heatmap_max_dst,
              dimension: heatmap,
              orient: 'horizontal',
              bottom: 'bottom',
              right: 'right',
              calculable: true,
              padding: 10,
              itemWidth: 10,
              itemHeight: 250,
              text: ['Profit', 'Loss'],
              inRange: {
                color: ['#a6611a', '#dfc27d', '#f5f5f5', '#80cdc1', '#018571'],
                opacity: 0.75
              },
              formatter: (value) => {return ~~(value/1000) + 'k'},
            },
            {
              seriesIndex: 4,
              show: false,
              type: 'continuous',
              min: scatter_min_dst,
              max: 0,
              orient: 'horizontal',
              inRange: {
                color: ['#d7191c', '#fdae61', '#ffffbf', '#a6d96a', '#1a9641'],
                symbolSize: [20, 0]
              },
            },
            {
              seriesIndex: 5,
              show: false,
              type: 'continuous',
              min: 0,
              max: scatter_max_dst,
              orient: 'horizontal',
              inRange: {
                color: ['#d7191c', '#fdae61', '#ffffbf', '#a6d96a', '#1a9641'],
                symbolSize: [0, 20]
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
              dimensions: ['date', scatter],
              encode: {},
              itemStyle: {
                borderColor: 'white',
                borderWidth: 3
              }
            },
            {
              type: 'scatter',
              coordinateSystem: 'calendar',
              datasetIndex: 0,
              calendarIndex: 0,
              dimensions: ['date', scatter],
              encode: {},
              itemStyle: {
                borderColor: 'white',
                borderWidth: 3
              }
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
              dimensions: ['date', scatter],
              encode: {},
              itemStyle: {
                borderColor: 'white',
                borderWidth: 3
              }
            },
            {
              type: 'scatter',
              coordinateSystem: 'calendar',
              datasetIndex: 1,
              calendarIndex: 1,
              dimensions: ['date', scatter],
              encode: {},
              itemStyle: {
                borderColor: 'white',
                borderWidth: 3
              }
            }
          ]
        });
      }
    }
  }
</script>

<style scoped>
</style>