<template>
  <div id="force_direct_graph" v-loading="loadingGraph"></div>
</template>
<script>
  import * as d3 from "d3";
  import EventService from "../utils/event-service";

  export default {
    name: 'DigraphView',
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
        this.renderDiGraph();
      },
    },
    mounted:function(){
      this.initDiGraph();
    },
    methods: {
      initDiGraph() {
        let width = this.$el.clientWidth;
        let height = this.$el.clientHeight;
        let margin_width = width/50;
        let margin_height = height/30;

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
            }
          },
          link:{
            'min_width':1.5,
            'max_width':1.5,
            'color':{
              'txn':'#1f77b4',
              'invest':'#ff7f0e',
            }
          },
          trade_panel:{
            min_width : margin_width,
            max_width : width - margin_width,
            min_height : height/3 + margin_height,
            max_height : 2*height/3 - margin_height
          },
          invest_panel:{
            min_width : margin_width,
            max_width : width - margin_width,
            min_height : margin_height,
            max_height : height/3 - margin_height
          },
          parallel_panel:{
            min_width : margin_width,
            max_width : width - margin_width,
            min_height : 2*height/3 + margin_height,
            max_height : height - margin_height,
            line_color:'#1f77b4',
            highlight_color:'#b82e2e',
            node_color:'#316395',
          }
        };
        this.svg = d3.select('#force_direct_graph')
                .append("svg")
                .attr("viewBox", [-width/2, -height/2,width,height])
                .style("font", "12px sans-serif");
      },
      renderDiGraph() {
        function drag(simulation) {
          function dragStarted(d) {
            if (!d3.event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
          }

          function dragged(d) {
            d.fx = d3.event.x;
            d.fy = d3.event.y;
          }

          function dragEnded(d) {
            if (!d3.event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          }

          return d3.drag()
                  .on("start", dragStarted)
                  .on("drag", dragged)
                  .on("end", dragEnded);
        }

        function linkArc(d) {
          const r = Math.hypot(d.target.x - d.source.x, d.target.y - d.source.y);
          return `
                    M${d.source.x},${d.source.y}
                    A${r},${r} 0 0,1 ${d.target.x},${d.target.y}
                  `;
        }
        this.svg.selectAll("g").remove();
        if (this.affiliatedPartyDetail !== null) {
          let data = this.affiliatedPartyDetail;
          let get_node_link_chart = (data)=>{
            let link_by_src = {};
            let link_by_dst = {};

            data.nodes.forEach(node => {
              link_by_src[node['id']]={'children':[]};
              link_by_dst[node['id']]={'parent':[]}
            });

            const links = data.links.map(link => {
              link.type = link.in_ratio? 'invest' : 'txn';
              link.value = link.in_ratio? (1/link.in_ratio): 0.5;
              link_by_src[link.source]['children'].push(link);
              link_by_dst[link.target]['parent'].push(link);
              return Object.create(link)
            });

            const nodes = data.nodes.map(node => {
              node.type = node.in ? 'investor' : 'taxpayer';
              // node.value = link_by_src[node['id']]['children'].filter(d=>d['ap_txn'])
              return Object.create(node)
            });

            let types = Array.from(new Set(links.map(d => d.type)));

            // let industrys =  Array.from(new Set(nodes.filter(d=>!d.in).map( d => d['industry'])));
            // let color = d3.scaleOrdinal(industrys, d3.schemeSet3);

            // schemeCategory10: 1f77b4,ff7f0e ,2ca02c,d62728,9467bd,8c564b,e377c2,7f7f7f,bcbd22,17becf
            // let color = d3.scaleOrdinal(types, d3.schemeCategory10);

            // node capital encoding
            let rScale = d3.scaleLinear()
                    .domain([d3.min(nodes, function(d){ return d['capital']; }), d3.max(data.nodes, function(d){ return d['capital']; })])
                    .range([this.cfg.node.min_r, this.cfg.node.max_r]);

            // node suspect value encoding
            // let rScale = d3.scaleLinear()
            //   .domain([d3.min(nodes, function(d){ return d['ap_txn_amount']; }), d3.max(data.nodes, function(d){ return d['ap_txn_amount']; })])
            //   .range([this.cfg.node.min_r, this.cfg.node.max_r]);

            // invest node suspect value encoding
            let irScale = d3.scaleLinear()
                    .domain([d3.min(nodes, function(d){ return d['suspect_value']; }), d3.max(data.nodes, function(d){ return d['suspect_value']; })])
                    .range([this.cfg.node.min_r, this.cfg.node.max_r]);


            // link stength encoding
            let lScale = d3.scaleLinear().domain([0,1]).range([this.cfg.link.min_width, this.cfg.link.max_width]);

            // trade link strength encoding
            let oScale = d3.scaleLinear()
                    .domain([d3.min(nodes, function(d){ return d['ap_txn_amount']; }),d3.max(nodes, function(d){ return d['ap_txn_amount']; })])
                    .range([0,1]);


            const simulation = d3.forceSimulation(nodes)
                    .force("link", d3.forceLink(links).id(d => d.id))
                    .force("charge", d3.forceManyBody().strength(-1000))
                    .force("x", d3.forceX())
                    .force("y", d3.forceY());

            this.svg.selectAll("g").remove();

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

            const link = this.svg.append("g")
                    .attr("fill", "none")
                    .selectAll("path")
                    .data(links)
                    .enter()
                    .append('path')
                    .attr("stroke", d => d.type === 'invest'? this.cfg.link.color.invest:this.cfg.link.color.txn)
                    .attr("stroke-width", d => lScale(d.value))
                    .attr('opacity', d => d.type === 'invest'? 1/d.value:oScale(d['ap_txn_amount']))
                    // link 线段终止坐标待计算
                    .attr("marker-end", d => `url(${new URL(`#arrow-${d.type}`, location)})`)
                    .on('click',function (d) {
                      EventService.emitAffiliatedTransactionSelected(d.source.id,d.target.id);
                      // this.getDetailTransactionView(d.source,d.target)
                    })

            const node = this.svg.append("g")
                    .attr("fill", "currentColor")
                    .attr("stroke-linecap", "round")
                    .attr("stroke-linejoin", "round")
                    .selectAll("g")
                    .data(nodes)
                    .enter()
                    .append('g')
                    .call(drag(simulation));

            // const in_node = this.svg.append("g")
            //   .attr("fill", "currentColor")
            //   .attr("stroke-linecap", "round")
            //   .attr("stroke-linejoin", "round")
            //   .selectAll("g")
            //   .data(nodes.filter(d=>!d.tp))
            //   .enter()
            //   .append('g')
            //   .call(drag(simulation));
            //
            // const tp_node = this.svg.append("g")
            //   .attr("fill", "currentColor")
            //   .attr("stroke-linecap", "round")
            //   .attr("stroke-linejoin", "round")
            //   .selectAll("g")
            //   .data(nodes.filter(d=>d.tp))
            //   .enter()
            //   .append('g')
            //   .call(drag(simulation));

            node.append("circle")
                    .attr("stroke", d=>d['tax_evader']?'red':'white')
                    // .attr("stroke", d=>d['in']?'white':color(d['industry']))
                    // .attr("fill", d=>color(d['industry']))
                    .attr("fill", d=>d['in']? this.cfg.node.color.in:this.cfg.node.color.tp)
                    .attr("stroke-width", 1.5)
                    .attr("r", d => d['in'] ? irScale(d['suspect_value']): rScale(d['capital']))
                    .on('click',function (d) {
                      console.log('click :',d)
                    });

            // transfer node into circle and rectangle
            // in_node.append("circle")
            //   .attr("stroke", d=>d['in']?'white':color(d['industry']))
            //   // .attr("fill", d=>color(d['industry']))
            //   .attr("fill", d=>d['in']? this.cfg.node.color.in:this.cfg.node.color.tp)
            //   .attr("stroke-width", 1.5)
            //   .attr("r", d => d['in'] ? irScale(d['suspect_value']): rScale(d['capital']))
            //   .on('click',function (d) {
            //     console.log('click :',d)
            //   })
            //   // .on("mouseover", function(){return this.tooltip.style("visibility", "visible");})
            //   // .on("mousemove", function(){return this.tooltip.style("top", (event.pageY-800)+"px").style("left",(event.pageX-800)+"px");})
            //   // .on("mouseout", function(){return this.tooltip.style("visibility", "hidden");});
            //
            //  tp_node.append("rect")
            //   .attr("stroke", d=>color(d['industry']))
            //   .attr("fill", d=>color(d['industry']))
            //   // .attr("fill", this.cfg.node.color.tp)
            //   .attr("stroke-width", 1.5)
            //   .attr("width", d=>rScale(d['capital']))
            //   .attr("height", d=>rScale(d['capital']))
            //   // .attr("x", d=>rScale(d['capital']))
            //   .on('click',function (d) {
            //     console.log('click :',d)
            //   })


            node.append("text")
                    .attr("x", 8)
                    .attr("y", "0.31em")
                    .text(d => {
                      return d.in? d.in_name: d.tp_name;
                    })
                    .clone(true).lower()
                    .attr("fill", "none")
                    .attr("stroke", "white")
                    .attr("stroke-width", 3);


            simulation.on("tick", () => {
              link.attr("d", linkArc);
              node.attr("transform", d => `translate(${d.x},${d.y})`);
              // tp_node.attr("transform", d => `translate(${d.x-3},${d.y-3})`);
            });
          };


          get_node_link_chart(data)

        }
      }
    }};
</script>
<style scoped>
</style>
