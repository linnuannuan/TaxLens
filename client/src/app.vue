<template>
  <div id="app" class="MainView">
    <el-row :gutter="5" class="MainView">
      <el-col :span="6" class="MainView">
        <el-row>
          <el-row>
            <el-col :span="12"><div style="padding-top: 5px; text-align: left; font-size: small"> Maximum Transaction length </div></el-col>
            <el-col :span="9"><el-input-number size="mini" v-model="max_transaction_length" :min="1" :max="10"></el-input-number></el-col>
            <el-col :span="3"></el-col>
          </el-row>
          <el-row>
            <el-col :span="12"><div style="padding-top: 5px; text-align: left; font-size: small"> Maximum Control length </div></el-col>
            <el-col :span="9"><el-input-number size="mini" v-model="max_control_length" :min="1" :max="10"></el-input-number></el-col>
            <el-col :span="3"><el-button size="mini" circle icon="el-icon-setting" @click="setModelSetting"></el-button></el-col>
          </el-row>
          <el-row>
            <el-col :span="5"><div style="padding-top: 5px; text-align: left; font-size: small"> Search ID </div></el-col>
            <el-col :span="16"><el-input size="mini" clearable v-model="search_id"></el-input></el-col>
            <el-col :span="3"><el-button size="mini" circle icon="el-icon-search" @click="searchID"></el-button></el-col>
          </el-row>
        </el-row>
        <el-row style="height: 400px">
          <suspicious-group-list
              class="grid-list"
              :affiliated-party-list="affiliatedPartyList">
          </suspicious-group-list>
        </el-row>
      </el-col>
      <el-col :span="18" class="MainView">
          <el-row style="height: 50%">
            <div style="width: 100%; height: 100%; ">
              <graph-view
                  class="grid-content"
                  :affiliated-party-detail="affiliatedPartyDetail"
                  style="width: 100%; height: 100%; ">
              </graph-view>
            </div>
          </el-row>
          <el-row style="height: 50%">
            <div style="width: 100%; height: 100%; ">
              <detail-view
                  class="grid-content"
                  :affiliated-party-detail="affiliatedPartyDetail"
                  style="width: 100%; height: 100%; ">
              </detail-view>
            </div>
          </el-row>
      </el-col>
    </el-row>
  </div>



</template>

<script>
  import SuspiciousGroupList from './components/suspicious-group-list'
  import GraphView from './components/graph-view.vue';
  import DetailView from './components/detail-view.vue';


  import DataService from './utils/data-service'
  import EventService from "./utils/event-service";

  export default {
    name: 'app',
    components: {
      SuspiciousGroupList,
      GraphView,
      DetailView,
      // TSNEView,
    },
    data() {
      return {
        affiliatedPartyList: [],
        affiliatedPartyDetail: {},

        max_transaction_length: 5,
        max_control_length: 5,
        search_id: '610198671502546',
      }
    },
    mounted () {
      DataService.loadAffiliatedPartyList((data)=>{
        this.affiliatedPartyList = data;
      });

      DataService.loadAffiliatedPartyDetailByAP(null, data=>{
        this.affiliatedPartyDetail = data;
      });

      EventService.onSuspiciousGroupSelected(ap_id=>{
        let para = {'ap_id': ap_id};
        DataService.loadAffiliatedPartyDetailByAP(para, data=>{
          this.affiliatedPartyDetail = data;
        });
      });
    },
    methods: {
      setModelSetting: function() {
        let para = {
          'max_transaction_length': this.max_transaction_length,
          'max_control_length': this.max_control_length
        };
        DataService.setAffiliatedPartySetting(para, data=>{
          this.affiliatedPartyList = data
        })
      },
      searchID: function() {
        let para = {'tp_id': this.search_id};
        DataService.loadAffiliatedPartyDetailByTP(para, data=>{
          this.affiliatedPartyDetail = data
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
    height: calc(100vh - 14px);
    margin: 2px;
  }

  .MainView{
    height: 100%;
  }

  .el-row {
    margin-bottom: 5px;
  }

  .grid-list {
    background: #e5e9f2;
    height: 100%;
  }
  .grid-content {
    border: 1px solid slategrey;
    border-radius: 5px;
    height: 100%;
  }
</style>