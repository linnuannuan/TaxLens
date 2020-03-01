/* eslint-disable */
<template>
    <div id="relation_structure"></div>
</template>
<script>
    import * as d3 from "d3";
    export default {
        name: 'graphView',
        data() {
            return {
                APIRN: null,
                APIRN_all: null
            };
        },
        watch:{
            APIRN_all:function () {
                this.renderGraph();
            }
        },
        mounted:function(){
            const apirnUrl = "http://127.0.0.1:9950/APIRN";
            this.axios.get(apirnUrl).then((response) => {
                this.APIRN = response.data;
            });

            this.axios.get(apirnUrl+"_all").then((response) => {
                this.APIRN_all = response.data;
            });
        },
        methods: {
            renderGraph() {
                const width = 1000, height = 500;

                function drag(simulation) {
                    function dragstarted(d) {
                        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
                        d.fx = d.x;
                        d.fy = d.y;
                    }

                    function dragged(d) {
                        d.fx = d3.event.x;
                        d.fy = d3.event.y;
                    }

                    function dragended(d) {
                        if (!d3.event.active) simulation.alphaTarget(0);
                        d.fx = null;
                        d.fy = null;
                    }

                    return d3.drag()
                        .on("start", dragstarted)
                        .on("drag", dragged)
                        .on("end", dragended);
                }

                function linkArc(d) {
                    const r = Math.hypot(d.target.x - d.source.x, d.target.y - d.source.y);
                    return `
                    M${d.source.x},${d.source.y}
                    A${r},${r} 0 0,1 ${d.target.x},${d.target.y}
                  `;
                }

                // A hard code example
                let data = this.APIRN_all['1581'];
                const links = data.links.map(link => {
                    // link.type = link.control? 'control' : 'invest'
                    link.value = link.in_ratio;
                    return Object.create(link)
                });
                const nodes = data.nodes.map(node => {
                    node.type = node.in ? 'investor' : 'taxpayer';
                    return Object.create(node)
                });

                var types = Array.from(new Set(links.map(d => d.type)))
                var color = d3.scaleOrdinal(types, d3.schemeCategory10)

                const simulation = d3.forceSimulation(nodes)
                    .force("link", d3.forceLink(links).id(d => d.id))
                    .force("charge", d3.forceManyBody().strength(-200))
                    .force("x", d3.forceX())
                    .force("y", d3.forceY());

                const svg = d3.select('#relation_structure')
                    .append("svg")
                    .attr("viewBox", [-width / 2, -height / 2, width, height])
                    .style("font", "12px sans-serif");

                // Per-type markers, as they don't inherit styles.
                svg.append("defs").selectAll("marker")
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

                const link = svg.append("g")
                    .attr("fill", "none")
                    .attr("stroke-width", 1.5)
                    .selectAll("path")
                    .data(links)
                    .enter()
                    .append('path')
                    .attr("stroke", d => color(d.type))
                    .attr("marker-end", d => `url(${new URL(`#arrow-${d.type}`, location)})`);

                const node = svg.append("g")
                    .attr("fill", "currentColor")
                    .attr("stroke-linecap", "round")
                    .attr("stroke-linejoin", "round")
                    .selectAll("g")
                    .data(nodes)
                    .enter()
                    .append('g')
                    .call(drag(simulation));

                node.append("circle")
                    .attr("stroke", "white")
                    .attr("stroke-width", 1.5)
                    .attr("r", 4);

                node.append("text")
                    .attr("x", 8)
                    .attr("y", "0.31em")
                    .text(d => {
                        if (d.in) return d.in_name
                        else return d.tp_name
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
    };
</script>
<style scoped>
</style>
