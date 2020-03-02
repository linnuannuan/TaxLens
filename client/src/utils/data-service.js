import Vue from 'vue';

let DataService = new Vue({
  data:{
    dataServerUrl: 'http://127.0.0.1:9950',
  },

  methods:{
    loadAffiliatedPartyList(callback){
      this.axios.get(`${this.dataServerUrl}/ap_list`)
        .then(response => {
          callback(response.data)
        }, errResponse => {
          console.log(errResponse)
        })
    },
    loadAffiliatedPartyDetail(param, callback){
      this.axios.post(`${this.dataServerUrl}/ap_detail`, param)
        .then(response => {
          callback(response.data)
        }, errResponse => {
          console.log(errResponse)
        })
    },
    // legacy
    loadAffiliatedParty(callback){
      this.axios.get(`${this.dataServerUrl}/APIRN_all`)
        .then(response => {
          callback(response.data)
        }, errResponse => {
          console.log(errResponse)
        })
    }
  }
});

export default DataService;
