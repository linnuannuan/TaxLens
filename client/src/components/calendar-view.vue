<template>
    <div class="view">
        <div class="calendar" id="calendar_view"></div>
<!--        <div class="detail" id="detail_view"></div>-->
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
      }
    },
    mounted: function () {
      this.initCalendar();
      // this.initDetail();
      this.renderCalendar();
    },
    methods: {
      initCalendar() {
        this.calendar = echarts.init(document.getElementById('calendar_view'));
        this.calendar.showLinks = true;
        this.calendar.nodes = [{name: 'top_left', x: 0, y: 0}, {name: 'bottom_right', x: 1200, y: 450}];
        this.calendar.showLoading(this.loadingCalendar);

        // let colorEncoding = [
        //   '#8c510a','#bf812d','#dfc27d','#f6e8c3',
        //   '#f5f5f5',
        //   '#c7eae5','#80cdc1','#35978f','#01665e'];
        let colorEncoding = ['#d73027','#f46d43','#fdae61','#fee08b','#ffffbf','#d9ef8b','#a6d96a','#66bd63','#1a9850'];
        let colorLoss = colorEncoding[0];
        let colorProfit = colorEncoding[colorEncoding.length-1];

        // An internal function for toolbox item handling periods operation
        let periodOperation = function (params, offset) {
          let originalStart = params.option.calendar[0].range[0];
          let quarterRange = DateService.parseDateToRange(originalStart, offset);
          EventService.emitAffiliatedTransactionSelected(null, null, quarterRange[0], quarterRange[1]);
        };

        // An internal function for toggling node-link visualization
        // Notice that the node link information is stored in the instance
        let toggleLinks = function (params) {
          params.scheduler.ecInstance.showLinks = !params.scheduler.ecInstance.showLinks;
          params.scheduler.ecInstance.setOption({
            series: {
              id: 'graph',
              nodes: params.scheduler.ecInstance.showLinks? params.scheduler.ecInstance.nodes: [],
              links: params.scheduler.ecInstance.showLinks? params.scheduler.ecInstance.links: [],
            }
          });
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
              myToggleLinks: {
                show: true,
                title: 'Toggle links',
                icon: 'image://calendar_view_day-black-18dp.svg',
                onclick: toggleLinks
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
              top: 60,
              bottom: '40',
              left: '40',
              right: '620',
              itemStyle: {borderWidth: 0.5},
              yearLabel: {margin: 7.5},
              dayLabel: {show: false},
            },
            // right calendar
            {
              id: 'dst_calendar',
              range: ['2014-01', '2014-03-31'],
              top: 60,
              bottom: '40',
              left: '620',
              right: '40',
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
              top: 'top',
              left: 'center',
              calculable: true,
              padding: 10,
              itemWidth: 10,
              itemHeight: 500,
              text: ['Profit', 'Loss'],
              inRange: { color: colorEncoding },
              formatter: (value) => {
                return appendThousandSeparator(~~(value / 1000)) + 'k'
              },
            },
            // right calendar
            {
              id: 'dst_vm_heatmap',
              seriesIndex: 2,
              type: 'continuous',
              show: false,
              inRange: { color: colorEncoding },
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
              encode: { tooltip: [0, 1] },
              itemStyle: { opacity: 0.8 },
              tooltip: { formatter: tooltipFormatterHeatmap }
            },
            {
              id: 'src_series_scatter',
              type: 'scatter',
              coordinateSystem: 'calendar',
              datasetIndex: 0,
              calendarIndex: 0,
              dimensions: ['date', 'ap_profit', 'rtp_profit'],
              encode: { tooltip: [0, 1] },
              // symbolOffset: [0, '-50%'],
              itemStyle: {
                color: function (data) {
                  return data.value[1] < 0? colorLoss: colorProfit;
                },
                opacity: 1,
                borderColor: 'white',
                borderWidth: 2,
              },
              tooltip: { formatter: tooltipFormatterScatter },
              z: 15
            },
            // right calendar
            {
              id: 'dst_series_heatmap',
              type: 'heatmap',
              coordinateSystem: 'calendar',
              datasetIndex: 1,
              calendarIndex: 1,
              dimensions: ['date', 'profit'],
              encode: { tooltip: [0, 1] },
              itemStyle: { opacity: 0.8 },
              tooltip: { formatter: tooltipFormatterHeatmap }
            },
            {
              id: 'dst_series_scatter',
              type: 'scatter',
              coordinateSystem: 'calendar',
              datasetIndex: 1,
              calendarIndex: 1,
              dimensions: ['date', 'ap_profit', 'rtp_profit'],
              encode: { tooltip: [0, 1] },
              // symbolOffset: [0, '-50%'],
              itemStyle: {
                color: function (data) {
                  return data.value[1] < 0? colorLoss: colorProfit;
                },
                opacity: 1,
                borderColor: 'white',
                borderWidth: 2,
              },
              tooltip: { formatter: tooltipFormatterScatter },
              z: 15
            },
            // graph
            {
              id: 'graph',
              nodes: this.nodes,
              links: this.links,
              type: 'graph',
              tooltip: { show: false },
              hoverAnimation: false,
              // symbolOffset: [0, '-50%'],
              lineStyle: {
                color: '#d6604d',
                width: 2,
                opacity: 1
              },
              width: '1200',
              height: '450',
              z: 10
            },
          ],
        });

        // this.calendar.on('click', function(event){
        //   // allow only heatmap and scatter to react
        //   event.seriesIndex < 4 && this.renderDetail(~~(event.seriesIndex/2), event.dataIndex);
        // }, this);
      },
      renderCalendar() {
        if (this.calendarData === undefined || this.calendarData.length === 0) return;
        this.calendar.showLoading(this.loadingCalendar);

        // date configuration
        let src_data = this.calendarData[0]['source'];
        let dst_data = this.calendarData[1]['source'];
        let date_start = src_data['date'][0];
        let date_end = src_data['date'][src_data['date'].length - 1];

        // min-max configuration for heatmap
        let src_profit_abs = src_data['profit'].map(Math.abs);
        let dst_profit_abs = dst_data['profit'].map(Math.abs);
        let profitMedian = [...src_profit_abs, ...dst_profit_abs].sort((a,b) => a-b);
        profitMedian = profitMedian.length !== 0 && profitMedian[~~(profitMedian.length*0.5)];
        let profitSmallerMax = Math.min(Math.max(...src_profit_abs), Math.max(...dst_profit_abs));
        let profitInterval = Math.max(profitMedian, profitSmallerMax);

        let maxProfitAP = Math.max(...src_data['ap_profit'].map(Math.abs),...dst_data['ap_profit'].map(Math.abs));

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
              min: -profitInterval,
              max: profitInterval,
            },
            // right calendar
            {
              id: 'dst_vm_heatmap',
              min: -profitInterval,
              max: profitInterval,
            },
          ],
          series: [
            // left calendar
            {
              id: 'src_series_scatter',
              symbol: function () {
                return 'circle';
              },
              symbolSize: function (value) {
                return value[1] && Math.abs(value[1] / maxProfitAP * 30) + 10;
              },
            },
            // right calendar
            {
              id: 'dst_series_scatter',
              symbol: function () {
                return 'circle';
              },
              symbolSize: function (value) {
                return value[1] && Math.abs(value[1] / maxProfitAP * 30) + 10;
              },
            }
          ]
        });

        this.processGraph(maxProfitAP);
        this.calendar.setOption({
          series: {
            id: 'graph',
            nodes: this.calendar.showLinks? this.calendar.nodes: [],
            links: this.calendar.showLinks? this.calendar.links: [],
          }
        });

        this.calendar.hideLoading(this.loadingCalendar);
      },
      processGraph(maxValue) {
        // Notice that the node link information is stored in the instance
        this.calendar.nodes = [
          {name: 'top_left', x: 0, y: 0, symbolSize: 0},
          {name: 'bottom_right', x: 1200, y: 450, symbolSize: 0}
        ];
        this.calendar.links = [];

        let data = this.calendarData[0].source;
        data['date'].forEach((d, i) => {
          // filter the dates where rtp is involved
          if (!data['rtp_revenue'][i] && !data['rtp_expense'][i]) return;

          let loc, size;
          // obtain the node coordinates in both calendars
          loc = this.calendar.convertToPixel({calendarIndex: 0}, d);
          size = Math.abs(data['ap_profit'][i] / maxValue * 30) + 10;
          this.calendar.nodes.push({name: 'src_'+d, x: loc[0], y: loc[1], symbolSize: size});
          loc = this.calendar.convertToPixel({calendarIndex: 1}, d);
          this.calendar.nodes.push({name: 'dst_'+d, x: loc[0], y: loc[1], symbolSize: size});

          // configure the edge symbols
          this.calendar.links.push({
            source: 'src_'+d,
            target: 'dst_'+d,
            symbol: [
              data['rtp_revenue'][i]?'arrow': 'none',
              data['rtp_expense'][i]?'arrow': 'none'
            ],
            lineStyle: {
              curveness: data['rtp_expense'][i]? 0.2: -0.2
            }
          });
        });
      },
      initDetail() {
        this.detail = echarts.init(document.getElementById('detail_view'));

        this.detail.setOption({
          grid: {},
          xAxis: {
            show: false,
            type: 'category',
            gridIndex: 0,
            axisTick: { alignWithLabel: true },
            axisLabel: { interval: 0 }
          },
          yAxis: { show: false, gridIndex: 0 },
          legend: {},
          series: {
            type:'bar',
            seriesLayoutBy: 'row',
            label: { show: true }
          },
        })
      },
      renderDetail(sourceIndex, dataIndex) {
        const source = this.calendarData[sourceIndex].source;
        const detailDimensions = ['profit', 'revenue', 'expense', 'ap_profit', 'ap_revenue', 'ap_expense', 'rtp_profit', 'rtp_revenue', 'rtp_expense'];
        let detailData = [detailDimensions, []];
        detailDimensions.forEach(d=>detailData[1].push(source[d][dataIndex]));
        this.detail.setOption({
          dataset: { source: detailData },
          xAxis: { show: true },
          yAxis: { show: true }
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
        height: 100%;
        /*border: 1px solid steelblue;*/
    }

    .detail{
        width: 100%;
        height: 40%;
        /*border: 1px solid forestgreen;*/
    }
</style>