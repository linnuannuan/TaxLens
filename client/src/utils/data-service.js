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
    setAffiliatedPartySetting(param, callback){
      this.axios.post(`${this.dataServerUrl}/set_model`, param)
        .then(response => {
          callback(response.data)
        }, errResponse => {
          console.log(errResponse)
        })
    },
  }
});

export default DataService;
