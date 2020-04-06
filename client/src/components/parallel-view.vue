/* eslint-disable */
<template>
    <div id="parallel_view"></div>
</template>

<script>
    import * as d3 from "d3";
    // import EventService from "../utils/event-service";

    export default {
          name: 'ParallelView',
          props: {
              affiliatedPartyDetail: Object,
              loadingGraph: Boolean
          },
          data() {
              return {
                  svg: null,
              }
          },
          watch: {
              affiliatedPartyDetail: function () {
                  this.renderGraph();
              },
          },
          mounted: function () {
              this.initGraph();
          },
          methods: {
              // getDetailTransactionView(source, target) {
              //   console.log('click to get detail tran:', ' source: ', source, 'target: ', target)
              //   EventService.emitAffiliatedTransactionSelected(source, target);
              // },
              initGraph() {
                  let width = this.$el.clientWidth;
                  let height = this.$el.clientHeight;
                  let margin_width = width / 30;
                  let margin_height = height / 20;

                  //config the node width and link width
                  this.cfg = {
                      width: width,
                      height: height,
                      parallel_panel: {
                          min_width: margin_width,
                          max_width: width - margin_width,
                          min_height: margin_height,
                          max_height: height - margin_height,
                          line_color: 'skyblue',
                          // line_color:'#1f77b4',
                          highlight_color: '#b82e2e',
                          node_color: '#316395',
                          default_opacity: 0.5,
                          highlight_opacity: 0.8,
                          default_stroke_width: 2,
                          highlight_stroke_width: 4
                      }
                  };
                  this.svg = d3.select('#parallel_view')
                      .append("svg")
                      .attr("viewBox", [0, 0, width, height])
                      .style("font", "12px sans-serif");
                  // this.tooltip = d3.select("#relation_structure")
                  //   .append("div")
                  //   .style("position", "absolute")
                  //   .style("visibility", "hidden")
                  //   .text("I'm tootip!");
              },
              renderGraph() {
                  this.svg.selectAll("g").remove();
                  let t_links = this.affiliatedPartyDetail.links.filter(l=>l.ap_txn);

                  // draw the parallel chart
                  let txn_attr_li = ['related strength', 'transaction strength', 'tax burden deviation', 'tb variation deviation', 'net profit deviation', 'np variation deviation', 'elastic deviation'];
                  let parallel_svg = this.svg.append('g').classed('parallel', !0);

                  // 坐标系的位置映射
                  let y_linear = d3.scaleLinear()
                      .domain([0, txn_attr_li.length])
                      .range([this.cfg.parallel_panel.min_height, this.cfg.parallel_panel.max_height]);

                  // mock the attr value for each tp link
                  t_links = t_links.map(d => {
                      txn_attr_li.forEach(attr => d[attr] = 1000 * Math.random());
                      return d
                  });
                  // console.log('After generating the suspect value of t link: ',t_links)

                  //创建每个轴的比例尺
                  let attrScale = [];
                  txn_attr_li.forEach(
                      d => {
                          let parallel_attr_svg = parallel_svg.append('g').classed(d, !0);
                          let dataset = t_links.map(link => link[d]);
                          // console.log('dataset: ',dataset)
                          // dataset
                          // 定义比例尺
                          let c_attrScale = d3.scaleLinear()
                              .domain([0, d3.max(dataset)])
                              .range([this.cfg.parallel_panel.min_width + 10, this.cfg.parallel_panel.max_width - 10]);
                          // 添加坐标轴
                          parallel_attr_svg.append("g")
                              .classed('x_axis', !0)
                              .attr("transform", "translate(0," + y_linear(txn_attr_li.indexOf((d))) + ")")
                              .call(d3.axisBottom(c_attrScale));

                          // 添加坐标轴属性的名称
                          parallel_attr_svg.append('g')
                              .classed('p_text', !0)
                              .selectAll('g.p_text')
                              .data(txn_attr_li)
                              .enter()
                              .append('text')
                              .attr('x', this.cfg.parallel_panel.min_width - 10)
                              .attr('y', d => y_linear(txn_attr_li.indexOf((d))) - 10)
                              .text(d => d);

                          // 把比例尺保留方便绘值
                          attrScale.push(c_attrScale)
                      }
                  );
                  // console.log('the parallel x axis: ', txn_attr_li, ' the scaler is: ', attrScale)


                  parallel_svg.append('g').classed('suspect_value', !0);

                  // draw each value line
                  t_links.forEach(link => {
                      let tplink_svg = this.svg.selectAll('g.suspect_value').append('g')
                          .classed('path-' + t_links.indexOf(link), !0);

                      // draw value line
                      tplink_svg
                          .datum(link)
                          .append('path')
                          .attr('id', 'tp' + t_links.indexOf(link))
                          .attr('d', () => {
                              let path = 'M';
                              txn_attr_li.forEach(
                                  attr => {
                                      let attr_index = txn_attr_li.indexOf(attr);
                                      if (attr_index !== 0) {
                                          path += 'L'
                                      }
                                      path += attrScale[attr_index](link[attr]) + ',' + y_linear(attr_index)
                                  }
                              );
                              return path
                          })
                          .attr('stroke', this.cfg.parallel_panel.line_color)
                          .attr('stroke-width', 2)
                          .attr('stroke-opacity', 0.9)
                          .attr('fill', 'none')
                          .on('mouseover', () => {
                              //当鼠标放在对应的parallel线上时。该条线被高亮
                              console.log('this', this, event.target);
                              d3.select('g.path-' + event.target.id.slice(2,))
                                  .transition()
                                  .duration(50)
                                  .selectAll('path')
                                  // .attr('r',15)
                                  .attr("stroke-width", 5)
                                  .attr("opacity", this.cfg.parallel_panel.highlight_opacity);

                              d3.select('g.path-' + event.target.id.slice(2,))
                                  .selectAll('circle')
                                  .attr("opacity", this.cfg.parallel_panel.highlight_opacity);

                          })
                          .on('mouseout', () => {
                              //当鼠标移出该条取值线。该取值线恢复正常
                              d3.select('g.path-' + event.target.id.slice(2,))
                                  .transition()
                                  .duration(50)
                                  .selectAll('path')
                                  .attr("stroke-width", this.cfg.parallel_panel.default_stroke_width);

                              d3.select('g.path-' + event.target.id.slice(2,))
                                  .selectAll('circle')
                                  // .attr('r',5)
                                  .attr("opacity", this.cfg.parallel_panel.default_opacity);
                          });

                      // draw value point
                      tplink_svg.selectAll('g.suspect_value')
                          .data(
                              txn_attr_li.map(attr => {
                                  let circle_position = {};
                                  circle_position.cx = attrScale[txn_attr_li.indexOf(attr)](link[attr]);
                                  circle_position.cy = y_linear(txn_attr_li.indexOf(attr));
                                  return circle_position
                              })
                          )
                          .enter()
                          .append('circle')
                          .attr('r', 2)
                          //把点映射到坐标
                          .attr('cx', d => d.cx)
                          .attr('cy', d => d.cy)
                          .attr('fill', this.cfg.parallel_panel.node_color)
                          .attr('fill-opacity', 0.8)
                          .attr("stroke-width", this.cfg.parallel_panel.node_color)
                          .attr("stroke-opacity", 1)
                          .attr('opacity', 0.8)
                  })
                  // this.svg.selectAll().attr('transform','rotate(90deg)')

              }
          }
  }
</script>

<style scoped>

</style>