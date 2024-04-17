<template>
  <div class="inputs">
    <form class="inputs__form" @submit.prevent="submitForm">

      <div id="inputs__select-currencies" class="inputs__select-currencies">
        <input type="checkbox" id="usd" value="Total in USD" v-model="checkedCurrencies">
        <label for="usd">USD</label>
        <input type="checkbox" id="pln" value="Total in PLN" v-model="checkedCurrencies">
        <label for="pln">PLN</label>
      </div>

      <div class="inputs__date-input">
        <label for="dateFrom"><strong>Date from: </strong></label>
        <input type="date" id="dateFrom" v-model="dateFrom" min="2009-01-01" max="2013-12-22" required>
      </div>

      <div class="inputs__date-input">
        <label for="dateTo"><strong>Date from: </strong></label>
        <input type="date" id="dateTo" v-model="dateTo" min="2009-01-01" max="2013-12-22" required>
      </div>

      <button>Show sales</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'InputSales',
  data() {
    return {
      dateFrom: '2009-01-01',
      dateTo: '2009-01-31',
      checkedCurrencies: ["Total in USD", "Total in PLN"],
    }
  },
  methods: {
    submitForm() {
      this.$emit('sales_input_data', {
        currencies: this.checkedCurrencies,
        dateFrom: this.dateFrom,
        dateTo: this.dateTo
      })
    },
  },
  created() {
    this.submitForm()
  }
}
</script>

<style scoped>

.inputs__form {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.inputs__select-currencies label {
  margin-right: 12px;
  font-size: medium;
}

input, option, select {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  font-size: medium;
  border: dotted #DFE3E8 1px;
  border-radius: 3px;
  padding: 3px;
}

button {
  padding: 5px;
  background-color: #2c3e50;
  border-radius: 3px;
  border: none;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  font-weight: bold;
  font-size: medium;
  color: white;
}

</style>