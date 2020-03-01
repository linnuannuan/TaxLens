import Vue from 'vue';

let DataService = new Vue({
  data:{
    dataServerUrl: 'http://127.0.0.1:9950',
  },

  methods:{
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
