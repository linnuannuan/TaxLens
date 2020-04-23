<template>
    <div id="app">
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
                        <el-col :span="3"><el-button size="mini" circle icon="el-icon-setting" @click="setModelParameter"></el-button></el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="10" class="overview-right-control-row">Search ID</el-col>
                        <el-col :span="11"><el-input size="mini" v-model="search_id"></el-input></el-col>
                        <el-col :span="3"><el-button size="mini" circle icon="el-icon-search" @click="searchID"></el-button></el-col>
                    </el-row>
                </el-row>
                <group-list
                        class="overview-right-list"
                        :affiliated-party-list="affiliatedPartyList"
                        :loading-list="loadingList">
                </group-list>
            </el-col>
        </el-row>
        <el-row class="detail-view">
            <el-col :span="12" class="detail-view">
                <graph-view
                        class="detail-view-graph"
                        :affiliated-party-detail="affiliatedPartyDetail"
                        :loading-graph="loadingGraph">
                </graph-view>
            </el-col>
            <el-col :span="12" class="detail-view">
                <calendar-view
                        class="detail-view-calendar"
                        :calendar-data="calendarData"
                        :calendar-source-id="calendarSourceId"
                        :calendar-target-id="calendarTargetId"
                        :loading-calendar="loadingCalendar">
                </calendar-view>
            </el-col>
        </el-row>
<!--        <el-row style="height: 100%">-->
<!--            <di-graph-view-->
<!--                    :affiliated-party-detail="affiliatedPartyDetail"-->
<!--                    :loading-graph="loadingGraph"-->
<!--                    style="width: 100%; height: 100%; ">-->
<!--            </di-graph-view>-->
<!--        </el-row>-->
    </div>

</template>

<script>
  import GroupList from './components/group-list'
  import GraphView from './components/graph-view.vue';
  // import DiGraphView from './components/digraph-view.vue';
  import GroupView from './components/group-view.vue';
  import TemporalView from './components/temporal-view.vue';
  import CalendarView from './components/calendar-view.vue';

  import DataService from './utils/data-service'
  import EventService from "./utils/event-service";

  export default {
    name: 'app',
    components: {
      GroupList,
      GraphView,
      // DiGraphView,
      GroupView,
      TemporalView,
      CalendarView,
    },
    data() {
      return {
        // Data acquired from server
        temporalOverview:{},
        affiliatedPartyList: [],
        affiliatedPartyTopoList:[],
        affiliatedPartyDetail: {},
        affiliatedTransactionDetail:{},
        calendarData:[],

        // Model settings
        periodStart: '2014-01-01',
        periodEnd: '2014-12-31',
        transactionChain: 3,
        controlChain: 2,
        search_id: '610198671502546',

        // Calendar query
        calendarSourceId: '610198748609852',
        calendarTargetId: '610198684755147',

        // Loading variable
        loadingList: true,
        loadingTopoList: true,
        loadingGraph: true,
        loadingCalendar:true,
        loadingDetailGraph:true,
        loadingGroupGlyph:true,
        loadingTimeSlider:true,

        // Default cases
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

      this.setModelParameter();

      DataService.loadAffiliatedPartyDetailByAP(null, data=>{
        this.affiliatedPartyDetail = data;
        this.loadingGraph = false;
      });

      DataService.loadCalendarDataByTransaction(null,(data)=>{
        this.calendarData = data;
        this.loadingCalendar = false;
      });

      EventService.onSuspiciousGroupSelected(ap_id=>{
        this.loadingGraph = true;
        let para = {'ap_id': ap_id};
        DataService.loadAffiliatedPartyDetailByAP(para, data=>{
          this.affiliatedPartyDetail = data;
          this.loadingGraph = false;
        });
      });

      EventService.onAffiliatedTransactionSelected((source, target, periodStart, periodEnd)=>{
        this.calendarSourceId = source || this.calendarSourceId;
        this.calendarTargetId = target || this.calendarTargetId;
        let para = {
          'seller_id': source || this.calendarSourceId,
          'buyer_id': target || this.calendarTargetId,
          'start_time': periodStart || this.periodStart,
          'end_time': periodEnd || this.periodEnd,
        };
        DataService.loadCalendarDataByTransaction(para, data=>{
          this.calendarData = data;
          this.loadingCalendar = false;
        })
      });
    },
    methods: {
      setPeriod: function (params) {
        this.periodStart = params.periodStart;
        this.periodEnd = params.periodEnd;
      },
      setModelParameter: function() {
        this.loadingList = true;
        this.loadingTopoList = true;
        let para = {
          'start_time': this.periodStart,
          'end_time': this.periodEnd,
          'max_txn_length': this.transactionChain,
          'max_control_length': this.controlChain
        };
        DataService.loadAffiliatedPartyList(para, data=>{
          this.affiliatedPartyList = data;
          this.loadingList = false;

          DataService.loadAffiliatedPartyTopoList((data)=>{
            this.affiliatedPartyTopoList = data;
            this.loadingTopoList = false;
          });
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
        /*border: 1px solid steelblue;*/
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
        padding-bottom: 4px;
        text-align: left;
        font-size: 14px;
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
        /*border: 1px solid steelblue;*/
    }

    .detail-view-calendar{
        width: 100%;
        height: 100%;
        /*border: 1px solid steelblue;*/
    }
</style>