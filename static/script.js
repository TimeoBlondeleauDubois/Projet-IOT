      // Appel à la route Flask pour récupérer les données
      fetch("/get_data")
          .then(response => response.json())
          .then(data => {
              // Extraction des valeurs du temps, température, humidité et pression
              const xValues = data.temps;
              const yTemperature = data.temperature;
              const yHumidity = data.humidity;
              const yPressure = data.pressure;
  
              // Création du graphique Plotly
              const plotData = [
                  {
                      x: xValues,
                      y: yTemperature,
                      type: "scatter",
                      mode: "lines",
                      name: "Température",
                      marker: { color: 'red' }
                  },
                  {
                      x: xValues,
                      y: yHumidity,
                      type: "scatter",
                      mode: "lines",
                      name: "Humidité",
                      marker: { color: 'blue' }
                  },
                  {
                      x: xValues,
                      y: yPressure,
                      type: "scatter",
                      mode: "lines",
                      name: "Pression",
                      marker: { color: 'green' }
                  }
              ];
  
              const plotLayout = {
                  title: "Graphique Température, Humidité, Pression en fonction du temps",
                  xaxis: { title: "Temps" },
                  yaxis: { title: "Mesures" }
              };
  
              Plotly.newPlot("myPlot", plotData, plotLayout);
          })
          .catch(error => console.error('Erreur lors de la récupération des données:', error));