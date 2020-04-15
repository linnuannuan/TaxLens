/* eslint-disable */
<template>
  <div id="relation_structure" v-loading="loadingGraph"></div>
</template>
<script>
  import * as d3 from "d3";
  import * as dagre from "dagre";
  import EventService from "../utils/event-service";

  export default {
    name: 'GraphView',
    props:{
      affiliatedPartyDetail: Object,
      loadingGraph: Boolean
    },
    data() {
      return {
        svg: null,
        cfg: null,
      }
    },
    watch:{
      affiliatedPartyDetail: function() {
        this.renderGraph();
      },
    },
    mounted:function(){
      this.initGraph();
    },
    methods: {
      initGraph() {
        let width = this.$el.clientWidth;
        let height = this.$el.clientHeight;
        let margin_width = width/10;
        let margin_height = height/10;

        //config the node width and link width
        this.cfg={
          width:width,
          height:height,
          node:{
            'strokeWidth':1.5,
            'invest_r':20,
            'min_r':4,
            'max_r':10,
            'color':{
              'tp':'#1f77b4',
              'in':'#ff7f0e'
            },
            'rect_width':30,
            'rect_height':30,
          },
          link:{
            'min_width':1.5,
            'max_width':1.5,
            'color':{
              'txn':'#1f77b4',
              'invest':'#ff7f0e',
            }
          },
          invest_panel:{
            min_width : margin_width,
            max_width : width - margin_width,
            min_height : margin_height,
            max_height : height/4 - margin_height,
            highlight_opacity:1,
            default_opacity:1,
            unimportant_opacity:0.7,
            highlight_stroke_width:5
          },
          trade_panel:{
            min_width:margin_width-width/2,
            // min_width : margin_width,
            max_width:width - margin_width -width/2,
            // max_width : width - margin_width,
            min_height : height/4 + margin_height -height/2,
            max_height : height - margin_height-height/2,
            unimportant_opacity:0.2,
            default_opacity:0.5,
            highlight_opacity:1,
            node_width: 30,
            node_height:50
          },
          parallel_panel:{
            highlight_color:'#b82e2e',
            default_opacity:0.5,
            highlight_opacity:0.8,
            default_stroke_width:2,
            highlight_stroke_width:4
          },
        };

        this.svg = d3.select('#relation_structure')
                .append("svg")
                .attr("viewBox", [-width/2, -height/2,width,height])
                .style("font", "12px sans-serif");
      },
      renderGraph() {
        this.svg.selectAll("g").remove();
        if (this.affiliatedPartyDetail.nodes !== undefined) {
          let data = this.affiliatedPartyDetail;
          console.log(data)
          // Create a new directed graph
          var g = new dagre.graphlib.Graph();

          // Set an object for the graph label
          g.setGraph({});

          // Default to assigning a new object as a label for each new edge.
          g.setDefaultEdgeLabel(()=>{});

          data.nodes.forEach(d=>{
            // Add nodes to the graph. The first argument is the node id. The second is metadata about the node.
            g.setNode( d.id, {
              label: d.tp ? "tp":"in",
              name: d.tp ? d.id.slice(d.id.length-4):d.in_name,
              width:this.cfg.node.rect_width,
              height:this.cfg.node.rect_height
            });
          });

          // Add edges to the graph.
          data.links.forEach(d=>{
            g.setEdge( d.source, d.target, { label: d.ap_txn?'txn':'invest'});
          });

          dagre.layout(g);

          let node_width = g.graph().width>(this.cfg.trade_panel.max_width - this.cfg.trade_panel.min_width) ?  (this.cfg.trade_panel.max_width - this.cfg.trade_panel.min_width)/g.graph().width * this.cfg.node.rect_width : this.cfg.node.rect_width;
          let node_height = g.graph().height>(this.cfg.trade_panel.max_height - this.cfg.trade_panel.min_height) ?  (this.cfg.trade_panel.max_height - this.cfg.trade_panel.min_height)/g.graph().height * this.cfg.node.rect_height : this.cfg.node.rect_height;


          let all_x = g.edges().reduce((acc,d)=>acc.concat(g.edge(d).points.map(p=>p.x)),[]).concat(g.nodes().map(d=>g.node(d).x));

          let x_position_linear = d3.scaleLinear()
                  .domain([d3.min(all_x), d3.max(all_x)])
                  .range([this.cfg.trade_panel.min_width,this.cfg.trade_panel.max_width]);


          let y_position_linear = d3.scaleLinear()
                  .domain([0,g.graph().height])
                  .range([this.cfg.trade_panel.min_height,this.cfg.trade_panel.max_height]);

          g.nodes().forEach(d=> {
            g.node(d).x = x_position_linear(g.node(d).x);
            g.node(d).y = y_position_linear(g.node(d).y);
          });
          g.edges().forEach(d=> g.edge(d).points.map(p=>{p.x = x_position_linear(p.x);p.y = y_position_linear(p.y);return p}));

          let types = ['invest','txn'];
          // Per-type markers, as they don't inherit styles.
          this.svg.append("g").selectAll("marker")
                  .data(types)
                  .enter()
                  .append('marker')
                  .attr("id", d => `arrow-${d}`)
                  .attr("viewBox", "0 -5 10 10")
                  .attr("refX", 15)
                  .attr("refY", -0.5)
                  .attr("markerWidth", 6)
                  .attr("markerHeight", 6)
                  .attr("orient", "auto")
                  .append("path")
                  .attr("fill", d=> this.cfg.link.color[d])
                  .attr("d", "M0,-5L10,0L0,5");

          // draw node
          this.svg.append('g').classed('node',!0)
                  .selectAll('g')
                  .data(g.nodes())
                  .enter()
                  .append('rect')
                  .attr('x',d=>g.node(d).x )
                  .attr('y',d=>g.node(d).y )
                  .attr('width',node_width)
                  .attr('height',node_height)
                  .attr('fill',d=>g.node(d).label === 'tp'? this.cfg.node.color.tp:this.cfg.node.color.in)
                  .on('click', d=>{
                    console.log(d);
                  });

          // add text to node
          this.svg.append('g').classed('text',!0)
                  .selectAll('g')
                  .data(g.nodes())
                  .enter()
                  .append('text')
                  .attr('x',d=>g.node(d).x - 12*g.node(d).name.length/2 + node_width/2)
                  .attr('y',d=>g.node(d).y - 2)
                  .attr('fill',d=>g.node(d).label === 'tp'? this.cfg.node.color.tp:this.cfg.node.color.in)
                  .text(d=>g.node(d).name);

          // draw edge
          var line = d3.line()
                  // .curve(d3.curveBasis)
                  .curve(d3.curveMonotoneY)
                  .x(d =>d[0])
                  .y(d =>d[1]);
          this.svg.append('g').classed('link',!0)
                  .selectAll('g')
                  .data(g.edges())
                  .enter()
                  .append('path')
                  .attr('d',d=> {
                    let offset_x = node_width/2;
                    let offset_y = node_height;
                    let link_data = [[g.node(d.v).x, + g.node(d.v).y]].concat(g.edge(d).points.map(p=>[p.x,p.y])).concat([[g.node(d.w).x,g.node(d.w).y]]);

                    let position_linear = d3.scaleLinear()
                            .domain([link_data[0][1], link_data[link_data.length-1][1]])
                            .range([link_data[0][1]+offset_y, link_data[link_data.length-1][1]]);
                    link_data.map(d=> { d[0] += offset_x ; d[1]= position_linear(d[1]); return d});
                    return line(link_data)
                  })
                  .attr("stroke", d=>g.edge(d).label==='invest'?this.cfg.link.color.invest:this.cfg.link.color.txn)
                  .attr("stroke-width", "2px")
                  .attr("marker-end", d => `url(${new URL(`#arrow-${g.edge(d).label}`, location)})`)
                  .attr("fill", "none")
                  .attr('cursor','pointer')
                  .on('click', d=>{
                    EventService.emitAffiliatedTransactionSelected(d.v, d.w);
                  });


        }
      }
    }};
</script>
<style scoped>
</style>
