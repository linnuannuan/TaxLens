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
      }
    },
    watch:{
      affiliatedPartyDetail: function() {
        this.renderGraph();
      },
    },
    mounted:function(){
      this.initGraph();
      this.renderGraph();
    },
    methods: {
      initGraph() {
        let width = this.$el.clientWidth;
        let height = this.$el.clientHeight;
        let margin_width = 30;
        let margin_height = 30;

        //config the node width and link width
        this.cfg={
          width:width,
          height:height,
          node:{
            strokeWidth:1.5,
            invest_r:15,
            min_r:4,
            max_r:10,
            color:{

              // tp:'white',
              // in:'white',
              tp:'#80b1d3',
              in:'#bebada',
              evader_stroke:"#fb8072",
              default_stroke:"#ccc",
              profit:'#35978f',
              loss:'#bf812d'
            },
            rect_width: 30,
            rect_height: 30,
          },
          link:{
            min_width: 1.5,
            max_width: 1.5,
            color: {
              txn:'#80b1d3',
              invest:'#bebada',
            }
          },
          invest_panel:{
            highlight_stroke_width:4,
            highlight_stroke_color:'#984ea3'
          },
          trade_panel:{
            unimportant_opacity:0.2,
            default_opacity:0.5,
            highlight_opacity:1,

            highlight_stroke_color:'#377eb8',

            // current config (dagre)
            margin_width: margin_width,
            max_width: width - margin_width*2,
            margin_height : margin_height,
            max_height : height - margin_height*2,
            node_width: 30,
            node_height: 50,
            text_unhighlight_opacity:0.5,
          },
        };

        this.svg = d3.select('#relation_structure')
                .append("svg")
                .attr("viewBox", [0, 0, width, height])
                .style("font", "12px sans-serif");
      },
      renderGraph() {
        if (this.affiliatedPartyDetail === undefined || this.affiliatedPartyDetail.nodes === undefined ) return;
        this.svg.selectAll("g").remove();
        let data = this.affiliatedPartyDetail;

        // Create a new directed graph
        let g = new dagre.graphlib.Graph();

        // Set an object for the graph label
        g.setGraph({});

        // Default to assigning a new object as a label for each new edge.
        g.setDefaultEdgeLabel(()=>{});

        data.nodes.forEach(d=>{
          // Add nodes to the graph. The first argument is the node id. The second is metadata about the node.
          // name: d.tp ? d.tp_name:d.in_name label: "Kevin Spacey",  width: 144, height: 100
          g.setNode( d.id, { label: d.tp ? "tp":"in", name: d.tp? d.tp_name: d.in_name, width:this.cfg.node.rect_width, height:this.cfg.node.rect_height, tax_evader:d.tax_evader, profit:d.profit });
        });

        data.links.forEach(d=>{
          // Add edges to the graph.
          if ( d.source.id === undefined ){
            g.setEdge( d.source, d.target, { label: d.ap_txn? 'txn':'invest', path: d.ap_txn? d.path: [] });
          } else {
            g.setEdge( d.source.id, d.target.id, { label: d.ap_txn? 'txn':'invest', path: d.ap_txn? d.path: [] });
          }
        });

        g.graph().align = 'UL';
        // g.graph().acyclicer = 'greedy';
        g.graph().ranker = 'longest-path';
        dagre.layout(g);

        let node_width = g.graph().width > this.cfg.trade_panel.max_width? this.cfg.trade_panel.max_width/g.graph().width*this.cfg.node.rect_width: this.cfg.node.rect_width;
        let node_height = g.graph().height > this.cfg.trade_panel.max_height? this.cfg.trade_panel.max_height/g.graph().height*this.cfg.node.rect_height: this.cfg.node.rect_height;
        // let graph_width = g.graph().width > this.cfg.trade_panel.max_width? this.cfg.trade_panel.max_width: g.graph().width < this.cfg.trade_panel.max_width/2? this.cfg.trade_panel.max_width/2: g.graph().width;
        // let graph_height = g.graph().height > this.cfg.trade_panel.max_height? this.cfg.trade_panel.max_height: g.graph().height < this.cfg.trade_panel.margin_height/2? this.cfg.trade_panel.margin_height/2: g.graph().height;

        let all_x = g.edges().reduce((acc,d)=>acc.concat(g.edge(d).points.map(p=>p.x)),[]).concat(g.nodes().map(d=>g.node(d).x));
        let x_position_linear = d3.scaleLinear()
                .domain([d3.min(all_x), d3.max(all_x)])
                .range([this.cfg.trade_panel.margin_width, this.cfg.trade_panel.max_width]);

        let y_position_linear = d3.scaleLinear()
                .domain([d3.min(g.nodes().map(d=>g.node(d).y)), d3.max(g.nodes().map(d=>g.node(d).y))])
                .range([this.cfg.trade_panel.margin_height, this.cfg.trade_panel.max_height]);

        g.nodes().forEach(d=> {
          g.node(d).x = x_position_linear(g.node(d).x);
          g.node(d).y = y_position_linear(g.node(d).y);
        });
        g.edges().forEach(d=> {
          g.edge(d).points.map(p => {
            p.x = x_position_linear(p.x);
            p.y = y_position_linear(p.y);
            return p
          })
        });

        let types = ['invest','txn'];
        // Per-type markers, as they don't inherit styles.
        this.svg.append("g").selectAll("marker")
                .data(types)
                .enter()
                .append('marker')
                .attr("id", d => `arrow-${d}`)
                .attr("viewBox", "0 -5 10 10")
                .attr("refX", 9)
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
                .append('circle')
                .attr('r',node_width/2)
                .attr('cx',d=>g.node(d).x + node_width/2)
                .attr('cy',d=>g.node(d).y + node_width/2)
                // .append('rect')
                // .attr('x',d=>g.node(d).x )
                // .attr('y',d=>g.node(d).y )
                // .attr('width',node_width)
                // .attr('height',node_height)
                // .attr('fill',d=>{
                //   return g.node(d).label === 'in'? this.cfg.node.color.in:
                //         g.node(d).profit === undefined? this.cfg.node.color.tp:
                //                 g.node(d).profit? this.cfg.node.color.profit: this.cfg.node.color.loss})
                .attr('fill',d=>{
                  return g.node(d).profit === undefined? 'white':
                                g.node(d).profit? this.cfg.node.color.profit: this.cfg.node.color.loss})
                // .attr('stroke',d=>g.node(d).tax_evader? this.cfg.node.color.evader_stroke:this.cfg.node.color.default_stroke)
                .attr('stroke',d=>g.node(d).tax_evader? this.cfg.node.color.evader_stroke:g.node(d).label === 'in'? this.cfg.node.color.in:this.cfg.node.color.tp)
                .attr('stroke-width',5)
                .on('mouseover', d=>{
                  // show its name
                  d3.select('#text-'+d).attr('fill-opacity',1)
                })
                .on('mouseout', d=>{
                  // unhighlight other node text
                  d3.select('#text-'+d).attr('fill-opacity',0)
                });

        // add text to node
        this.svg.append('g').classed('text',!0)
                .selectAll('g')
                .data(g.nodes())
                .enter()
                .append('text')
                .attr('id', d=>'text-'+d)
                .attr('x',d=>g.node(d).x - 12*g.node(d).name.length/2 + node_width/2)
                .attr('y',d=>g.node(d).y + node_height + 12)
                .attr('fill',d=>g.node(d).label === 'tp'? this.cfg.node.color.tp:this.cfg.node.color.in)
                .attr('fill-opacity',0)
                .text(d=>g.node(d).name);

        // add id text to node
        this.svg.append('g').classed('text',!0)
                .selectAll('g')
                .data(g.nodes())
                .enter()
                .append('text')
                .attr('id', d=>'text-'+d)
                .attr('x',d=>g.node(d).x + node_width + 3 )
                .attr('y',d=>g.node(d).y + node_height/2 + 6)
                .attr('fill',d=>g.node(d).label === 'tp'? this.cfg.node.color.tp:this.cfg.node.color.in)
                .text(d=>d.slice(d.length-4));

        // draw edge
        var line = d3.line()
                .curve(d3.curveBasis)
                .x(d =>d[0])
                .y(d =>d[1]);
        this.svg.append('g').classed('link',!0)
                .selectAll('g')
                .data(g.edges())
                .enter()
                .append('path')
                .attr('id', d=> g.edge(d).label + "-" + d.v + "-" + d.w)
                .attr('d',d=> {
                  let offset_x = node_width/2;
                  let offset_y = node_height;
                  let link_data = [[g.node(d.v).x, + g.node(d.v).y]].concat(g.edge(d).points.map(p=>[p.x,p.y])).concat([[g.node(d.w).x,g.node(d.w).y]]);

                  let position_linear = d3.scaleLinear()
                          .domain([link_data[0][1], link_data[link_data.length-1][1]])
                          .range([link_data[0][1]+offset_y, link_data[link_data.length-1][1]]);

                  // link_data.map(d=> { d[0] += offset_x ; d[1] += 2*offset_y; return d})

                  link_data.map(d=> { d[0] += offset_x ; d[1]= position_linear(d[1]); return d});
                  return line(link_data)
                })
                .attr("stroke", d=>g.edge(d).label==='invest' ? this.cfg.link.color.invest:this.cfg.link.color.txn)
                .attr("stroke-width", "2px")
                .attr("marker-end", d => `url(${new URL(`#arrow-${g.edge(d).label}`, location)})`)
                .attr("fill", "none")
                .attr('cursor','pointer')
                .on('mouseover',d=>{
                  //对应的invest_path高亮
                  if(g.edge(d).label === 'txn'){
                    for(let path_id in g.edge(d).path){
                      for( let node_id in g.edge(d).path[path_id]){
                        if( node_id < (g.edge(d).path[path_id].length-1) ){
                          // d3.select('#txn-'+d.v+"-"+d.w)
                          //         .attr('stroke-width', this.cfg.invest_panel.highlight_stroke_width);
                          // d3.select('#invest' + '-' + g.edge(d).path[path_id][parseInt(node_id)] + '-' + g.edge(d).path[path_id][parseInt(node_id) + parseInt(1)])
                          //         .attr('stroke-width', this.cfg.invest_panel.highlight_stroke_width);
                          d3.select('#txn-'+d.v+"-"+d.w)
                                  .attr('stroke', this.cfg.trade_panel.highlight_stroke_color);
                          d3.select('#invest' + '-' + g.edge(d).path[path_id][parseInt(node_id)] + '-' + g.edge(d).path[path_id][parseInt(node_id) + parseInt(1)])
                                  .attr('stroke', this.cfg.invest_panel.highlight_stroke_color);
                          d3.select('#invest'+ '-' + g.edge(d).path[path_id][parseInt(node_id) + parseInt(1)] + '-' + g.edge(d).path[path_id][parseInt(node_id)])
                                  .attr('stroke', this.cfg.invest_panel.highlight_stroke_color)
                        }
                      }
                    }
                  }
                })
                .on('mouseout',d=>{
                  if(g.edge(d).label === 'txn') {
                    for (let path_id in g.edge(d).path) {
                      for (let node_id in g.edge(d).path[path_id]) {
                        if (node_id < (g.edge(d).path[path_id].length - 1)) {
                          // unhighlight correspond invest link (undirect link)
                          // d3.select('#txn-' + d.v + "-" + d.w)
                          //         .attr('stroke-width', 2);
                          // d3.select('#invest' + '-' + g.edge(d).path[path_id][parseInt(node_id)] + '-' + g.edge(d).path[path_id][parseInt(node_id) + parseInt(1)])
                          //         .attr('stroke-width', 2);
                          // d3.select('#invest' + '-' + g.edge(d).path[path_id][parseInt(node_id) + parseInt(1)] + '-' + g.edge(d).path[path_id][parseInt(node_id)])
                          //         .attr('stroke-width', 2)
                          d3.select('#txn-' + d.v + "-" + d.w)
                                  .attr('stroke', this.cfg.link.color.txn);
                          d3.select('#invest' + '-' + g.edge(d).path[path_id][parseInt(node_id)] + '-' + g.edge(d).path[path_id][parseInt(node_id) + parseInt(1)])
                                  .attr('stroke', this.cfg.link.color.invest);
                          d3.select('#invest' + '-' + g.edge(d).path[path_id][parseInt(node_id) + parseInt(1)] + '-' + g.edge(d).path[path_id][parseInt(node_id)])
                                  .attr('stroke', this.cfg.link.color.invest)
                        }
                      }
                    }
                  }
                })
                .on('click', d=>{
                  EventService.emitAffiliatedTransactionSelected(d.v, d.w);
                });
      }
    }
  };
</script>
<style scoped>
</style>
