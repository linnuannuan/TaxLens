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
        let margin_width = width/30
        let margin_height = height/20

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
              max_height : 2*height/3 - margin_height,
              unimportant_opacity:0.2,
              default_opacity:0.5,
              highlight_opacity:1
          },
          invest_panel:{
              min_width : margin_width,
              max_width : width - margin_width,
              min_height : margin_height,
              max_height : height/3 - margin_height,
              highlight_opacity:1,
              default_opacity:1,
              unimportant_opacity:0.7,
              highlight_stroke_width:5
          },
          parallel_panel:{
              min_width : margin_width,
              max_width : width - margin_width,
              min_height : 2*height/3 + margin_height,
              max_height : height - margin_height,
              line_color:'skyblue',
              // line_color:'#1f77b4',
              highlight_color:'#b82e2e',
              node_color:'#316395',
              default_opacity:0.5,
              highlight_opacity:0.8,
              default_stroke_width:2,
              highlight_stroke_width:4
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

          let get_new_layout = (data)=> {
              console.log('input data: ',data)

              let t_nodes = data.nodes.filter(d=>d.tp)
              let t_links = data.links.filter(d=>d.ap_txn)
              console.log('Input t_nodes , t_links: ', t_nodes, t_links)
              t_links = t_links.map(d=>{
                  // console.log('check t link:', d.source, d.target)
                  if(d.throw){d= null;return d}
                  //如果存在互相交易的边
                  if(t_links.find(link=> link.target == d.source && link.source == d.target)){
                      console.log('exist reverse link')
                     //若当前方向ap txn amount < 反向link ap txn amount
                     if((t_links.find(link=> link.target == d.source && link.source == d.target).ap_txn_amount) > d.ap_txn_amount){
                       // 保留差值为正的边
                        t_links.find(link=> link.target == d.source && link.source == d.target).ap_txn_amount = t_links.find(link=> link.target == d.source && link.source == d.target).ap_txn_amount - d.ap_txn_amount
                        //设置互相交易标志true
                        t_links.find(link=> link.target == d.source && link.source == d.target).bi_direct = true
                        //保留差值用于绘图
                        t_links.find(link=> link.target == d.source && link.source == d.target).amount_offset = d.ap_txn_amount
                        // console.log('reset current link',d)
                         d = null
                     }
                     //若当前方向ap txn amount > 反向link ap txn amount
                     else{
                         d.ap_txn_amount = d.ap_txn_amount - t_links.find(link=> link.target == d.source && link.source == d.target).ap_txn_amount
                         d.bi_direct = true
                         d.amount_offset = t_links.find(link=> link.target == d.source && link.source == d.target).ap_txn_amount
                         t_links.find(link=> link.target == d.source && link.source == d.target).throw = true
                         // console.log('delete reverse link:', t_links.find(link=> link.target == d.source && link.source == d.target))
                     }
                   }
                  return d
              }).filter(d=>!!d)

              // init all t_node Object
              t_nodes.map(d=>{
                  d.lay_index = 1
                  d.sourceLinks = t_links.filter(link=>link.source == d.id)
                  d.targetLinks = t_links.filter(link=>link.target == d.id)
                  //用于记录算过坐标的节点集合，防止闭环计算
                  d.previous_cal_node_list =[]
              })
              console.log('Removed mutual transaction t_nodes,t_links:', t_nodes, t_links)

              /* calculate the lay index of taxpayer */
              let min_lay_index = 0

              // console.log('get_position of t nodes:',t_nodes)

              let iter = 0
              function  get_position(t_nodes,t_links,c_lay_index,node) {
                  //从0开始
                  iter++
                  if(iter>10){return 0;}
                  // console.log('current loop: ','node: ', node.map(d=>d.tp_name),'lay_index: ', c_lay_index)
                  if(c_lay_index < min_lay_index){
                     min_lay_index = c_lay_index
                  }
                  node.forEach (node=>{
                         //根据targetlink决定当前的lay-index  根据sourcelink决定之后的lay_index
                         //若当前的node的lay_index未设置，或原本值的偏大，需要reset lay_index 为更小的值
                         if( (node.lay_index == 1)|| ( node.lay_index > c_lay_index )){
                             // 设置当前节点的lay index
                             // console.log('reset lay_index: ',node,'with',c_lay_index)
                             t_nodes.find(d=> d.id == node.id).lay_index = c_lay_index

                             // 更改他的前向节点的lay index
                             let previous_node_li = node.targetLinks.map(link=> t_nodes.find(d => d.id == link.source))
                             // console.log('previous_node_li: ', previous_node_li.map(d=>d.tp_name))
                             if( previous_node_li.length >0 ){
                                     previous_node_li = previous_node_li.map(n=>{
                                         // console.log('previous_cal_node_list:',t_nodes.find(d => d.id == n.id).previous_cal_node_list.map(d=>d.tp_name), 'current node:',n.tp_name)
                                         if(t_nodes.find(d => d.id == node.id).previous_cal_node_list.indexOf(n)>-1){
                                            // 若本节点的坐标已经计算过
                                            //  console.log('There is a calculated node: ', n)
                                             n=null
                                         }
                                         else{
                                             // 记录已经计算过lay_index的前向节点id，防止闭环死循环
                                             t_nodes.find(d => d.id == node.id).previous_cal_node_list.push(n)
                                             // console.log('node:', n, 's previous cal node li:', t_nodes.find(d => d.id == node.id).previous_cal_node_list)
                                             // t_nodes.find(d => d.id == n.id).previous_cal_node_list = t_nodes.find(d => d.id == n.id).previous_cal_node_list.concat(node.previous_cal_node_list)
                                         }
                                         return n
                                     }).filter(d=>d!=null)
                                     // console.log('After remove calculated node from previous_node_li: ', previous_node_li.map(d=>d.tp_name))
                                     // console.log('reset previous node' +
                                     //     '', previous_node_li, t_nodes, t_links)
                                     return get_position(t_nodes,t_links,c_lay_index-1, previous_node_li)
                             }
                         }
                  })
              }
              console.log('get min source links num from :', t_nodes, t_nodes.filter( n=>!(n.sourceLinks.length==0 && n.targetLinks.length==0) ).map(n=>n.sourceLinks.length))
              console.log('get max target links num:from', t_nodes.filter(node=>node.sourceLinks.length == min_source_links_num).map(n=>n.targetLinks.length))

              let min_source_links_num = d3.min(t_nodes.filter( n=>!(n.sourceLinks.length==0 && n.targetLinks.length==0) ).map(n=>n.sourceLinks.length))
              let max_target_links_num = d3.max(t_nodes.filter( n=>!(n.sourceLinks.length==0 && n.targetLinks.length==0) ).filter(node=>node.sourceLinks.length == min_source_links_num).map(n=>n.targetLinks.length))

              console.log('min_source_links_num:', min_source_links_num, 'max_target_links_num:',max_target_links_num)
              get_position(t_nodes, t_links, 0, t_nodes.filter(node=>node.sourceLinks.length == min_source_links_num && node.targetLinks.length == max_target_links_num ))

              console.log('Calculated t_node x position: t_nodes:',t_nodes,'t_links:', t_links)

              // handle vertical transaction link : put the node into two lay
              console.log('Vertical trade link:', t_links.filter(l=>t_nodes.find( n=>n.id==l.source ).lay_index == t_nodes.find( n=> n.id==l.target).lay_index))
              t_links.filter(l=>t_nodes.find( n=>n.id==l.source ).lay_index == t_nodes.find( n=> n.id==l.target).lay_index).forEach(
                  link=>{
                      let curr_lay = t_nodes.find( n=> n.id == link.target).lay_index

                      // source_node lay index -1 layindex 之前所有node layindex -1 min_lay_index -1
                      t_nodes = t_nodes.filter( n=>!(n.lay_index<curr_lay) )
                                       .concat( t_nodes.filter( n => n.lay_index<curr_lay ).map( d => {d.lay_index = d.lay_index-1;return d }))
                      t_nodes.find( n=> n.id == link.source).lay_index -= 1
                      min_lay_index --;
                  }
              )
              console.log('Handled the vertical transaction link: t_nodes:',t_nodes,'t_links:', t_links)



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
                        .attr('x',d=> (d.x1<(this.cfg.trade_panel.max_width/2))? d.x1+10 : d.x0-150)
                        .attr('y',d=> d.y0 + 15)
                        .attr('dy', '0.35em')
                        .text(d => d.tp_name)
                        .on('click',d=>{console.log(d)});

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
                        // console.log('draw link: ',d, 'source:', source_node,' target:', target_node)
                        let path_d;
                        if(target_node.lay_index < source_node.lay_index){
                            //设置offset 外环半径为15
                            let offset_r = 30
                            let inner_offset_r = 10
                            path_d = 'M '
                                + ((source_node.x1) + strokeWidth) +','+ source_node.y0
                                + 'A '+ offset_r +','+offset_r +' 0 0 1 '+ ((source_node.x1)+ strokeWidth) +','+ (source_node.y0 + 2*offset_r)
                                + 'L' + (target_node.x0 - strokeWidth) + ',' + (target_node.y0 + 2*offset_r)
                                + 'A' + offset_r +','+offset_r +' 0 0 1 '+ (target_node.x0 - strokeWidth) + ',' + target_node.y0
                                /* 第二段弧 */
                                + 'L'+ (target_node.x0 - strokeWidth) + ',' + target_node.y1
                                + 'A '+ inner_offset_r +','+inner_offset_r +' 0 0 0 '+ ((target_node.x0) - strokeWidth) +','+ (target_node.y1 + 2*inner_offset_r)
                                + 'L' + (source_node.x1 + strokeWidth) + ',' + (source_node.y1 + 2*inner_offset_r)
                                + 'A' + inner_offset_r +','+inner_offset_r +' 0 0 0 '+ (source_node.x1 + strokeWidth) + ',' + source_node.y1
                                + 'Z'
                        }
                        else{
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
                            path_d = 'M'
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
                        }
                        return path_d
                    })
                    .attr('stroke-opacity', 0.5)
                    .attr('stroke',this.cfg.link.color.txn)
                    .attr('fill',this.cfg.link.color.txn)
                    .attr('opacity', this.cfg.trade_panel.default_opacity)
                    .on('mouseover', d=>{
                        //当鼠标放在交易上时，对应的交易信息在parallel视图中被高亮
                        d3.select('#tp'+t_links.indexOf(d))
                            .transition()
                            .duration(50)
                            // .attr("stroke",this.cfg.parallel_panel.highlight_color)
                            .attr("stroke-width",this.cfg.parallel_panel.highlight_stroke_width)
                            .attr('opacity',this.cfg.parallel_panel.highlight_opacity);

                        //当鼠标放在交易上时，处本交易以外，其他关联交易透明度降低。
                        d3.selectAll('g.trade_link')
                            .selectAll('path')
                            .attr('opacity',this.cfg.trade_panel.unimportant_opacity)
                        d3.select(event.target).attr('opacity',this.cfg.trade_panel.highlight_opacity)

                        //对应的invest_path高亮
                        d3.select('g.invest_link').attr('opacity',this.cfg.invest_panel.unimportant_opacity)
                        for(let path_id in d.path){
                            for( let node_id in d.path[path_id]){
                                if(node_id < (d.path[path_id].length-1)){
                                    // highlight correspond invest link (undirect link)

                                    // console.log(d)
                                    // Distinguish between co-investor and interlocking
                                    console.log(d.path[path_id][parseInt(node_id)+parseInt(1)], d.path[path_id][node_id], [d.source.id, d.target.id])
                                    if( ([d.source.id, d.target.id].indexOf( d.path[path_id][parseInt(node_id)+parseInt(1)])> -1)  || ([d.source.id, d.target.id].indexOf(d.path[path_id][node_id])>-1)){
                                        console.log('co-investor')
                                        d3.select('g.invest_link #in-'+ d.path[path_id][node_id]+'-'+d.path[path_id][parseInt(node_id)+parseInt(1)])
                                        .attr('opacity',this.cfg.invest_panel.highlight_opacity)
                                        .attr('stroke-width',this.cfg.invest_panel.highlight_stroke_width)

                                        d3.select('g.invest_link #in-'+ d.path[path_id][parseInt(node_id)+parseInt(1)]+'-'+d.path[path_id][node_id])
                                        .attr('opacity',this.cfg.invest_panel.highlight_opacity)
                                        .attr('stroke-width',this.cfg.invest_panel.highlight_stroke_width)

                                    }
                                    else{
                                        console.log('sharelocking')
                                        d3.select('g.invest_link #in-'+ d.path[path_id][node_id]+'-'+d.path[path_id][parseInt(node_id)+parseInt(1)])
                                        .attr('opacity',this.cfg.invest_panel.highlight_opacity)
                                        .attr('stroke','red')
                                        .attr('stroke-width',this.cfg.invest_panel.highlight_stroke_width)

                                        d3.select('g.invest_link #in-'+ d.path[path_id][parseInt(node_id)+parseInt(1)]+'-'+d.path[path_id][node_id])
                                        .attr('opacity',this.cfg.invest_panel.highlight_opacity)
                                        .attr('stroke', 'red')
                                        // .attr('stroke', '#ff7f0e')
                                        .attr('stroke-width',this.cfg.invest_panel.highlight_stroke_width)
                                    }

                                }
                                // highlight correspond node
                                d3.select('g.invest_node #in-'+ d.path[path_id][node_id])
                                        .attr('opacity',this.cfg.invest_panel.highlight_opacity)
                                        .attr('stroke-width',this.cfg.invest_panel.highlight_stroke_width)
                            }
                        }


                    })
                    .on('mouseout', d=>{
                        //当鼠标放在交易上时，对应的交易信息在parallel视图中被取消高亮
                        d3.select('#tp'+t_links.indexOf(d))
                            .transition()
                            .duration(50)
                            .attr("stroke",this.cfg.parallel_panel.line_color)
                            .attr('stroke-width',2)
                            .attr('opacity',this.cfg.parallel_panel.default_opacity);

                        // All trade path
                        d3.selectAll('g.trade_link').attr('opacity',this.cfg.trade_panel.default_opacity)

                        //当鼠标放在交易上时，处本交易以外，其他关联交易透明度降低。
                        d3.selectAll('g.trade_link')
                            .selectAll('path')
                            .attr('opacity',this.cfg.trade_panel.unimportant_opacity)
                        d3.select(event.target).attr('opacity',this.cfg.trade_panel.highlight_opacity)

                        //对应的invest_path取消高亮
                        d3.select('g.invest_link').attr('opacity',this.cfg.invest_panel.default_opacity)
                        for(let path_id in d.path){
                            for( let node_id in d.path[path_id]){
                                if(node_id < d.path[path_id].length-1){
                                    // cancel highlight correspond link
                                    // undirect link
                                    d3.select('g.invest_link #in-'+ d.path[path_id][node_id]+'-'+d.path[path_id][parseInt(node_id)+parseInt(1)])
                                        .attr('opacity',this.cfg.invest_panel.default_opacity)
                                        .attr('stroke',this.cfg.link.color.invest)
                                        .attr('stroke-width',this.cfg.invest_panel.default_stroke_width)

                                    d3.select('g.invest_link #in-'+ d.path[path_id][parseInt(node_id)+parseInt(1)]+'-'+d.path[path_id][node_id])
                                        .attr('opacity', this.cfg.invest_panel.default_opacity)
                                        .attr('stroke',this.cfg.link.color.invest)
                                        .attr('stroke-width', this.cfg.invest_panel.default_stroke_width)
                                }
                                // cancel highlight correspond node
                                d3.select('g.invest_node #in-'+ d.path[path_id][node_id])
                                        .attr('opacity',this.cfg.invest_panel.default_opacity)
                                        .attr('stroke-width',this.cfg.invest_panel.default_stroke_width)
                            }
                        }
                    })


              let invest_panel_svg = this.svg.append('g')
                        .classed('invest_panel',!0)

              /* draw i node */
              let i_nodes = data.nodes.filter(d=>!d.tp)
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
              // console.log('calculating i node:',i_nodes)
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
              function reduce_overlap(i_nodes,i,direct,max_width,min_width,margin){
                    // Input： i_nodes, i(current iter index), direct(current iter direction. 1:forward, 0:backward)
                    if( (direct && (i >= (i_nodes.length-1))) || (!direct && i == 1) ){
                            return true
                    }
                    // console.log('current loop index:', i, 'node_li:', i_nodes.map(d=>d.x), 'direction:', direct)

                    // 当遍历的两个节点之间的间距差小于 invest直径
                    if( ((i_nodes[i+direct].x - i_nodes[i+(direct-1)].x) < margin) && (i_nodes[i+direct].y_layindex == i_nodes[i+(direct-1)].y_layindex) ) {
                            // 要么前向节点-2*r  以前向节点向前check,
                            // 要么后向节点+2r   以后向节点向后check
                            // 正向
                            // console.log('reduce_overlap with i:',i_nodes[i+direct].in_name, ' and ', i_nodes[i+(direct-1)].in_name, '：', (i_nodes[i+direct].x - i_nodes[i+(direct-1)].x) < margin)
                            if( direct ){
                                //后继节点没有超过max_width边界
                                if( i_nodes[i+(direct-1)].x + margin < max_width ){
                                    i_nodes[i+direct].x = i_nodes[i+(direct-1)].x + margin
                                    // console.log('reset the forward x as : ', i_nodes[i+direct].x)
                                }
                                //超过边界 则后推回溯
                                else{
                                    // console.log('exeed the maximum width',i_nodes[i+direct])
                                    i_nodes[i+direct].x = max_width
                                    i_nodes[i+direct-1].x = max_width - margin
                                    reduce_overlap(i_nodes, i, 0, max_width,min_width,margin)
                                }
                            }
                            // 反向
                            else {
                                // 前继节点没有超过min_width 边界
                                if( i_nodes[i+(direct)].x - margin > min_width ){
                                    i_nodes[i+(direct-1)].x = i_nodes[i+(direct)].x - margin
                                    // console.log('reset the backward x as : ', i_nodes[i+direct-1].x)
                                }
                                //超过边界 则后推回溯
                                else{
                                    reduce_overlap(i_nodes,i+1,1,max_width,min_width,margin)
                                }
                            }
                     }
                    else if(!direct){
                        return true
                    }
                    return reduce_overlap(i_nodes,direct?i+1:i-1, direct, max_width, min_width, margin)
              }
              reduce_overlap(i_nodes,0,1,this.cfg.trade_panel.max_width,this.cfg.trade_panel.min_width,2*this.cfg.node.invest_r+3)

              console.log('After calculating the position of i node: ', i_nodes)

              var in_y__position = d3.scaleLinear()
                  .domain([d3.min(i_nodes.map(d=>d.y_layindex)), d3.max(i_nodes.map(d=>d.y_layindex))])
                  .range([this.cfg.invest_panel.min_height, this.cfg.invest_panel.max_height])

              i_nodes.map(d=>{
                  d.y = in_y__position(d.y_layindex)
                  return d
              })


              let i_links = data.links.filter(d=>!d.ap_txn)

              // draw invest link
              invest_panel_svg.append('g')
                    .classed('invest_link',!0)
                    .attr('fill', 'none') // to avoid fill the path
                    .attr('opacity', this.cfg.invest_panel.default_opacity)
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
                        // if both source node and target node are the tp_node




                        let source_node = (i_nodes.concat(t_nodes)).find(node => node.id == d.source)
                        let target_node = (t_nodes.concat(i_nodes)).find(node => node.id == d.target)
                        console.log('draw invest link: ',d, 'source:', source_node,' target:', target_node)

                        if(source_node.tp){
                            source_node.x = (source_node.x0 + source_node.x1)/2
                            source_node.y = (source_node.y0 + source_node.y1)/2
                        }

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
                            .attr('stroke',this.cfg.parallel_panel.line_color)
                            .attr('stroke-width',2)
                            .attr('stroke-opacity',0.9)
                            .attr('fill','none')
                            .on('mouseover', d=> {
                                //当鼠标放在对应的parallel线上时。该条线被高亮
                                console.log('this',this)
                                d3.select('g.path-'+ t_links.indexOf(d).slice(2,))
                                    .transition()
                                    .duration(50)
                                    .selectAll('path')
                                    // .attr('r',15)
                                    .attr("stroke-width",5)
                                    .attr("opacity",this.cfg.parallel_panel.highlight_opacity);

                                d3.select('g.path-'+t_links.indexOf(d).slice(2,))
                                    .selectAll('circle')
                                    .attr("opacity",this.cfg.parallel_panel.highlight_opacity);

                            })
                            .on('mouseout', d=>{
                                //当鼠标移出该条取值线。该取值线恢复正常
                                d3.select('g.path-'+ t_links.indexOf(d).slice(2,))
                                    .transition()
                                    .duration(50)
                                    .selectAll('path')
                                    .attr("stroke-width",this.cfg.parallel_panel.default_stroke_width)

                                d3.select('g.path-'+ t_links.indexOf(d).slice(2,))
                                    .selectAll('circle')
                                    // .attr('r',5)
                                    .attr("opacity",this.cfg.parallel_panel.default_opacity);
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
                            .attr('r',2)
                            //把点映射到坐标
                            .attr('cx', d=>d.cx)
                            .attr('cy', d=>d.cy)
                            .attr('fill', this.cfg.parallel_panel.node_color)
                            .attr('fill-opacity', 0.8)
                            .attr("stroke-width", this.cfg.parallel_panel.node_color)
                            .attr("stroke-opacity", 1)
                            .attr('opacity', 0.8)
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
