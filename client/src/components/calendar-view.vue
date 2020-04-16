<template>
    <div class="view">
        <div class="calendar" id="calendar_view"></div>
        <div class="detail" id="detail_view"></div>
    </div>
</template>

<script>
  import * as echarts from "echarts";
  import DateService from "../utils/date-service";
  import EventService from "../utils/event-service";

  export default {
    name: 'CalendarView',
    props: {
      calendarData: Array,
      calendarSourceId: String,
      calendarTargetId: String,
      loadingCalendar: Boolean,
    },
    data() {
      return {
        // the DOM element
        calendar: null,
        detail: null,
      }
    },
    watch: {
      calendarData: function () {
        this.renderCalendar();
      },
    },
    mounted: function () {
      this.initCalendar();
      this.initDetail();
      this.renderCalendar();
    },
    methods: {
      initCalendar() {
        this.calendar = echarts.init(document.getElementById('calendar_view'));
        this.calendar.showLoading(this.loadingCalendar);

        // An internal function for toolbox item handling periods operation
        let periodOperation = function (params, offset) {
          let originalStart = params.option.calendar[0].range[0];
          let quarterRange = DateService.parseDateToRange(originalStart, offset);
          // params.scheduler.ecInstance.setOption()
          EventService.emitAffiliatedTransactionSelected(null, null, quarterRange[0], quarterRange[1]);
        };

        // An internal function for formatting numbers
        let appendThousandSeparator = function (number) {
          return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        };

        // An internal function for formatting tooltip text in heatmap hovers
        let tooltipFormatterHeatmap = function (params) {
          let date = params.value[0];
          let profit = params.value[1] >= 0 ? 'profit' : 'loss';
          let value = appendThousandSeparator(Math.abs(params.value[1]));
          return params.marker + date +
            '<br> Net ' + profit + ': ' + value;
        };

        // An internal function for formatting tooltip text in scatter plot hovers
        let tooltipFormatterScatter = function (params) {
          let date = params.value[0];
          let profit = params.value[1] >= 0 ? 'profit' : 'loss';
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
                onclick: function (params) {
                  periodOperation(params, -1)
                }
              },
              myCalendarSwitch: {
                show: true,
                title: 'Switch to year view',
                icon: 'image://date_range-black-18dp.svg',
                onclick: function (params) {
                  DateService.toggleQuarterMode();
                  periodOperation(params);
                }
              },
              myQuarterNext: {
                show: true,
                title: 'Next period',
                icon: 'image://keyboard_arrow_right-black-18dp.svg',
                onclick: function (params) {
                  periodOperation(params, +1)
                }
              },
            }
          },
          calendar: [
            // left calendar
            {
              id: 'src_calendar',
              range: ['2014-01', '2014-03-31'],
              top: 50,
              bottom: '60',
              left: '5%',
              right: '52.5%',
              itemStyle: {borderWidth: 0.5},
              yearLabel: {margin: 7.5},
              dayLabel: {show: false},
            },
            // right calendar
            {
              id: 'dst_calendar',
              range: ['2014-01', '2014-03-31'],
              top: 50,
              bottom: '60',
              left: '52.5%',
              right: '5%',
              itemStyle: {borderWidth: 0.5},
              yearLabel: {margin: 7.5},
              dayLabel: {show: false},
            }
          ],
          visualMap: [
            // left calendar
            {
              id: 'src_vm_heatmap',
              seriesIndex: 0,
              type: 'continuous',
              orient: 'horizontal',
              bottom: '20',
              left: 'left',
              calculable: true,
              padding: 10,
              itemWidth: 10,
              itemHeight: 200,
              text: ['Profit', 'Loss'],
              inRange: {
                color: ['#a6611a', '#dfc27d', '#f5f5f5', '#80cdc1', '#018571'],
              },
              formatter: (value) => {
                return appendThousandSeparator(~~(value / 1000)) + 'k'
              },
            },
            {
              id: 'src_vm_scatter',
              seriesIndex: 1,
              type: 'continuous',
              orient: 'horizontal',
              bottom: 'bottom',
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
              bottom: '20',
              right: 'right',
              calculable: true,
              padding: 10,
              itemWidth: 10,
              itemHeight: 200,
              text: ['Profit', 'Loss'],
              inRange: {
                color: ['#a6611a', '#dfc27d', '#f5f5f5', '#80cdc1', '#018571'],
              },
              formatter: (value) => {
                return appendThousandSeparator(~~(value / 1000)) + 'k'
              },
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

        this.calendar.on('click', function(event){
          this.renderDetail(~~(event.seriesIndex/2), event.dataIndex);
        }, this);
      },
      renderCalendar() {
        if (this.calendarData === undefined || this.calendarData.length === 0) return;
        this.calendar.showLoading(this.loadingCalendar);
        let src_data = this.calendarData[0]['source'];
        let dst_data = this.calendarData[1]['source'];

        // date configuration
        let date_start = src_data['date'][0];
        let date_end = src_data['date'][src_data['date'].length - 1];

        // min-max configuration for heatmap
        let heatmap_interval_src = (Math.max(...src_data['profit']) + Math.abs(Math.min(...src_data['profit'], 0))) / 2;
        let heatmap_interval_dst = (Math.max(...dst_data['profit']) + Math.abs(Math.min(...dst_data['profit'], 0))) / 2;
        // min-max configuration for scatter plots
        let scatter_max_src = Math.max.apply(null, src_data['ap_profit'].map(Math.abs));
        let scatter_max_dst = Math.max.apply(null, dst_data['ap_profit'].map(Math.abs));

        this.calendar.setOption({
          dataset: this.calendarData,
          title: [
            {left: '100', text: this.calendarSourceId},
            {right: '100', text: this.calendarTargetId},
          ],
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
                return value[2] ? 'diamond' : 'circle';
              },
              symbolSize: function (value) {
                return value[1] && Math.abs(value[1] / scatter_max_src * 15) + 5;
              },
            },
            // right calendar
            {
              id: 'dst_series_scatter',
              symbol: function (value) {
                return value[2] ? 'diamond' : 'circle';
              },
              symbolSize: function (value) {
                return value[1] && Math.abs(value[1] / scatter_max_dst * 15) + 5;
              },
            },
          ]
        });
        this.calendar.hideLoading(this.loadingCalendar);
      },
      initDetail() {
        this.detail = echarts.init(document.getElementById('detail_view'));

        this.detail.setOption({
          grid: {},
          xAxis: {
            type: 'category',
            gridIndex: 0,
            axisTick: { alignWithLabel: true },
            axisLabel: {
              interval: 0,
            }
          },
          yAxis: {gridIndex: 0},
          legend: {},
          series: {
            type:'bar',
            seriesLayoutBy: 'row',
            label: {show:true}
          },
        })
      },
      renderDetail(sourceIndex, dataIndex) {
        const source = this.calendarData[sourceIndex].source;
        const detailDimensions = ['profit', 'revenue', 'expense', 'ap_profit', 'ap_revenue', 'ap_expense', 'rtp_profit', 'rtp_revenue', 'rtp_expense'];
        let detailData = [detailDimensions, []];
        detailDimensions.forEach(d=>detailData[1].push(source[d][dataIndex]));
        this.detail.setOption({
          dataset: { source: detailData }
        })
      }
    }
  }
</script>

<style scoped>
    .view{
        width: 100%;
        height: 100%;
    }

    .calendar{
        width: 100%;
        height: 60%;
        /*border: 1px solid steelblue;*/
    }

    .detail{
        width: 100%;
        height: 40%;
        /*border: 1px solid forestgreen;*/
    }
</style>