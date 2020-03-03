<template>
  <el-table
      :data="affiliatedPartyList"
      :default-sort = "{prop: 'num_ap_txn', order: 'descending'}"
      size="mini"
      class="grid-content"
      max-height="400">
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

  export default {
    name: "SuspiciousGroupList",
    props:{
      affiliatedPartyList: Array,
    },
    computed: {
      affiliatedPartyNum: function () {
        return "Count: " + this.affiliatedPartyList.length;
      }
    },
    methods: {
      handleView(index, row) {
        EventService.emitSuspiciousGroupSelected(row['ap_id']);
      }
    },
  }
</script>

<style scoped>
  .grid-content {
    border: 1px solid slategrey;
    border-radius: 5px;
    height: 100%;
  }
</style>