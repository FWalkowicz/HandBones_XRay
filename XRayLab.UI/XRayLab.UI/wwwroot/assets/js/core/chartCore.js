function createChart(ctx) {

        var chartHandler = new Chart(ctx, {
            type: 'line',
            data: {
                //labels: [1, 2, 3, 4],
                datasets: [
                    {
                        label: 'Idealny pomiar',
                        borderWidth: 2,
                        borderColor: '#000000'
                    },
                    {
                        label: 'Obecny pomiar',
                        borderWidth: 2,
                        borderColor: '#FF6384'
                    },
                ]

            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
        return chartHandler;
    }

