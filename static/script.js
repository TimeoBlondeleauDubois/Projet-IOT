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
              const plotDataTemp = [
                  {
                      x: xValues,
                      y: yTemperature,
                      type: "scatter",
                      mode: "lines",
                      name: "Température",
                      marker: { color: 'red' }
                  }
                ];
                const plotDataHum = [
                      {
                          x: xValues,
                          y: yHumidity,
                          type: "scatter",
                          mode: "lines",
                          name: "Humidité",
                          marker: { color: 'blue' }
                      }
                ];
                const plotDataPress = [
                       {
                            x: xValues,
                            y: yPressure,
                            type: "scatter",
                            mode: "lines",
                            name: "Pression",
                            marker: { color: 'green' }
                        }
                ];
                  
             const plotLayoutTemp = {
                  title: "Graphique Température en fonction du temps",
                  xaxis: { title: "Temps" },
                  yaxis: { title: "°C" }
              };
              const plotLayoutHum = {
                  title: "Graphique Humidité en fonction du temps",
                  xaxis: { title: "Temps" },
                  yaxis: { title: "%" }
              };
              const plotLayoutPress = {
                  title: "Graphique Pression en fonction du temps",
                  xaxis: { title: "Temps" },
                  yaxis: { title: "hPa" }
              };
              Plotly.newPlot("myPlotTemp", plotDataTemp, plotLayoutTemp);
              Plotly.newPlot("myPlotHum", plotDataHum, plotLayoutHum);
              Plotly.newPlot("myPlotPress", plotDataPress, plotLayoutPress);
          })
          .catch(error => console.error('Erreur lors de la récupération des données:', error));