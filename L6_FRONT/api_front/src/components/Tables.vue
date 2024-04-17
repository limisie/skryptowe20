<template>
  <div>
    <h2>Check Rates</h2>

    <div class="tables__inputs__rates">
      <InputRates @rates_input_data="setRatesData"/>
    </div>

    <div class="tables__table__rates">
      <TableRates
          :data="this.rates"
          :currency="this.currency"
          :top-bar="['Date', 'Rate', 'Interpolated']"
      />
    </div>

    <div class="tables__chart__rates">
      <div v-if="this.rates.length > 0">
        <line-chart
            :chartData="this.rates"
            :label="this.currency"
        />
      </div>
    </div>

    <h2>Check Sales</h2>
    <div class="tables__inputs__sales">
      <InputSales @sales_input_data="setSalesData"/>
    </div>

    <div class="tables__table__sales">
      <TableSales
          :data="this.sales"
          :currencies="this.currencies"
          :top-bar="['Date'].concat(currencies)"
      />
    </div>

    <div class="tables__chart__sales">
      <div v-if="this.sales.length > 0">
        <bar-chart
            :chartData="this.sales"
        />
      </div>
    </div>
  </div>
</template>

<script>
import InputRates from "@/components/InputRates";
import InputSales from "@/components/InputSales";
import TableRates from "@/components/TableRates";
import TableSales from "@/components/TableSales";
import LineChart from "@/components/LineChart";
import BarChart from "@/components/BarChart";
import axios from "axios";

export default {
  name: 'Tables',
  components: {
    InputRates,
    InputSales,
    TableRates,
    TableSales,
    LineChart,
    BarChart
  },
  data() {
    return {
      currency: '',
      ratesDateFrom: '',
      ratesDateTo: '',

      currencies: [],
      salesDateFrom: '',
      salesDateTo: '',

      rates: [],
      sales: [],
    }
  },
  computed: {
    ratesUrl() {
      return `http://localhost:5000/rates/${this.currency}/${this.ratesDateFrom}/${this.ratesDateTo}`
    },
    salesUrl() {
      return `http://localhost:5000/sales/${this.salesDateFrom}/${this.salesDateTo}`
    }
  },
  methods: {
    setRatesData(rates_input_data) {
      this.currency = rates_input_data.code
      this.ratesDateFrom = rates_input_data.dateFrom
      this.ratesDateTo = rates_input_data.dateTo

      this.getRates()
    },

    setSalesData(sales_input_data) {
      this.currencies = sales_input_data.currencies
      this.salesDateFrom = sales_input_data.dateFrom
      this.salesDateTo = sales_input_data.dateTo

      this.getSales()
    },

    async getRates() {
      this.rates = []

      const request = await axios.get(this.ratesUrl);
      const rates_data = request.data

      rates_data.Rates.forEach(d => {
        this.rates.push({
          date: d['Date'],
          rate: d['Rate'],
          ipd: d['Interpolated']
        })
      });
    },

    async getSales() {
      this.sales = []

      const request = await axios.get(this.salesUrl);
      const sales_data = request.data

      sales_data.Sales.forEach(d => {
        this.sales.push({
          date: d['Date'],
          usd: d['USD Total'],
          pln: d['PLN Total'],
        })
      });
    }
  },
}
</script>