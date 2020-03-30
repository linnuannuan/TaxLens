import Vue from 'vue';

let EventService = new Vue({
  data:{
    SuspiciousGroupSelected: 'suspicious_group_selected',
    TimeRangeSelected: 'time_range_selected',
    TimeRangeBrushed: 'time_range_brushed',
    AffiliatedTransactionSelected: 'affiliated_transaction_selected',
  },

  methods:{
    emitSuspiciousGroupSelected: function(msg){
      this.$emit(this.SuspiciousGroupSelected, msg);
    },
    onSuspiciousGroupSelected: function(callback){
      this.$on(this.SuspiciousGroupSelected, function(msg){
        callback(msg);
      })
    },

    //------------------------------------------------------------
    //When time range in time series view is selected this will trigger
    //msg{start: sec, end: sec}
    emitTimeRangeSelected: function(msg){
      this.$emit(this.TimeRangeSelected, msg);
    },
    onTimeRangeSelected: function(callback){
      this.$on(this.TimeRangeSelected, function(msg){
        callback(msg);
      })
    },

    //------------------------------------------------------------
    //When time range in time series view is selected this will trigger
    //msg{start: sec, end: sec}
    emitTimeRangeBrushed: function(msg){
      this.$emit(this.TimeRangeBrushed, msg);
    },
    onTimeRangeBrushed: function(callback){
      this.$on(this.TimeRangeBrushed, function(msg){
        callback(msg);
      })
    },

    // When user click on a transaction to see its detail info
    emitAffiliatedTransactionSelected: function(source, target){
      console.log('emitAffiliatedTransactionSelected msg:',source, target)
      this.$emit(this.AffiliatedTransactionSelected,source, target);
    },
    onAffiliatedTransactionSelected: function (callback) {
        this.$on(this.AffiliatedTransactionSelected, function(source, target){
        callback(source, target);
      })
    },
  }
});

export default EventService;
