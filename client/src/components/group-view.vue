<template>
    <div id="group_view" v-loading="loadingTopoList"></div>
</template>

<script>
  import * as d3 from "d3";
  import EventService from "../utils/event-service";

  export default {
    name: "GroupView",
    props:{
      affiliatedPartyTopoList: Array,
      loadingTopoList: Boolean
    },
    data: function () {
      return {
        svg: null,
      }
    },
    watch: {
      affiliatedPartyTopoList: function() {
        this.renderGroupView();
      },
    },
    mounted:function(){
      this.initGroupView();
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
              min_r: 15,
              max_r: 30,
              color:'skyblue',
              margin:{
                left:50,
                top:40
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
          'row_num':2,
          'col_num':10,
          'row_margin':0.5,
          'col_margin':1,
        };
        this.svg = d3.select('#group_view')
          .append("svg")
          .attr("viewBox", [0, 0, width, height]);
      },
      renderGroupView(){
        this.svg.selectAll("g").remove();

        let data = this.affiliatedPartyTopoList;

        // 创建值映射器
        // group circle size encoder
        let groupRScaler = d3.scaleLinear()
          .domain([d3.min(data, d=>d.profit), d3.max(data, d=>d.profit)])
          .range([this.cfg.node.group.min_r, this.cfg.node.group.max_r]);

        /* draw each group with circle (size encode tax gap) and node_link graph represent inner ap_transaction */
        // draw group circle
        this.svg.append('g')
          .selectAll('circle')
          .data(data)
          .enter()
          .append('circle')
          .attr('r', d=>groupRScaler(d.profit))
          // 设置x坐标为 该容器width 11等分（1等分留作间距），间距设置为5
          .attr('cx',d=>this.cfg.node.group.margin.left + (data.indexOf(d)%this.cfg.col_num) * (this.cfg.width-2*this.cfg.node.group.margin.left) / (this.cfg.col_num-1))
          // 设置默认20个组, 10上10下, 该容器height 3等分（1等分留作间距），间距设置为5
          .attr('cy',d=>this.cfg.node.group.margin.top + (Math.floor(data.indexOf(d)/this.cfg.col_num)) * (this.cfg.height-2*this.cfg.node.group.margin.top) / (this.cfg.row_num-1))
          .attr('fill',this.cfg.node.group.color)
          .attr('fill-opacity',0.5)
          .attr('stroke',this.cfg.node.group.color)
          .attr('stroke-width',2)
          .on('click',d=>this.handleView(d.ap_id));

        let group_content_svg = this.svg.append('g')
          .classed('group_content',!0);

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

        for( let g_id in data ){
          let group_svg = group_content_svg.append('g').classed('group-'+g_id,!0);
          let group_data = data[g_id];
          let group_min_x = g_id % this.cfg.col_num * (this.cfg.width-2*this.cfg.node.group.margin.left) / (this.cfg.col_num-1) + this.cfg.node.group.margin.left - groupRScaler(group_data.profit);
          let group_max_x = g_id % this.cfg.col_num * (this.cfg.width-2*this.cfg.node.group.margin.left) / (this.cfg.col_num-1) + this.cfg.node.group.margin.left + groupRScaler(group_data.profit);
          let group_y = (Math.floor(g_id/this.cfg.col_num) * (this.cfg.height-2*this.cfg.node.group.margin.top) / (this.cfg.row_num-1) + this.cfg.node.group.margin.top);
          let xPositionLinear = d3.scaleLinear()
            .domain([0, group_data.nodes.length-1])
            .range([group_min_x+7, group_max_x-7]);

          let lineWidthScaler = d3.scaleLinear()
            .domain([d3.min(group_data.links, d=>d.ap_txn_amount), d3.max(group_data.links, d=>d.ap_txn_amount)])
            .range([this.cfg.link.min_width, this.cfg.link.max_width]);

          // draw the involved trader and their transaction amount in each group
          // draw nodes
          group_svg.selectAll('circle')
            .data(group_data.nodes)
            .enter()
            .append('circle')
            .attr('r', this.cfg.node.individual.min_r)
            // .attr('r', d => tpRScaler(d.capital) )
            .attr('cx',d => xPositionLinear(group_data.nodes.indexOf(d)))
            .attr('cy',group_y)
            .attr('fill',this.cfg.node.individual.color);
          // console.log(group_data.links)

          // draw link
          group_svg.selectAll('path')
            .data(group_data.links)
            .enter()
            .append('path')
            .attr('d',d=>{
              let source_x = xPositionLinear(group_data.nodes.findIndex(n=>n.id === d.source));
              let y = group_y;
              let target_x = xPositionLinear(group_data.nodes.findIndex(n=>n.id === d.target));

              if(group_data.links.find( link=> (link.source === d.target) && (link.target === d.source) )){
                //存在互相交易
                let r = Math.hypot(target_x - source_x, 0);
                return `M${source_x},${y} A${r},${r} 0 0,1 ${target_x},${y}`;
              }
              else{
                return 'M'+source_x + ',' + y + 'L' + target_x + ',' + y
              }
            })
            .attr('stroke-width',d=>lineWidthScaler(d.ap_txn_amount))
            .attr('stroke',this.cfg.link.color)
            .attr('fill','none')
        }
      }
    },
  }
</script>

<style scoped>
</style>