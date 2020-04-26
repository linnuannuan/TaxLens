<template>
    <div id="amount_bar"  class="amount-bar"></div>
</template>

<script>
    import * as d3 from "d3";
    import EventService from "../utils/event-service";
    export default {
        name: "AmountBarChart",
        props: {
            affiliatedPartyAmountData: Object,
        },
        watch: {
            affiliatedAmountData: function () {
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
                        'affiliated_amount': '#a6cee3',
                        'affiliated_num':'#1f78b4'
                    }

                };
                this.svg = d3.select(this.$el).append('svg').attr("viewBox", [0, 0, width, height]);
            },
            renderGroupView() {
                this.svg.selectAll("g").remove();

                let data = this.affiliatedPartyAmountData;

                console.log('_amount data:', data)


                /* draw each group with circle (size encode tax gap) and node_link graph represent inner ap_transaction */
                // draw ap_amount
                this.svg.append('g')
                      .append('rect')
                      .attr('x', 0)
                      .attr('y', 0)
                      .attr('width', data['ap_txn_amount']/data['max_amount']*this.cfg.width)
                      .attr('height', this.cfg.height)
                      .attr('fill', this.cfg.color.affiliated_amount)
                      .attr('stroke', this.cfg.color.node)
                      .attr('stroke-width', 4)

            }
        }
    }
</script>

<style scoped>
.amount-bar{
    width: 80px;
    height:30px
}
</style>