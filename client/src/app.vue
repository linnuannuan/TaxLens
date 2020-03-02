<template>
  <div id="app" class="MainView">
    <el-row :gutter="5" class="MainView">
      <el-col :span="6" class="MainView">
        <div style="width: 100%; height: 100%; ">
          <suspicious-group-list
              class="grid-list"
              :affiliated-party-list="affiliatedPartyList">
          </suspicious-group-list>
        </div>
      </el-col>
      <el-col :span="18" class="MainView">
        <div style="width: 100%; height: 100%; ">
          <graph-view
              class="grid-content"
              :affiliated-party-detail="affiliatedPartyDetail"
              style="width: 100%; height: 100%; ">
          </graph-view>
        </div>
      </el-col>
    </el-row>
    <el-row :gutter="5" class="MainView">
    </el-row>
  </div>



</template>

<script>
  import SuspiciousGroupList from './components/suspicious-group-list'
  import GraphView from './components/graph-view.vue';

  import DataService from './utils/data-service'
  import EventService from "./utils/event-service";

  export default {
    name: 'app',
    components: {
      SuspiciousGroupList,
      GraphView,
      // TSNEView,
    },
    data() {
      return {
        affiliatedPartyList: null,
        affiliatedPartyDetail: null,
      }
    },
    mounted () {
      DataService.loadAffiliatedPartyList((data)=>{
        this.affiliatedPartyList = data;
      });

      DataService.loadAffiliatedPartyDetail(null, data=>{
        this.affiliatedPartyDetail = data;
      });

      EventService.onSuspiciousGroupSelected(ap_id=>{
        let para = {'ap_id': ap_id};
        DataService.loadAffiliatedPartyDetail(para, data=>{
          this.affiliatedPartyDetail = data;
        });
      });
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