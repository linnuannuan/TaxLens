/* eslint-disable */
<template>
  <div id="relation_structure" v-loading="loadingGraph"></div>
</template>
<script>
  import * as d3 from "d3";
  import EventService from "../utils/event-service";
  // import DataService from "../utils/data-service";

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
        let margin_width = width/10
        let margin_height = height/10

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
            min_width : margin_width,
            max_width : width - margin_width,
            min_height : height/4 + margin_height,
            max_height : height - margin_height,
            unimportant_opacity:0.2,
            default_opacity:0.5,
            highlight_opacity:1,
            node_width: 30,
            node_height:30
          },
          parallel_panel:{
            highlight_color:'#b82e2e',
            default_opacity:0.5,
            highlight_opacity:0.8,
            default_stroke_width:2,
            highlight_stroke_width:4
          },
        }

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
        this.svg.selectAll("g").remove()
        if (this.affiliatedPartyDetail !== null) {
          let data = this.affiliatedPartyDetail;

          let get_new_layout = (data)=> {
            let t_nodes = data.nodes.filter(d=>d.tp)
            let t_links = data.links.filter(d=>d.ap_txn)
            let i_links = data.links.filter(d=>d.in_ratio)
            let i_nodes = data.nodes.filter(d=>!d.tp)

            t_links = t_links.map(d=>{
              if(d.throw){d= null;return d}
              //如果存在互相交易的边
              if(t_links.find(link=> link.target === d.source && link.source === d.target)){
                //若当前方向ap txn amount < 反向link ap txn amount
                if((t_links.find(link=> link.target === d.source && link.source === d.target).ap_txn_amount) > d.ap_txn_amount){
                  // 保留差值为正的边
                  t_links.find(link=> link.target === d.source && link.source === d.target).ap_txn_amount = t_links.find(link=> link.target === d.source && link.source === d.target).ap_txn_amount - d.ap_txn_amount
                  //设置互相交易标志true
                  t_links.find(link=> link.target === d.source && link.source === d.target).bi_direct = true
                  //保留差值用于绘图
                  t_links.find(link=> link.target === d.source && link.source === d.target).amount_offset = d.ap_txn_amount
                  d = null
                }
                //若当前方向ap txn amount > 反向link ap txn amount
                else{
                  d.ap_txn_amount = d.ap_txn_amount - t_links.find(link=> link.target === d.source && link.source === d.target).ap_txn_amount
                  d.bi_direct = true
                  d.amount_offset = t_links.find(link=> link.target === d.source && link.source === d.target).ap_txn_amount
                  t_links.find(link=> link.target === d.source && link.source === d.target).throw = true
                }
              }
              return d
            }).filter(d=>!!d)

            // init all t_node object
            t_nodes.map(d=>{
              d.x_index = 1
              d.y_index = 0
              d.sourceLinks = t_links.filter(link=>link.source === d.id)
              d.targetLinks = t_links.filter(link=>link.target === d.id)
              //用于记录算过坐标的节点集合，防止闭环计算
              d.previous_cal_node_list =[]
            })

            /* calculate the lay index of taxpayer */
            let min_lay_index = 0

            // console.log('get_position of t nodes:',t_nodes)

            let iter = 0
            function  get_position(t_nodes,t_links,c_lay_index,node) {
              // 从0开始
              iter++
              if(iter>10){return 0;}
              // console.log('current loop: ','node: ', node.map(d=>d.tp_name),'lay_index: ', c_lay_index)
              if(c_lay_index < min_lay_index){
                min_lay_index = c_lay_index
              }
              node.forEach( (node, index)=>{
                // 根据targetlink决定当前的lay-index  根据sourcelink决定之后的lay_index
                // 若当前的node的lay_index未设置，或原本值的偏大，需要reset lay_index 为更小的值

                // make each transaction lay in the horizontal direction and let invest relation to decide the vertical position
                c_lay_index -= index*2

                if( (node.x_index === 1)|| ( node.x_index > c_lay_index )){
                  // 设置当前节点的lay index
                  t_nodes.find(d=> d.id === node.id).x_index = c_lay_index

                  // 更改他的前向节点的lay index
                  let previous_node_li = node.targetLinks.map(link=> t_nodes.find(d => d.id === link.source))
                  if( previous_node_li.length >0 ){
                    previous_node_li = previous_node_li.map(n=>{
                      if(t_nodes.find(d => d.id === node.id).previous_cal_node_list.indexOf(n)>-1){
                        // 若本节点的坐标已经计算过
                        n=null
                      }
                      else{
                        // 记录已经计算过lay_index的前向节点id，防止闭环死循环
                        t_nodes.find(d => d.id === node.id).previous_cal_node_list.push(n)
                      }
                      return n
                    }).filter(d=>d!==null)
                    return get_position(t_nodes,t_links,c_lay_index-1, previous_node_li)
                  }
                }
              })
            }

            // calculated the position start from node list with the minimum source link num  and maximum target link num
            let min_source_links_num = d3.min(t_nodes.filter( n=>!(n.sourceLinks.length===0 && n.targetLinks.length===0) ).map(n=>n.sourceLinks.length))
            let max_target_links_num = d3.max(t_nodes.filter( n=>!(n.sourceLinks.length===0 && n.targetLinks.length===0) ).filter(node=>node.sourceLinks.length === min_source_links_num).map(n=>n.targetLinks.length))

            get_position(t_nodes, t_links, 0, t_nodes.filter(node=>node.sourceLinks.length === min_source_links_num && node.targetLinks.length === max_target_links_num ))


            // handle the position of those trader with no transaction
            t_nodes.filter(d=>d.x_index === 1).sort((x,y)=> i_links.filter(link=> link.source ===y.id || link.target === y.id).length < i_links.filter(link=> link.source ===x.id || link.target === x.id).length )
                    .forEach((d,index)=>{
                      t_nodes.find(n=>n.id===d.id).x_index += index
                    })


            // handle vertical transaction link : put the node into two lay
            t_links.filter(l=>t_nodes.find( n=>n.id===l.source ).x_index === t_nodes.find( n=> n.id===l.target).x_index).forEach(
                    link=>{
                      let curr_lay = t_nodes.find( n=> n.id === link.target).x_index

                      // source_node lay index -1 layindex 之前所有node layindex -1 min_lay_index -1
                      t_nodes = t_nodes.filter( n=>!(n.x_index<curr_lay) )
                              .concat( t_nodes.filter( n => n.x_index<curr_lay ).map( d => {d.x_index = d.x_index-1;return d }))
                      t_nodes.find( n=> n.id === link.source).x_index -= 1
                      min_lay_index --;
                    }
            )

            // step 2  get the y_index of each t_node
            t_nodes.map(n=>{
              // get the y_index of each node
              if(n.in){
                let target_i_nodes = i_links.filter(l=>l.source === n.id).map(n=>n.target)
                let source_i_nodes= i_links.filter(l=>l.target === n.id).map(n=>n.source)
                let max_source_y_index = source_i_nodes.length == 0? 0: d3.max(source_i_nodes.map(node=> t_nodes.find(n=>n.id===node)? t_nodes.find(n=>n.id===node).y_index:0))
                let reset_target = true
                // 获取每一个前置节点 取最大y_index +1
                while(source_i_nodes.length>0){
                  // get all previous nodes
                  source_i_nodes = i_links.filter(l=>l.target in source_i_nodes).map(n=>n.source)
                  // get max lay_index in previous nodes
                  let current_max_lay = d3.max(source_i_nodes.map(node=> t_nodes.find(n=>n.id===node)? t_nodes.find(n=>n.id===node).y_index:0))
                  // reset if forward node is tp_node and current y_index > previous set y_index

                  max_source_y_index = (!!current_max_lay) & current_max_lay > max_source_y_index? current_max_lay : max_source_y_index
                }
                n.y_index = max_source_y_index + 1

                // 获取每一个后置节点 设置其y_index 为当前的y_index +1
                // 若后置节点已经计算过，则判断后置节点的lay_index是否小于当前要设置的值，若小于重置后置节点lay_index
                let target_y_index = n.y_index + 1
                while(reset_target){
                  // reset current target nodes
                  reset_target = false
                  target_i_nodes.map(node=> {
                    if(t_nodes.find(n=>n.id === node).y_index < target_y_index){
                      t_nodes.find(n=>n.id === node).y_index = target_y_index
                      reset_target = true
                    }
                  })
                  if(reset_target){
                    target_i_nodes = i_links.filter(l=>l.source in target_i_nodes).map(n=>n.target)
                    target_y_index++
                  }
                }
              }
              return n;
            })


            // sort the t_node by y_index


            // step 1  mark the overlapping t_links

            t_links.map(d=>{
              // 若当前的target node 的 lay_index 不是最小的 ，且与比他小的任意的t_node 具有相同 y_index
              let target_node_with_same_source = t_links.filter( l => l.source === d.source ).map( link => t_nodes.find(n => n.id === link.target) ).sort( (x,y) => x.x_index-y.x_index )
              let target_node = t_nodes.find(n => n.id===d.target)
              let target_node_index_in_same = target_node_with_same_source.indexOf(target_node)
              if( (target_node_index_in_same!==0)  && (target_node.y_index in target_node_with_same_source.slice(0,target_node_index_in_same).map(n=>n.y_index))){
                d.overlap = true
              }
              return d
            })



            var x_position = d3.scaleLinear()
                    .domain([d3.min(t_nodes.map(d=>d.x_index)), d3.max(t_nodes.map(d=>d.x_index))])
                    .range([this.cfg.trade_panel.min_width, this.cfg.trade_panel.max_width])

            var y_position =d3.scaleLinear()
                    .domain([d3.min(t_nodes.map(d=>d.y_index)), d3.max(t_nodes.map(d=>d.y_index))])
                    .range([this.cfg.trade_panel.min_height, this.cfg.trade_panel.max_height])

            // set the position info of each node
            t_nodes.map(n=>{
              // get the y_index of each node
              n.x0= x_position(n.x_index);
              n.x1= n.x0 + this.cfg.trade_panel.node_width;
              n.y0= y_position(n.y_index)
              n.y1= n.y0 + this.cfg.trade_panel.node_width ;
              return n;
            })


            // draw transaction panel
            let trade_panel_svg = this.svg.append('g')
                    .classed('trade_panel',!0)

            /* draw t node */
            // draw each node
            trade_panel_svg
                    .append('g')
                    .attr('stroke', '#000')
                    .selectAll('rect')
                    .data(t_nodes)
                    .enter()
                    .append('rect')
                    .attr('width', this.cfg.trade_panel.node_width)
                    .attr('height', this.cfg.trade_panel.node_height)
                    .attr('x',d=> d.x0)
                    .attr('y',d=> d.y0)                        // .attr('stroke-width',5)
                    .attr('fill',this.cfg.node.color.tp)
                    .on('click',d=>{console.log('click on: ',d)})

            /* add text of each node */
            trade_panel_svg
                    .append('g')
                    .classed('trade_text',!0)
                    .style('font', '10px sans-serif')
                    .selectAll('text')
                    .data(t_nodes)
                    .enter()
                    .append('text')
                    .attr('id',d=> 'text-' + d.id)
                    .attr('x',d=> d.x0 - d.tp_name.length*10/2)
                    // .attr('x',d=> (d.x1<(this.cfg.trade_panel.max_width/2))? d.x1+10 : d.x0-150)
                    .attr('y',d=> d.y0 + 40)
                    .attr('dy', '0.35em')
                    .text(d => d.tp_name)
                    .on('click',d=>{console.log(d)});


            // for(let i = min_lay_index; i<=1; i++){
            //   // get node list of current lay
            //   let node_li = t_nodes.filter(d => d.x_index === i)
            //
            //   // vertical position linear encoder
            //   let y_position = d3.scaleLinear()
            //         .domain([0, node_li.length])
            //         .range([this.cfg.trade_panel.min_height, this.cfg.trade_panel.max_height])

            // calculate the position of each node
            // node_li.forEach(node=>{
            //     let t_node = t_nodes[t_nodes.indexOf(node)]
            //     t_node.width = 30
            //     t_node.height = 30
            //     t_node.x0= x_position(t_node.x_index);
            //     t_node.x1= t_node.x0 + t_node.width;
            //     t_node.y0= y_position(node_li.indexOf(t_node));
            //     t_node.y1= t_node.y0 + t_node.width ;
            // })

            // step 3 get the t node y position based on the vertical rules
            // i_links.forEach(link=>{
            //     // 如果sourcenode
            //     if(link.source && link.target){
            //
            //     }
            // })



            // draw each node
            // trade_panel_svg
            //         .append('g')
            //         .attr('stroke', '#000')
            //         .selectAll('rect')
            //         .data(node_li)
            //         .enter()
            //         .append('rect')
            //         .attr('width', d=>d.width)
            //         .attr('height', d=>d.height)
            //         .attr('x',d=> d.x0)
            //         .attr('y',d=> d.y0)
            //         // .attr('stroke-width',5)
            //         .attr('fill',this.cfg.node.color.tp)
            //         .on('click',d=>{console.log('click on: ',d)})

            /* add text of each node */
            // trade_panel_svg
            //         .append('g')
            //         .style('font', '10px sans-serif')
            //         .selectAll('text')
            //         .data(node_li)
            //         .enter()
            //         .append('text')
            //         .attr('x',d=> (d.x1<(this.cfg.trade_panel.max_width/2))? d.x1+10 : d.x0-150)
            //         .attr('y',d=> d.y0 + 15)
            //         .attr('dy', '0.35em')
            //         .text(d => d.tp_name)
            //         .on('click',d=>{console.log(d)});


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
                      let source_node = t_nodes.find(node => node.id === d.source)
                      let target_node = t_nodes.find(node => node.id === d.target)
                      let path_d;

                      // draw self loop transaction
                      if(target_node.x_index < source_node.x_index){
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
                      // draw overlapping path
                      else if(d.overlap){
                        let offset_r = 30
                        let inner_offset_r = 10
                        path_d = 'M '
                                + ((source_node.x1) + strokeWidth) + ',' + source_node.y0
                                + 'A '+ offset_r + ',' + offset_r + ' 0 0 1 ' + ((source_node.x1) + strokeWidth + offset_r) +','+ (source_node.y0 + offset_r)
                                + 'A' + inner_offset_r + ',' + inner_offset_r + ' 0 0 0 ' + ((source_node.x1) + strokeWidth + offset_r + inner_offset_r) +','+ (source_node.y0 + offset_r +inner_offset_r)
                                + 'L' + (target_node.x0- strokeWidth - inner_offset_r - offset_r) + ',' + (target_node.y0 + offset_r +inner_offset_r)
                                + 'A '+ inner_offset_r + ',' +inner_offset_r + ' 0 0 0 ' + ((target_node.x0)- strokeWidth - offset_r) +','+ (target_node.y0 + offset_r)
                                + 'A' + offset_r + ',' +offset_r + ' 0 0 1 ' + ((target_node.x0)- strokeWidth) +','+ (target_node.y0)
                                //  第二段弧
                                + 'L' + (target_node.x0) + ',' + (target_node.y1)
                                + 'A '+ inner_offset_r + ',' + inner_offset_r + ' 0 0 0 ' + ((target_node.x0)- strokeWidth - inner_offset_r) +','+ (target_node.y1 + inner_offset_r)
                                + 'A' + offset_r + ',' + offset_r + ' 0 0 1 ' + ((target_node.x0)- strokeWidth - inner_offset_r - offset_r) +','+ (target_node.y1 + inner_offset_r + offset_r)
                                + 'L' + ((source_node.x1) + strokeWidth + inner_offset_r + offset_r) +','+ (source_node.y1 + inner_offset_r + offset_r)
                                + 'A '+ offset_r + ',' + offset_r + ' 0 0 1 ' + ((source_node.x1) + strokeWidth + inner_offset_r) +','+ (source_node.y1 + inner_offset_r)
                                + 'A' + inner_offset_r + ',' + inner_offset_r + ' 0 0 0 ' + ((source_node.x1) + strokeWidth) +','+ (source_node.y1)
                                + 'Z'

                      }

                      // draw normal transaction
                      else{
                        let control_point1 = {
                          x:(source_node.x1 + target_node.x0)/2,
                          y: source_node.y0
                        }
                        let control_point2 = {
                          x:(source_node.x1 + target_node.x0)/2,
                          y:target_node.y0
                        };
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
                      d3.select('g.trade_text')
                              .selectAll('text')
                              .attr('opacity',this.cfg.trade_panel.unimportant_opacity)
                      d3.select('#text-'+d.source.id)
                              .attr('opacity',this.cfg.trade_panel.highlight_opacity)
                      d3.select('#text-'+d.target.id)
                              .attr('opacity',this.cfg.trade_panel.highlight_opacity)


                      //对应的invest_path高亮
                      d3.select('g.invest_link').attr('opacity',this.cfg.invest_panel.unimportant_opacity)
                      for(let path_id in d.path){
                        for( let node_id in d.path[path_id]){
                          if(node_id < (d.path[path_id].length-1)){
                            // highlight correspond invest link (undirect link)

                            // console.log(d)
                            // Distinguish between co-investor and interlocking
                            if( ([d.source.id, d.target.id].indexOf( d.path[path_id][parseInt(node_id)+parseInt(1)])> -1)  || ([d.source.id, d.target.id].indexOf(d.path[path_id][node_id])>-1)){
                              // console.log('co-investor')
                              d3.select('g.invest_link #in-'+ d.path[path_id][node_id]+'-'+d.path[path_id][parseInt(node_id)+parseInt(1)])
                                      .attr('opacity',this.cfg.invest_panel.highlight_opacity)
                                      .attr('stroke-width',this.cfg.invest_panel.highlight_stroke_width)

                              d3.select('g.invest_link #in-'+ d.path[path_id][parseInt(node_id)+parseInt(1)]+'-'+d.path[path_id][node_id])
                                      .attr('opacity',this.cfg.invest_panel.highlight_opacity)
                                      .attr('stroke-width',this.cfg.invest_panel.highlight_stroke_width)

                            }
                            else{
                              // console.log('sharelocking')
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
                              .attr('opacity',this.cfg.trade_panel.highlight_opacity)
                      d3.select(event.target).attr('opacity',this.cfg.trade_panel.highlight_opacity)
                      d3.select('g.trade_text')
                              .selectAll('text')
                              .attr('opacity',this.cfg.trade_panel.highlight_opacity)


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
                    .on('click', d=>{
                        // 渲染对应calendar view this.$emit('setPeriod', {periodStart: periodStart, periodEnd: periodEnd});
                        EventService.emitAffiliatedTransactionSelected(d.source.id, d.target.id);
                    })


            let invest_panel_svg = this.svg.append('g')
                    .classed('invest_panel',!0)

            /* draw i node */
            i_nodes = i_nodes.map(
                    d=>{
                      d.sourceLinks = data.links.filter(link=>link.source === d.id)
                      d.targetLinks = data.links.filter(link=>link.target === d.id)
                      d.to_calulate = []

                      let accumulate_x = 0
                      d.sourceLinks.forEach(link=>{
                        if(!t_nodes.find(n => n.id === link.target)){

                          console.log('find ',link.target,' from i_node:',i_nodes,i_nodes.find(n => n.id === link.target))
                          // 存在二级投资，暂不考虑二级投资的x值
                          let target_node = i_nodes.find(n => (n.id === link.target))

                          // 如果当前投资的节点仍为投资点，
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
                          accumulate_x += t_nodes.find(n => n.id === link.target).x0
                          d.y = 0
                        }
                      })
                      d.x = accumulate_x / (d.sourceLinks.length - d.to_calulate.length)
                      return d
                    }
            )
            while( i_nodes.filter(d=>d.to_calulate.length>0).length>0 ){
              //存在尚未计算x的i_node
              i_nodes.filter(d=>d.to_calulate.length>0).map(
                      r_node=>{
                        let accumulate_x = 0
                        let calculated_count = 0
                        r_node.to_calulate.forEach(node_id=>{
                          // console.log('to calculate the node',node_id)
                          // console.log('get node from i_nodes',i_nodes,  i_nodes.find(n=>n.id === node_id))
                          let target_node = i_nodes.find(n=>n.id === node_id)
                          if(target_node.to_calulate.length===0){
                            accumulate_x += target_node.x
                            r_node.to_calulate.splice(r_node.to_calulate.findIndex(item => item === node_id), 1)
                            calculated_count++
                          }
                        })
                        r_node.x = (r_node.x + accumulate_x)/(calculated_count+1)
                      }
              )
            }

            // fix the overlapping problem of invest nodes.
            i_nodes= i_nodes.sort( function(a,b){ return a.x - b.x } )

            for (let i = 0 ; i < i_nodes.length - 1;i++){
              //若两个相邻的x差值超过invest的Node的直径, 存在overlapping
              if( ((i_nodes[i+1].x - i_nodes[i].x) < (2*this.cfg.node.invest_r)) ){
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
              if( (direct && (i >= (i_nodes.length-1))) || (!direct && i === 1) ){
                return true
              }

              // 当遍历的两个节点之间的间距差小于 invest直径
              if( ((i_nodes[i+direct].x - i_nodes[i+(direct-1)].x) < margin) ) {
                // 要么前向节点-2*r  以前向节点向前check,
                // 要么后向节点+2r   以后向节点向后check
                // 正向
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


            i_nodes.map(d=>{
              d.y= (this.cfg.invest_panel.min_height + this.cfg.invest_panel.max_height)/2
              return d
            })



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
                      // get the source node and target node

                      let source_node = (i_nodes.concat(t_nodes)).find(node => node.id === d.source)
                      let target_node = (t_nodes.concat(i_nodes)).find(node => node.id === d.target)
                      // console.log('draw invest link: ',d, 'source:', source_node,' target:', target_node)

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
                      // console.log('path',path_d)
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


            // step 1 sort ap txn by  x position
            // draw the correspond calendar chart with  transaction



          }

          // get_node_link_chart(data)
          get_new_layout(data)

        }
      }
    }};
</script>
<style scoped>
</style>
