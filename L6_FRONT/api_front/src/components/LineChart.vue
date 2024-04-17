<script>
import {Line} from 'vue-chartjs';

export default {
  extends: Line,
  props: {
    chartData: {
      type: Array,
      required: true
    },
    label: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          xAxes: [{
            display: true,
            gridLines: {
              display: false
            },
            ticks: {
              lineHeight: 2
            }
          }],
          yAxes: [{
            display: true,
            ticks: {
              precision: 2
            }
          }],
        },
      },
    }
  },
  mounted() {
    let dates = this.chartData.map(d => d.date);
    let rates = this.chartData.map(d => d.rate);

    if (rates.length === 1) {
      rates.unshift(rates[0])
      rates.push(rates[0])
      dates.unshift(null)
      dates.push(null)
    }

    this.renderChart({
      labels: dates,
      datasets: [{
        label: this.label.toUpperCase(),
        data: rates,
        fill: false,
        borderColor: '#2c3e50',
        pointRadius: 2,
        pointBorderColor: "#2c3e50",
        pointBackgroundColor: "#2c3e50",
        pointHoverBackgroundColor: "#55bae7",
        pointHoverBorderColor: "#55bae7",
        lineTension: 0.1,
      }],
    }, this.options);
  }
}
</script>