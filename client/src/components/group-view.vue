<template>
    <el-table
            ref="groupView"
            :data="affiliatedPartyTopoList"
            :default-sort = "{prop: 'affiliatedPartyTopoData.ap_txn_amount', order: 'descending'}"
            v-loading="loadingTopoList"
            @current-change="handleClick"
            size="mini"
            max-height="790">
        <el-table-column prop="affiliatedPartyTopoData" :label="affiliatedPartyNum" width="100px">
            <template slot-scope="scope">
                <GroupGlyph :affiliated-party-topo-data="scope.row.affiliatedPartyTopoData"></GroupGlyph>
            </template>
        </el-table-column>
        <el-table-column prop="affiliatedPartyTopoData.ap_txn_amount" sortable width="100px"></el-table-column>
        <el-table-column prop="num_nodes" sortable width="45px"></el-table-column>
        <el-table-column prop="num_ap_txn" sortable width="45px"></el-table-column>
        <el-table-column prop="num_evader" sortable width="45px"></el-table-column>
        <el-table-column prop="num_deducted" sortable width="45px"></el-table-column>
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
      affiliatedPartyTopoList: function() {
        // this.renderGroupView();
        this.$refs.groupView.clearSelection();
      },
    },
    computed: {
      affiliatedPartyNum: function () {
        return "Count: " + this.affiliatedPartyTopoList.length;
      },
    },
    methods: {
      handleClick(row) {
        row && EventService.emitSuspiciousGroupSelected(row['ap_id']);
      },
    },
  }
</script>


<style scoped>
</style>