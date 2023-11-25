// Set new default font family and font color to mimic Bootstrap's default styling

// Bar Chart Example
var ctx = document.getElementById("possibleBestSellerChart");
var myLineChart = new Chart(ctx, {
  type: "bar",
  data: {
    labels: [
      "Bonkerz Nrb",
      "Crafted Nairobi",
      "Metamorphisized",
      "Nairobi Nnoize",
      "Peni Mbili",
      "Smoke The Nemisis",
    ],
    datasets: [
      {
        label: "Possible Best Seller",
        backgroundColor: "rgba(2,117,216,1)",
        borderColor: "rgba(2,117,216,1)",
        data: [25600, 55264, 8100, 102090, 44950, 2],
      },
    ],
  },
  options: {
    scales: {
      xAxes: [
        {
          time: {
            unit: "month",
          },
          gridLines: {
            display: false,
          },
          ticks: {
            maxTicksLimit: 6,
          },
        },
      ],
      yAxes: [
        {
          ticks: {
            min: 0,
            max: 100000,
            maxTicksLimit: 10,
          },
          gridLines: {
            display: true,
          },
        },
      ],
    },
    legend: {
      display: false,
    },
  },
});

// Possible Less Bar Chart Example
var ctx = document.getElementById("possibleLessSellerChart");
var myLineChart = new Chart(ctx, {
  type: "bar",
  data: {
    labels: [
      "Bonkerz Nrb",
      "Crafted Nairobi",
      "Metamorphisized",
      "Nairobi Nnoize",
      "Peni Mbili",
      "Smoke The Nemisis",
    ],
    datasets: [
      {
        label: "Possible Best Seller",
        backgroundColor: "rgba(216,2,2,1)",
        borderColor: "rgba(2,117,216,1)",
        data: [12800, 27632, 40500, 51045, 22475, 2],
      },
    ],
  },
  options: {
    scales: {
      xAxes: [
        {
          time: {
            unit: "month",
          },
          gridLines: {
            display: false,
          },
          ticks: {
            maxTicksLimit: 6,
          },
        },
      ],
      yAxes: [
        {
          ticks: {
            min: 0,
            max: 100000,
            maxTicksLimit: 10,
          },
          gridLines: {
            display: true,
          },
        },
      ],
    },
    legend: {
      display: false,
    },
  },
});
