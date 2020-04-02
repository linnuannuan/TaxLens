<template>
    <div id="temporal_view"></div>
</template>

<script>
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
        computed: {

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
                // draw time slider for transaction of 2014-2015
            },
            renderTimeSlider() {
                // render time slider

                var date = this.affiliatedPartyTimeList.date
                var data = this.affiliatedPartyTimeList.ap_txn_amount

                console.log('affiliatedPartyTimeList',this.affiliatedPartyTimeList)

                let option = {
                    tooltip: {
                        trigger: 'axis',
                        position: function (pt) {
                            return [pt[0], '10%'];
                        }
                    },
                    // title: {
                    //     left: 'center',
                    //     text: '关联交易流量图',
                    // },
                    // toolbox: {
                    //     feature: {
                    //         dataZoom: {
                    //             yAxisIndex: 'none'
                    //         },
                    //         restore: {},
                    //         saveAsImage: {}
                    //     }
                    // },
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        data: date
                    },
                    yAxis: {
                        type: 'value',
                        boundaryGap: [0, '100%']
                    },
                    dataZoom: [{
                        type: 'inside',
                        start: 0,
                        end: 10
                    }, {
                        start: 0,
                        end: 10,
                        handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                        handleSize: '80%',
                        handleStyle: {
                            color: '#fff',
                            shadowBlur: 3,
                            shadowColor: 'rgba(0, 0, 0, 0.6)',
                            shadowOffsetX: 2,
                            shadowOffsetY: 2
                        }
                    }],
                    series: [
                        {
                            name: 'cuurent data',
                            type: 'line',
                            smooth: true,
                            symbol: 'none',
                            sampling: 'average',
                            itemStyle: {
                                color: 'rgb(255, 70, 131)'
                            },
                            areaStyle: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                    offset: 0,
                                    color: 'rgb(255, 158, 68)'
                                }, {
                                    offset: 1,
                                    color: 'rgb(255, 70, 131)'
                                }])
                            },
                            data: data
                        }
                    ]
                };
                var myChart = echarts.init(document.getElementById('temporal_view'));
                myChart.setOption(option);

            }
        }
    }
</script>

<style scoped>

</style>