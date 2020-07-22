import Vue from 'vue';

let EventService = new Vue({
  data:{
    SuspiciousGroupSelected: 'suspicious_group_selected',
    AffiliatedTransactionSelected: 'affiliated_transaction_selected',
    SuspiciousNodeSelected:'suspicious_node_selected',

    CalendarPeriodPrevious: 'calendar_period_previous',
    CalendarPeriodNext: 'calendar_period_next',
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

    // When user click on a transaction to see its detail info
    emitAffiliatedTransactionSelected: function(source, target, periodStart, periodEnd){
      this.$emit(this.AffiliatedTransactionSelected, source, target, periodStart, periodEnd);
    },
    onAffiliatedTransactionSelected: function (callback) {
      this.$on(this.AffiliatedTransactionSelected, function(source, target, periodStart, periodEnd){
        callback(source, target, periodStart, periodEnd);
      })
    },

    // when user click on a suspicious node
    emitSuspiciousNodeSelected: function (msg) {
      this.$emit(this.SuspiciousNodeSelected, msg);
    },
    onSuspiciousNodeSelected: function (callback) {
      this.$on(this.SuspiciousNodeSelected, function(msg){
        callback(msg);
      })
    },

  }
});

export default EventService;
