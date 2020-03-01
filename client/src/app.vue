<template>
  <div id="app" class="MainView">
    <el-row :gutter="5" class="MainView">
      <el-col :span="8" class="MainView">
        <div style="width: 100%; height: 100%; ">
          <suspicious-group-list class="grid-list"
              :data-affiliated-party="dataAffiliatedParty">
          </suspicious-group-list>
        </div>
      </el-col>
      <el-col :span="16" class="MainView">
        <div style="width: 100%; height: 100%; ">
          <graph-view class="grid-content"
              :data-affiliated-party="dataAffiliatedParty"
              style="width: 100%; height: 100%; ">
          </graph-view>
        </div>
      </el-col>
    </el-row>
  </div>



</template>

<script>
  import SuspiciousGroupList from './components/suspicious-group-list'
  import GraphView from './components/graph-view.vue';

  import DataService from './utils/data-service'

  export default {
    name: 'app',
    components: {
      SuspiciousGroupList,
      GraphView,
      // TSNEView,
    },
    data() {
      return {
        dataAffiliatedParty: null,
      }
    },
    mounted () {
      DataService.loadAffiliatedParty((data)=>{
        this.dataAffiliatedParty = data;
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