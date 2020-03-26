/* eslint-disable */
<template>
  <div id="relation_structure" v-loading="loadingGraph"></div>
</template>
<script>
  import * as d3 from "d3";
  // import EventService from "../utils/event-service";

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
    },
    methods: {
      // getDetailTransactionView(source, target) {
      //   console.log('click to get detail tran:', ' source: ', source, 'target: ', target)
      //   EventService.emitAffiliatedTransactionSelected(source, target);
      // },
      initGraph() {
        let width = this.$el.clientWidth;
        let height = this.$el.clientHeight;
        let margin_width = width/50
        let margin_height = height/30

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
              max_height : height - margin_height
          }
        };
        this.svg = d3.select('#relation_structure')
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
        // function drag(simulation) {
        //   function dragStarted(d) {
        //     if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        //     d.fx = d.x;
        //     d.fy = d.y;
        //   }
        //
        //   function dragged(d) {
        //     d.fx = d3.event.x;
        //     d.fy = d3.event.y;
        //   }
        //
        //   function dragEnded(d) {
        //     if (!d3.event.active) simulation.alphaTarget(0);
        //     d.fx = null;
        //     d.fy = null;
        //   }
        //
        //   return d3.drag()
        //     .on("start", dragStarted)
        //     .on("drag", dragged)
        //     .on("end", dragEnded);
        // }
        //
        // function linkArc(d) {
        //   const r = Math.hypot(d.target.x - d.source.x, d.target.y - d.source.y);
        //   return `
        //             M${d.source.x},${d.source.y}
        //             A${r},${r} 0 0,1 ${d.target.x},${d.target.y}
        //           `;
        // }
        this.svg.selectAll("g").remove()
        if (this.affiliatedPartyDetail !== null) {
          let data = this.affiliatedPartyDetail;
          // let get_node_link_chart = (data)=>{
          //   let link_by_src = {}
          //   let link_by_dst = {}
          //
          // data.nodes.forEach(node => {
          //   link_by_src[node['id']]={'children':[]}
          //   link_by_dst[node['id']]={'parent':[]}
          // });
          //
          // const links = data.links.map(link => {
          //   link.type = link.in_ratio? 'invest' : 'txn';
          //   link.value = link.in_ratio? (1/link.in_ratio): 0.5;
          //   link_by_src[link.source]['children'].push(link)
          //   link_by_dst[link.target]['parent'].push(link)
          //   return Object.create(link)
          // });
          //
          // const nodes = data.nodes.map(node => {
          //   node.type = node.in ? 'investor' : 'taxpayer';
          //   // node.value = link_by_src[node['id']]['children'].filter(d=>d['ap_txn'])
          //   return Object.create(node)
          // });
          //
          // let types = Array.from(new Set(links.map(d => d.type)));
          //
          // let industrys =  Array.from(new Set(nodes.filter(d=>!d.in).map( d => d['industry'])));
          // let color = d3.scaleOrdinal(industrys, d3.schemeSet3);
          //
          // // schemeCategory10: 1f77b4,ff7f0e ,2ca02c,d62728,9467bd,8c564b,e377c2,7f7f7f,bcbd22,17becf
          // // let color = d3.scaleOrdinal(types, d3.schemeCategory10);
          //
          // // node capital encoding
          // let rScale = d3.scaleLinear()
          //   .domain([d3.min(nodes, function(d){ return d['capital']; }), d3.max(data.nodes, function(d){ return d['capital']; })])
          //   .range([this.cfg.node.min_r, this.cfg.node.max_r]);
          //
          // // node suspect value encoding
          // // let rScale = d3.scaleLinear()
          // //   .domain([d3.min(nodes, function(d){ return d['ap_txn_amount']; }), d3.max(data.nodes, function(d){ return d['ap_txn_amount']; })])
          // //   .range([this.cfg.node.min_r, this.cfg.node.max_r]);
          //
          // // invest node suspect value encoding
          // let irScale = d3.scaleLinear()
          //   .domain([d3.min(nodes, function(d){ return d['suspect_value']; }), d3.max(data.nodes, function(d){ return d['suspect_value']; })])
          //   .range([this.cfg.node.min_r, this.cfg.node.max_r]);
          //
          //
          // // link stength encoding
          // let lScale = d3.scaleLinear().domain([0,1]).range([this.cfg.link.min_width, this.cfg.link.max_width]);
          //
          // // trade link strength encoding
          // let oScale = d3.scaleLinear()
          //     .domain([d3.min(nodes, function(d){ return d['ap_txn_amount']; }),d3.max(nodes, function(d){ return d['ap_txn_amount']; })])
          //     .range([0,1]);
          //
          //
          // const simulation = d3.forceSimulation(nodes)
          //   .force("link", d3.forceLink(links).id(d => d.id))
          //   .force("charge", d3.forceManyBody().strength(-500))
          //   .force("x", d3.forceX())
          //   .force("y", d3.forceY());
          //
          // this.svg.selectAll("g").remove();
          //
          // // Per-type markers, as they don't inherit styles.
          // this.svg.append("g").selectAll("marker")
          //   .data(types)
          //   .enter()
          //   .append('marker')
          //   .attr("id", d => `arrow-${d}`)
          //   .attr("viewBox", "0 -5 10 10")
          //   .attr("refX", 15)
          //   .attr("refY", -0.5)
          //   .attr("markerWidth", 6)
          //   .attr("markerHeight", 6)
          //   .attr("orient", "auto")
          //   .append("path")
          //   .attr("fill", d=> this.cfg.link.color[d])
          //   .attr("d", "M0,-5L10,0L0,5");
          //
          // const link = this.svg.append("g")
          //   .attr("fill", "none")
          //   .selectAll("path")
          //   .data(links)
          //   .enter()
          //   .append('path')
          //   .attr("stroke", d => d.type == 'invest'? this.cfg.link.color.invest:this.cfg.link.color.txn)
          //   .attr("stroke-width", d => lScale(d.value))
          //   .attr('opacity', d => d.type == 'invest'? 1/d.value:oScale(d['ap_txn_amount']))
          //   // link 线段终止坐标待计算
          //   .attr("marker-end", d => `url(${new URL(`#arrow-${d.type}`, location)})`)
          //   .on('click',function (d) {
          //       console.log('click on d where source = ',d.source,'target = ',d.target)
          //       EventService.emitAffiliatedTransactionSelected(d.source.id,d.target.id);
          //       // this.getDetailTransactionView(d.source,d.target)
          //   })
          //
          //  const node = this.svg.append("g")
          //   .attr("fill", "currentColor")
          //   .attr("stroke-linecap", "round")
          //   .attr("stroke-linejoin", "round")
          //   .selectAll("g")
          //   .data(nodes)
          //   .enter()
          //   .append('g')
          //   .call(drag(simulation));
          //
          // // const in_node = this.svg.append("g")
          // //   .attr("fill", "currentColor")
          // //   .attr("stroke-linecap", "round")
          // //   .attr("stroke-linejoin", "round")
          // //   .selectAll("g")
          // //   .data(nodes.filter(d=>!d.tp))
          // //   .enter()
          // //   .append('g')
          // //   .call(drag(simulation));
          // //
          // // const tp_node = this.svg.append("g")
          // //   .attr("fill", "currentColor")
          // //   .attr("stroke-linecap", "round")
          // //   .attr("stroke-linejoin", "round")
          // //   .selectAll("g")
          // //   .data(nodes.filter(d=>d.tp))
          // //   .enter()
          // //   .append('g')
          // //   .call(drag(simulation));
          //
          //   node.append("circle")
          //   .attr("stroke", d=>d['in']?'white':color(d['industry']))
          //   // .attr("fill", d=>color(d['industry']))
          //   .attr("fill", d=>d['in']? this.cfg.node.color.in:this.cfg.node.color.tp)
          //   .attr("stroke-width", 1.5)
          //   .attr("r", d => d['in'] ? irScale(d['suspect_value']): rScale(d['capital']))
          //   .on('click',function (d) {
          //     console.log('click :',d)
          //   })
          //
          // // transfer node into circle and rectangle
          // // in_node.append("circle")
          // //   .attr("stroke", d=>d['in']?'white':color(d['industry']))
          // //   // .attr("fill", d=>color(d['industry']))
          // //   .attr("fill", d=>d['in']? this.cfg.node.color.in:this.cfg.node.color.tp)
          // //   .attr("stroke-width", 1.5)
          // //   .attr("r", d => d['in'] ? irScale(d['suspect_value']): rScale(d['capital']))
          // //   .on('click',function (d) {
          // //     console.log('click :',d)
          // //   })
          // //   // .on("mouseover", function(){return this.tooltip.style("visibility", "visible");})
          // //   // .on("mousemove", function(){return this.tooltip.style("top", (event.pageY-800)+"px").style("left",(event.pageX-800)+"px");})
          // //   // .on("mouseout", function(){return this.tooltip.style("visibility", "hidden");});
          // //
          // //  tp_node.append("rect")
          // //   .attr("stroke", d=>color(d['industry']))
          // //   .attr("fill", d=>color(d['industry']))
          // //   // .attr("fill", this.cfg.node.color.tp)
          // //   .attr("stroke-width", 1.5)
          // //   .attr("width", d=>rScale(d['capital']))
          // //   .attr("height", d=>rScale(d['capital']))
          // //   // .attr("x", d=>rScale(d['capital']))
          // //   .on('click',function (d) {
          // //     console.log('click :',d)
          // //   })
          //
          //
          // node.append("text")
          //   .attr("x", 8)
          //   .attr("y", "0.31em")
          //   .text(d => {
          //     return d.in? d.in_name: d.tp_name;
          //   })
          //   .clone(true).lower()
          //   .attr("fill", "none")
          //   .attr("stroke", "white")
          //   .attr("stroke-width", 3);
          //
          //
          // simulation.on("tick", () => {
          //   link.attr("d", linkArc);
          //   node.attr("transform", d => `translate(${d.x},${d.y})`);
          //   // tp_node.attr("transform", d => `translate(${d.x-3},${d.y-3})`);
          // });
          //     console.log('',data)
          // }

          let get_new_layout = (data)=> {
              console.log('input data: ',data)

              let t_nodes = data.nodes.filter(d=>!d.in)
              let t_links = data.links.filter(d=>d.ap_txn)
              console.log('t_nodes , t_links: ', t_nodes, t_links)
              t_links = t_links.map(d=>{
                  console.log('check t link:', d.source, d.target)
                  if(d.throw){d= null;return d}
                  //如果存在互相交易的边
                  if(t_links.find(link=> link.target == d.source && link.source == d.target)){
                     //若当前方向ap txn amount < 反向link ap txn amount
                     if((t_links.find(link=> link.target == d.source && link.source == d.target).ap_txn_amount) > d.ap_txn_amount){
                       // 保留差值为正的边
                        t_links.find(link=> link.target == d.source && link.source == d.target).ap_txn_amount = t_links.find(link=> link.target == d.source && link.source == d.target).ap_txn_amount - d.ap_txn_amount
                        //设置互相交易标志true
                        t_links.find(link=> link.target == d.source && link.source == d.target).bi_direct = true
                        //保留差值用于绘图
                        t_links.find(link=> link.target == d.source && link.source == d.target).amount_offset = d.ap_txn_amount
                        // console.log('reset this link',d)
                         d = null
                     }
                     //若当前方向ap txn amount > 反向link ap txn amount
                     else{
                         d.ap_txn_amount = d.ap_txn_amount - t_links.find(link=> link.target == d.source && link.source == d.target).ap_txn_amount
                         d.bi_direct = true
                         d.amount_offset = t_links.find(link=> link.target == d.source && link.source == d.target).ap_txn_amount
                         t_links.find(link=> link.target == d.source && link.source == d.target).throw = true
                         // console.log('delete link:', t_links)
                     }
                   }
                  return d
              }).filter(d=>!!d)

              //计算互相交易
              t_nodes.map(d=>{
                  d.lay_index = 1
                  d.sourceLinks = t_links.filter(link=>link.source == d.id)
                  d.targetLinks = t_links.filter(link=>link.target == d.id)
              })
              console.log('---- t_nodes,t_links:', t_nodes, t_links)

              /* calculate the lay index of taxpayer */
              let min_lay_index = 0

              console.log('get_position of t nodes:',t_nodes)

              function  get_position(t_nodes,t_links,c_lay_index,node) {
                  //从0开始
                  console.log('current loop: ','node: ', node,'lay_index: ', c_lay_index)
                  if(c_lay_index < min_lay_index){
                     min_lay_index = c_lay_index
                  }
                  node.forEach (node=>{
                         //根据targetlink决定当前的lay-index  根据sourcelink决定之后的lay_index
                         //当当前的node的lay_index未设置，或设值的偏大，需前移选择最大的 lay_index
                         if( (node.lay_index == 1)|| (c_lay_index < node.lay_index)){
                             // 设置当前节点的lay index
                             t_nodes.find(d=> d.id == node.id).lay_index = c_lay_index
                             // 更改他的前向节点的lay index
                             console.log('set previous node', node.targetLinks, t_nodes, t_links)
                             let previous_node_li = node.targetLinks.map(link=> t_nodes.find(d => d.id == link.source))
                             if( previous_node_li.length >0 ){
                                     return get_position(t_nodes,t_links,c_lay_index-1, previous_node_li)
                             }
                         }
                         else{
                             // console.log('current node: ',node,' index: ', c_lay_index)
                         }
                  })
              }
              get_position(t_nodes, t_links, 0, t_nodes.filter(node=>node.sourceLinks.length==0 && node.targetLinks.length!=0))

              var x_position = d3.scaleLinear()
                  .domain([d3.min(t_nodes.map(d=>d.lay_index)), d3.max(t_nodes.map(d=>d.lay_index))])
                  .range([this.cfg.trade_panel.min_width, this.cfg.trade_panel.max_width])

              // draw transaction panel
              let trade_panel_svg = this.svg.append('g')
                        .classed('trade_panel',!0)

              /* draw t node */
              for(let i = min_lay_index; i<=1; i++){

                // get node list of current lay
                let node_li = t_nodes.filter(d => d.lay_index === i)
                // console.log('lay index: ',i, 'node_li: ', node_li)

                //垂直高度
                let y_position = d3.scaleLinear()
                      .domain([0, node_li.length])
                      .range([this.cfg.trade_panel.min_height, this.cfg.trade_panel.max_height])

                // calculate the position of each node
                node_li.forEach(node=>{
                    let t_node = t_nodes[t_nodes.indexOf(node)]
                    t_node.width = 30
                    t_node.height = 30
                    t_node.x0= x_position(t_node.lay_index);
                    t_node.x1= t_node.x0 + t_node.width;
                    t_node.y0= y_position(node_li.indexOf(t_node));
                    t_node.y1= t_node.y0 + t_node.width ;
                })

                // draw each node
                trade_panel_svg
                        .append('g')
                        .attr('stroke', '#000')
                        .selectAll('rect')
                        .data(node_li)
                        .enter()
                        .append('rect')
                        .attr('width', d=>d.width)
                        .attr('height', d=>d.height)
                        .attr('x',d=> d.x0)
                        .attr('y',d=> d.y0)
                        // .attr('stroke-width',5)
                        .attr('fill',this.cfg.node.color.tp)
                        .on('click',d=>{console.log('click on: ',d)})

                /* add text of each node */
                trade_panel_svg
                        .append('g')
                        .style('font', '10px sans-serif')
                        .selectAll('text')
                        .data(node_li)
                        .enter()
                        .append('text')
                        .attr('x',d=> (d.x1<(this.cfg.trade_panel.max_width/2))? d.x1+10 : d.x0-100)
                        .attr('y',d=> d.y0 + 15)
                        .attr('dy', '0.35em')
                        .text(d => d.tp_name);

              }

              /* draw t link */
              trade_panel_svg
                    .append('g')
                    .classed('trade_link', !0)
                    .attr('fill', 'none')
                    .selectAll('g')
                    .data(t_links)
                    .enter()
                    .append('path')
                    .attr('d', d=>{
                        // set config
                        let strokeWidth = this.cfg.node.strokeWidth
                        // get the source node and target node
                        let source_node = t_nodes.find(node => node.id == d.source)
                        let target_node = t_nodes.find(node => node.id == d.target)
                        console.log('draw link: ',d, 'source:', source_node,' target:', target_node)

                        // if(source_node.x1<target_node.x0){
                        // }
                        let control_point1 = {
                            x:(source_node.x1 + target_node.x0)/2,
                            y: source_node.y0
                        }
                        let control_point2 = {
                            x:(source_node.x1 + target_node.x0)/2,
                            y:target_node.y0
                        }
                        let right_control_point1 = {
                            x:(source_node.x1 + target_node.x0)/2,
                            y: source_node.y1
                        }
                        let right_control_point2 = {
                            x:(source_node.x1 + target_node.x0)/2,
                            y:target_node.y1
                        }

                        let path_d = 'M'
                                + ((source_node.x1)+ strokeWidth) +','+ source_node.y0
                                /* 第一段弧 */
                                // 控制点1 为 investor 正下方中点坐标为起始节点圆心的平均y
                                + 'C'+ control_point1.x +','+control_point1.y
                                // 控制点2 为 investor 正下方中点坐标为起始节点圆心的平均y
                                +','+ control_point2.x +','+control_point2.y
                                // 终点  x为目标节点的 x - r
                                +','+ (target_node.x0 - strokeWidth) + ',' + target_node.y0
                                /* 第二段弧 */
                                // value 表示 rate
                                +'L'+ (target_node.x0 - strokeWidth) + ',' + target_node.y1
                                // 画C
                                // 第二个控制点右平移rate的距离
                                +'C'+ right_control_point2.x + ',' + right_control_point2.y
                                // 第一个控制点右平移rate的距离
                                + ',' + right_control_point1.x +','+ right_control_point1.y
                                + ',' + source_node.x1+','+ source_node.y1
                                + 'Z'
                        console.log('path: ',path_d)
                        return path_d
                    })
                    .attr('stroke-opacity', 0.5)
                    .attr('stroke',this.cfg.link.color.txn)
                    .attr('fill',this.cfg.link.color.txn)
                    .attr('opacity', 0.5)
                    .on('mouseover', d=>{
                        //当鼠标放在交易上时，对应的交易信息在parallel视图中被高亮
                        d3.select('#tp'+t_links.indexOf(d))
                            .transition()
                            .duration(50)
                            .attr("stroke-width",5)
                            .attr('opacity',0.8);

                        //当鼠标放在交易上时，处本交易以外，其他关联交易透明度降低。
                        d3.selectAll('g.trade_link')
                            .selectAll('path')
                            .attr('opacity',0.2)
                        d3.select(event.target).attr('opacity',1)

                        //对应的invest_path高亮
                        console.log(d)
                        console.log('invest paths',d.path)
                        for(let path_id in d.path){
                            console.log('iterator to path: ',  d.path[path_id])
                            for( let node_id in d.path[path_id]){
                                console.log('iterate for node id as :', node_id,' node:', d.path[path_id][node_id])
                                d3.select('g.invest_link').attr('opacity',0.7)
                                if(node_id < (d.path[path_id].length-1)){
                                    // highlight correspond link (undirect link)
                                    d3.select('g.invest_link #in-'+ d.path[path_id][node_id]+'-'+d.path[path_id][parseInt(node_id)+parseInt(1)])
                                        .attr('opacity',1)
                                        .attr('stroke-width',5)
                                    d3.select('g.invest_link #in-'+ d.path[path_id][parseInt(node_id)+parseInt(1)]+'-'+d.path[path_id][node_id])
                                        .attr('opacity',1)
                                        .attr('stroke-width',5)
                                }
                                // highlight correspond node
                                d3.select('g.invest_node #in-'+ d.path[path_id][node_id])
                                        .attr('opacity',1)
                                        .attr('stroke-width',5)
                            }
                        }


                    })
                    .on('mouseout', d=>{
                        //当鼠标放在交易上时，对应的交易信息在parallel视图中被取消高亮
                        d3.select('#tp'+t_links.indexOf(d))
                            .transition()
                            .duration(50)//当鼠标放在矩形上时，矩形变成黄色
                            .attr("stroke-width",2)
                            .attr('opacity',0.5);

                        // All trade path
                        d3.selectAll('g.trade_link').attr('opacity',0.5)

                        //当鼠标放在交易上时，处本交易以外，其他关联交易透明度降低。
                        d3.selectAll('g.trade_link')
                            .selectAll('path')
                            .attr('opacity',0.2)
                        d3.select(event.target).attr('opacity',1)

                        //对应的invest_path取消高亮
                        d3.select('g.invest_link').attr('opacity',1)
                        for(let path_id in d.path){
                            for( let node_id in d.path[path_id]){
                                if(node_id < d.path[path_id].length-1){
                                    // cancel highlight correspond link
                                    // undirect link
                                    d3.select('g.invest_link #in-'+ d.path[path_id][node_id]+'-'+d.path[path_id][parseInt(node_id)+parseInt(1)])
                                        .attr('opacity',1)
                                        .attr('stroke-width',2)

                                    d3.select('g.invest_link #in-'+ d.path[path_id][parseInt(node_id)+parseInt(1)]+'-'+d.path[path_id][node_id])
                                        .attr('opacity',1)
                                        .attr('stroke-width',2)
                                }
                                // cancel highlight correspond node
                                d3.select('g.invest_node #in-'+ d.path[path_id][node_id])
                                        .attr('opacity',1)
                                        .attr('stroke-width',2)
                            }
                        }
                    })



              let invest_panel_svg = this.svg.append('g')
                        .classed('invest_panel',!0)
              /* draw i node */
              let i_nodes = data.nodes.filter(d=>d.in)
              i_nodes = i_nodes.map(
                  d=>{
                      console.log('calculate i node position  ', d)
                      d.sourceLinks = data.links.filter(link=>link.source == d.id)
                      d.targetLinks = data.links.filter(link=>link.target == d.id)
                      d.to_calulate = []

                      let accumulate_x = 0
                      d.sourceLinks.forEach(link=>{
                          // console.log(link,t_nodes.find(n => n.id == link.target))
                          if(!t_nodes.find(n => n.id == link.target)){

                            console.log('find ',link.target,' from i_node:',i_nodes,i_nodes.find(n => n.id == link.target))
                            // 存在二级投资，暂不考虑二级投资的x值
                            let target_node = i_nodes.find(n => (n.id == link.target))

                            //如果当前投资的节点仍为投资点，
                            // 判断 该投资点是否算过坐标？
                            if(target_node.x){
                                // 算过则直接计算
                                accumulate_x += target_node.x
                                d.y =  target_node.y+1
                            }
                            else{
                               // 没算过则保留taregt id，后面再算
                               d.to_calulate.push(link.target)
                            }
                          }
                          else{
                            //  target node是trader
                            accumulate_x += t_nodes.find(n => n.id == link.target).x0
                            d.y = 0
                          }
                      })
                      d.x = accumulate_x / (d.sourceLinks.length - d.to_calulate.length)

                      if(d.to_calulate.length){
                          console.log('!!!!!! remained to calculate! ', d.to_calulate)
                      }
                      return d
                  }
              )


              console.log('calculating i node:',i_nodes)
              while( i_nodes.filter(d=>d.to_calulate.length>0).length>0 ){
                  //存在尚未计算x的i_node
                  i_nodes.filter(d=>d.to_calulate.length>0).map(
                      r_node=>{
                          let accumulate_x = 0
                          let calculated_count = 0
                          r_node.to_calulate.forEach(node_id=>{
                              console.log('to calculate the node',node_id)
                              console.log('get node from i_nodes',i_nodes,  i_nodes.find(n=>n.id == node_id))
                              let target_node = i_nodes.find(n=>n.id == node_id)
                              if(target_node.to_calulate.length==0){
                                  accumulate_x += target_node.x
                                  r_node.to_calulate.splice(r_node.to_calulate.findIndex(item => item === node_id), 1)
                                  calculated_count++
                              }
                          })
                          r_node.x = (r_node.x + accumulate_x)/(calculated_count+1)
                      }
                  )
              }

              i_nodes.filter(d=>d.targetLinks.length== 0 ).map(
                  node =>{
                    node.y_layindex = 1
                  })
              i_nodes.filter(d=>d.targetLinks.length> 0).map(
                  node =>{
                    node.y_layindex = node.targetLinks.reduce((acc,cur) => i_nodes.find(d => d.id==cur.source).y_layindex > acc ? i_nodes.find(d => d.id==cur.source).y_layindex:acc, 0) + parseInt(1)
                  }
              )
               // fix the overlapping problem of invest nodes.
              i_nodes= i_nodes.sort( function(a,b){ return a.x - b.x } )
              for (let i = 0 ; i < i_nodes.length - 1;i++){
                    //若两个相邻的x差值超过invest的Node的直径, 存在overlapping
                    if( ((i_nodes[i+1].x - i_nodes[i].x) < (2*this.cfg.node.invest_r)) && (i_nodes[i+1].y_layindex == i_nodes[i].y_layindex) ){
                        // 设置investor之间的最小margin为h
                        // 当下一个investor的坐标大于最大宽度时前移该节点
                        if(i_nodes[i].x + 2*this.cfg.node.invest_r + 5 > this.cfg.invest_panel.max_width){
                            i_nodes[i].x = i_nodes[i].x - 2*this.cfg.node.invest_r - 5
                        }
                        else{
                            i_nodes[i+1].x = i_nodes[i].x + 2*this.cfg.node.invest_r + 5
                        }
                    }
              }
              console.log('After calculating the position of i node: ', i_nodes)

              var in_y__position = d3.scaleLinear()
                  .domain([d3.min(i_nodes.map(d=>d.y_layindex)), d3.max(i_nodes.map(d=>d.y_layindex))])
                  .range([this.cfg.invest_panel.min_height, this.cfg.invest_panel.max_height])
              i_nodes.map(d=>{
                  d.y = in_y__position(d.y_layindex)
                  return d
              })


              let i_links = data.links.filter(d=>!d.ap_txn)

              // draw invest node
              invest_panel_svg.append('g')
                        .classed('invest_node',!0)
                        .attr('stroke', '#000')
                        .selectAll('circle')
                        .data(i_nodes)
                        .enter()
                        .append('circle')
                        .attr('id',d=>'in-'+d.id)
                        .attr('cx', d=>d.x)
                        .attr('cy', d=>d.y)
                        .attr('r',this.cfg.node.invest_r)
                        .attr('fill',this.cfg.node.color.in)
                        .on('click',d=>{console.log('click on: ',d)})

              // draw invest link
              invest_panel_svg.append('g')
                    .classed('invest_link',!0)
                    .attr('fill', 'none') // to avoid fill the path
                    .attr('opacity', 1)
                    .selectAll('g')
                    .data(i_links)
                    .enter()
                    // .append('g')
                    .append('path')
                    .attr('id',d=>'in-'+d.source+'-'+d.target)
                    .attr('d', d=>{
                        // set config
                        // let strokeWidth = this.cfg.node.strokeWidth
                        // get the source node and target node
                        let source_node = i_nodes.find(node => node.id == d.source)
                        let target_node = (t_nodes.concat(i_nodes)).find(node => node.id == d.target)
                        console.log('draw invest link: ',d, 'source:', source_node,' target:', target_node)
                        if(!target_node.in){
                            target_node.x = (target_node.x0 + target_node.x1)/2
                            target_node.y = (target_node.y0 + target_node.y1)/2
                        }

                        let control_point1 = {
                            x: source_node.x,
                            y: (source_node.y + target_node.y)/2,
                        }
                        let control_point2 = {
                            x: target_node.x,
                            y: (source_node.y+ target_node.y)/2,
                        }
                        let path_d = 'M'
                                + source_node.x +','+ source_node.y
                                /* 第一段弧 */
                                // 控制点1 为 investor 正下方中点坐标为起始节点圆心的平均y
                                + 'C'+ control_point1.x +','+control_point1.y
                                // // 控制点2 为 investor 正下方中点坐标为起始节点圆心的平均y
                                +','+ control_point2.x +','+control_point2.y
                                +','+ (target_node.x) + ',' + target_node.y
                                // + 'Z'
                        console.log('path',path_d)
                        return path_d
                    })
                    .attr('stroke',this.cfg.link.color.invest)
                    .attr('stroke-opacity', 0.5)
                    // .attr('fill',this.cfg.link.color.invest)

              /* get text of each invest node*/
              invest_panel_svg
                        .append('g')
                        .classed('invest_text',!0)
                        .style('font', '10px sans-serif')
                        .selectAll('text')
                        .data(i_nodes)
                        .enter()
                        .append('text')
                        .attr('x',d=> d.x - this.cfg.node.invest_r)
                        // .attr('x',d=> d.x>(this.cfg.invest_panel.max_width/2)?d.x+20:d.x-50)
                        .attr('y',d=> d.y - 30)
                        .attr('dy', '0.35em')
                        .text(d => d.in_name);

              // draw the parallel chart
              let txn_attr_li = ['related strength', 'transaction strength', 'tax burden deviation', 'tb variation deviation', 'net profit deviation', 'np variation deviation', 'elastic deviation']
              let parallel_svg = this.svg.append('g').classed('parallel',!0)

               // 坐标系的位置映射
              let y_linear = d3.scaleLinear()
                                .domain([0,txn_attr_li.length])
                                .range([this.cfg.parallel_panel.min_height, this.cfg.parallel_panel.max_height])

              // mock the attr value for each tp link
              t_links = t_links.map(d=>{
                  txn_attr_li.forEach(attr => d[attr] = 1000*Math.random())
                  return d
              })
              // console.log('After generating the suspect value of t link: ',t_links)

              //创建每个轴的比例尺
              let attrScale=[]
              txn_attr_li.forEach(
                  d=>{
                      let parallel_attr_svg = parallel_svg.append('g').classed(d,!0)
                      let dataset = t_links.map(link=>link[d])
                      // console.log('dataset: ',dataset)
                      // dataset
                      // 定义比例尺
                      let c_attrScale = d3.scaleLinear()
                                      .domain([0, d3.max(dataset)])
                                      .range([this.cfg.parallel_panel.min_width + 10, this.cfg.parallel_panel.max_width - 10]);
                      // 添加坐标轴
                      parallel_attr_svg.append("g")
                            .classed('x_axis',!0)
                            .attr("transform","translate(0,"+ y_linear(txn_attr_li.indexOf((d))) +")")
                            .call(d3.axisBottom(c_attrScale))

                      // 添加坐标轴属性的名称
                      parallel_attr_svg.append('g')
                            .classed('p_text',!0)
                            .selectAll('g.p_text')
                            .data(txn_attr_li)
                            .enter()
                            .append('text')
                            .attr('x', this.cfg.parallel_panel.min_width - 10 )
                            .attr('y', d => y_linear(txn_attr_li.indexOf((d)))-10 )
                            .text(d=>d)

                      // 把比例尺保留方便绘值
                      attrScale.push(c_attrScale)
                  }
              )
              // console.log('the parallel x axis: ', txn_attr_li, ' the scaler is: ', attrScale)


              parallel_svg.append('g').classed('suspect_value',!0)

              // draw each value line
              t_links.forEach(link=>{
                    let tplink_svg = this.svg.selectAll('g.suspect_value').append('g')
                                  .classed('path-' + t_links.indexOf(link), !0)

                    // draw value line
                    tplink_svg
                            .datum(link)
                            .append('path')
                            .attr('id', 'tp'+t_links.indexOf(link))
                            .attr('d', ()=>{
                                let path = 'M'
                                txn_attr_li.forEach(
                                    attr=>{
                                        let attr_index = txn_attr_li.indexOf(attr)
                                        if(attr_index != 0){
                                            path += 'L'
                                        }
                                        path += attrScale[attr_index](link[attr])+','+ y_linear(attr_index)
                                    }
                                )
                                return path
                            })
                            .attr('stroke','pink')
                            .attr('fill','none')
                            .on('mouseover',function(){
                                //当鼠标放在对应的parallel线上时。该条线被高亮
                                d3.select('g.path-'+this.id.slice(2,))
                                    .transition()
                                    .duration(100)
                                    .attr('r',15)
                                    .attr("stroke-width",5)
                                    .attr("opacity",1);

                            })
                            .on('mouseout',function(){
                                //当鼠标移出该条取值线。该取值线恢复正常
                                d3.select('g.path-'+this.id.slice(2,))
                                    .transition()
                                    .duration(100)
                                    .attr("stroke-width",2)
                                    .attr('r',5)
                                    .attr("opacity",0.5);
                            });

                    // draw value point
                    tplink_svg.selectAll('g.suspect_value')
                            .data(
                                txn_attr_li.map(attr=>{
                                        let circle_position  = {}
                                        circle_position.cx = attrScale[txn_attr_li.indexOf(attr)](link[attr])
                                        circle_position.cy = y_linear(txn_attr_li.indexOf(attr))
                                        return circle_position
                                })
                            )
                            .enter()
                            .append('circle')
                            .attr('r',5)
                            //把点映射到坐标
                            .attr('cx', d=>d.cx)
                            .attr('cy', d=>d.cy)
                            .attr('fill','pink')
                            .attr("stroke-width",'pink')
                            .attr("stroke-opacity",1)
                            .attr('opacity',0.8)
                    })


          }

          // get_node_link_chart(data)
          get_new_layout(data)

      }
    }
  }};
</script>
<style scoped>
</style>
