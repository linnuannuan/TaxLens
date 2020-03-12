/* eslint-disable */
import * as d3 from "d3";
let width = 960,
    height = 500,
    margin = 40,
    scalepop = d3.scaleSqrt().domain([0, 100000]).range([0.2, 24]),
    scalecountry = d3.scaleOrdinal(d3.schemeCategory10),

    centerx = d3.scaleLinear()
                .range([width / 2 - height / 2 + margin, width / 2 + height / 2 - margin]);

    var centery = d3.scaleLinear()
                        .range([margin, height - margin]);

    var cities =[
    {
        "2015": "38001.018",
        "2030": "37190.489",
        "Country Code": "392.0",
        "Urban Agglomeration": "Tokyo",
        "Latitude": "35.6895",
        "Longitude": "139.69171"
    },
    {
        "2015": "25703.168",
        "2030": "36060.1",
        "Country Code": "356.0",
        "Urban Agglomeration": "Delhi",
        "Latitude": "28.66667",
        "Longitude": "77.21667"
    },
    {
        "2015": "23740.778",
        "2030": "30750.671",
        "Country Code": "156.0",
        "Urban Agglomeration": "Shanghai",
        "Latitude": "31.22222",
        "Longitude": "121.45806"
    },
    {
        "2015": "21066.245",
        "2030": "23444.363",
        "Country Code": "76.0",
        "Urban Agglomeration": "São Paulo",
        "Latitude": "-23.5475",
        "Longitude": "-46.63611"
    },
    {
        "2015": "21042.538",
        "2030": "27796.555",
        "Country Code": "356.0",
        "Urban Agglomeration": "Mumbai (Bombay)",
        "Latitude": "19.073975",
        "Longitude": "72.880838"
    },
    {
        "2015": "20998.543",
        "2030": "23864.706",
        "Country Code": "484.0",
        "Urban Agglomeration": "Ciudad de México (Mexico City)",
        "Latitude": "19.427318",
        "Longitude": "-99.141869"
    },
    {
        "2015": "20383.994",
        "2030": "27706.032",
        "Country Code": "156.0",
        "Urban Agglomeration": "Beijing",
        "Latitude": "39.9075",
        "Longitude": "116.39723"
    },
    {
        "2015": "20237.645",
        "2030": "19975.677",
        "Country Code": "392.0",
        "Urban Agglomeration": "Kinki M.M.A. (Osaka)",
        "Latitude": "34.675834",
        "Longitude": "135.553823"
    },
    {
        "2015": "18771.769",
        "2030": "24502.15",
        "Country Code": "818.0",
        "Urban Agglomeration": "Al-Qahirah (Cairo)",
        "Latitude": "30.039173",
        "Longitude": "31.239411"
    },
    {
        "2015": "18593.22",
        "2030": "19885.263",
        "Country Code": "840.0",
        "Urban Agglomeration": "New York-Newark",
        "Latitude": "40.717042",
        "Longitude": "-74.003663"
    },
    {
        "2015": "17598.228",
        "2030": "27373.593",
        "Country Code": "50.0",
        "Urban Agglomeration": "Dhaka",
        "Latitude": "23.7104",
        "Longitude": "90.40744"
    },
    {
        "2015": "16617.644",
        "2030": "24837.881",
        "Country Code": "586.0",
        "Urban Agglomeration": "Karachi",
        "Latitude": "24.9056",
        "Longitude": "67.0822"
    },
    {
        "2015": "15180.176",
        "2030": "16956.491",
        "Country Code": "32.0",
        "Urban Agglomeration": "Buenos Aires",
        "Latitude": "-34.605083",
        "Longitude": "-58.400368"
    },
    {
        "2015": "14864.919",
        "2030": "19092.461",
        "Country Code": "356.0",
        "Urban Agglomeration": "Kolkata (Calcutta)",
        "Latitude": "22.533455",
        "Longitude": "88.356045"
    },
    {
        "2015": "14163.989",
        "2030": "16694.313",
        "Country Code": "792.0",
        "Urban Agglomeration": "Istanbul",
        "Latitude": "41.0138",
        "Longitude": "28.9497"
    },
    {
        "2015": "13331.579",
        "2030": "17380.364",
        "Country Code": "156.0",
        "Urban Agglomeration": "Chongqing",
        "Latitude": "29.56278",
        "Longitude": "106.55278"
    },
    {
        "2015": "13122.829",
        "2030": "24239.435",
        "Country Code": "566.0",
        "Urban Agglomeration": "Lagos",
        "Latitude": "6.45306",
        "Longitude": "3.39583"
    },
    {
        "2015": "12946.263",
        "2030": "16755.63",
        "Country Code": "608.0",
        "Urban Agglomeration": "Manila",
        "Latitude": "14.6042",
        "Longitude": "120.9822"
    },
    {
        "2015": "12902.306",
        "2030": "14173.748",
        "Country Code": "76.0",
        "Urban Agglomeration": "Rio de Janeiro",
        "Latitude": "-22.90278",
        "Longitude": "-43.2075"
    },
    {
        "2015": "12458.13",
        "2030": "17574.395",
        "Country Code": "156.0",
        "Urban Agglomeration": "Guangzhou, Guangdong",
        "Latitude": "23.125457",
        "Longitude": "113.257374"
    },
    {
        "2015": "12309.53",
        "2030": "13256.838",
        "Country Code": "840.0",
        "Urban Agglomeration": "Los Angeles-Long Beach-Santa Ana",
        "Latitude": "34.031656",
        "Longitude": "-118.241716"
    },
    {
        "2015": "12165.704",
        "2030": "12200.375",
        "Country Code": "643.0",
        "Urban Agglomeration": "Moskva (Moscow)",
        "Latitude": "55.754996",
        "Longitude": "37.621849"
    },
    {
        "2015": "11586.914",
        "2030": "19996.156",
        "Country Code": "180.0",
        "Urban Agglomeration": "Kinshasa",
        "Latitude": "-4.32758",
        "Longitude": "15.31357"
    },
    {
        "2015": "11210.329",
        "2030": "14655.411",
        "Country Code": "156.0",
        "Urban Agglomeration": "Tianjin",
        "Latitude": "39.108842",
        "Longitude": "117.18862"
    },
    {
        "2015": "10843.285",
        "2030": "11803.252",
        "Country Code": "250.0",
        "Urban Agglomeration": "Paris",
        "Latitude": "48.85341",
        "Longitude": "2.3488"
    },
    {
        "2015": "10749.473",
        "2030": "12672.821",
        "Country Code": "156.0",
        "Urban Agglomeration": "Shenzhen",
        "Latitude": "22.541487",
        "Longitude": "114.063427"
    },
    {
        "2015": "10323.142",
        "2030": "13811.975",
        "Country Code": "360.0",
        "Urban Agglomeration": "Jakarta",
        "Latitude": "-6.211831",
        "Longitude": "106.841646"
    },
    {
        "2015": "10313.307",
        "2030": "11467.322",
        "Country Code": "826.0",
        "Urban Agglomeration": "London",
        "Latitude": "51.50853",
        "Longitude": "-0.12574"
    },
    {
        "2015": "10087.132",
        "2030": "14762.088",
        "Country Code": "356.0",
        "Urban Agglomeration": "Bangalore",
        "Latitude": "12.97194",
        "Longitude": "77.59369"
    },
    {
        "2015": "9897.033",
        "2030": "12221.301",
        "Country Code": "604.0",
        "Urban Agglomeration": "Lima",
        "Latitude": "-12.04318",
        "Longitude": "-77.02824"
    },
    {
        "2015": "9890.427",
        "2030": "13920.944",
        "Country Code": "356.0",
        "Urban Agglomeration": "Chennai (Madras)",
        "Latitude": "13.053091",
        "Longitude": "80.24875"
    },
    {
        "2015": "9773.746",
        "2030": "9959.675",
        "Country Code": "410.0",
        "Urban Agglomeration": "Seoul",
        "Latitude": "37.56826",
        "Longitude": "126.97783"
    },
    {
        "2015": "9764.769",
        "2030": "11966.118",
        "Country Code": "170.0",
        "Urban Agglomeration": "Bogotá",
        "Latitude": "4.60971",
        "Longitude": "-74.08175"
    },
    {
        "2015": "9406.264",
        "2030": "9304.101",
        "Country Code": "392.0",
        "Urban Agglomeration": "Chukyo M.M.A. (Nagoya)",
        "Latitude": "35.18147",
        "Longitude": "136.90641"
    },
    {
        "2015": "9398.698",
        "2030": "11573.129",
        "Country Code": "710.0",
        "Urban Agglomeration": "Johannesburg",
        "Latitude": "-26.20227",
        "Longitude": "28.04363"
    },
    {
        "2015": "9269.823",
        "2030": "11527.934",
        "Country Code": "764.0",
        "Urban Agglomeration": "Krung Thep (Bangkok)",
        "Latitude": "13.721964",
        "Longitude": "100.525248"
    },
    {
        "2015": "8943.523",
        "2030": "12773.548",
        "Country Code": "356.0",
        "Urban Agglomeration": "Hyderabad",
        "Latitude": "17.37528",
        "Longitude": "78.47444"
    },
    {
        "2015": "8744.835",
        "2030": "9493.032",
        "Country Code": "840.0",
        "Urban Agglomeration": "Chicago",
        "Latitude": "41.85003",
        "Longitude": "-87.65005"
    },
    {
        "2015": "8741.365",
        "2030": "13033.135",
        "Country Code": "586.0",
        "Urban Agglomeration": "Lahore",
        "Latitude": "31.5497222",
        "Longitude": "74.3436111"
    },
    {
        "2015": "8432.196",
        "2030": "9989.806",
        "Country Code": "364.0",
        "Urban Agglomeration": "Tehran",
        "Latitude": "35.69439",
        "Longitude": "51.42151"
    },
    {
        "2015": "7905.572",
        "2030": "9441.574",
        "Country Code": "156.0",
        "Urban Agglomeration": "Wuhan",
        "Latitude": "30.58333",
        "Longitude": "114.26667"
    },
    {
        "2015": "7555.705",
        "2030": "10104.406",
        "Country Code": "156.0",
        "Urban Agglomeration": "Chengdu",
        "Latitude": "30.66667",
        "Longitude": "104.06667"
    },
    {
        "2015": "7434.935",
        "2030": "8700.622",
        "Country Code": "156.0",
        "Urban Agglomeration": "Dongguan",
        "Latitude": "23.02116",
        "Longitude": "113.741411"
    },
    {
        "2015": "7369.157",
        "2030": "9754.28",
        "Country Code": "156.0",
        "Urban Agglomeration": "Nanjing, Jiangsu",
        "Latitude": "32.048183",
        "Longitude": "118.789812"
    },
    {
        "2015": "7342.85",
        "2030": "10526.6",
        "Country Code": "356.0",
        "Urban Agglomeration": "Ahmadabad",
        "Latitude": "23.03333",
        "Longitude": "72.61667"
    },
    {
        "2015": "7313.557",
        "2030": "7885.155",
        "Country Code": "344.0",
        "Urban Agglomeration": "Hong Kong",
        "Latitude": "22.279588",
        "Longitude": "114.188697"
    },
    {
        "2015": "7297.78",
        "2030": "10200.392",
        "Country Code": "704.0",
        "Urban Agglomeration": "Thành Pho Ho Chí Minh (Ho Chi Minh City)",
        "Latitude": "10.75",
        "Longitude": "106.66667"
    },
    {
        "2015": "7035.945",
        "2030": "8353.315",
        "Country Code": "156.0",
        "Urban Agglomeration": "Foshan",
        "Latitude": "23.022778",
        "Longitude": "113.119953"
    },
    {
        "2015": "6836.911",
        "2030": "9422.889",
        "Country Code": "458.0",
        "Urban Agglomeration": "Kuala Lumpur",
        "Latitude": "3.1412",
        "Longitude": "101.68653"
    },
    {
        "2015": "6642.848",
        "2030": "9710.309",
        "Country Code": "368.0",
        "Urban Agglomeration": "Baghdad",
        "Latitude": "33.34058",
        "Longitude": "44.40088"
    },
    {
        "2015": "6507.4",
        "2030": "7122.444",
        "Country Code": "152.0",
        "Urban Agglomeration": "Santiago",
        "Latitude": "-33.45694",
        "Longitude": "-70.64827"
    },
    {
        "2015": "6390.637",
        "2030": "8821.757",
        "Country Code": "156.0",
        "Urban Agglomeration": "Hangzhou",
        "Latitude": "30.29365",
        "Longitude": "120.16142"
    },
    {
        "2015": "6369.71",
        "2030": "7940.087",
        "Country Code": "682.0",
        "Urban Agglomeration": "Ar-Riyadh (Riyadh)",
        "Latitude": "24.690466",
        "Longitude": "46.709566"
    },
    {
        "2015": "6315.47",
        "2030": "7910.905",
        "Country Code": "156.0",
        "Urban Agglomeration": "Shenyang",
        "Latitude": "41.79222",
        "Longitude": "123.43278"
    },
    {
        "2015": "6199.254",
        "2030": "6707.421",
        "Country Code": "724.0",
        "Urban Agglomeration": "Madrid",
        "Latitude": "40.4165",
        "Longitude": "-3.70256"
    },
    {
        "2015": "6043.7",
        "2030": "7903.831",
        "Country Code": "156.0",
        "Urban Agglomeration": "Xi'an, Shaanxi",
        "Latitude": "34.289413",
        "Longitude": "108.940242"
    },
    {
        "2015": "5992.739",
        "2030": "6956.552",
        "Country Code": "124.0",
        "Urban Agglomeration": "Toronto",
        "Latitude": "43.70011",
        "Longitude": "-79.4163"
    },
    {
        "2015": "5817.221",
        "2030": "6553.633",
        "Country Code": "840.0",
        "Urban Agglomeration": "Miami",
        "Latitude": "25.789097",
        "Longitude": "-80.204044"
    },
    {
        "2015": "5727.53",
        "2030": "8091.387",
        "Country Code": "356.0",
        "Urban Agglomeration": "Pune (Poona)",
        "Latitude": "18.516057",
        "Longitude": "73.861578"
    },
    {
        "2015": "5716.422",
        "2030": "6438.83",
        "Country Code": "76.0",
        "Urban Agglomeration": "Belo Horizonte",
        "Latitude": "-19.92083",
        "Longitude": "-43.93778"
    }];
      console.log(cities);
      const data = cities
        .sort((a, b) => d3.descending(+a[2015], +b[2015]))
        .map((d, i) => [+d.Longitude, + d.Latitude, d['Urban Agglomeration'], +d[2015], +d['Country Code']])
        .slice(0, 800);

      const canvas = d3.select("#tsne_view").append("canvas")
        .attr("width", width)
        .attr("height", height);

      const model = new tsnejs.tSNE({
        dim: 2,
        perplexity: 30,
      });

      // initialize data with pairwise distances
      const dists = data.map(d => data.map(e => d3.geoDistance(d, e)));
      model.initDataDist(dists);


      const forcetsne = d3.forceSimulation(
            data.map(d => (d.x = width / 2, d.y = height / 2, d))
         )
        .alphaDecay(0.005)
        .alpha(0.1)
        .force('tsne', function (alpha) {
          // every time you call this, solution gets better
          model.step();

          // Y is an array of 2-D points that you can plot
          let pos = model.getSolution();

          centerx.domain(d3.extent(pos.map(d => d[0])));
          centery.domain(d3.extent(pos.map(d => d[1])));

          data.forEach((d, i) => {
                d.x += alpha * (centerx(pos[i][0]) - d.x);
                d.y += alpha * (centery(pos[i][1]) - d.y);
              });
            })
            .force('collide', d3.forceCollide().radius(d => 1.5 + scalepop(d[3])))
            .on('tick', function () {

              let nodes = data.map((d, i) => {
                return {
                  x: d.x,
                  y: d.y,
                  r: scalepop(d[3]),
                  color: scalecountry(d[4]),
                };
              });

              draw(canvas, nodes);

            });

          function draw(canvas, nodes) {
            let context = canvas.node().getContext("2d");
            context.clearRect(0, 0, width, width);

            for (var i = 0, n = nodes.length; i < n; ++i) {
              var node = nodes[i];
              context.beginPath();
              context.moveTo(node.x, node.y);
              context.arc(node.x, node.y, node.r, 0, 2 * Math.PI);
              context.lineWidth = 0.5;
              context.fillStyle = node.color;
              context.fill();
            }
          }
        ;