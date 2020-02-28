/* eslint-disable */
import * as d3 from "d3";
function initialize(){
    console.log('load graph view.js')
    var width = 1000,
        height = 500;

    function drag (simulation) {
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
    var data = {
        "directed": true,
        "multigraph": false,
        "graph": {},
        "nodes": [
            {
                "in": false,
                "tp": true,
                "tp_name": "铜川凯通工贸有限责任公司",
                "lr_name": "刘浩",
                "pc": "727031",
                "business": "许可经营项目：普通运货、煤炭销售（不含仓储）。\t一般经营项目：。（依法须经批准的项目，经相关部门批准后方可开展经营活动）",
                "capital": 5000000.0,
                "employee": 10.0,
                "industry": "道路货物运输",
                "id": "91610201580769253D"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "陕西玉祥出租汽车集团有限公司",
                "lr_name": "吕玉良",
                "pc": "712100",
                "business": "出租客运（道路运输经营许可证有效期至２０１４年１２月３０日）；汽车零配件的销售。",
                "capital": 20000000.0,
                "employee": 7.0,
                "industry": "出租车客运",
                "id": "616999710070935"
            },
            {
                "tp": false,
                "in": true,
                "in_name": "冯连武",
                "in_entity": "510",
                "id": "610102195309030035"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "陕西暨嘉信息科技有限公司",
                "lr_name": "吕玉良",
                "pc": "710061",
                "business": "计算机系统集成；智能化储物柜、安防监控产品、网络设备、计算机辅助设备、电子产品、体育健身器材、教学器材、建筑材料的销售；安防、监控工程的施工。（上述经营范围中涉及许可经营项目的，凭许可证明文件，证件在有效期内经营，未经许可不得经营）",
                "capital": 3000000.0,
                "employee": 5.0,
                "industry": "其他机械设备及电子产品批发",
                "id": "610113074527497"
            },
            {
                "tp": false,
                "in": true,
                "in_name": "史进元",
                "in_entity": "510",
                "id": "610623195605090111"
            },
            {
                "tp": false,
                "in": true,
                "in_name": "许坚",
                "in_entity": "510",
                "id": "610104197308022131"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "兴平市玉祥出租汽车有限公司",
                "lr_name": "孙振宽",
                "pc": "713100",
                "business": "出租客运、车辆维修、配件销售。",
                "capital": 8000000.0,
                "employee": 3.0,
                "industry": "出租车客运",
                "id": "610481709954696"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "西安赛科非金属有限责任公司",
                "lr_name": "王健",
                "pc": "710075",
                "business": "非金属材料、半导体材料的开发、研制、生产、销售及技术服务。（以上不含国家专项审批）",
                "capital": 1500000.0,
                "employee": 2.0,
                "industry": "其他未列明制造业",
                "id": "610198742830089"
            },
            {
                "tp": false,
                "in": true,
                "in_name": "史玉英",
                "in_entity": "510",
                "id": "610102195404030025"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "西安宽祥餐饮有限公司经开区分公司",
                "lr_name": "李新会",
                "pc": "710018",
                "business": "许可经营项目：餐饮服务；卷烟、雪茄烟的零售。（依法须经批准的项目，经相关部门批准后方可展开经营活动）\t一般经营项目：***",
                "capital": 10000.0,
                "employee": 5.0,
                "industry": "其他未列明批发业",
                "id": "610197357099445"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "西安晟林科技有限公司",
                "lr_name": "史玉英",
                "pc": "710075",
                "business": "电气设备、电力自动控制设备、电力自动化技术和计算机软件的科研开发、制造销售、应用服务、投资咨询。",
                "capital": 5600000.0,
                "employee": 3.0,
                "industry": "电气信号设备装置制造",
                "id": "610198757838411"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "礼泉县玉祥出租汽车有限公司",
                "lr_name": "伊小荣",
                "pc": "713200",
                "business": "公路客运、货运、出租汽车营运，汽车租赁，汽车零配销售。（依法须经批准的项目，经相关部门批准后方可开展经营活动）",
                "capital": 1000000.0,
                "employee": 6.0,
                "industry": "出租车客运",
                "id": "916104257326695009"
            },
            {
                "tp": false,
                "in": true,
                "in_name": "辛蓉",
                "in_entity": "510",
                "id": "610112197509010524"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "陕西致博物流有限责任公司",
                "lr_name": "王健",
                "pc": "710000",
                "business": "普通货物整批（车）运输；物流配送咨询服务。（依法须经批准的项目，经相关部门批准后方可开展经营活动）",
                "capital": 5000000.0,
                "employee": 3.0,
                "industry": "道路货物运输",
                "id": "610104552181946"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "陕西正源建材有限公司",
                "lr_name": "冯连武",
                "pc": "710077",
                "business": "建筑装饰材料、化工产品的开发、生产、销售及技术服务；环保节能产品、五金交电、电器元件、仪器仪表、机电产品、计算机的销售；管道工程、建筑装饰工程的施工；环保设备、机电设备、工业自动化设备的安装、销售及维修服务。",
                "capital": 5000000.0,
                "employee": 2.0,
                "industry": "其他未列明零售业",
                "id": "610198552308900"
            },
            {
                "tp": false,
                "in": true,
                "in_name": "伊小荣",
                "in_entity": "510",
                "id": "610104197102134445"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "宝鸡信天游汽车服务有限公司",
                "lr_name": "伊小荣",
                "pc": "721000",
                "business": "汽车销售（小轿车除外）；配件、汽车用品销售；汽车美容装潢；二手车销售；汽车维修；汽车租赁。（依法须经批准的项目，经相关部门批准后方可开展经营活动）",
                "capital": 120000.0,
                "employee": 8.0,
                "industry": "汽车修理与维护",
                "id": "91610303305539760Y"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "西安星瑞机电设备有限公司",
                "lr_name": "雷迎飞",
                "pc": "710071",
                "business": "汽车零部件、机电设备（除专控）、汽车（除乘用车）的销售。",
                "capital": 5000000.0,
                "employee": 3.0,
                "industry": "汽车零配件零售",
                "id": "610113663169851"
            },
            {
                "tp": false,
                "in": true,
                "in_name": "孙振宽",
                "in_entity": "510",
                "id": "610104195312280011"
            },
            {
                "tp": false,
                "in": true,
                "in_name": "储亚玲",
                "in_entity": "510",
                "id": "610104196011092142"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "西安恒热环保科技有限责任公司",
                "lr_name": "冯连武",
                "pc": "710086",
                "business": "一般经营项目:粉煤灰的分选及综合利用新产品的开发与销售。(以上经营范围不包含国家规定的专控及前置许可项目)。",
                "capital": 800000.0,
                "employee": 16.0,
                "industry": "其他未列明制造业",
                "id": "610185757849030"
            },
            {
                "tp": true,
                "in": true,
                "tp_name": "西安宽祥餐饮有限公司",
                "lr_name": "孙振宽",
                "pc": "710065",
                "business": "许可经营项目：餐饮服务（中型餐馆：中型类制售、含凉菜、不含裱花蛋糕、不含生食海产品，许可证有效期至２０１３年１１月２６日）",
                "capital": 30000.0,
                "employee": 20.0,
                "industry": "其他资本市场服务",
                "in_name": "西安宽祥餐饮有限公司",
                "in_entity": "159",
                "id": "61011305712352X"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "西安亮丽电力设备有限责任公司",
                "lr_name": "冯连武",
                "pc": "710075",
                "business": "电气设备的制造电力电缆,电力通讯设备,电气设备的安装,修理,调试,销售;电力办公自动化设备,电气设备,计算机软件的开发及技术咨询,服务.",
                "capital": 1000000.0,
                "employee": 10.0,
                "industry": "发电机及发电机组制造",
                "id": "610198628054290"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "陕西怀矩堂文化发展有限公司",
                "lr_name": "冯连武",
                "pc": "710000",
                "business": "艺术品的经营与投资；展示展览筹划与实施；文化活动的推广、交流与传播；工艺礼品的销售。",
                "capital": 5000000.0,
                "employee": 3.0,
                "industry": "其他未列明零售业",
                "id": "610103661197947"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "陕西信天游保险代理有限公司",
                "lr_name": "伊小荣",
                "pc": "710071",
                "business": "代理销售保险产品；代理收取保险费；根据保险公司的委托，代理相关业务的损失勘查和理赔。",
                "capital": 3000000.0,
                "employee": 12.0,
                "industry": "其他专业咨询",
                "id": "610113779930569"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "兴平市信天游汽车服务有限公司",
                "lr_name": "张斌",
                "pc": "713100",
                "business": "洗车展示，代理汽车销售，车辆维修，配件销售，汽车租赁，车辆装潢及美容。（依法须经批准的项目，经相关部门批准后方可开展经营活动）",
                "capital": 700000.0,
                "employee": 10.0,
                "industry": "汽车修理与维护",
                "id": "610481305402609"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "渭南信天游汽车销售服务有限公司",
                "lr_name": "吕玉良",
                "pc": "714000",
                "business": "汽车销售；汽车零配件、汽车用品、汽车辅料的销售；机动车维修（凭许可证明文件在有效期内经营）;汽车装潢；销售业务推广及宣传。（依法须经批准的项目，经相关部门批准后方可开展经营活动）",
                "capital": 6000000.0,
                "employee": 20.0,
                "industry": "汽车零售",
                "id": "91610594MA6Y22320M"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "陕西成长出国留学咨询服务有限公司",
                "lr_name": "伊小荣",
                "pc": "710000",
                "business": "许可经营项目：出国中介（依法须经批准的项目，经相关部门批准后方可开展经营活动）。",
                "capital": 2000000.0,
                "employee": 2.0,
                "industry": "其他专业咨询",
                "id": "91610135MA6TXEGK84"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "陕西恒智科工贸有限责任公司",
                "lr_name": "冯连武",
                "pc": "710086",
                "business": "化工产品（危险、易制毒化学品除外）、金属材料（贵稀有金属除外）、电力设备、电线电缆、机动车配件、水暖器材、建筑材料、仪器仪表、五金交电、通讯器材（地面卫星接收系统除外）、办公自动化设备的销售；环境治理工程、给排水处理工程的咨询服务；电子设备及仪器仪表配件的生产。（依法须经批准的项目，经相关部门批准后方可开展经营活动）",
                "capital": 5000000.0,
                "employee": 6.0,
                "industry": "其他化工产品批发",
                "id": "916100006237382398"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "西安亮丽中超电力线缆有限公司",
                "lr_name": "冯连武",
                "pc": "710016",
                "business": "电解铜、无氧铜杆、变压器、开关柜及配件、电线电缆系列产品的销售；电力设计、安装；电线电缆系列产品的制造。",
                "capital": 900000.0,
                "employee": 40.0,
                "industry": "其他常用有色金属冶炼",
                "id": "610103628001375"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "陕西融泰汽车销售服务有限公司",
                "lr_name": "伊小荣",
                "pc": "710016",
                "business": "东风雪铁龙品牌汽车销售；小型汽车维修（机动车维修经营许可证有效期至2017年03月08日）；汽车用品、辅料的销售；汽车美容；代理车务服务（租赁除外）；代理机动车辆保险（保险兼业代理业务许可证有效期至2014年07月07日）；二手车置换。（上述范围涉及许可经营项目的，凭许可证在有效期内经营，未经许可，不得经营。）",
                "capital": 5000000.0,
                "employee": 32.0,
                "industry": "其他未列明批发业",
                "id": "610185698447743"
            },
            {
                "tp": false,
                "in": true,
                "in_name": "刘浩",
                "in_entity": "510",
                "id": "610203198105215017"
            },
            {
                "tp": false,
                "in": true,
                "in_name": "史友琴",
                "in_entity": "510",
                "id": "61010419650120512X"
            },
            {
                "tp": false,
                "in": true,
                "in_name": "王键",
                "in_entity": "510",
                "id": "610102196103140313"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "陕西本源电力工程建设有限公司",
                "lr_name": "冯连武",
                "pc": "710043",
                "business": "电力工程的设计、施工及技术服务",
                "capital": 3000000.0,
                "employee": 20.0,
                "industry": "其他未列明专业技术服务业",
                "id": "610104050442958"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "铜川和信科技环保有限责任公司",
                "lr_name": "许坚",
                "pc": "727031",
                "business": "工业废弃物（粉煤灰、脱硫石膏、炉渣）、一般建筑材料的收购、销售",
                "capital": 500000.0,
                "employee": 8.0,
                "industry": "再生物资回收与批发",
                "id": "610201694932047"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "陕西卓晟汽车销售有限公司",
                "lr_name": "孙振宽",
                "pc": "714000",
                "business": "汽车（小轿车除外）及配件销售；汽车装潢。",
                "capital": 3000000.0,
                "employee": 10.0,
                "industry": "其他未列明零售业",
                "id": "610597074500796"
            },
            {
                "in": false,
                "tp": true,
                "tp_name": "陕西正源股份有限公司",
                "lr_name": "冯连武",
                "pc": "710071",
                "business": "建筑、金属、装饰材料与针纺织品、通讯器材、化工产品、暖道设备、五金交电、电器元件、仪器仪表、机电产品、计算机、办公自动化设备的销售；粉煤灰的深加工；管道工程、环保设备、污水处理设备、机电设备的安装、调试及咨询服务；物流配送信息咨询服务。",
                "capital": 30000000.0,
                "employee": 3.0,
                "industry": "其他未列明批发业",
                "id": "610198671502546"
            }
        ],
        "links": [
            {
                "in_ratio": 1.0,
                "source": "610102195309030035",
                "target": "610103628001375"
            },
            {
                "in_ratio": 0.9,
                "source": "610102195309030035",
                "target": "610185698447743"
            },
            {
                "in_ratio": 0.5,
                "source": "610102195309030035",
                "target": "610104050442958"
            },
            {
                "in_ratio": 0.3,
                "source": "610102195309030035",
                "target": "610198671502546"
            },
            {
                "in_ratio": 0.1,
                "source": "610102195309030035",
                "target": "610198628054290"
            },
            {
                "in_ratio": 0.3,
                "source": "610623195605090111",
                "target": "610198671502546"
            },
            {
                "in_ratio": 0.3,
                "source": "610623195605090111",
                "target": "610103661197947"
            },
            {
                "in_ratio": 1.0,
                "source": "610104197308022131",
                "target": "610201694932047"
            },
            {
                "in_ratio": 0.4,
                "source": "610104197308022131",
                "target": "610103661197947"
            },
            {
                "in_ratio": 0.4,
                "source": "610104197308022131",
                "target": "610198671502546"
            },
            {
                "in_ratio": 1.0,
                "source": "610102195404030025",
                "target": "610198552308900"
            },
            {
                "in_ratio": 0.612,
                "source": "610102195404030025",
                "target": "610198757838411"
            },
            {
                "in_ratio": 0.494,
                "source": "610102195404030025",
                "target": "916100006237382398"
            },
            {
                "in_ratio": 0.3,
                "source": "610102195404030025",
                "target": "610103661197947"
            },
            {
                "in_ratio": 0.4,
                "source": "610112197509010524",
                "target": "916104257326695009"
            },
            {
                "in_ratio": 0.4,
                "source": "610112197509010524",
                "target": "616999710070935"
            },
            {
                "in_ratio": 0.82,
                "source": "610104197102134445",
                "target": "610113779930569"
            },
            {
                "in_ratio": 0.5,
                "source": "610104197102134445",
                "target": "91610303305539760Y"
            },
            {
                "in_ratio": 0.4,
                "source": "610104197102134445",
                "target": "610481305402609"
            },
            {
                "in_ratio": 0.2,
                "source": "610104197102134445",
                "target": "91610135MA6TXEGK84"
            },
            {
                "in_ratio": 0.2,
                "source": "610104197102134445",
                "target": "610113663169851"
            },
            {
                "in_ratio": 0.1,
                "source": "610104197102134445",
                "target": "610597074500796"
            },
            {
                "in_ratio": 0.1,
                "source": "610104197102134445",
                "target": "610185698447743"
            },
            {
                "in_ratio": 1.0,
                "source": "610104195312280011",
                "target": "91610594MA6Y22320M"
            },
            {
                "in_ratio": 0.94,
                "source": "610104195312280011",
                "target": "610481709954696"
            },
            {
                "in_ratio": 0.8,
                "source": "610104195312280011",
                "target": "91610135MA6TXEGK84"
            },
            {
                "in_ratio": 0.8,
                "source": "610104195312280011",
                "target": "610597074500796"
            },
            {
                "in_ratio": 0.8,
                "source": "610104195312280011",
                "target": "610113074527497"
            },
            {
                "in_ratio": 0.6667,
                "source": "610104195312280011",
                "target": "61011305712352X"
            },
            {
                "in_ratio": 0.6,
                "source": "610104195312280011",
                "target": "916104257326695009"
            },
            {
                "in_ratio": 0.6,
                "source": "610104195312280011",
                "target": "616999710070935"
            },
            {
                "in_ratio": 0.1666,
                "source": "610104195312280011",
                "target": "91610303305539760Y"
            },
            {
                "in_ratio": 0.3333,
                "source": "610104196011092142",
                "target": "61011305712352X"
            },
            {
                "in_ratio": 0.2,
                "source": "610104196011092142",
                "target": "610113074527497"
            },
            {
                "in_ratio": 1.0,
                "source": "61011305712352X",
                "target": "610197357099445"
            },
            {
                "in_ratio": 0.6,
                "source": "610203198105215017",
                "target": "91610201580769253D"
            },
            {
                "in_ratio": 0.4,
                "source": "610203198105215017",
                "target": "610104552181946"
            },
            {
                "in_ratio": 0.3,
                "source": "61010419650120512X",
                "target": "610104552181946"
            },
            {
                "in_ratio": 0.20199999999999999,
                "source": "61010419650120512X",
                "target": "916100006237382398"
            },
            {
                "in_ratio": 0.1,
                "source": "61010419650120512X",
                "target": "610185757849030"
            },
            {
                "in_ratio": 0.4,
                "source": "610102196103140313",
                "target": "610198742830089"
            },
            {
                "in_ratio": 0.304,
                "source": "610102196103140313",
                "target": "916100006237382398"
            },
            {
                "in_ratio": 0.3,
                "source": "610102196103140313",
                "target": "610104552181946"
            }
        ]
    }
    const links = data.links.map(link => {
        // link.type = link.control? 'control' : 'invest'
        link.value = link.in_ratio
        return Object.create(link)
    });
    const nodes = data.nodes.map(node => {
         //        "in": false,
         //        "tp": true,
         //        "tp_name": "西安宽祥餐饮有限公司经开区分公司",
         //        "lr_name": "李新会",
         //        "pc": "710018",
         //        "business": "许可经营项目：餐饮服务；卷烟、雪茄烟的零售。（依法须经批准的项目，经相关部门批准后方可展开经营活动）\t一般经营项目：***",
         //        "capital": 10000.0,
         //        "employee": 5.0,
         //        "industry": "其他未列明批发业",
         //        "id": "610197357099445"
        node.type = node.in? 'investor' : (node.tp? 'taxpayer':'controller')
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
            if(d.in)return d.in_name
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
