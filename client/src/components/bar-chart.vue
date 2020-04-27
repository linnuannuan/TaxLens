<template>
    <div id="num_bar"  class="num-bar"></div>
</template>

<script>
    import * as d3 from "d3";
    import EventService from "../utils/event-service";
    export default {
        name: "BarChart",
        props: {
            affiliatedPartyNumData: Object,
        },
        watch: {
            affiliatedPartyNumData: function () {
                this.renderGroupView();
            },
        },
        mounted: function () {
            this.initGroupView();
            this.renderGroupView();
        },
        methods: {
            handleView(id) {
                EventService.emitSuspiciousGroupSelected(id);
            },
            initGroupView() {
                // config the color scheme
                let width = this.$el.clientWidth;
                let height = this.$el.clientHeight;
                this.cfg = {
                    width:width,
                    height:height,
                    color: {
                        'node': '#d9d9d9',
                        'ap_node': '#1f78b4',
                        'evader': '#ff7f00'
                    }

                };
                this.svg = d3.select(this.$el).append('svg').attr("viewBox", [0, 0, width, height]);
            },
            renderGroupView() {
                this.svg.selectAll("g").remove();

                let data = this.affiliatedPartyNumData;
                // data['max_num_nodes'] = 34

                console.log('bar-chart-data:', this.affiliatedPartyNumData)


                /* draw each group with circle (size encode tax gap) and node_link graph represent inner ap_transaction */
                // draw node num
                // this.svg.append('g')
                //       .append('rect')
                //       .attr('x', 0)
                //       .attr('y', 0)
                //       .attr('width', data['num_nodes']/data['max_num_nodes']*this.cfg.width)
                //       .attr('height', this.cfg.height)
                //       .attr('fill', this.cfg.color.node)
                //       // .attr('fill-opacity', 0.5)
                //       .attr('stroke', this.cfg.color.node)
                //       .attr('stroke-width', 4)

                // draw ap_node num
                this.svg.append('g')
                      .append('rect')
                      .attr('x', 0)
                      .attr('y', 0)
                      .attr('width', data['num_ap_nodes']/data['max_num_nodes']*this.cfg.width)
                      .attr('height', this.cfg.height)
                      .attr('fill', this.cfg.color.ap_node)
                      // .attr('fill-opacity', 0.5)
                      // .attr('stroke', this.cfg.color.node)
                      // .attr('stroke-width', 2)

                // draw evader num
                this.svg.append('g')
                      .append('rect')
                      .attr('x', 0)
                      .attr('y', 0)
                      .attr('width', data['num_evader']/data['max_num_nodes']*this.cfg.width)
                      .attr('height', this.cfg.height)
                      .attr('fill', this.cfg.color.evader)
                      // .attr('fill-opacity', 0.5)
                      // .attr('stroke', this.cfg.color.node)
                      // .attr('stroke-width', 2)

            }
        }
    }
</script>

<style scoped>
.num-bar{
    width: 100px;
    height:30px
}
</style>