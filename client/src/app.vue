<template>
    <div id="app" class="MainView">
        <el-row class="overview">
            <el-col :span="19" class="overview">
                <temporal-view
                        class="overview-left"
                        :temporal-overview="temporalOverview"
                        :loading-time-slider="loadingDetailGraph"
                        @setPeriod="setPeriod">
                </temporal-view>
                <group-view
                        class="overview-left"
                        :affiliated-party-topo-list="affiliatedPartyTopoList"
                        :loading-topo="loadingTopoList">
                </group-view>
            </el-col>
            <el-col :span="5" class="overview">
                <el-row class="overview-right-control">
                    <el-row>
                        <el-col :span="10" class="overview-right-control-row">Period</el-col>
                        <el-col :span="14" class="overview-right-control-row">{{periodStart}} to {{periodEnd}}</el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="10" class="overview-right-control-row">Transaction chain</el-col>
                        <el-col :span="11"><el-input-number size="mini" v-model="transactionChain" :min="1" :max="10"></el-input-number></el-col>
                        <el-col :span="3"></el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="10" class="overview-right-control-row">Control chain</el-col>
                        <el-col :span="11"><el-input-number size="mini" v-model="controlChain" :min="1" :max="10"></el-input-number></el-col>
                        <el-col :span="3"><el-button size="mini" circle icon="el-icon-setting" @click="setModelSetting"></el-button></el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="10" class="overview-right-control-row">Search ID</el-col>
                        <el-col :span="11"><el-input size="mini" v-model="search_id"></el-input></el-col>
                        <el-col :span="3"><el-button size="mini" circle icon="el-icon-search" @click="searchID"></el-button></el-col>
                    </el-row>
                </el-row>
                <suspicious-group-list
                        class="overview-right-list"
                        :affiliated-party-list="affiliatedPartyList"
                        :loading-list="loadingList">
                </suspicious-group-list>
            </el-col>
        </el-row>
        <el-row class="detail-view">
            <!--            <el-col style="width: 25%; height: 60%">-->
            <!--                <detail-view-->
            <!--                        class="grid-content"-->
            <!--                        :affiliated-party-detail="affiliatedPartyDetail"-->
            <!--                        :loading-graph="loadingCalendar">-->
            <!--                </detail-view>-->
            <!--            </el-col>-->
            <graph-view
                    class="detail-view-graph"
                    :affiliated-party-detail="affiliatedPartyDetail"
                    :loading-graph="loadingGraph">
            </graph-view>
            <parallel-view
                    class="detail-view-parallel"
                    :affiliated-party-detail="affiliatedPartyDetail"
                    :loading-graph="loadingGraph">
            </parallel-view>
        </el-row>
        <el-row style="height: 100%">
            <di-graph-view
                    :affiliated-party-detail="affiliatedPartyDetail"
                    :loading-graph="loadingGraph"
                    style="width: 100%; height: 100%; ">
            </di-graph-view>
        </el-row>
    </div>

</template>

<script>
  import SuspiciousGroupList from './components/suspicious-group-list'
  import GraphView from './components/graph-view.vue';
  import DiGraphView from './components/digraph-view.vue';
  // import DetailView from './components/detail-view.vue';
  import GroupView from './components/group-view.vue';
  import TemporalView from './components/temporal-view.vue';
  import ParallelView from './components/parallel-view.vue';
  // import TsneView from './components/tsne-view.vue';

  import DataService from './utils/data-service'
  import EventService from "./utils/event-service";

  export default {
    name: 'app',
    components: {
      SuspiciousGroupList,
      GraphView,
      DiGraphView,
      GroupView,
      TemporalView,
      ParallelView,
    },
    data() {
      return {
        temporalOverview:{},
        affiliatedPartyList: [],
        affiliatedPartyTopoList:[],
        affiliatedPartyDetail: {},
        affiliatedTransactionDetail:{},

        periodStart: '2014-01-01',
        periodEnd: '2015-12-31',
        transactionChain: 5,
        controlChain: 3,
        search_id: '610198671502546',

        loadingList: true,
        loadingTopoList: true,
        loadingGraph: true,
        loadingDetailGraph:true,
        loadingGroupGlyph:true,
        loadingTimeSlider:true,
        loadingCalendar:true,

        default_detail_transaction_source:"610201694932047",
        default_detail_transaction_target:"610198671502546"
      }
    },
    mounted () {
      // First load the temporal overview
      DataService.loadTemporalOverview((data)=>{
        this.temporalOverview = data;
        this.loadingTimeSlider = false;
      });

      DataService.loadAffiliatedPartyList(null, (data)=>{
        this.affiliatedPartyList = data;
        this.loadingList = false;
      });

      DataService.loadAffiliatedPartyTopoList((data)=>{
        this.affiliatedPartyTopoList = data;
        this.loadingTopoList = false;
      });

      DataService.loadAffiliatedPartyDetailByAP(null, data=>{
        this.affiliatedPartyDetail = data;
        this.loadingGraph = false;
      });

      DataService.loadDetailAffiliatedTransaction(null,(data)=>{
        this.affiliatedTransactionDetail = data;
        this.loadingDetailGraph = false;
      });

      EventService.onAffiliatedTransactionSelected((source, target)=>{
        this.loadingDetailGraph = true;
        let para = {'source': source, 'target':target};
        DataService.loadDetailAffiliatedTransaction(para,(data)=>{
          this.affiliatedTransactionDetail = data;
          this.loadingDetailGraph = false;
        });
      });

      EventService.onSuspiciousGroupSelected(ap_id=>{
        this.loadingGraph = true;
        let para = {'ap_id': ap_id};
        DataService.loadAffiliatedPartyDetailByAP(para, data=>{
          this.affiliatedPartyDetail = data;
          this.loadingGraph = false;
        });
      });
    },
    methods: {
      setPeriod: function (params) {
        console.log(`on message ${params.periodStart} to ${params.periodEnd}`);
        this.periodStart = params.periodStart;
        this.periodEnd = params.periodEnd;
      },
      setModelSetting: function() {
        this.loadingList = true;
        let para = {
          'max_transaction_length': this.transactionChain,
          'max_control_length': this.controlChain
        };
        DataService.setAffiliatedPartySetting(para, data=>{
          this.affiliatedPartyList = data;
          this.loadingList = false;
        })
      },
      searchID: function() {
        this.loadingGraph = true;
        let para = {'tp_id': this.search_id};
        DataService.loadAffiliatedPartyDetailByTP(para, data=>{
          this.affiliatedPartyDetail = data;
          this.loadingGraph = false;
        })
      },
      searchAPT: function() {
        this.loadingDetailGraph = true;
        let para = {
          'source':this.default_detail_transaction_source,
          'target':this.default_detail_transaction_target
        };
        DataService.loadDetailAffiliatedTransaction(para, data=>{
          this.affiliatedTransactionDetail = data;
          this.loadingDetailGraph = false;
        })
      },
    }
  }
</script>

<style>
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        width: 1440px;
        height: 900px;
        border: 1px solid black;
    }

    .overview{
        width: 100%;
        height: 300px;
    }

    .overview-left{
        width: 100%;
        height: 150px;
    }

    .overview-right-control{
        width: 100%;
        height: 110px;
    }

    .overview-right-control-row{
        padding-left: 4px;
        padding-top: 4px;
        text-align: left;
        font-size: small;
    }

    .overview-right-list{
        width: 100%;
        height: 190px;
        background: #e5e9f2;
    }

    .detail-view {
        width: 100%;
        height: 600px;
    }

    .detail-view-graph{
        width: 100%;
        height: 450px;
    }

    .detail-view-parallel{
        width: 100%;
        height: 150px;
    }
</style>