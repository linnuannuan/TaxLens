/* eslint-disable */
<template>
    <div id="detail_view" v-loading="loadingDetailGraph">

    <div id="d3Tooltip"></div>
  </div>
</template>
<script>
    import * as d3 from "d3";
    import {
        sankey as d3Sankey,
        sankeyLinkHorizontal,
        // sankeyLinkVertical
    } from 'd3-sankey'



  export default {
      name: 'DetailView',
      props: {
          affiliatedTransactionDetail:Object,
          loadingDetailGraph:Boolean,
      },
      data() {
          return {
              svg: null,
          }
      },
      watch: {
          affiliatedTransactionDetail: function () {
              this.renderGraph();
          },
      },
      mounted: function () {
          this.initGraph();
      },
      methods: {
          initGraph() {
              let width = this.$el.clientWidth/2;
              let height = this.$el.clientHeight;
              //config the node width and link width
              this.cfg = {
                  node: {
                      'min_r': 4,
                      'max_r': 10,
                      'default_width': 6,
                      'color': {
                          'in': '#ff7f0e',
                          'tp': '#1f77b4'
                      },
                      'y_base':{
                          'in': height/8,
                          'tp': height/2
                      },
                      invest_r:30
                  },
                  link: {
                      'min_width': 10,
                      'max_width': 30,
                      'color': {
                          'txn': '#1f77b4',
                          'invest': '#ff7f0e',
                      }
                  },
                  viewBox: {
                      min_x: 0,
                      min_y: 0,
                      max_x: width,
                      max_y: height,
                      margin:{left:30,height:30,top:30,bottom:30}
                  }
              };
              //设置大小
              this.svg = d3.select('#detail_view')
                  .append("svg")
                  .attr("viewBox", [0, 0, width, height])
                  .attr("width",width)
                  .attr("height",height)
                  .style("font", "12px sans-serif");
          },
          renderGraph: function () {
              /*绘制双向桑基图*/
              let chart = ({
                    // container,
                    data,
                    // margin,
                    size: { width, height },
                    nodeWidth = 10,
                    nodePadding = 20,
                    // getPopupContent = () => {},
                    onNodeClick
                }) => {
                    // select(container).select('svg').remove()
                    this.svg.selectAll("g").remove()
                    const svg = this.svg
                    // console.log(data, data.nodes, data.links)

                    // config the sankey for transaction
                    const { nodes, links } = d3Sankey()
                        .nodeId(d => d.id)
                        .nodeWidth(nodeWidth)
                        .nodePadding(nodePadding)
                        //[[x0, y0], [x1, y1]], where x0 is the left side of the extent, y0 is the top, x1 is the right and y1 is the bottom.
                        .extent([[width*0.2, this.cfg.node.y_base.tp], [width*0.8, height*0.8]])({
                            nodes: data.nodes.filter(d=>!d.in).map(d => Object.assign({}, d)),
                            // set the default value of ap_txn as 0.5
                            links: data.links.filter(d=>d.ap_txn).map(d => { d.value = 0.5 ; return Object.assign({}, d)})
                        })

                    nodes.map((d)=>{
                        d.cy = (d.y0 + d.y1) / 2
                        d.cx = (d.x0 < width / 2 ? d.x1 : d.x0)
                        d.r =  (d.y1-d.y0)/2
                        return d
                    })
                    console.log('calculate position of nodes, links:', nodes, links)

                    const color = d => {return d.tp ? this.cfg.node.color.tp: this.cfg.node.color.in}
                    // const format = d => `$${d3Format(',.0f')(d)}`
                    // const infoPopup = select('#d3Tooltip')

                    // get invest node height*0.5
                    let i_nodes = data.nodes.filter(d=>d.in)
                    let i_links = data.links.filter(d=>!d.ap_txn).map(d=>{d.value = d.in_ratio; return Object.assign({}, d)})

                    console.log('i_nodes,i_links:',i_nodes,i_links)

                    // get the position of investor based on the position of related taxpayers
                    let i_base = this.cfg.node.y_base.in
                    i_nodes.map(
                        function(d){
                            //find all investor start from a investor
                            let related_link = i_links.filter(link=>link.source == d['id'] )

                            // calculate the x position of node based the x position of related taxpayers
                            let position_x = related_link.reduce((acc, cur) => acc+nodes[nodes.findIndex(element =>element['id'] == cur.target)].x0,0) /related_link.length
                            console.log('id:',d['id'],'related_link:',related_link,'position_x',position_x)
                            d.x = position_x
                            d.y = i_base

                            d.x0 = position_x - 30
                                // - this.cfg.node.invest_r  //r=30
                            d.x1 = position_x + 30
                                // + this.cfg.node.invest_r  //r=30
                            d.y0 = i_base
                                // - this.cfg.node.invest_r  //r=30
                            d.y1 = i_base
                                // + this.cfg.node.invest_r  //r=30
                            d.r = 30
                            return d
                    })
                    console.log('get invest nodes position: ',i_nodes)
                    i_links = i_links.map(d=>{d.source = i_nodes.find(elements => elements.id == d.source), d.target = nodes.find(elements => elements.id == d.target); return Object.assign({}, d)})
                    console.log('get invest source target: ', i_links)

                    // draw investor node
                    svg.append('g')
                        .attr('stroke', '#000')
                        .selectAll('rect')
                        .data(i_nodes)
                        .enter()
                        .append('circle')
                        .attr('cx', d => d.x - this.cfg.node.invest_r)
                        .attr('cy', d => d.y)
                        .attr('r', this.cfg.node.invest_r)
                        .attr('fill', d => color(d))
                        .on('click', onNodeClick)
                        // .style('cursor', 'pointer')

                    // draw taxpayer node
                    svg.append('g')
                        .attr('stroke', '#000')
                        .selectAll('rect')
                        .data(nodes)
                        .enter()
                        .append('rect')
                        .attr("x",d => (d.x0 < width / 2 ? d.x1 : d.x0))
                        .attr("y", d => d.y0)
                        .attr("height", d => d.y1 - d.y0)
                        .attr("width", d => d.x1 - d.x0)
                        // .append('circle')
                        // .attr('cx', d => (d.x0 < width / 2 ? d.x1 : d.x0))
                        // .attr('cy', d => (d.y0 + d.y1) / 2)
                        // .attr('r', d => (d.y1-d.y0)/2)
                        .attr('fill', d => color(d))
                        .on('click', onNodeClick)
                        // .style('cursor', 'pointer')


                    const link = svg.append('g')
                        .attr('fill', 'none')
                        .attr('stroke-opacity', 0.5)
                        .selectAll('g')
                        .data(links)
                        .enter()
                        .append('g')
                        .style('mix-blend-mode', 'multiply')
                        .on('click',d=>{console.log(d)})


                    // 渐变色线段
                    // const gradient = link.append('linearGradient')
                    //     .attr('id', (d) => {
                    //         return d.id
                    //         // d.uid = guid()
                    //         // return d.uid
                    //     })
                    //     .attr('gradientUnits', 'userSpaceOnUse')
                    //     .attr('x1', d => d.source.x1)
                    //     .attr('x2', d => d.target.x0)
                    //
                    // gradient.append('stop')
                    //     .attr('offset', '0%')
                    //     .attr('stop-color', d => color(d))
                    //
                    // gradient.append('stop')
                    //     .attr('offset', '100%')
                    //     .attr('stop-color', d => color(d))

                    link.append('path')
                        .attr('d', sankeyLinkHorizontal())
                        // .attr('stroke', d => `url(#${d.uid})`)
                        .attr('stroke', this.cfg.link.color.txn)
                        .attr('stroke-width', d=>d.width)

                    const i_link = svg.append('g')
                        .attr('fill', 'none')
                        .attr('stroke-opacity', 0.5)
                        .selectAll('g')
                        .data(i_links)
                        .enter()
                        .append('g')
                        .style('mix-blend-mode', 'multiply')
                        .on('click',d=>{console.log(d)})

                    i_link.append('path')
                        // .attr('d', sankeyLinkVertical())
                        .attr('d', d =>{

                            // get link list with the same source

                            /* neglect the link width*/
                            // let i_link_with_same_source = i_links.filter(l=>l.source.id == d.source.id)
                            // since the invest ratio is based on the ratio of target node, the rate should reset for source node

                            /* neglect the link width*/
                            // let i_link_with_same_source_total_ratio = i_link_with_same_source.reduce((acc,cur)=>acc+cur.value,0)

                            // get link list with the same target
                            let i_link_with_same_target = i_links.filter(l=>l.target.id == d.target.id)
                            // console.log('current link is ',d)
                            // console.log('i_link_with_same_source',i_link_with_same_source)
                            // console.log('i_link_with_same_target',i_link_with_same_target)

                            /* consider the link width */
                            // let source_offset =  2*d.source.r*(i_link_with_same_source.slice(0,i_link_with_same_source.findIndex(e => e == d)).reduce((acc,cur)=>acc+cur.value,0))/i_link_with_same_source_total_ratio

                            /* target offset as rect */
                            let target_offset =  (d.target.x1 - d.target.x0) * (i_link_with_same_target.slice(0,i_link_with_same_target.findIndex(e => e == d)).reduce((acc,cur)=>acc+cur.value,0))

                            /* target offset as circle */
                            // let target_offset = 2*d.target.r*(i_link_with_same_target.slice(0,i_link_with_same_target.findIndex(e => e == d)).reduce((acc,cur)=>acc+cur.value,0))

                            //start point x
                            let start_point = {
                                x: d.source.x0,
                                y: d.source.y

                                // consider the link strength with width
                                // x:(d.source.x0 + source_offset),
                                // y: d.source.y
                            }
                            //control point 1
                            let control_point1 = {
                                /* control_point1 as a rect neglect the link width*/
                                x:d.source.x0,
                                y:(d.source.y + d.target.y0)/2

                                /* control_point1 as a rect consider the link width*/
                                // x:(d.source.x0 + source_offset),
                                // y:(d.source.y + d.target.y0)/2

                                /* control_point1 as a circle */
                                // x:d.source.x0 + source_offset,
                                // y:(d.source.y + d.target.cy)/2
                            }
                            //control point 2
                            let control_point2 = {
                                /* control_point2 as a rect neglect the link width*/
                                x: d.target.x0 ,
                                y:(d.source.y1 + d.target.y0)/2

                                /* control_point2 as a rect consider the link width*/
                                // x:(d.target.x0 + source_offset),
                                // y:(d.source.y1 + d.target.y0)/2

                                /* control_point2 as a circle */
                                // x:(d.target.cx - d.target.r + source_offset),
                                // y:(d.source.y1 + d.target.cy)/2
                            }
                            //left end point
                            let end_point1 = {
                                /* end point as a rect */
                                x:((d.target.x0 < width / 2 ? d.target.x1 : d.target.x0) + target_offset),
                                y:(d.target.y0)

                                /* end point as a circle */
                                // x:(d.target.cx-d.target.r + target_offset),
                                // y:(d.target.cy)
                            }
                            //right end point
                            let end_point2 = {
                                /* end point as a  rect */
                                x:((d.target.x0 < width / 2 ? d.target.x1 : d.target.x0) + target_offset),
                                y:(d.target.y0)

                                /* end point as a circle */
                                // x:((d.target.cx-d.target.r) + target_offset + (2*d.target.r * d.value)),
                                // y:(d.target.cy)
                            }
                            // control point 2 with offset
                            let right_control_point2 = {
                                /* right_control_point2 as a rect neglect the link width*/
                                x:((d.target.x0 < width / 2 ? d.target.x1 : d.target.x0)),
                                y:(d.source.y1 + d.target.y0)/2


                                /* right_control_point2 as a rect consider the link width*/
                                // x:((d.target.x0 < width / 2 ? d.target.x1 : d.target.x0) + target_offset),
                                // y:(d.source.y1 + d.target.y0)/2

                                /* right_control_point2 as a circle */
                                // x:((d.target.cx - d.target.r) + target_offset + (2*d.target.r * d.value)),
                                // y:(d.source.y1 + d.target.cy)/2
                            }
                            // control point 1 with offset
                            let right_control_point1 = {
                                /* right_control_point1 as a  rect neglect the link width*/
                                x:(d.source.x0),
                                y:(d.source.y + d.target.y0)/2


                                /* right_control_point1 as a  rect consider the link width*/
                                // x:(d.source.x0 + target_offset + (2*d.source.r * d.value)/i_link_with_same_source_total_ratio),
                                // y:(d.source.y + d.target.y0)/2

                               /* right_control_point1 as a  circle */
                                // x:(d.source.x0 + target_offset + (2*d.source.r * d.value)/i_link_with_same_source_total_ratio),
                                // y:(d.source.y + d.target.cy)/2
                            }

                            // fix the problem of inner intersection of line
                            if(control_point1.x > right_control_point1.x){
                                let t = control_point1
                                control_point1 = right_control_point1
                                right_control_point1 = t
                            }
                            if(control_point2.x > right_control_point2.x){
                                let t = control_point2
                                control_point2 = right_control_point2
                                right_control_point2 = t
                            }

                            // start point x with offset
                            let start_point2 = {
                                /* neglict the link with with link ratio */
                                x:(d.source.x0),
                                y:d.source.y

                                /* consider the link width of d.source */
                                // x:(d.source.x0 + source_offset+ (2*d.source.r * d.value)/i_link_with_same_source_total_ratio),
                                // y:d.source.y
                            }

                            return 'M'
                                // 起始点坐标：若非首个由该investor流出的边，x设置offset = i_links.slice(0,i_links.findIndex(e => e == d)).reduce((acc,cur)=>acc+cur.value,0)
                                + (start_point.x) +','+ start_point.y
                                /* 第一段弧 */
                                // 控制点1 为 investor 正下方中点坐标为起始节点圆心的平均y
                                + 'C'+ control_point1.x+','+control_point1.y
                                // 控制点2 为 investor 正下方中点坐标为起始节点圆心的平均y
                                +','+ control_point2.x+','+control_point2.y
                                // 终点  x为目标节点的 x - r
                                +','+ end_point1.x + ',' + end_point1.y
                                /* 第二段弧 */
                                // value 表示 rate
                                +'L'+ end_point2.x + ',' + end_point2.y
                                // 画C
                                // 第二个控制点右平移rate的距离
                                +'C'+ right_control_point2.x + ',' + right_control_point2.y
                                // 第一个控制点右平移rate的距离
                                + ',' + right_control_point1.x +','+ right_control_point1.y
                                + ',' + start_point2.x+','+ start_point2.y
                                + 'Z'

                        })
                        // .attr('stroke', d => `url(#${d.uid})`)
                        .attr('stroke', this.cfg.link.color.invest)
                        .attr('stroke-width', d=>d.width)
                        .attr('fill', this.cfg.link.color.invest)
                        .attr('opacity',0.5)
                        // .on('click',d=>{console.log(d)})
                        // d => Math.max(1, d.value))

                    // add text for in node
                    svg.append('g')
                        .style('font', '10px sans-serif')
                        .selectAll('text')
                        .data(i_nodes)
                        .enter()
                        .append('text')
                        .attr('x', d => (d.x0 < width / 2 ? d.x0 : d.x1 ))
                        // 名称向内显示
                        // .attr('x', d => (d.x0 < width / 2 ? d.x1 + 6 : d.x0 - 6))
                        .attr('y', d => (d.y1 + d.y0) / 2)
                        .attr('dy', '0.35em')
                        .attr('text-anchor', d => (d.x0 < width / 2 ? 'start' : 'end'))
                        .text(d => d.in_name)

                    // add text for tp node
                    svg.append('g')
                        .style('font', '10px sans-serif')
                        .selectAll('text')
                        .data(nodes)
                        .enter()
                        .append('text')
                        .attr('x', d => (d.x0 < width / 2 ? d.x1 + 6 : d.x0 - 6))
                        .attr('y', d => (d.y1 + d.y0) / 2)
                        .attr('dy', '0.35em')
                        .attr('text-anchor', d => (d.x0 < width / 2 ? 'start' : 'end'))
                        .text(d => d.tp_name)
                         return svg.node()

                }
                chart({
                    container:'#detail_view',
                    // data:{
                    //     "directed": true,
                    //     "multigraph": false,
                    //     "graph": {
                    //       "num_ap_txn": 1,
                    //       "num_tp": 3,
                    //       "num_in": 2
                    //     },
                    //     "nodes": [
                    //       {
                    //         "in": false,
                    //         "tp": true,
                    //         "tp_name": "西安亚欣航空机械制造有限公司",
                    //         "lr_name": "罗湖平",
                    //         "pc": "710089",
                    //         "business": "许可经营项目：（上述经营范围涉及许可经营项目的，凭许可证明文件或批准证书在有效期内经营，未经许可不得经营）一般经营项目：机械零部件、非标设备的设计、生产、安装、销售；航材销售***（以上经营范围不含国家规定的专控及前置许可项目、禁止项目）",
                    //         "capital": 1000000.0,
                    //         "employee": 8.0,
                    //         "industry": "机械零部件加工",
                    //         "id": "610114091651625"
                    //       },
                    //       {
                    //         "in": false,
                    //         "tp": true,
                    //         "tp_name": "西安弗莱航空机械制造有限公司",
                    //         "lr_name": "张晓庆",
                    //         "pc": "710089",
                    //         "business": "机械零组件及非标设备的设计、生产、销售；航材销售**（以上经营范围凡涉及国家有专项专营规定的从其规定）",
                    //         "capital": 500000.0,
                    //         "employee": 12.0,
                    //         "industry": "其他通用设备制造业",
                    //         "id": "610181698600875"
                    //       },
                    //       {
                    //         "tp": true,
                    //         "in": true,
                    //         "tp_name": "西安市阎良区弗航机械加工厂",
                    //         "lr_name": "张晓庆",
                    //         "pc": "710089",
                    //         "business": "一般经营项目：机械零部件加工***（未取得专项许可的项目除外）",
                    //         "capital": NaN,
                    //         "employee": NaN,
                    //         "industry": "机械零部件加工",
                    //         "in_name": "张晓庆",
                    //         "in_entity": "510",
                    //         "id": "610114198406243541"
                    //       },
                    //       {
                    //         "tp": false,
                    //         "in": true,
                    //         "in_name": "罗湖平",
                    //         "in_entity": "510",
                    //         "id": "610114197501230015"
                    //       }
                    //     ],
                    //     "links": [
                    //       {
                    //         "ap_txn": true,
                    //         "source": "610114091651625",
                    //         "target": "610181698600875"
                    //       },
                    //       {
                    //         "in_ratio": 0.8,
                    //         "source": "610114198406243541",
                    //         "target": "610181698600875"
                    //       },
                    //       {
                    //         "in_ratio": 1.0,
                    //         "source": "610114197501230015",
                    //         "target": "610114091651625"
                    //       },
                    //       {
                    //         "in_ratio": 0.2,
                    //         "source": "610114197501230015",
                    //         "target": "610181698600875"
                    //       }
                    //     ]
                    //   },
                    // data: (copy_data !== null)? copy_data:{
                    //     "directed": true,
                    //     "multigraph": false,
                    //     "graph": {
                    //       "num_ap_txn": 1,
                    //       "num_tp": 3,
                    //       "num_in": 2
                    //     },
                    //     "nodes": [
                    //       {
                    //         "in": false,
                    //         "tp": true,
                    //         "tp_name": "西安亚欣航空机械制造有限公司",
                    //         "lr_name": "罗湖平",
                    //         "pc": "710089",
                    //         "business": "许可经营项目：（上述经营范围涉及许可经营项目的，凭许可证明文件或批准证书在有效期内经营，未经许可不得经营）一般经营项目：机械零部件、非标设备的设计、生产、安装、销售；航材销售***（以上经营范围不含国家规定的专控及前置许可项目、禁止项目）",
                    //         "capital": 1000000.0,
                    //         "employee": 8.0,
                    //         "industry": "机械零部件加工",
                    //         "id": "610114091651625"
                    //       },
                    //       {
                    //         "in": false,
                    //         "tp": true,
                    //         "tp_name": "西安弗莱航空机械制造有限公司",
                    //         "lr_name": "张晓庆",
                    //         "pc": "710089",
                    //         "business": "机械零组件及非标设备的设计、生产、销售；航材销售**（以上经营范围凡涉及国家有专项专营规定的从其规定）",
                    //         "capital": 500000.0,
                    //         "employee": 12.0,
                    //         "industry": "其他通用设备制造业",
                    //         "id": "610181698600875"
                    //       },
                    //       {
                    //         "tp": true,
                    //         "in": true,
                    //         "tp_name": "西安市阎良区弗航机械加工厂",
                    //         "lr_name": "张晓庆",
                    //         "pc": "710089",
                    //         "business": "一般经营项目：机械零部件加工***（未取得专项许可的项目除外）",
                    //         "capital": NaN,
                    //         "employee": NaN,
                    //         "industry": "机械零部件加工",
                    //         "in_name": "张晓庆",
                    //         "in_entity": "510",
                    //         "id": "610114198406243541"
                    //       },
                    //       {
                    //         "tp": false,
                    //         "in": true,
                    //         "in_name": "罗湖平",
                    //         "in_entity": "510",
                    //         "id": "610114197501230015"
                    //       }
                    //     ],
                    //     "links": [
                    //       {
                    //         "ap_txn": true,
                    //         "source": "610114091651625",
                    //         "target": "610181698600875"
                    //       },
                    //       {
                    //         "in_ratio": 0.8,
                    //         "source": "610114198406243541",
                    //         "target": "610181698600875"
                    //       },
                    //       {
                    //         "in_ratio": 1.0,
                    //         "source": "610114197501230015",
                    //         "target": "610114091651625"
                    //       },
                    //       {
                    //         "in_ratio": 0.2,
                    //         "source": "610114197501230015",
                    //         "target": "610181698600875"
                    //       }
                    //     ]
                    //   },
                    // data: copy_data,
                    data:this.affiliatedTransactionDetail,
                    size: { width:this.$el.clientWidth/2, height:this.$el.clientHeight},
                    onNodeClick:d => { console.log('click on :', d) }
                })

    }
  }}
</script>
<style scoped>
</style>
