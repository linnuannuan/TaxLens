<template>
    <div id="group_view"  class="group-glyph"></div>
</template>

<script>
  import * as d3 from "d3";
  import EventService from "../utils/event-service";

  export default {
    name: "GroupGlyph",
    props:{
      affiliatedPartyTopoData: Object,
      // maxProfit:String,
    },
    data: function () {
      return {
        svg: null,
        test: false,
      }
    },
    watch: {
      affiliatedPartyTopoData: function() {
        this.renderGroupView();
      },
    },
    mounted:function(){
      this.initGroupView();
      this.renderGroupView();
    },
    methods: {
      handleView(id) {
        EventService.emitSuspiciousGroupSelected(id);
      },
      initGroupView(){
        // init the overview of group
        let width = this.$el.clientWidth;
        let height = this.$el.clientHeight;
        this.cfg = {
          'width':width,
          'height':height,
          'node':{
            'group':{
              min_r: height/4,
              max_r: height/2,
              color:'skyblue',
              margin:{
                left:0,
                top:0
              }
            },
            'individual':{
              min_r: 3,
              max_r: 6,
              color:'#1F497D'
            }
          },
          'link':{
            min_width: 1,
            max_width: 3,
            color:'#1f77b4'
          },
          'row_num':10,
          'col_num':5,
          'row_margin':0.5,
          'col_margin':1,
        };
        this.svg = d3.select(this.$el).append('svg').attr("viewBox", [0, 0, width, height]);
        // this.svg = d3.select('#group_view')
        //   .append("svg")
        //   .attr("viewBox", [0, 0, width, height]);
        // console.log(this.svg)
      },
      renderGroupView() {
          this.svg.selectAll("g").remove();

          let data = this.affiliatedPartyTopoData;

          console.log('group-glyph-data:', this.affiliatedPartyTopoData)


          /* draw each group with circle (size encode tax gap) and node_link graph represent inner ap_transaction */
          // draw group circle
          // this.svg.append('g')
          //     .append('rect')
          //     .attr('x', this.cfg.node.group.margin.left)
          //     .attr('y', this.cfg.node.group.margin.top)
          //     .attr('width', data['ap_txn_amount'] / data['max_amount'])
          //     // .attr('width',d=>groupRScaler(d['profit']))
          //     .attr('height', this.cfg.height)
          //     .attr('fill', this.cfg.node.group.color)
          //     .attr('fill-opacity', 0.5)
          //     .attr('stroke', this.cfg.node.group.color)
          //     .attr('stroke-width', 2)
          //     .on('click', d => this.handleView(d.ap_id));

          let group_content_svg = this.svg.append('g')
              .classed('group_content', !0);

          group_content_svg.append("defs").append("marker")
              .attr("id", `arrow`)
              .attr("viewBox", "0 -5 10 10")
              .attr("refX", 15)
              .attr("refY", -0.5)
              .attr("markerWidth", 6)
              .attr("markerHeight", 6)
              .attr("orient", "auto")
              .append("path")
              .attr("fill", this.cfg.link.color)
              .attr("d", "M0,-5L10,0L0,5");


          let group_data = data;
          let group_min_x = this.cfg.node.group.margin.left
          let group_max_x = this.cfg.width - this.cfg.node.group.margin.left
          let xPositionLinear = d3.scaleLinear()
              .domain([0, group_data.nodes.length - 1])
              .range([group_min_x + 7, group_max_x - 7]);

          let lineWidthScalar = d3.scaleLinear()
              .domain([d3.min(group_data.links, d => d['ap_txn_amount']), d3.max(group_data.links, d => d['ap_txn_amount'])])
              .range([this.cfg.link.min_width, this.cfg.link.max_width]);

          // draw link
          group_content_svg.selectAll('path')
              //  奇怪的bug，绑定data的时候少了第一个link,所以暂时添加一个空的后期再解决
              .data([{}].concat(group_data.links))
              .enter()
              .append('path')
              .attr('d', d => {
                  // console.log('Get Path: ', d.source, d.target)
                  let source_x = xPositionLinear(group_data.nodes.findIndex(n => n.id === d.source));
                  let y = this.cfg.height / 2;
                  let target_x = xPositionLinear(group_data.nodes.findIndex(n => n.id === d.target));

                  if (group_data.links.find(link => (link.source === d.target) && (link.target === d.source))) {
                      //存在互相交易
                      // let r = Math.hypot(target_x - source_x, 0)>this.cfg.height/2? Math.hypot(target_x - source_x, 0):this.cfg.height/2
                       let r = 1
                      // let r = Math.hypot(target_x - source_x, 0)

                      return `M${source_x},${y} A${r},${r} 0 0,1 ${target_x},${y}`;
                  } else {
                      return 'M' + source_x + ',' + y + 'L' + target_x + ',' + y
                  }
              })
              .attr('stroke-width', d => lineWidthScalar(d['ap_txn_amount']))
              .attr('stroke', this.cfg.link.color)
              .attr('fill', 'none')

          // draw the involved trader and their transaction amount in each group
          // draw nodes
          group_content_svg.selectAll('circle')
              .data(group_data.nodes)
              .enter()
              .append('circle')
              .attr('r', this.cfg.node.individual.min_r)
              // .attr('r', d => tpRScalar(d.capital) )
              .attr('cx', d => xPositionLinear(group_data.nodes.indexOf(d)))
              .attr('cy', this.cfg.height / 2)
              .attr('fill', this.cfg.node.individual.color);

      }
      }
  }
</script>


<style scoped>
    .group-glyph{
        width: 100px;
        height:100px
    }
</style>