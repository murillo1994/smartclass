/**
 * SmartClass - Renderização de Gráficos de Séries Temporais Modernos (Chart.js)
 * Suporte completo a Modo Claro e Modo Escuro (Dark Mode).
 */
import { formatShortTime } from './utils.js';

export function createTelemetryChart(ctx) {
  if (!ctx) return null;

  const isDark = document.documentElement.classList.contains('dark');

  // Gradiente suave de Temperatura (Laranja / Âmbar)
  const tempGradient = ctx.createLinearGradient(0, 0, 0, 320);
  tempGradient.addColorStop(0, 'rgba(249, 115, 22, 0.25)');
  tempGradient.addColorStop(0.6, 'rgba(249, 115, 22, 0.05)');
  tempGradient.addColorStop(1, 'rgba(249, 115, 22, 0.0)');

  // Gradiente suave de Umidade (Azul Celeste / Ciano)
  const humGradient = ctx.createLinearGradient(0, 0, 0, 320);
  humGradient.addColorStop(0, 'rgba(14, 165, 233, 0.22)');
  humGradient.addColorStop(0.6, 'rgba(14, 165, 233, 0.04)');
  humGradient.addColorStop(1, 'rgba(14, 165, 233, 0.0)');

  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [
        {
          label: 'Temperatura (°C)',
          data: [],
          borderColor: '#ea580c', // orange-600
          backgroundColor: tempGradient,
          borderWidth: 2.5,
          pointRadius: 3.5,
          pointBackgroundColor: isDark ? '#0f172a' : '#ffffff',
          pointBorderColor: '#ea580c',
          pointBorderWidth: 2,
          pointHoverRadius: 6,
          pointHoverBackgroundColor: '#ea580c',
          pointHoverBorderColor: '#ffffff',
          pointHoverBorderWidth: 2.5,
          tension: 0.38,
          fill: true,
          yAxisID: 'y'
        },
        {
          label: 'Umidade (%)',
          data: [],
          borderColor: '#0284c7', // sky-600
          backgroundColor: humGradient,
          borderWidth: 2,
          pointRadius: 3,
          pointBackgroundColor: isDark ? '#0f172a' : '#ffffff',
          pointBorderColor: '#0284c7',
          pointBorderWidth: 2,
          pointHoverRadius: 5.5,
          pointHoverBackgroundColor: '#0284c7',
          pointHoverBorderColor: '#ffffff',
          pointHoverBorderWidth: 2,
          borderDash: [5, 4],
          tension: 0.38,
          fill: true,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false
      },
      animation: {
        duration: 600,
        easing: 'easeOutQuart'
      },
      plugins: {
        legend: {
          position: 'top',
          align: 'end',
          labels: {
            usePointStyle: true,
            pointStyle: 'circle',
            boxWidth: 7,
            boxHeight: 7,
            padding: 18,
            color: isDark ? '#e2e8f0' : '#475569',
            font: {
              family: "'Inter', system-ui, sans-serif",
              size: 12,
              weight: '600'
            }
          }
        },
        tooltip: {
          backgroundColor: 'rgba(15, 23, 42, 0.95)',
          titleColor: '#f8fafc',
          bodyColor: '#cbd5e1',
          titleFont: { family: "'Inter', sans-serif", size: 12, weight: '700' },
          bodyFont: { family: "'Inter', sans-serif", size: 12, weight: '500' },
          padding: 12,
          cornerRadius: 10,
          borderWidth: 1,
          borderColor: isDark ? 'rgba(255, 255, 255, 0.15)' : 'rgba(255, 255, 255, 0.1)',
          displayColors: true,
          boxWidth: 8,
          boxHeight: 8,
          usePointStyle: true,
          callbacks: {
            label: function(context) {
              const label = context.dataset.label || '';
              const val = context.parsed.y;
              if (val === null || isNaN(val)) return ` ${label}: —`;
              if (context.datasetIndex === 0) {
                return ` ${label}: ${val.toFixed(1)} °C`;
              }
              return ` ${label}: ${val.toFixed(1)}%`;
            }
          }
        }
      },
      scales: {
        x: {
          grid: {
            display: false,
            drawBorder: false
          },
          ticks: {
            font: { family: "'Inter', sans-serif", size: 11, weight: '500' },
            color: isDark ? '#64748b' : '#94a3b8',
            maxRotation: 0,
            autoSkip: true,
            maxTicksLimit: 8
          }
        },
        y: {
          type: 'linear',
          display: true,
          position: 'left',
          title: {
            display: true,
            text: 'Temperatura (°C)',
            color: '#ea580c',
            font: { family: "'Inter', sans-serif", size: 11, weight: '700' },
            padding: { bottom: 8 }
          },
          suggestedMin: 18,
          suggestedMax: 32,
          grid: {
            color: isDark ? 'rgba(51, 65, 85, 0.4)' : 'rgba(226, 232, 240, 0.6)',
            borderDash: [4, 4],
            drawBorder: false
          },
          ticks: {
            color: isDark ? '#94a3b8' : '#64748b',
            font: { family: "'Inter', sans-serif", size: 11 },
            callback: (v) => `${v}°`
          }
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          title: {
            display: true,
            text: 'Umidade (%)',
            color: '#0284c7',
            font: { family: "'Inter', sans-serif", size: 11, weight: '700' },
            padding: { bottom: 8 }
          },
          suggestedMin: 30,
          suggestedMax: 90,
          grid: {
            display: false,
            drawBorder: false
          },
          ticks: {
            color: isDark ? '#94a3b8' : '#64748b',
            font: { family: "'Inter', sans-serif", size: 11 },
            callback: (v) => `${v}%`
          }
        }
      }
    }
  });
}

export function setChartTheme(chart, isDark) {
  if (!chart) return;

  // Atualiza cores das legendas
  if (chart.options.plugins.legend) {
    chart.options.plugins.legend.labels.color = isDark ? '#e2e8f0' : '#475569';
  }

  // Atualiza cores dos eixos e grades
  if (chart.options.scales.x) {
    chart.options.scales.x.ticks.color = isDark ? '#64748b' : '#94a3b8';
  }
  if (chart.options.scales.y) {
    chart.options.scales.y.grid.color = isDark ? 'rgba(51, 65, 85, 0.4)' : 'rgba(226, 232, 240, 0.6)';
    chart.options.scales.y.ticks.color = isDark ? '#94a3b8' : '#64748b';
  }
  if (chart.options.scales.y1) {
    chart.options.scales.y1.ticks.color = isDark ? '#94a3b8' : '#64748b';
  }

  // Atualiza background dos pontos
  if (chart.data.datasets) {
    chart.data.datasets.forEach(ds => {
      ds.pointBackgroundColor = isDark ? '#0f172a' : '#ffffff';
    });
  }

  chart.update();
}

export function updateChart(chart, readings, selectedRoom = 'all') {
  if (!chart) return;

  // Filtra por sala se não for 'all'
  let filtered = readings;
  if (selectedRoom && selectedRoom !== 'all') {
    filtered = readings.filter(r => r.sala_id === selectedRoom);
  }

  // Ordena cronologicamente para a curva temporal (mais antigo -> mais recente)
  const sorted = [...filtered].sort((a, b) => new Date(a.data_registro) - new Date(b.data_registro));

  // Pega as últimas 30 medições para manter a leitura limpa e responsiva
  const recent = sorted.slice(-30);

  const labels = recent.map(r => formatShortTime(r.data_registro));
  const temps = recent.map(r => Number(r.temperatura));
  const hums = recent.map(r => r.umidade !== null ? Number(r.umidade) : null);

  chart.data.labels = labels;
  chart.data.datasets[0].data = temps;
  chart.data.datasets[1].data = hums;
  chart.update();
}
