<template>
    <el-table
            ref="groupView"
            :data="affiliatedPartyTopoList"
            :default-sort = "{prop: 'affiliatedPartyAmountData.ap_txn_amount', order: 'descending'}"
            v-loading="loadingTopoList"
            highlight-current-row
            @current-change="handleClick"
            size="mini"
            max-height="789"
            :row-class-name="rowStyle"
        >
        <el-table-column prop="affiliatedPartyTopoData" width="150px" >
            <template slot-scope="scope">
                <GroupGlyph :affiliated-party-topo-data="scope.row.affiliatedPartyTopoData"></GroupGlyph>
            </template>
        </el-table-column>
<!--        <el-table-column prop="affiliatedPartyNumData"  label="nodes" width="100px">-->
<!--            <template slot-scope="scope">-->
<!--                <BarChart :affiliated-party-num-data="scope.row.affiliatedPartyNumData"></BarChart>-->
<!--            </template>-->
<!--        </el-table-column>-->
<!--        <el-table-column prop="affiliatedPartyAmountData" label="links" width="100px">-->
<!--            <template slot-scope="scope">-->
<!--                <AmountBarChart :affiliated-party-amount-data="scope.row.affiliatedPartyAmountData"></AmountBarChart>-->
<!--            </template>-->
<!--        </el-table-column>-->
<!--        <el-table-column prop="num" label="links" width="100px"></el-table-column>-->
        <el-table-column prop="num_evader" sortable width="75x">
            <template slot-scope="scope">
                <svg width="75" height="120"  transform="rotate(180)">
                    <rect x="12" y="0" width="50" :height="scope.row.num_evader_height" fill="#fccde5" ></rect>
                </svg>
             </template>
        </el-table-column>
        <el-table-column prop="ap_txn_amount" sortable width="75px">
             <template slot-scope="scope">
                 <svg width="75" height="120"  transform="rotate(180)">
                     <rect x="15" y="0" width="50" :height="scope.row.ap_txn_amount_height" fill="#80b1d3" >></rect>
                 </svg>
             </template>
        </el-table-column>
        <el-table-column prop="num_effective" sortable width="75px">
             <template slot-scope="scope">
                <svg width="75" height="120"  transform="rotate(180)">
                    <rect x="22" y="0" width="50" :height="scope.row.num_effective_height" fill="#bebada" >></rect>
                </svg>
             </template>
        </el-table-column>
    </el-table>
</template>

<script>
  import EventService from "../utils/event-service";
  import GroupGlyph from "./group-glyph";
  // import BarChart from "./bar-chart";
  // import AmountBarChart from "./amount-bar-chart";


  export default {
    name: "GroupView",
    components: {
      GroupGlyph,
      // BarChart,
      // AmountBarChart
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
      rowStyle() {
        return 'row';
      }

    },
  }
</script>


<style>
    .el-table .row{
        height:120px
    }

    .el-table th > .cell{
        text-align: center;
    }
</style>