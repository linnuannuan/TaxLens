import Vue from 'vue'
import App from './app.vue'
import './plugins/element.js'
import './plugins/axios.js'

Vue.config.productionTip = false;

new Vue({
  render: h => h(App),
}).$mount('#app');
