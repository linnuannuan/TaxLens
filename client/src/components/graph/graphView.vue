import * as d3 from "d3";
<template>
    <div class="container">
        <div id="relation_graph"></div>
    </div>
</template>

<script>
    // import NetService from '../../services/net-service';
    // import DataService from '../../services/data-service';
    // eslint-disable-next-line import/newline-after-import,import/no-extraneous-dependencies
    export default {
        name: 'graphView',
        data() {
            return {};
        },
        mounted() {
            this.initialize();
        },
        methods: {
        },

    };
</script>

<style scoped>
    .container {
        text-align: center;
    }
</style>
