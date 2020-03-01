<template>
  <div id="app">
    <graph-view></graph-view>
  </div>
</template>

<script>
  import graphView from './components/graphView.vue';
  // import tsneView from './components/tsneView.vue';
  
export default {
  name: 'app',
  components: {
    graphView,
    // tsneView,
  },
  data() {
    return {
      APIRN: null,
    }
  },
  mounted () {
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>