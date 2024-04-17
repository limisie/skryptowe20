<template>
  <div class="table">

    <table v-if="data.length > 0">
      <tr>
        <th v-for="(label, index) in topBar" :key="index">{{ label }}</th>
      </tr>

      <tr v-for="d in data" :key="d.date">
        <td>{{ d.date }}</td>
        <td>{{ d.rate }}</td>
        <td v-if="d.ipd">{{ d.ipd }}</td>
        <td v-else></td>
      </tr>
    </table>

  </div>
</template>

<script>
export default {
  name: 'TableRates',
  props: {
    currency: {
      type: String,
      required: true,
    },
    topBar: {
      type: Array,
      required: true,
    },
    data: {
      type: Array,
      required: true
    },
  },
};
</script>

<style scoped>
table {
  width: 100%;
  margin: 20px auto 20px auto;
  padding: 5px;
  background-color: white;
  text-align: left;
}

th, td {
  border-bottom: 1px solid #DFE3E8;
  justify-content: left;
}
</style>