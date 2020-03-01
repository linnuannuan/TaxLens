<template>
  <div id="app" class="MainView">
    <el-row :gutter="10" class="top">
      <el-col :span="8" class="left">
        <div style="width: 100%; height: 100%; ">
          <suspicious-group-list
              :data-affiliated-party="dataAffiliatedParty"
              style="width: 100%; height: 100%; ">
          </suspicious-group-list>
        </div>
      </el-col>
      <el-col :span="16" class="right">
        <div style="width: 100%; height: 100%; ">
          <graph-view
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
    height: calc(100vh - 16px);
    margin: 4px;
  }
  .MainView{
    /*background: #efedf2;*/
    height: 100%;
  }
  .top{
    height: 100%;
  }
  .left{
    height: 100%;
  }
  .right{
    height: 100%;
  }
  .bg-purple-dark {
    background: #99a9bf;
  }
  .bg-purple {
    background: #d3dce6;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }
  .grid-content {
    border-radius: 4px;
    height: 100%;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
</style>