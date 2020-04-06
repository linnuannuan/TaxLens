<template>
  <el-table
      :data="affiliatedPartyList"
      :default-sort = "{prop: 'num_ap_txn', order: 'descending'}"
      v-loading="loadingList"
      size="mini"
      max-height="190">
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
    name: "GroupList",
    props:{
      affiliatedPartyList: Array,
      loadingList: Boolean
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
</style>