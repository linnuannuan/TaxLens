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
      try() {
        console.log('success')
      },
      initCalendar() {
        this.calendar = echarts.init(document.getElementById('calendar_view'));

        // An internal function for toolbox item handling periods operstion
        let goToQuarter = function (params, offset) {
          let originalStart = params.option.calendar[0].range[0];

          // Parse the date
          let year = parseInt(originalStart.slice(0, 4));
          // start month must be [1,4,7,10]; ~~ is equivalent to parse Int
          let quarter = ~~((parseInt(originalStart.slice(5, 7)) - 1) / 3) + offset;
          // Handle year change
          year = quarter === -1? year-1: quarter === 4? year+1: year;
          quarter = quarter === -1? 3: quarter === 4? 0: quarter;
          // day end must be either 30 for [6, 9] or 31 for [3, 12]
          let end = (quarter === 1 || quarter === 2)? '-30': '-31';

          // Calculate new range
          let startValue = year + '-' + (quarter*3+1).toString().padStart(2, '0') + '-01';
          let endValue = year + '-' + ((quarter+1)*3).toString().padStart(2, '0') + end;

          params.scheduler.ecInstance.setOption({
              calendar: [
                // left calendar
                {
                  id: 'src_calendar',
                  range: [startValue, endValue],
                },
                // right calendar
                {
                  id: 'dst_calendar',
                  range: [startValue, endValue],
                }
              ],
            }
          )
        };


        // An internal function for formatting numbers
        let appendThousandSeparator = function (number) {
          return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        };

        // An internal function for formatting tooltip text in heatmap hovers
        let tooltipFormatterHeatmap = function (params) {
          let date = params.value[0];
          let profit = params.value[1] >= 0? 'profit': 'loss';
          let value = appendThousandSeparator(Math.abs(params.value[1]));
          return params.marker + date +
            '<br> Net ' + profit + ': ' + value;
        };

        // An internal function for formatting tooltip text in scatter plot hovers
        let tooltipFormatterScatter = function (params) {
          let date = params.value[0];
          let profit = params.value[1] >= 0? 'profit': 'loss';
          let value = appendThousandSeparator(Math.abs(params.value[1]));
          return params.marker + date +
            '<br> Net affiliated ' + profit + ': ' + value;
        };

        this.calendar.setOption({
          tooltip: {
            triggerOn: 'mousemove'
          },
          toolbox: {
            feature: {
              myQuarterPrevious: {
                show: true,
                title: 'Previous period',
                icon: 'image://keyboard_arrow_left-black-18dp.svg',
                onclick: function (params) { goToQuarter(params, -1) }
              },
              myQuarterNext: {
                show: true,
                title: 'Next period',
                icon: 'image://keyboard_arrow_right-black-18dp.svg',
                onclick: function (params) { goToQuarter(params, +1) }
              },
            }
          },
          calendar: [
            // left calendar
            {
              id: 'src_calendar',
              range: ['2014-01', '2014-03-31'],
              top: 50,
              bottom: '50%',
              left: '5%',
              right: '52.5%',
              itemStyle: { borderWidth: 0.5 },
              yearLabel: { margin: 7.5 },
              dayLabel: { show: false },
            },
            // right calendar
            {
              id: 'dst_calendar',
              range: ['2014-01', '2014-03-31'],
              top: 50,
              bottom: '50%',
              left: '52.5%',
              right: '5%',
              itemStyle: { borderWidth: 0.5 },
              yearLabel: { margin: 7.5 },
              dayLabel: { show: false },
            }
          ],
          visualMap: [
            // left calendar
            {
              id: 'src_vm_heatmap',
              seriesIndex: 0,
              type: 'continuous',
              orient: 'horizontal',
              bottom: '43%',
              left: 'left',
              calculable: true,
              padding: 10,
              itemWidth: 10,
              itemHeight: 200,
              text: ['Profit', 'Loss'],
              inRange: {
                color: ['#a6611a', '#dfc27d', '#f5f5f5', '#80cdc1', '#018571'],
              },
              formatter: (value) => {return appendThousandSeparator(~~(value/1000)) + 'k'},
            },
            {
              id: 'src_vm_scatter',
              seriesIndex: 1,
              type: 'continuous',
              orient: 'horizontal',
              bottom: '40%',
              left: '20%',
              padding: 10,
              itemWidth: 10,
              itemHeight: 250,
              text: ['Affiliated gain', 'Affiliated loss'],
              hoverLink: false,
              inRange: {
                color: ['#d7191c', '#fdae61', '#ffffbf', '#a6d96a', '#1a9641'],
              },
            },
            // right calendar
            {
              id: 'dst_vm_heatmap',
              seriesIndex: 2,
              type: 'continuous',
              orient: 'horizontal',
              bottom: '43%',
              right: 'right',
              calculable: true,
              padding: 10,
              itemWidth: 10,
              itemHeight: 200,
              text: ['Profit', 'Loss'],
              inRange: {
                color: ['#a6611a', '#dfc27d', '#f5f5f5', '#80cdc1', '#018571'],
              },
              formatter: (value) => {return appendThousandSeparator(~~(value/1000)) + 'k'},
            },
            {
              id: 'dst_vm_scatter',
              seriesIndex: 3,
              type: 'continuous',
              show: false,
              inRange: {
                color: ['#d7191c', '#fdae61', '#ffffbf', '#a6d96a', '#1a9641'],
              },
            },
          ],
          series: [
            // left calendar
            {
              id: 'src_series_heatmap',
              type: 'heatmap',
              coordinateSystem: 'calendar',
              datasetIndex: 0,
              calendarIndex: 0,
              dimensions: ['date', 'profit'],
              encode: {
                tooltip: [0, 1]
              },
              itemStyle: {
                opacity: 0.75
              },
              tooltip: {
                formatter: tooltipFormatterHeatmap
              }
            },
            {
              id: 'src_series_scatter',
              type: 'scatter',
              coordinateSystem: 'calendar',
              datasetIndex: 0,
              calendarIndex: 0,
              dimensions: ['date', 'ap_profit', 'rtp_profit'],
              encode: {
                tooltip: [0,1]
              },
              symbolOffset: [0, '-50%'],
              itemStyle: {
                borderColor: 'black',
                borderWidth: 1,
              },
              tooltip: {
                formatter: tooltipFormatterScatter
              }
            },
            // right calendar
            {
              id: 'dst_series_heatmap',
              type: 'heatmap',
              coordinateSystem: 'calendar',
              datasetIndex: 1,
              calendarIndex: 1,
              dimensions: ['date', 'profit'],
              encode: {
                tooltip: [0, 1]
              },
              itemStyle: {
                opacity: 0.75
              },
              tooltip: {
                formatter: tooltipFormatterHeatmap
              }
            },
            {
              id: 'dst_series_scatter',
              type: 'scatter',
              coordinateSystem: 'calendar',
              datasetIndex: 1,
              calendarIndex: 1,
              dimensions: ['date', 'ap_profit', 'rtp_profit'],
              encode: {
                tooltip: [0, 1]
              },
              symbolOffset: [0, '-50%'],
              itemStyle: {
                borderColor: 'black',
                borderWidth: 1,
              },
              tooltip: {
                formatter: tooltipFormatterScatter
              }
            },
          ]
        });
      },
      renderCalendar() {
        if (this.calendarData === undefined || this.calendarData.length === 0) return;
        let src_data = this.calendarData[0]['source'];
        let dst_data = this.calendarData[1]['source'];

        // date configuration
        let date_start  = src_data['date'][0];
        let date_end    = src_data['date'][src_data['date'].length-1];

        // min-max configuration for heatmap
        let heatmap_interval_src = (Math.max(...src_data['profit']) + Math.abs(Math.min(...src_data['profit']))) / 2;
        let heatmap_interval_dst = (Math.max(...dst_data['profit']) + Math.abs(Math.min(...dst_data['profit']))) / 2;
        // min-max configuration for scatter plots
        let scatter_max_src = Math.max.apply(null, src_data['ap_profit'].map(Math.abs));
        let scatter_max_dst = Math.max.apply(null, dst_data['ap_profit'].map(Math.abs));

        this.calendar.setOption({
          dataset: this.calendarData,
          calendar: [
            // left calendar
            {
              id: 'src_calendar',
              range: [date_start, date_end],
            },
            // right calendar
            {
              id: 'dst_calendar',
              range: [date_start, date_end],
            }
          ],
          visualMap: [
            // left calendar
            {
              id: 'src_vm_heatmap',
              min: -heatmap_interval_src,
              max: heatmap_interval_src,
            },
            {
              id: 'src_vm_scatter',
              min: -scatter_max_src,
              max: scatter_max_src,
            },
            // right calendar
            {
              id: 'dst_vm_heatmap',
              min: -heatmap_interval_dst,
              max: heatmap_interval_dst,
            },
            {
              id: 'dst_vm_scatter',
              min: -scatter_max_dst,
              max: scatter_max_dst,
            },
          ],
          series: [
            // left calendar
            {
              id: 'src_series_scatter',
              symbol: function (value) {
                return value[2]? 'diamond': 'circle';
              },
              symbolSize: function (value) {
                return value[1] && Math.abs(value[1]/scatter_max_src*15)+5;
              },
            },
            // right calendar
            {
              id: 'dst_series_scatter',
              symbol: function (value) {
                return value[2]? 'diamond': 'circle';
              },
              symbolSize: function (value) {
                return value[1] && Math.abs(value[1]/scatter_max_dst*15)+5;
              },
            },
          ]
        });
      },
    }
  }
</script>

<style scoped>
</style>