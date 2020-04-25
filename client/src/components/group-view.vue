<template>
  <el-table
      :data="affiliatedPartyTopoList"
      :default-sort = "{prop: 'num_ap_txn', order: 'descending'}"
      v-loading="loadingTopoList"
      size="mini"
      max-height="790">
    <el-table-column label="Topology" prop="affiliatedPartyTopoData">
        <template slot-scope="scope">
            <GroupGlyph :affiliated-party-topo-data="scope.row.affiliatedPartyTopoData"></GroupGlyph>
        </template>
    </el-table-column>
    <el-table-column label="Nodes" prop="num_nodes" sortable></el-table-column>
    <el-table-column label="AP txns" prop="num_ap_txn" sortable></el-table-column>
    <el-table-column :label="affiliatedPartyNum" align="right">
      <template slot-scope="scope">
        <el-button size="mini" @click="handleView(scope.$index, scope.row)">View</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
  import EventService from "../utils/event-service";
  import GroupGlyph from "./group-glyph";


  export default {
    name: "GroupView",
    components: {
      GroupGlyph,
    },
    props:{
      affiliatedPartyTopoList: Array,
      loadingTopoList: Boolean
    },
    data: function () {
      return {
        svg: null,
        test: false,
      }
    },
    watch: {
      // affiliatedPartyTopoList: function() {
        // this.renderGroupView();
      // },
    },
    mounted:function(){
      // this.initGroupView();
      // this.renderGroupView();
    },
    computed: {
      affiliatedPartyNum: function () {
        return "Count: " + this.affiliatedPartyTopoList.length;
      },
    },
    methods: {
      handleView(id) {
        EventService.emitSuspiciousGroupSelected(this.affiliatedPartyTopoList[id].ap_id);
      },
    },
  }
</script>


<style scoped>
</style>