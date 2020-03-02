/* eslint-disable */
<template>
  <div id="relation_structure"></div>
</template>
<script>
  import * as d3 from "d3";

  export default {
    name: 'GraphView',
    props:{
      affiliatedPartyDetail: Object,
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
    },
    methods: {
      initGraph() {
        let width = this.$el.clientWidth;
        let height = this.$el.clientHeight;
        //config the node width and link width
        this.cfg={
          node:{
            'min_r':4,
            'max_r':10
          },
          link:{
            'min_width':1,
            'max_width':2
          }
        };
        this.svg = d3.select('#relation_structure')
          .append("svg")
          .attr("viewBox", [-width / 2, -height / 2, width, height])
          .style("font", "12px sans-serif");
        this.tooltip = d3.select("#relation_structure")
          .append("div")
          .style("position", "absolute")
          .style("visibility", "hidden")
          .text("I'm tootip!");
      },
      renderGraph() {
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

        if (this.affiliatedPartyDetail !== null) {
          let data = this.affiliatedPartyDetail;
          const links = data.links.map(link => {
            link.type = link.in_ratio? 'invest' : 'txn';
            link.value = link.in_ratio? (reverse_ratio-link.in_ratio): 0.5;
            return Object.create(link)
          });
          const nodes = data.nodes.map(node => {
            node.type = node.in ? 'investor' : 'taxpayer';
            return Object.create(node)
          });

          console.log(d3.max(data.nodes, function(d){ return d['capital']; }));
          console.log(d3.min(data.nodes, function(d){ return d['capital']; }));

          let types = Array.from(new Set(links.map(d => d.type)));
          // schemeCategory10: 1f77b4,ff7f0e ,2ca02c,d62728,9467bd,8c564b,e377c2,7f7f7f,bcbd22,17becf
          let color = d3.scaleOrdinal(types, d3.schemeCategory10);

          // node capital encoding
          let rScale = d3.scaleLinear()
            .domain([d3.min(nodes, function(d){ return d['capital']; }), d3.max(data.nodes, function(d){ return d['capital']; })])
            .range([this.cfg.node.min_r, this.cfg.node.max_r]);
          // link stength encoding
          let lScale = d3.scaleLinear().domain([0,1]).range([this.cfg.link.min_width, this.cfg.link.max_width]);

          // reverse the strength of link
          const reverse_ratio = 1.1;

          const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.id))
            .force("charge", d3.forceManyBody().strength(-500))
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
            .attr("fill", color)
            .attr("d", "M0,-5L10,0L0,5");

          const link = this.svg.append("g")
            .attr("fill", "none")
            .selectAll("path")
            .data(links)
            .enter()
            .append('path')
            .attr("stroke", d => color(d.type))
            .attr("stroke-width", d => lScale(d.value))
            .attr('opacity', d => reverse_ratio - d.value)
            .attr("marker-end", d => `url(${new URL(`#arrow-${d.type}`, location)})`);

          const node = this.svg.append("g")
            .attr("fill", "currentColor")
            .attr("stroke-linecap", "round")
            .attr("stroke-linejoin", "round")
            .selectAll("g")
            .data(nodes)
            .enter()
            .append('g')
            .call(drag(simulation));

          node.append("circle")
            .attr("stroke", function (d) {
              return d['in']? '#ff7f0e': 'white';
            })
            .attr("stroke-width", 1.5)
            .attr("r", d => d['in'] ? this.cfg.node.min_r : rScale(d['capital']))
            .on('click',function (d) {
              console.log('click :',d)
            })
            .on("mouseover", function(){return this.tooltip.style("visibility", "visible");})
            .on("mousemove", function(){return this.tooltip.style("top", (event.pageY-800)+"px").style("left",(event.pageX-800)+"px");})
            .on("mouseout", function(){return this.tooltip.style("visibility", "hidden");});

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
          });
        }
      }
    }
  };
</script>
<style scoped>
</style>
