// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';
// static/js/charts.js

function renderPendidikanChart(universityNames, universityValues) {
    var ctx = document.getElementById('pendidikanChart');
    var pendidikanChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: universityNames,  // List of university names
            datasets: [{
                label: 'Jumlah Kandidat S3 per Universitas',
                backgroundColor: '#4e73df',  // Blue color for bars
                hoverBackgroundColor: '#2e59d9',  // Darker shade on hover
                borderColor: '#4e73df',  // Matching border color
                data: universityValues,  // Number of PhD candidates per university
            }],
        },
        options: {
            maintainAspectRatio: false,
            layout: {
                padding: {
                    left: 10,
                    right: 25,
                    top: 25,
                    bottom: 0
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        maxTicksLimit: 6
                    },
                    maxBarThickness: 25,
                },
                y: {
                    ticks: {
                        min: 0,  // Start y-axis from 0
                        max: Math.max(...universityValues),  // Dynamic max value based on data
                        maxTicksLimit: 5,
                        padding: 10,
                    },
                    grid: {
                        color: 'rgb(234, 236, 244)',
                        zeroLineColor: 'rgb(234, 236, 244)',
                        drawBorder: false,
                        borderDash: [2],
                        zeroLineBorderDash: [2]
                    }
                },
            },
            legend: {
                display: false
            },
            tooltips: {
                titleMarginBottom: 10,
                titleFontColor: '#6e707e',
                titleFontSize: 14,
                backgroundColor: 'rgb(255,255,255)',
                bodyFontColor: '#858796',
                borderColor: '#dddfeb',
                borderWidth: 1,
                xPadding: 15,
                yPadding: 15,
                displayColors: false,
                caretPadding: 10,
                callbacks: {
                    label: function(tooltipItem) {
                        return tooltipItem.dataset.label + ': ' + tooltipItem.raw;
                    }
                }
            }
        }
    });
}
