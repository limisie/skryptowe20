<template>
  <div id="app">
    <div class="app-tile">

      <div class="app-tile__title">
        <h1>Rates &#38; Sales API</h1>
      </div>

      <div class="app-tile__tables">
        <Tables/>
      </div>
    </div>

    <div class="app-tile">
      <div class="app-tile__documentation">
        <Documentation/>
      </div>
    </div>
  </div>
</template>

<script>
import Documentation from "@/components/Documentation";
import Tables from "@/components/Tables";

export default {
  name: 'App',
  components: {
    Documentation,
    Tables,
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}

.app-tile {
  display: block;
  margin: auto;
  margin-bottom: 30px;
  padding: 30px;
  width: 60%;
  border-radius: 10px;
  background-color: white;
  box-shadow: #eeeeee 0 0 10px;
}

h1 {
  margin: 0;
}
</style>
