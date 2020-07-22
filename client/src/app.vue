<template>
    <div id="app">
        <el-col :span="6" class="control-panel">
            <el-row class="control-panel-top">
                <el-row>
                    <el-col :span="11" class="control-panel-top-row">Period</el-col>
                    <el-col :span="13" class="control-panel-top-row">{{periodStart}} to {{periodEnd}}</el-col>
                </el-row>
                <el-row>
                    <el-col :span="10" class="control-panel-top-row">Transaction chain</el-col>
                    <el-col :span="12"><el-input-number size="mini" v-model="transactionChain" :min="1" :max="10"></el-input-number></el-col>
                    <el-col :span="2"></el-col>
                </el-row>
                <el-row>
                    <el-col :span="10" class="control-panel-top-row">Control chain</el-col>
                    <el-col :span="12"><el-input-number size="mini" v-model="controlChain" :min="1" :max="10"></el-input-number></el-col>
                    <el-col :span="2"><el-button size="mini" circle icon="el-icon-setting" @click="setModelParameter"></el-button></el-col>
                </el-row>
                <el-row>
                    <el-col :span="10" class="control-panel-top-row">Search ID</el-col>
                    <el-col :span="12"><el-input size="mini" v-model="search_id"></el-input></el-col>
                    <el-col :span="2"><el-button size="mini" circle icon="el-icon-search" @click="searchID"></el-button></el-col>
                </el-row>
            </el-row>
            <group-view
                    class="overview-spatial"
                    :affiliated-party-topo-list="affiliatedPartyTopoList"
                    :loading-topo="loadingTopoList">
            </group-view>
        </el-col>
        <el-col :span="18" class="views">
            <temporal-view
                    class="overview-temporal"
                    :temporal-overview="temporalOverview"
                    :loading-time-slider="loadingDetailGraph"
                    @setPeriod="setPeriod">
            </temporal-view>

            <el-row class="detail-view-graph">
                <graph-view
                        class="detail-view-graph"
                        :affiliated-party-detail="affiliatedPartyDetail"
                        :loading-graph="loadingGraph"
                        :highlight-node="highlightNode"
                        :unhighlight-node="unhighlightNode"
                        >
                </graph-view>
            </el-row>

            <el-row class="detail-view-calendar">
                <calendar-view
                        class="detail-view-calendar"
                        :calendar-data="calendarData"
                        :calendar-source-id="calendarSourceId"
                        :calendar-target-id="calendarTargetId"
                        :loading-calendar="loadingCalendar">
                </calendar-view>
            </el-row>
        </el-col>
    </div>

</template>

<script>
  import GraphView from './components/graph-view.vue';
  import GroupView from './components/group-view.vue';
  import TemporalView from './components/temporal-view.vue';
  import CalendarView from './components/calendar-view.vue';

  import DataService from './utils/data-service'
  import EventService from "./utils/event-service";

  export default {
    name: 'app',
    components: {
      GraphView,
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
        search_id: '',
        highlightNode:null,
        unhighlightNode:null,

        // search_id: '610198671502546',

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

      EventService.onSuspiciousNodeSelected(tp_id=>{
        this.loadingGraph = false;
        this.highlightNode = tp_id;
      });

      EventService.onSuspiciousNodeUnSelected(tp_id=>{
        this.loadingGraph = false;
        this.unhighlightNode = tp_id;
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
        DataService.loadAffiliatedPartyTopoList(para, (data)=>{
          this.affiliatedPartyTopoList = data;
          this.loadingTopoList = false;
        });
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
        color:#444;
        /*color: #2c3e50;*/
        width: 1600px;
        height: 900px;
        border: 1px solid black;
    }

    .control-panel{
        width: 100%;
        height: 100%;
    }

    .control-panel-top{
        width: 100%;
        height: 110px;
    }

    .control-panel-top-row{
        padding-left: 4px;
        padding-top: 4px;
        padding-bottom: 4px;
        text-align: left;
        font-size: 14px;
    }
    .el-row{
        padding:3px;
    }
   .overview-spatial{
        width: 100%;
        height: 764px;
    }

    .views{
        width: 100%;
        height: 100%;
        /*border: 1px solid steelblue;*/
    }

    .overview-temporal{
        width: 100%;
        height: 150px;
    }

    .detail-view-graph{
        width: 100%;
        height: 300px;
        /*border: 1px solid steelblue;*/
    }

    .detail-view-calendar{
        width: 100%;
        height: 450px;
        /*border: 1px solid steelblue;*/
    }
</style>