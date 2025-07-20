# maintenance_app/models.py

from django.db import models

class MaintenanceData(models.Model):
    """
    Modelo para almacenar datos de uso de herramientas de mantenimiento y métricas.
    """
    INDUSTRY_CHOICES = [
        ('manufactura', 'Manufactura'),
        ('energia', 'Energía'),
        ('transporte', 'Transporte'),
        ('mineria', 'Minería'),
        # Add more industries as needed
    ]

    TOOL_CHOICES = [
        ('manual', 'Manual'),
        ('electrica', 'Eléctrica'),
        ('hidraulica', 'Hidráulica'),
        ('diagnostico', 'Diagnóstico'),
        ('software CMMS', 'Software CMMS'),
        ('analisis predictivo', 'Análisis Predictivo'),
        # Add more tool types as needed
    ]

    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
    period = models.CharField(max_length=10) # Ej: '2023', '2024'
    tool = models.CharField(max_length=50, choices=TOOL_CHOICES)
    usage = models.IntegerField(default=0) # Number of uses or quantity
    mtbf = models.FloatField(null=True, blank=True) # Mean Time Between Failures
    mttr = models.FloatField(null=True, blank=True) # Mean Time To Repair

    def __str__(self):
        return f"{self.period} - {self.industry} - {self.tool}"

    class Meta:
        verbose_name_plural = "Maintenance Data"
        # Ensures no duplicates for the same combination
        unique_together = ('industry', 'period', 'tool')

```python
# maintenance_app/views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import MaintenanceData
from django.db.models import Sum, Avg, F # Import F for database functions
import json

def dashboard_view(request):
    """
    Main dashboard view. Renders the HTML template.
    """
    # This view simply renders the template.
    # Filtering and data update logic will be handled
    # with JavaScript on the frontend calling the API view.
    industries = [choice[0] for choice in MaintenanceData.INDUSTRY_CHOICES]
    # Get unique periods from the data
    periods = sorted(list(set(MaintenanceData.objects.values_list('period', flat=True))))
    return render(request, 'maintenance_app/dashboard.html', {'industries': industries, 'periods': periods})

def get_dashboard_data(request):
    """
    API view to get dashboard data based on filters.
    Returns a JSON with filtered and calculated data.
    """
    industry_filter = request.GET.get('industry', 'all')
    period_filter = request.GET.get('period', 'all')

    # Get all data initially
    data = MaintenanceData.objects.all()

    # Apply filters if they are not 'all'
    if industry_filter != 'all':
        data = data.filter(industry=industry_filter)
    if period_filter != 'all':
        data = data.filter(period=period_filter)

    # Calculate key metrics
    total_usage = data.aggregate(Sum('usage'))['usage__sum'] or 0
    avg_mtbf = data.aggregate(Avg('mtbf'))['mtbf__avg']
    avg_mttr = data.aggregate(Avg('mttr'))['mttr__avg']

    # Prepare data for tool usage chart/table
    tool_usage_data = data.values('tool').annotate(total_usage=Sum('usage')).order_by('tool')
    tool_usage_labels = [item['tool'] for item in tool_usage_data]
    tool_usage_values = [item['total_usage'] for item in tool_usage_data]

    # Prepare data for performance impact table (average per tool)
    performance_impact_data = data.values('tool').annotate(avg_mtbf=Avg('mtbf'), avg_mttr=Avg('mttr')).order_by('tool')
    performance_impact_list = list(performance_impact_data) # Convert to list for JSON serialization

    # Prepare data for evolution chart/table (average per period)
    # Calculate total usage per tool per period to find the most used tool efficiently
    tool_usage_per_period = data.values('period', 'tool').annotate(total_usage=Sum('usage')).order_by('period', '-total_usage')

    evolution_data = data.values('period').annotate(
        avg_mtbf=Avg('mtbf'),
        avg_mttr=Avg('mttr'),
    ).order_by('period')

    evolution_list = []
    for item in evolution_data:
         period = item['period']
         # Find the most used tool for this period from the pre-calculated data
         most_used_tool_entry = next((t for t in tool_usage_per_period if t['period'] == period), None)
         most_used_tool = most_used_tool_entry['tool'] if most_used_tool_entry else 'N/A'


         evolution_list.append({
             'period': period,
             'avg_mtbf': round(item['avg_mtbf'], 2) if item['avg_mtbf'] is not None else '-',
             'avg_mttr': round(item['avg_mttr'], 2) if item['avg_mttr'] is not None else '-',
             'most_used_tool': most_used_tool
         })


    # Build the JSON response
    response_data = {
        'key_metrics': {
            'total_usage': total_usage,
            'avg_mtbf': round(avg_mtbf, 2) if avg_mtbf is not None else '-',
            'avg_mttr': round(avg_mttr, 2) if avg_mttr is not None else '-',
        },
        'tool_usage': {
            'labels': tool_usage_labels,
            'values': tool_usage_values,
            'total_usage': total_usage, # Pass the total to calculate percentages in JS
        },
        'performance_impact': performance_impact_list,
        'evolution': evolution_list,
    }

    return JsonResponse(response_data)

```python
# maintenance_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # URL for the main dashboard view
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # URL for the API that provides dashboard data
    path('dashboard/data/', views.get_dashboard_data, name='get_dashboard_data'),
]

```html
{# maintenance_app/templates/maintenance_app/dashboard.html #}
{% extends 'base.html' %} {# Assumes you have a base.html for the general structure #}

{% block title %}Dashboard de Mantenimiento{% endblock %}

{% block content %}
    <div class="dashboard-container">
        <h1 class="text-2xl font-bold mb-6 text-center">Dashboard de Análisis de Herramientas de Mantenimiento</h1>

        <div class="flex flex-wrap gap-4 mb-6 items-center">
            <label for="industry-select" class="font-semibold">Seleccionar Industria:</label>
            <select id="industry-select">
                <option value="all">Todas</option>
                {% for industry in industries %}
                    <option value="{{ industry }}">{{ industry|capfirst }}</option>
                {% endfor %}
            </select>

            <label for="period-select" class="font-semibold">Seleccionar Periodo:</label>
            <select id="period-select">
                <option value="all">Todo el Tiempo</option>
                 {% for period in periods %}
                    <option value="{{ period }}">{{ period }}</option>
                {% endfor %}
            </select>

            <button id="apply-filters">Aplicar Filtros</button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
            <div class="card">
                <div class="card-title">Uso Total de Herramientas</div>
                <div id="total-usage" class="text-xl font-bold">-</div>
            </div>
            <div class="card">
                <div class="card-title">MTBF Promedio</div>
                <div id="avg-mtbf" class="text-xl font-bold">-</div>
            </div>
            <div class="card">
                <div class="card-title">MTTR Promedio</div>
                <div id="avg-mttr" class="text-xl font-bold">-</div>
            </div>
        </div>

        <div class="card">
            <div class="card-title">Frecuencia de Uso por Tipo de Herramienta</div>
            <div id="tool-usage-analysis">
                 <table id="tool-usage-table">
                     <thead>
                         <tr>
                             <th>Tipo de Herramienta</th>
                             <th>Usos</th>
                             <th>Porcentaje (%)</th>
                         </tr>
                     </thead>
                     <tbody>
                         </tbody>
                 </table>
                 <canvas id="tool-usage-pie-chart"></canvas> </div>
        </div>

        <div class="card">
            <div class="card-title">Impacto del Uso de Herramientas en Métricas de Rendimiento</div>
            <div id="performance-impact">
                 <p>Análisis de correlación entre el uso de herramientas y métricas como MTBF/MTTR.</p>
                 <table id="performance-impact-table">
                      <thead>
                          <tr>
                              <th>Tipo de Herramienta</th>
                              <th>Impacto en MTBF (horas)</th>
                              <th>Impacto en MTTR (horas)</th>
                          </tr>
                      </thead>
                      <tbody>
                          </tbody>
                 </table>
            </div>
        </div>

         <div class="card">
             <div class="card-title">Evolución del Uso de Herramientas y Métricas</div>
             <div id="evolution-analysis">
                 <p>Visualización de cómo el uso de herramientas y las métricas de rendimiento han cambiado con el tiempo.</p>
                 <table id="evolution-table">
                      <thead>
                          <tr>
                              <th>Periodo</th>
                              <th>Herramienta Más Usada</th>
                              <th>MTBF Promedio</th>
                              <th>MTTR Promedio</th>
                          </tr>
                      </thead>
                      <tbody>
                          </tbody>
                 </table>
                 <canvas id="evolution-bar-chart"></canvas> </div>
         </div>

    </div>

{% endblock %}

{% block extra_head %}
    <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
    <link href="[https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap](https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap)" rel="stylesheet">
    <script src="[https://cdn.jsdelivr.net/npm/chart.js](https://cdn.jsdelivr.net/npm/chart.js)"></script>
    <style>
        /* CSS styles adapted from the previous example */
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f4f7f6;
            color: #333;
        }
        .dashboard-container {
            max-width: 1200px;
            margin: 20px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .card {
            background-color: #e0f2f7; /* Soft background color */
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        .card-title {
            font-size: 1.1em;
            font-weight: 600;
            margin-bottom: 10px;
            color: #007bff; /* Vibrant blue color */
        }
        select, button {
            padding: 8px;
            border-radius: 5px;
            border: 1px solid #ccc;
            margin-right: 10px;
            font-size: 1em;
        }
        button {
             background-color: #007bff;
             color: white;
             cursor: pointer;
             transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #0056b3;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #007bff;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        canvas {
            max-width: 100%; /* Ensures the canvas is responsive */
            height: auto;
            margin-top: 15px;
        }
    </style>
{% endblock %}

{% block extra_js %}
    <script>
        let toolUsagePieChart; // Variable to store the pie chart instance
        let evolutionBarChart; // Variable to store the bar chart instance

        // Function to fetch data from the Django backend
        async function fetchDashboardData(industry, period) {
            const url = `/dashboard/data/?industry=${industry}&period=${period}`;
            console.log("Fetching data from:", url);
            try {
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                console.log("Data received:", data);
                return data;
            } catch (error) {
                console.error("Error fetching dashboard data:", error);
                return null;
            }
        }

        // Function to update key metrics
        function updateKeyMetrics(metrics) {
            console.log("Updating Key Metrics with:", metrics);
            document.getElementById('total-usage').innerText = metrics.total_usage;
            document.getElementById('avg-mtbf').innerText = metrics.avg_mtbf !== null ? metrics.avg_mtbf : '-';
            document.getElementById('avg-mttr').innerText = metrics.avg_mttr !== null ? metrics.avg_mttr : '-';
        }

        // Function to update the tool usage table and chart
        function updateToolUsageAnalysis(toolUsageData) {
            console.log("Updating Tool Usage Analysis with:", toolUsageData);
            const tableBody = document.getElementById('tool-usage-table').querySelector('tbody');
            tableBody.innerHTML = ''; // Clear table body

            const labels = toolUsageData.labels;
            const dataValues = toolUsageData.values;
            const totalUsage = toolUsageData.total_usage;

            const backgroundColors = [
                'rgba(255, 99, 132, 0.7)',
                'rgba(54, 162, 235, 0.7)',
                'rgba(255, 206, 86, 0.7)',
                'rgba(75, 192, 192, 0.7)',
                'rgba(153, 102, 255, 0.7)',
                'rgba(255, 159, 64, 0.7)'
            ];
             const borderColors = [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ];


            // Update table
            labels.forEach((tool, index) => {
                const row = tableBody.insertRow();
                const usage = dataValues[index];
                const percentage = totalUsage > 0 ? ((usage / totalUsage) * 100).toFixed(2) : 0;
                row.insertCell(0).innerText = tool;
                row.insertCell(1).innerText = usage;
                row.insertCell(2).innerText = percentage;
            });


            // Update pie chart
            const ctx = document.getElementById('tool-usage-pie-chart').getContext('2d');

            if (toolUsagePieChart) {
                toolUsagePieChart.destroy(); // Destroy previous chart instance if it exists
            }

            toolUsagePieChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        data: dataValues,
                        backgroundColor: backgroundColors.slice(0, labels.length),
                        borderColor: borderColors.slice(0, labels.length),
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: 'Distribución del Uso de Herramientas'
                        },
                         tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.raw;
                                     // Recalculate percentage using the passed totalUsage
                                    const percentage = totalUsage > 0 ? ((value / totalUsage) * 100).toFixed(2) : 0;
                                    return `${label}: ${value} (${percentage}%)`;
                                }
                            }
                        }
                    }
                }
            });
        }

         // Function to update the performance impact table
         function updatePerformanceImpactTable(performanceImpactData) {
             console.log("Updating Performance Impact Table with:", performanceImpactData);
             const tableBody = document.getElementById('performance-impact-table').querySelector('tbody');
             tableBody.innerHTML = ''; // Clear table body

             performanceImpactData.forEach(item => {
                 const row = tableBody.insertRow();
                 row.insertCell(0).innerText = item.tool;
                 row.insertCell(1).innerText = item.avg_mtbf !== null ? item.avg_mtbf.toFixed(2) : '-';
                 row.insertCell(2).innerText = item.avg_mttr !== null ? item.avg_mttr.toFixed(2) : '-';
             });
         }

         // Function to update the evolution table and chart
         function updateEvolutionAnalysis(evolutionData) {
              console.log("Updating Evolution Analysis with:", evolutionData);
              const tableBody = document.getElementById('evolution-table').querySelector('tbody');
              tableBody.innerHTML = ''; // Clear table body

              const periods = [];
              const mtbfValues = [];
              const mttrValues = [];

              evolutionData.forEach(item => {
                  const row = tableBody.insertRow();
                  row.insertCell(0).innerText = item.period;
                  row.insertCell(1).innerText = item.most_used_tool;
                  row.insertCell(2).innerText = item.avg_mtbf !== null ? item.avg_mtbf : '-';
                  row.insertCell(3).innerText = item.avg_mttr !== null ? item.avg_mttr : '-';

                  periods.push(item.period);
                  mtbfValues.push(parseFloat(item.avg_mtbf) || 0);
                  mttrValues.push(parseFloat(item.avg_mttr) || 0);
              });


              // Update bar chart
              const ctx = document.getElementById('evolution-bar-chart').getContext('2d');

              if (evolutionBarChart) {
                  evolutionBarChart.destroy(); // Destroy previous chart instance if it exists
              }

              evolutionBarChart = new Chart(ctx, {
                  type: 'bar',
                  data: {
                      labels: periods,
                      datasets: [
                          {
                              label: 'MTBF Promedio (horas)',
                              data: mtbfValues,
                              backgroundColor: 'rgba(54, 162, 235, 0.7)',
                              borderColor: 'rgba(54, 162, 235, 1)',
                              borderWidth: 1
                          },
                           {
                              label: 'MTTR Promedio (horas)',
                              data: mttrValues,
                              backgroundColor: 'rgba(255, 99, 132, 0.7)',
                              borderColor: 'rgba(255, 99, 132, 1)',
                              borderWidth: 1
                          }
                      ]
                  },
                  options: {
                      responsive: true,
                       scales: {
                          y: {
                              beginAtZero: true,
                              title: {
                                  display: true,
                                  text: 'Horas'
                              }
                          },
                           x: {
                              title: {
                                  display: true,
                                  text: 'Periodo'
                              }
                          }
                      },
                      plugins: {
                          legend: {
                              position: 'top',
                          },
                          title: {
                              display: true,
                              text: 'Evolución de MTBF y MTTR por Periodo'
                          }
                      }
                  }
              });
         }


        // Main function to update the dashboard
        async function updateDashboard() {
            console.log("Updating Dashboard...");
            const selectedIndustry = document.getElementById('industry-select').value;
            const selectedPeriod = document.getElementById('period-select').value;

            const data = await fetchDashboardData(selectedIndustry, selectedPeriod);

            if (data) {
                updateKeyMetrics(data.key_metrics);
                updateToolUsageAnalysis(data.tool_usage);
                updatePerformanceImpactTable(data.performance_impact);
                updateEvolutionAnalysis(data.evolution);
            } else {
                 // Handle case where data fetching failed
                 console.error("Failed to update dashboard: No data received.");
                 // Optional: Show a message to the user
            }

            console.log("Dashboard update complete.");
        }

        // Event Listener for the apply filters button
        document.getElementById('apply-filters').addEventListener('click', updateDashboard);

        // Initialize the dashboard with all data on page load
        window.onload = updateDashboard;

    </script>
{% endblock %}

```html
{# base.html - A simple base template example #}
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Mi Aplicación Django{% endblock %}</title>
    {# You can include global CSS here #}
    {% block extra_head %}{% endblock %} {# For page-specific CSS and JS #}
</head>
<body>
    <header>
        {# Site Header #}
    </header>

    <main>
        {% block content %}{% endblock %} {# Content from dashboard.html will be inserted here #}
    </main>

    <footer>
        {# Site Footer #}
    </footer>

    {% block extra_js %}{% endblock %} {# For page-specific JS #}
</body>
</html>
