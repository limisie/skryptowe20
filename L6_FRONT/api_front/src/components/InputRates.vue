<template>
  <div class="inputs">
    <form class="inputs__form" @submit.prevent="submitForm">

      <div class="inputs__select-currnecy">
        <label for="currencySelector"><strong>Currency: </strong></label>
        <select id="currencySelector" v-model="selectedCurrency">
          <option :value="option.value"
                  v-for="(option, index) in currencies"
                  :key="index">
            {{ option.name }}
          </option>
        </select>
      </div>

      <div class="inputs__date-input">
        <label for="dateFrom"><strong>Date from: </strong></label>
        <input type="date" id="dateFrom" v-model="dateFrom" min="2009-01-01" max="2021-01-19" required>
      </div>

      <div class="inputs__date-input">
        <label for="dateTo"><strong>Date from: </strong></label>
        <input type="date" id="dateTo" v-model="dateTo" min="2009-01-01" max="2021-01-19" required>
      </div>

      <button>Show rates</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'InputRates',
  data() {
    return {
      dateFrom: '2021-01-01',
      dateTo: '2021-01-15',
      selectedCurrency: 'usd',
      currencies: [
        {value: 'usd', name: 'USD'},
        {value: 'eur', name: 'EUR'},
        {value: 'gbp', name: 'GBP'},
      ],
    }
  },
  methods: {
    submitForm() {
      this.$emit('rates_input_data', {
        code: this.selectedCurrency,
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

input, option, select {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  font-size: medium;
  border: dotted #DFE3E8 1px;
  border-radius: 3px;
  padding: 3px;
}

button {
  padding: 5px;
  margin: 0;
  background-color: #2c3e50;
  border-radius: 3px;
  border: none;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  font-weight: bold;
  color: white;
  font-size: medium;
}
</style>