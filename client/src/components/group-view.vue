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
        <el-table-column prop="affiliatedPartyNumData"  label="nodes" width="80px">
            <template slot-scope="scope">
                <BarChart :affiliated-party-num-data="scope.row.affiliatedPartyNumData"></BarChart>
            </template>
        </el-table-column>

        <el-table-column prop="affiliatedPartyAmountData" label="links" width="80px" sortable>
            <template slot-scope="scope">
                <AmountBarChart :affiliated-party-amount-data="scope.row.affiliatedPartyAmountData"></AmountBarChart>
            </template>
        </el-table-column>
<!--        <el-table-column prop="num_nodes" sortable width="45px"></el-table-column>-->
<!--        <el-table-column prop="num_ap_txn" sortable width="45px"></el-table-column>-->
<!--        <el-table-column prop="num_evader" sortable width="45px"></el-table-column>-->
<!--        <el-table-column prop="num_deducted" sortable width="45px"></el-table-column>-->
    </el-table>
</template>

<script>
  import EventService from "../utils/event-service";
  import GroupGlyph from "./group-glyph";
  import BarChart from "./bar-chart";
  import AmountBarChart from "./amount-bar-chart";


  export default {
    name: "GroupView",
    components: {
      GroupGlyph,
      BarChart,
      AmountBarChart
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
      }
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