import Vue from 'vue';

let DateService = new Vue({
  data:{
    quarterMode: true,
  },
  methods: {
    toggleQuarterMode: function () {
      this.quarterMode = !this.quarterMode;
    },
    parseDateToRange: function (date, quarterOffset) {
      quarterOffset = (quarterOffset || 0) * (!this.quarterMode && 4 || 1);
      // Parse the date
      let year = parseInt(date.slice(0, 4));
      // start month must be [1,4,7,10]; ~~ is equivalent to parse Int
      let quarter = ~~((parseInt(date.slice(5, 7)) - 1) / 3) + quarterOffset;
      // Handle year change
      year =    quarter <= -1? year-1  : quarter >= 4? year+1 : year;
      quarter = quarter <= -1? 3       : quarter >= 4? 0      : quarter;
      // day end must be either 30 for [6, 9] or 31 for [3, 12]
      let end = (quarter === 1 || quarter === 2)? '-30': '-31';

      // Calculate new range
      let startDate = year + '-' + (quarter*3+1).toString().padStart(2, '0') + '-01';
      let endDate = year + '-' + ((quarter+1)*3).toString().padStart(2, '0') + end;
      if ( !this.quarterMode ) {
        startDate = year + '-01-01';
        endDate = year + '-12-31';
      }
      return [startDate, endDate];
    }
  }
});

export default DateService;
