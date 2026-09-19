/**
 * SmartClass - Módulo de Exportação de Relatórios em PDF e CSV
 * Utiliza jsPDF e jsPDF-AutoTable para geração client-side em alta fidelidade.
 */
import { formatDate, classifyThermalComfort } from './utils.js';

export function exportChartAnalysisPdf({ readings, selectedRoom, chartInstance }) {
  if (!window.jspdf || !window.jspdf.jsPDF) {
    alert('Biblioteca jsPDF não carregada. Verifique a conexão com a internet.');
    return;
  }

  const { jsPDF } = window.jspdf;
  const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'mm',
    format: 'a4'
  });

  // Filtra dados pela sala selecionada
  let filtered = readings;
  const roomLabel = (selectedRoom && selectedRoom !== 'all') ? selectedRoom : 'Todas as Salas (Média Global)';
  if (selectedRoom && selectedRoom !== 'all') {
    filtered = readings.filter(r => r.sala_id === selectedRoom);
  }

  // Cálculos estatísticos
  const temps = filtered.map(r => Number(r.temperatura)).filter(t => !isNaN(t));
  const hums = filtered.map(r => r.umidade !== null ? Number(r.umidade) : null).filter(h => h !== null && !isNaN(h));

  const totalAmostras = filtered.length;
  const mediaTemp = temps.length ? (temps.reduce((a, b) => a + b, 0) / temps.length).toFixed(2) : '—';
  const maxTemp = temps.length ? Math.max(...temps).toFixed(2) : '—';
  const minTemp = temps.length ? Math.min(...temps).toFixed(2) : '—';
  const mediaHum = hums.length ? (hums.reduce((a, b) => a + b, 0) / hums.length).toFixed(2) + '%' : '—';

  // % de conformidade com a NR-17 (20°C a 24.5°C)
  const amostrasConfortaveis = temps.filter(t => t >= 20.0 && t <= 24.5).length;
  const percConformidade = temps.length ? ((amostrasConfortaveis / temps.length) * 100).toFixed(1) + '%' : '—';

  // 1. Cabeçalho Institucional
  doc.setFillColor(30, 41, 59); // slate-800
  doc.rect(0, 0, 210, 24, 'F');

  doc.setTextColor(255, 255, 255);
  doc.setFontSize(14);
  doc.setFont('helvetica', 'bold');
  doc.text('SmartClass • Relatório de Análise Térmica e Conforto', 14, 12);

  doc.setFontSize(8);
  doc.setFont('helvetica', 'normal');
  doc.setTextColor(203, 213, 225); // slate-300
  doc.text(`Emissão: ${new Date().toLocaleString('pt-BR')} | Módulo: Monitoramento IoT Escolar`, 14, 18);

  // 2. Metadados do Relatório
  doc.setTextColor(51, 65, 85);
  doc.setFontSize(10);
  doc.setFont('helvetica', 'bold');
  doc.text(`Ambiente Analisado: `, 14, 32);
  doc.setFont('helvetica', 'normal');
  doc.text(`${roomLabel}`, 52, 32);

  doc.setFont('helvetica', 'bold');
  doc.text(`Total de Amostras: `, 130, 32);
  doc.setFont('helvetica', 'normal');
  doc.text(`${totalAmostras} registros`, 165, 32);

  // Linha divisória
  doc.setDrawColor(226, 232, 240);
  doc.line(14, 36, 196, 36);

  // 3. Quadro de Indicadores Estatísticos (Tabela de KPIs)
  const kpiData = [
    [
      `Média: ${mediaTemp} °C`,
      `Máxima: ${maxTemp} °C`,
      `Mínima: ${minTemp} °C`,
      `Umidade Média: ${mediaHum}`,
      `Conformidade NR-17: ${percConformidade}`
    ]
  ];

  doc.autoTable({
    startY: 40,
    head: [['Temp. Média', 'Temp. Máxima', 'Temp. Mínima', 'Umidade Média', 'Índice de Conforto (NR-17)']],
    body: [
      [
        `${mediaTemp} °C`,
        `${maxTemp} °C`,
        `${minTemp} °C`,
        `${mediaHum}`,
        `${percConformidade}`
      ]
    ],
    theme: 'grid',
    headStyles: {
      fillColor: [79, 70, 229], // indigo-600
      textColor: [255, 255, 255],
      fontSize: 8,
      fontStyle: 'bold',
      halign: 'center'
    },
    bodyStyles: {
      fontSize: 9,
      fontStyle: 'bold',
      halign: 'center',
      textColor: [30, 41, 59]
    },
    margin: { left: 14, right: 14 }
  });

  // 4. Imagem do Gráfico de Séries Temporais
  let currentY = doc.lastAutoTable.finalY + 8;

  doc.setFont('helvetica', 'bold');
  doc.setFontSize(10);
  doc.setTextColor(30, 41, 59);
  doc.text('Evolução Temporal da Temperatura e Umidade:', 14, currentY);

  if (chartInstance) {
    try {
      const chartImg = chartInstance.toBase64Image('image/png', 1.0);
      doc.addImage(chartImg, 'PNG', 14, currentY + 3, 182, 75);
      currentY += 82;
    } catch (e) {
      console.warn('Não foi possível exportar imagem do gráfico:', e);
      currentY += 10;
    }
  } else {
    currentY += 10;
  }

  // 5. Parecer Técnico e Observações de Conforto Térmico
  doc.setFillColor(248, 250, 252); // slate-50
  doc.roundedRect(14, currentY, 182, 36, 2, 2, 'FD');
  doc.setDrawColor(203, 213, 225);

  doc.setFontSize(9);
  doc.setFont('helvetica', 'bold');
  doc.setTextColor(79, 70, 229);
  doc.text('Parecer Técnico de Ergonomia Térmica (NR-17):', 18, currentY + 7);

  doc.setFontSize(8);
  doc.setFont('helvetica', 'normal');
  doc.setTextColor(71, 85, 105);

  const parecerTexto = (mediaTemp !== '—' && Number(mediaTemp) >= 20.0 && Number(mediaTemp) <= 24.5)
    ? 'O ambiente escolar avaliado manteve-se predominantemente dentro da faixa ideal de conforto térmico estipulada pela NR-17 (20°C a 24.5°C), favorecendo o rendimento cognitivo e concentração dos alunos.'
    : 'Identificou-se oscilação térmica fora da faixa ótima da NR-17. Recomenda-se a revisão dos horários de climatização e ventilação para mitigar sonolência ou estresse térmico no período letivo.';

  const splitParecer = doc.splitTextToSize(parecerTexto, 174);
  doc.text(splitParecer, 18, currentY + 14);

  doc.setFontSize(7.5);
  doc.setTextColor(148, 163, 184);
  doc.text('* Dados gerados e validados automaticamente pelo sistema SmartClass via PostgreSQL imutável.', 18, currentY + 31);

  // 6. Rodapé
  const pageCount = doc.internal.getNumberOfPages();
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i);
    doc.setFontSize(7.5);
    doc.setTextColor(148, 163, 184);
    doc.text(`SmartClass IoT • Página ${i} de ${pageCount}`, 14, 290);
    doc.text(`PostgreSQL Backend API • ${new Date().toLocaleDateString('pt-BR')}`, 140, 290);
  }

  // Salva o arquivo PDF
  const filename = `smartclass_relatorio_analise_${roomLabel.replace(/\s+/g, '_').toLowerCase()}.pdf`;
  doc.save(filename);
}

export function exportHistoryTablePdf({ readings, selectedRoom, searchTerm }) {
  if (!window.jspdf || !window.jspdf.jsPDF) {
    alert('Biblioteca jsPDF não carregada.');
    return;
  }

  const { jsPDF } = window.jspdf;
  const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'mm',
    format: 'a4'
  });

  // Filtra dados
  let filtered = readings;
  if (selectedRoom && selectedRoom !== 'all') {
    filtered = filtered.filter(r => r.sala_id === selectedRoom);
  }
  if (searchTerm) {
    const term = searchTerm.toLowerCase().trim();
    filtered = filtered.filter(r =>
      r.sala_id.toLowerCase().includes(term) ||
      String(r.id).includes(term) ||
      String(r.temperatura).includes(term)
    );
  }

  // 1. Cabeçalho Institucional
  doc.setFillColor(30, 41, 59); // slate-800
  doc.rect(0, 0, 210, 22, 'F');

  doc.setTextColor(255, 255, 255);
  doc.setFontSize(13);
  doc.setFont('helvetica', 'bold');
  doc.text('SmartClass • Relatório Histórico de Telemetria IoT', 14, 11);

  doc.setFontSize(8);
  doc.setFont('helvetica', 'normal');
  doc.setTextColor(203, 213, 225);
  doc.text(`Extração em: ${new Date().toLocaleString('pt-BR')} | Registros Exportados: ${filtered.length}`, 14, 17);

  // 2. Tabela de Registros
  const tableRows = filtered.map(item => {
    const conforto = classifyThermalComfort(item.temperatura);
    const umidade = item.umidade !== null ? `${Number(item.umidade).toFixed(1)}%` : '—';
    return [
      `#${item.id}`,
      item.sala_id,
      `${Number(item.temperatura).toFixed(2)} °C`,
      umidade,
      conforto.label,
      formatDate(item.data_registro)
    ];
  });

  doc.autoTable({
    startY: 28,
    head: [['ID', 'Sala / Ambiente', 'Temperatura', 'Umidade', 'Status de Conforto', 'Data e Hora (Local)']],
    body: tableRows.length ? tableRows : [['—', 'Nenhum registro encontrado', '—', '—', '—', '—']],
    theme: 'striped',
    headStyles: {
      fillColor: [79, 70, 229], // indigo-600
      textColor: [255, 255, 255],
      fontSize: 8,
      fontStyle: 'bold'
    },
    bodyStyles: {
      fontSize: 8,
      textColor: [30, 41, 59]
    },
    alternateRowStyles: {
      fillColor: [248, 250, 252]
    },
    margin: { left: 14, right: 14, bottom: 15 },
    didDrawPage: function (data) {
      // Rodapé em cada página
      const pageNum = doc.internal.getCurrentPageInfo().pageNumber;
      doc.setFontSize(7.5);
      doc.setTextColor(148, 163, 184);
      doc.text(`SmartClass • Auditoria de Telemetria • Página ${pageNum}`, 14, 290);
      doc.text(`PostgreSQL Database Imutável`, 150, 290);
    }
  });

  const filename = `smartclass_historico_telemetria_${new Date().toISOString().slice(0, 10)}.pdf`;
  doc.save(filename);
}

export function exportHistoryCsv({ readings, selectedRoom, searchTerm }) {
  let filtered = readings;
  if (selectedRoom && selectedRoom !== 'all') {
    filtered = filtered.filter(r => r.sala_id === selectedRoom);
  }
  if (searchTerm) {
    const term = searchTerm.toLowerCase().trim();
    filtered = filtered.filter(r =>
      r.sala_id.toLowerCase().includes(term) ||
      String(r.id).includes(term)
    );
  }

  const headers = ['ID', 'Sala', 'Temperatura_C', 'Umidade_Perc', 'Status_Conforto', 'Data_Hora_ISO'];
  const csvRows = [headers.join(',')];

  filtered.forEach(item => {
    const conforto = classifyThermalComfort(item.temperatura);
    csvRows.push([
      item.id,
      `"${item.sala_id}"`,
      item.temperatura,
      item.umidade !== null ? item.umidade : '',
      `"${conforto.label}"`,
      `"${item.data_registro}"`
    ].join(','));
  });

  const csvContent = '\uFEFF' + csvRows.join('\n'); // UTF-8 BOM para Excel
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', `smartclass_telemetria_${new Date().toISOString().slice(0, 10)}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
