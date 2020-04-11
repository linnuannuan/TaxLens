import Vue from 'vue';

let DataService = new Vue({
  data:{
    dataServerUrl: 'http://127.0.0.1:9950',
  },

  methods:{
    loadTemporalOverview(callback){
      this.axios.get(`${this.dataServerUrl}/temporal_overview`)
        .then(response => {
          callback(response.data)
        }, errResponse => {
          console.log(errResponse)
        })
    },
    loadAffiliatedPartyList(param, callback){
      this.axios.post(`${this.dataServerUrl}/ap_list`, param)
        .then(response => {
          callback(response.data)
        }, errResponse => {
          console.log(errResponse)
        })
    },
    loadAffiliatedPartyTopoList(callback){
      this.axios.get(`${this.dataServerUrl}/ap_topo_list`)
        .then(response => {
          callback(response.data)
        }, errResponse => {
          console.log(errResponse)
        })
    },
    loadAffiliatedPartyDetailByAP(param, callback){
      this.axios.post(`${this.dataServerUrl}/ap_detail`, param)
        .then(response => {
          callback(response.data)
        }, errResponse => {
          console.log(errResponse)
        })
    },
    loadAffiliatedPartyDetailByTP(param, callback){
      this.axios.post(`${this.dataServerUrl}/tp_detail`, param)
        .then(response => {
          callback(response.data)
        }, errResponse => {
          console.log(errResponse)
        })
    },
    loadCalendarDataByTransaction(param, callback){
      this.axios.post(`${this.dataServerUrl}/profit_detail`, param)
        .then(response => {
          callback(response.data)
        }, errResponse => {
          console.log(errResponse)
        })
    },

    // loadDetailAffiliatedTransaction(param, callback){
    //   this.axios.post(`${this.dataServerUrl}/ap_txn_detail`, param)
    //     .then(response => {
    //       callback(response.data)
    //     }, errResponse => {
    //       console.log(errResponse)
    //     })
    // },
  }
});

export default DataService;
