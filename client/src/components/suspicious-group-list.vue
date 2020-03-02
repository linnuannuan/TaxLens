<template>
  <el-table
      :data="listAffiliatedParty.filter((data) => !search_id || data.id.includes(search_id))"
      :default-sort = "{prop: 'num_ap_txn', order: 'descending'}"
      class="grid-content"
      max-height="800">
    <el-table-column
        label="Group id"
        prop="id"
        sortable>
    </el-table-column>
    <el-table-column
        label="Taxpayer"
        prop="num_tp"
        sortable>
    </el-table-column>
    <el-table-column
        label="AP txns"
        prop="num_ap_txn"
        sortable>
    </el-table-column>
    <el-table-column
        align="right">
      <template slot="header">
        <el-input
            v-model="search_id"
            size="mini"
            placeholder="TODO: BUG, default:1581"/>
      </template>
      <template slot-scope="scope">
        <el-button
            size="mini"
            @click="handleView(scope.$index, scope.row)">View</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>


<script>
  import EventService from "../utils/event-service";
  let object = require('lodash/fp/object');

  export default {
    name: "SuspiciousGroupList",
    props:{
      dataAffiliatedParty: Object,
    },
    data() {
      return {
        listAffiliatedParty: [],
        search_id: "",
      }
    },
    watch:{
      dataAffiliatedParty:function (newData) {
        this.listAffiliatedParty = [];
        for(let id in newData) {
          this.listAffiliatedParty.push(
            object.extend({'id': id}, newData[id]['graph'])
          )
        }
      }
    },
    methods: {
      handleView(index, row) {
        EventService.emitSuspiciousGroupSelected(row.id);
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