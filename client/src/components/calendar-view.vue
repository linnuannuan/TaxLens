/* eslint-disable */
<template>
    <div id="calendar_view"></div>
</template>

<script>
    import * as d3 from "d3";
    import * as echarts from "echarts";
    // import EventService from "../utils/event-service";

    export default {
          name: 'CalendarView',
          props: {
              calendarData: Object,
              loadingCalendar: Boolean,
          },
          data() {
              return {
                  svg: null,
              }
          },
          watch: {
              calendarData: function () {
                  this.renderGraph();
              },
          },
          mounted: function () {
              this.initGraph();
          },
          methods: {
              initGraph() {
                  let width = this.$el.clientWidth;
                  let height = this.$el.clientHeight;
                  // let margin_width = width / 30;
                  // let margin_height = height / 20;

                  //config the node width and link width
                  this.cfg = {
                      width: width,
                      height: height
                  };
                  this.svg = d3.select('#calendar_view')
                      .append("svg")
                      .attr("viewBox", [0, 0, width, height])
                      .style("font", "12px sans-serif");
              },
              renderGraph() {
                  // 生成模拟数据
                  console.log('origin_data:', this.calendarData)
                  // let src_data = this.calendarData[0]
                  // let dst_data = this.calendarData[0]
                  // src_data = src_data.date.map((key,value)=>[key, src_data.cumulative_profit[value], src_data.cumulative_profit[value]]);


                  drawCalendar(this.calendarData,document.getElementById('calendar_view'))
                  // data: calendar data
                  // element document.getElementById('calendar_view')

                  function drawCalendar(origin_data, element) {
                        const cyear =2014
                        let src_dataset = [origin_data[0].columns].concat(origin_data[0].data)
                        let dst_dataset = [origin_data[1].columns].concat(origin_data[1].data)
                        let dataset = src_dataset.slice(1,).concat(dst_dataset.slice(1,)).map(d=>{
                            return [d[0],d[7],(d[5]-d[6])]
                        })

                         // origin dataset =
                         // {
                         // 'date': ['2014-01-01', '2014-01-02', '2014-01-03', '2014-01-04'],
                         // 'revenue': [0, 0, 0, 0],
                         // 'expense': [0, 0, 0, 0],
                         // 'ap_revenue': [0, 0, 0, 0],
                         // 'ap_expense': [0, 0, 0, 0],
                         // 'rtp_revenue': [0, 0, 0, 0],
                         // 'rtp_expense': [0, 0, 0, 0],
                         // 'cumulative_profit': [0, 0, 0, 0]}
                        //         7,               5-6                  3-4
                        // "Date", "Profit", "Normal Transaction", "Ap Transaction

                        console.log(src_dataset,dst_dataset)

                        var option = {
                            dataset:{
                                source: dataset,
                            },
                            tooltip: {
                                position: 'top',
                            },
                            // //"Date", "Profit", "Normal Transaction", "Ap Transaction
                            // set the visual map of profit
                            visualMap: [
                            // encode the normal transaction
                            {
                                min: -Math.max(...dataset.map(d=>Math.abs(d[2]))),
                                max: Math.max(...dataset.map(d=>Math.abs(d[2]))),
                                calculable: true,
                                orient: 'horizontal',
                                left: 'center',
                                top: 'top',
                                dimension:2,
                                inRange: {
                                    // color: ['green','white','red'],
                                    // opacity: [0.5,0.5],
                                    symbolSize:[15,0,15]
                                },
                                seriesIndex:[1,3],
                                show:false
                            },
                            // encode the ap_transaction
                            {
                                min: -Math.max(...dataset.map(d=>Math.abs(d[3]))),
                                max: Math.max(...dataset.map(d=>Math.abs(d[3]))),
                                calculable: true,
                                orient: 'horizontal',
                                left: 'right',
                                top: 'top',
                                inRange: {
                                    // color: ['green','white','red'],
                                    // opacity: [0.5,0.5],
                                    symbolSize:[15,0,15]
                                },
                                dimension:2,
                                seriesIndex:[2,5],
                                show:false
                            },
                            // set the color visual map of profit and normal transaction based on profit
                            {
                                min: Math.min(...dataset.map(d=>d[2])),
                                max: Math.max(...dataset.map(d=>d[2])),
                                calculable: true,
                                orient: 'horizontal',
                                left: 'right',
                                top: 'top',
                                inRange: {
                                    color: ['green','white','red'],
                                    opacity: [0.5,0.5],
                                },
                                controller: {
                                    inRange: {
                                        opacity: [0.5, 0.5]
                                    },
                                    outOfRange: {
                                        color: '#ccc'
                                    }
                                },
                                dimension :1,
                                seriesIndex:[0,1,3,4]
                            }],
                            legend: {
                                top: '10',
                                left: '70',
                                data: ['Normal Transaction','Ap Transaction'],
                                textStyle: {
                                    // color: '#fff'
                                }
                            },

                            calendar: [
                            {
                                range: [cyear+'-01-01', cyear+'-03-30']
                            },
                            {
                                right: 25,
                                range: [cyear+'-01-01', cyear+'-03-30']
                            }],

                            series: [
                            {
                                type: 'heatmap',
                                coordinateSystem: 'calendar',
                                calendarIndex: 0,
                                data: src_dataset,
                                tooltip: {
                                        formatter: function (param) {
                                            return [
                                                'Date: ' + param.data[0] + '<hr size=1 style="margin: 3px 0">',
                                                'Profit: ' + param.data[1].toFixed(2) + '<br/>',
                                                'Normal Transaction: ' + param.data[2].toFixed(2) + '<br/>',
                                                'Ap Transaction: ' + param.data[3].toFixed(2) + '<br/>',
                                            ].join('');
                                        }
                                }
                            },
                            {
                                name: 'Normal Transaction',
                                type: 'scatter',
                                coordinateSystem: 'calendar',
                                data: src_dataset,
                                hoverAnimation: true,
                                // symbolSize: function (val) {
                                //     return Math.abs(val[2] / 80);
                                // },
                                itemStyle: {
                                    color: '#ddb926',
                                    // color:"yellow"
                                }
                            },
                            {
                                name: 'Ap Transaction',
                                type: 'effectScatter',
                                coordinateSystem: 'calendar',
                                data: src_dataset.filter(d=>d[3]),
                                // symbolSize: function (val) {
                                //     return Math.abs(val[3] / 80);
                                // },
                                showEffectOn: 'render',
                                rippleEffect: {
                                    brushType: 'stroke'
                                },
                                hoverAnimation: true,
                                itemStyle: {
                                    color: '#f4e925',
                                    shadowBlur: 10,
                                    shadowColor: '#333'
                                },
                                zlevel: 1
                            },
                            {
                                type: 'heatmap',
                                coordinateSystem: 'calendar',
                                calendarIndex: 1,
                                data: dst_dataset,
                                tooltip: {
                                        formatter: function (param) {
                                            return [
                                                'Date: ' + param.data[0] + '<hr size=1 style="margin: 3px 0">',
                                                'Profit: ' + param.data[1] + '<br/>',
                                                'Normal Transaction: ' + param.data[2] + '<br/>',
                                                'Ap Transaction: ' + param.data[3] + '<br/>',
                                            ].join('');
                                        }
                                },
                                seriesIndex:1
                            },
                            {
                                name: 'Normal Transaction',
                                type: 'scatter',
                                calendarIndex: 1,
                                coordinateSystem: 'calendar',
                                data: dst_dataset,
                                // symbolSize: function (val) {
                                //     return Math.abs(val[2] / 80);
                                // },
                                itemStyle: {
                                    color: '#ddb926',
                                    // color:"yellow"
                                }
                            },
                            {
                                name: 'Ap Transaction',
                                type: 'effectScatter',
                                calendarIndex: 1,
                                coordinateSystem: 'calendar',
                                data: src_dataset.filter(d=>d[3]),
                                // symbolSize: function (val) {
                                //     return Math.abs(val[3] / 80);
                                // },
                                showEffectOn: 'render',
                                rippleEffect: {
                                    brushType: 'stroke'
                                },
                                hoverAnimation: true,
                                itemStyle: {
                                    color: '#f4e925',
                                    shadowBlur: 10,
                                    shadowColor: 'red'
                                },
                                zlevel: 1
                            }]
                        };

                      var calendar_chart =  echarts.init(element);
                      calendar_chart.setOption(option)
                 }
              },
              renderD3Graph() {
                    // draw calendar view
                    let calendar_svg = this.svg.append('g').classed('calendar_panel',!0)


                    let formatMonth = d3.utcFormat("%b")
                    let formatDay = d => "SMTWTFS"[d.getUTCDay()]
                    let formatDate = d3.utcFormat("%x")
                    let formatClose = d3.format("$,.2f")
                    let formatValue = d3.format(".2%")

                    function pathMonth(t) {
                      const n = 7;
                      const d = Math.max(0, Math.min(n, countDay(t)));
                      const w = timeWeek.count(d3.utcYear(t), t);
                      return `${d === 0 ? `M${w * cellSize},0`
                          : d === n ? `M${(w + 1) * cellSize},0`
                          : `M${(w + 1) * cellSize},0V${d * cellSize}H${w * cellSize}`}V${n * cellSize}`;
                    }

                    let countDay =  d => d.getUTCDay()
                    let timeWeek = d3.utcSunday
                    // let width = this.cfg.calendar_panel.max_width - this.cfg.calendar_panel.min_width
                    let cellSize = 17
                    let height = cellSize * 9
                    //  record the offset Z
                    let calendar_width = cellSize * 8
                    let t_links = this.affiliatedPartyDetail.links.filter(d=>d.ap_txn)
                    let t_nodes = this.affiliatedPartyDetail.nodes.filter(d=>d.tp)
                    t_links
                        .sort((a,b)=>t_nodes.find(node=>node.id==a.source).x_index - t_nodes.find(node=>node.id==b.target).x_index)
                        .forEach(
                        (d,index) =>{
                            // 对每一笔关联交易 都画出交易双方的calendar chart
                            // 垂直排列日历图
                            // source 排第一层 y: this.cfg.calendar_panel.min_height
                            // target 排第二层 y: this.cfg.min_height +
                            let cur_svg = calendar_svg.append('g')
                                        // .classed('calendar',!0)
                                        .attr('id','calendar-'+d.source+'-'+d.target)

                            let offset_x = this.cfg.calendar_panel.min_width + calendar_width * index
                            let source_offset_y = this.cfg.calendar_panel.min_height
                            let target_offset_y = this.cfg.calendar_panel.min_height + height
                            get_calendar_view(cur_svg.append('g'), offset_x, source_offset_y)
                            get_calendar_view(cur_svg.append('g'), offset_x, target_offset_y)

                        }
                    )

                    function get_calendar_view(cur_svg, offset_x, offset_y){
                        let calendar_data = []
                        for(let i = 1 ; i < 31 ; i++){
                            calendar_data.push({
                                date: new Date(2020,0,i+1),
                                value: Math.random()*100,
                                ap_txn:Math.random()>0.8?true:false,
                                ap_txn_amount: Math.random()*10
                            })
                        }
                        let years = [[2020,calendar_data]]

                        // 创建颜色映射器
                        let color = d3.scaleSequential([d3.min(calendar_data.map(d=>d.value)), d3.max(calendar_data.map(d=>d.value))], d3.interpolateBlues)

                        const year = cur_svg.selectAll("g")
                            .data(years)
                            .join("g")
                              // .attr("transform", (d, i) => `translate(40,${height * i + cellSize * 1.5})`);

                        year.append("text")
                              .attr("x", offset_x - 5)
                              .attr("y", offset_y - 5)
                              .attr("font-weight", "bold")
                              .attr("text-anchor", "end")
                              .text(([key]) => key);

                        year.append("g")
                              .attr("text-anchor", "end")
                            .selectAll("text")
                            .data((d3.range(7)).map(i => new Date(1995, 0, i)))
                            .join("text")
                              .attr("x", offset_x - 5)
                              .attr("y", d => offset_y + (countDay(d) + 0.5) * cellSize )
                              .attr("dy", "0.31em")
                              .text(formatDay);

                        year.append("g")
                            .selectAll("rect")
                            .data(([, values]) => values)
                            .join("rect")
                              .attr("width", cellSize - 1)
                              .attr("height", cellSize - 1)
                              .attr("x", d => offset_x + timeWeek.count(d3.utcYear(d.date), d.date) * cellSize + 0.5)
                              .attr("y", d => offset_y + countDay(d.date) * cellSize + 0.5)
                              .attr("fill", d => color(d.value))
                              .attr("stroke",d=> d.ap_txn? 'yellow' : "currentColor")
                            .append("title")
                              .text(d => `  ${formatDate(d.date)}
                                            ${formatValue(d.value)}${d.close === undefined ? "" : `
                                            ${formatClose(d.close)}`}`);

                        const month = year.append("g")
                                            .selectAll("g")
                                            .data(([, values]) =>d3.utcMonths(d3.utcMonth(values[0].date), values[values.length - 1].date))
                                            .join("g");

                        month.filter((d, i) => i).append("path")
                              .attr("fill", "none")
                              .attr("stroke", "#fff")
                              .attr("stroke-width", 3)
                              .attr("d", pathMonth);

                        month.append("text")
                              .attr("x", d => offset_x + timeWeek.count(d3.utcYear(d), timeWeek.ceil(d)) * cellSize + 2)
                              .attr("y", offset_y -5)
                              .text(formatMonth);
                    }
              }
          }
  }
</script>

<style scoped>
    .calendar{
        width: 100%;
        height: 300px;
    }
    #calendar_view{
        padding-top: 50px;
    }

</style>