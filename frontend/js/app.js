/**
 * SmartClass - Controlador Principal do Dashboard Web
 * Interface fluida, moderna e responsiva com suporte a abas, Modo Escuro (Dark Mode), exportações PDF/CSV e feedback por Toasts.
 */
import { fetchRecentReadings, checkApiHealth, sendTelemetryReading } from './api.js';
import { formatDate, aggregateByRoom, classifyThermalComfort } from './utils.js';
import { createTelemetryChart, updateChart, setChartTheme } from './charts.js';
import { exportChartAnalysisPdf, exportHistoryTablePdf, exportHistoryCsv } from './pdf_export.js';
import { getAuthUser, logoutUser } from './auth.js';
import {
  emitSingleReading,
  emitBurstReadings,
  startContinuousSimulation,
  stopContinuousSimulation,
  isSimulationActive,
  seedInitialDataIfLow
} from './simulation.js';

class SmartClassDashboard {
  constructor() {
    this.readings = [];
    this.roomSummaries = [];
    this.selectedRoom = 'all';
    this.selectedStatusFilter = 'all';
    this.activeTab = 'overview';
    this.pollingIntervalMs = 5000;
    this.pollingTimer = null;
    this.chart = null;
    this.isInitialLoad = true;
    this.isDarkMode = false;

    this.initElements();
    this.initTheme();
    this.initUser();
    this.attachEventListeners();
    this.initChart();
    this.initSimulation();
    this.startPolling();
  }

  initElements() {
    this.el = {
      connectionBadge: document.getElementById('connectionBadge'),
      connectionPing: document.getElementById('connectionPing'),
      connectionDot: document.getElementById('connectionDot'),
      connectionText: document.getElementById('connectionText'),
      errorBanner: document.getElementById('errorBanner'),
      errorMessage: document.getElementById('errorMessage'),
      lastUpdateLabel: document.getElementById('lastUpdateLabel'),
      btnRefresh: document.getElementById('btnRefresh'),
      selectAutoRefresh: document.getElementById('selectAutoRefresh'),
      btnThemeToggle: document.getElementById('btnThemeToggle'),
      iconSun: document.getElementById('iconSun'),
      iconMoon: document.getElementById('iconMoon'),
      
      // Simulation Stream Controls
      btnToggleSimStream: document.getElementById('btnToggleSimStream'),
      simStreamText: document.getElementById('simStreamText'),
      
      // User Profile & Logout
      btnLogout: document.getElementById('btnLogout'),
      userNameDisplay: document.getElementById('userNameDisplay'),
      userAvatar: document.getElementById('userAvatar'),
      
      // Overview Metric Cards
      statTotalSalas: document.getElementById('statTotalSalas'),
      statMediaTemp: document.getElementById('statMediaTemp'),
      statMediaHum: document.getElementById('statMediaHum'),
      statSalasIdeais: document.getElementById('statSalasIdeais'),
      
      // Containers & Skeletons
      roomsSkeleton: document.getElementById('roomsSkeleton'),
      roomsGrid: document.getElementById('roomsGrid'),
      emptyState: document.getElementById('emptyState'),
      selectChartRoom: document.getElementById('selectChartRoom'),
      
      // Table & Filters
      tableBody: document.getElementById('tableBody'),
      searchInput: document.getElementById('searchInput'),
      btnClearSearch: document.getElementById('btnClearSearch'),
      filterTableRoom: document.getElementById('filterTableRoom'),
      filterChips: document.querySelectorAll('.filter-chip'),

      // Quick Send Simulation
      btnSimulate: document.getElementById('btnSimulate'),

      // PDF / CSV Export Buttons
      btnExportChartPdf: document.getElementById('btnExportChartPdf'),
      btnExportHistoryPdf: document.getElementById('btnExportHistoryPdf'),
      btnExportHistoryCsv: document.getElementById('btnExportHistoryCsv'),

      // Toast Notification Container
      toastContainer: document.getElementById('toastContainer')
    };
  }

  initSimulation() {
    startContinuousSimulation(() => {
      this.refreshData(false);
    }, 6000);
  }

  toggleSimulation() {
    if (isSimulationActive()) {
      stopContinuousSimulation();
      if (this.el.simStreamText) this.el.simStreamText.textContent = 'Simulador Pausado';
      if (this.el.btnToggleSimStream) {
        this.el.btnToggleSimStream.className = 'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200/80 dark:border-slate-700 text-xs font-semibold shadow-subtle active:scale-95 transition-all';
      }
      this.showToast('Simulação Pausada', 'A emissão contínua de telemetria foi suspensa.', 'info');
    } else {
      startContinuousSimulation(() => {
        this.refreshData(false);
      }, 6000);
      if (this.el.simStreamText) this.el.simStreamText.textContent = 'Simulador Ativo';
      if (this.el.btnToggleSimStream) {
        this.el.btnToggleSimStream.className = 'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-indigo-50 dark:bg-indigo-950/60 text-indigo-700 dark:text-indigo-300 border border-indigo-200/80 dark:border-indigo-800 text-xs font-semibold shadow-subtle active:scale-95 transition-all';
      }
      this.showToast('Simulação Ativada 📡', 'O motor está transmitindo medições térmicas para o backend.', 'success');
    }
  }

  initTheme() {
    const savedTheme = localStorage.getItem('smartclass_theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    this.isDarkMode = savedTheme === 'dark' || (!savedTheme && prefersDark);
    this.applyTheme(this.isDarkMode, false);
  }

  toggleTheme() {
    this.isDarkMode = !this.isDarkMode;
    this.applyTheme(this.isDarkMode, true);
  }

  applyTheme(isDark, showToastNotification = true) {
    if (isDark) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('smartclass_theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('smartclass_theme', 'light');
    }

    if (this.chart) {
      setChartTheme(this.chart, isDark);
    }

    if (showToastNotification) {
      this.showToast(
        isDark ? 'Modo Escuro Ativado 🌙' : 'Modo Claro Ativado ☀️',
        isDark ? 'Tema escuro configurado para conforto visual noturno.' : 'Tema claro configurado com visualização diurna.',
        'info'
      );
    }
  }

  initUser() {
    const user = getAuthUser();
    if (user && this.el.userNameDisplay) {
      this.el.userNameDisplay.textContent = user.username || 'univesp';
      if (this.el.userAvatar) {
        this.el.userAvatar.textContent = (user.username || 'U').charAt(0).toUpperCase();
      }
    }
  }

  attachEventListeners() {
    this.el.btnRefresh?.addEventListener('click', () => this.refreshData(true));
    this.el.btnThemeToggle?.addEventListener('click', () => this.toggleTheme());
    this.el.btnToggleSimStream?.addEventListener('click', () => this.toggleSimulation());
    this.el.btnLogout?.addEventListener('click', () => {
      this.showToast('Encerrando Sessão...', 'Até logo!', 'info');
      setTimeout(() => logoutUser(), 400);
    });
    
    this.el.selectAutoRefresh?.addEventListener('change', (e) => {
      this.pollingIntervalMs = parseInt(e.target.value, 10);
      this.startPolling();
      this.showToast(
        'Auto-refresh Atualizado',
        this.pollingIntervalMs > 0 ? `Sincronização a cada ${this.pollingIntervalMs / 1000}s.` : 'Atualização automática pausada.',
        'info'
      );
    });

    this.el.selectChartRoom?.addEventListener('change', (e) => {
      this.selectedRoom = e.target.value;
      updateChart(this.chart, this.readings, this.selectedRoom);
    });

    this.el.filterTableRoom?.addEventListener('change', () => this.renderTable());
    
    this.el.searchInput?.addEventListener('input', (e) => {
      if (this.el.btnClearSearch) {
        if (e.target.value.length > 0) {
          this.el.btnClearSearch.classList.remove('hidden');
        } else {
          this.el.btnClearSearch.classList.add('hidden');
        }
      }
      this.renderTable();
    });

    this.el.btnClearSearch?.addEventListener('click', () => {
      if (this.el.searchInput) {
        this.el.searchInput.value = '';
        this.el.btnClearSearch.classList.add('hidden');
        this.renderTable();
      }
    });

    // Chips de filtro por status
    this.el.filterChips?.forEach(chip => {
      chip.addEventListener('click', (e) => {
        const targetStatus = e.currentTarget.getAttribute('data-filter-status');
        this.selectedStatusFilter = targetStatus;

        // Atualiza estilo visual dos chips com suporte a Dark Mode
        this.el.filterChips.forEach(c => {
          c.className = 'filter-chip px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300 font-medium transition-all';
        });
        e.currentTarget.className = 'filter-chip px-2.5 py-1 rounded-lg bg-slate-900 dark:bg-slate-100 text-white dark:text-slate-900 font-semibold transition-all shadow-xs';

        this.renderTable();
      });
    });

    this.el.btnSimulate?.addEventListener('click', () => this.handleSimulateQuickReading());

    // Eventos de Exportação PDF / CSV com feedback em Toast
    this.el.btnExportChartPdf?.addEventListener('click', () => {
      try {
        exportChartAnalysisPdf({
          readings: this.readings,
          selectedRoom: this.selectedRoom,
          chartInstance: this.chart
        });
        this.showToast('Relatório Gerado', 'O PDF de Análise Térmica foi baixado com sucesso.', 'success');
      } catch (err) {
        this.showToast('Erro ao Exportar', err.message, 'error');
      }
    });

    this.el.btnExportHistoryPdf?.addEventListener('click', () => {
      try {
        exportHistoryTablePdf({
          readings: this.readings,
          selectedRoom: this.el.filterTableRoom?.value || 'all',
          searchTerm: this.el.searchInput?.value || ''
        });
        this.showToast('Tabela Exportada', 'O PDF de auditoria foi baixado com sucesso.', 'success');
      } catch (err) {
        this.showToast('Erro ao Exportar', err.message, 'error');
      }
    });

    this.el.btnExportHistoryCsv?.addEventListener('click', () => {
      try {
        exportHistoryCsv({
          readings: this.readings,
          selectedRoom: this.el.filterTableRoom?.value || 'all',
          searchTerm: this.el.searchInput?.value || ''
        });
        this.showToast('CSV Gerado', 'Arquivo de dados exportado para planilha com sucesso.', 'success');
      } catch (err) {
        this.showToast('Erro ao Exportar', err.message, 'error');
      }
    });
  }

  initChart() {
    const canvas = document.getElementById('telemetryChart');
    if (canvas) {
      this.chart = createTelemetryChart(canvas.getContext('2d'));
    }
  }

  switchTab(tabId) {
    this.activeTab = tabId;

    // 1. Alterna visibilidade dos containers
    document.querySelectorAll('.tab-view').forEach(view => {
      view.classList.add('hidden');
    });

    const targetView = document.getElementById(`view-${tabId}`);
    if (targetView) {
      targetView.classList.remove('hidden');
    }

    // 2. Alterna visual do segmented control
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.classList.remove('tab-active');
      btn.classList.add('text-slate-600', 'dark:text-slate-400');
    });

    const activeBtn = document.getElementById(`tabBtn-${tabId}`);
    if (activeBtn) {
      activeBtn.classList.add('tab-active');
      activeBtn.classList.remove('text-slate-600', 'dark:text-slate-400');
    }

    // 3. Atualiza tamanho do chart se necessário
    if (tabId === 'charts' && this.chart) {
      setTimeout(() => {
        this.chart.resize();
        updateChart(this.chart, this.readings, this.selectedRoom);
      }, 50);
    }
  }

  startPolling() {
    if (this.pollingTimer) {
      clearInterval(this.pollingTimer);
      this.pollingTimer = null;
    }

    // Executa a primeira carga imediatamente
    this.refreshData();

    if (this.pollingIntervalMs > 0) {
      this.pollingTimer = setInterval(() => {
        this.refreshData(false);
      }, this.pollingIntervalMs);
    }
  }

  async refreshData(showLoading = false) {
    if (showLoading && this.el.btnRefresh) {
      this.el.btnRefresh.classList.add('animate-spin');
    }

    try {
      let data = await fetchRecentReadings(100);
      
      if (this.isInitialLoad) {
        const seeded = await seedInitialDataIfLow(data.length, 12);
        if (seeded) {
          data = await fetchRecentReadings(100);
        }
      }

      this.readings = data;
      this.roomSummaries = aggregateByRoom(data);
      
      this.setConnectionStatus(true);
      this.renderOverviewMetrics();
      this.renderRoomCards();
      this.populateRoomSelects();
      
      if (this.chart) {
        updateChart(this.chart, this.readings, this.selectedRoom);
      }
      
      this.renderTable();
      
      if (this.el.lastUpdateLabel) {
        this.el.lastUpdateLabel.textContent = `Sincronizado às ${new Date().toLocaleTimeString('pt-BR')}`;
      }

      if (this.isInitialLoad) {
        this.isInitialLoad = false;
        if (this.el.roomsSkeleton) this.el.roomsSkeleton.classList.add('hidden');
        if (this.el.roomsGrid) this.el.roomsGrid.classList.remove('hidden');
      }
    } catch (error) {
      this.setConnectionStatus(false, error.message);
      if (this.isInitialLoad) {
        if (this.el.roomsSkeleton) this.el.roomsSkeleton.classList.add('hidden');
      }
    } finally {
      if (showLoading && this.el.btnRefresh) {
        setTimeout(() => this.el.btnRefresh.classList.remove('animate-spin'), 300);
      }
    }
  }

  setConnectionStatus(online, message = '') {
    if (!this.el.connectionBadge) return;

    if (online) {
      this.el.connectionBadge.className = 'inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold bg-indigo-500/10 dark:bg-indigo-950/50 text-indigo-700 dark:text-indigo-300 border border-indigo-500/20 dark:border-indigo-800/40 shadow-subtle';
      if (this.el.connectionPing) {
        this.el.connectionPing.className = 'radar-pulse absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75';
      }
      if (this.el.connectionDot) {
        this.el.connectionDot.className = 'relative inline-flex rounded-full h-2 w-2 bg-indigo-500';
      }
      if (this.el.connectionText) {
        this.el.connectionText.textContent = 'Simulação IoT Ativa 📡';
      }
      if (this.el.errorBanner) this.el.errorBanner.classList.add('hidden');
    } else {
      this.el.connectionBadge.className = 'inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold bg-rose-500/10 dark:bg-rose-950/50 text-rose-700 dark:text-rose-300 border border-rose-500/20 dark:border-rose-800/40 shadow-subtle';
      if (this.el.connectionPing) {
        this.el.connectionPing.className = 'hidden';
      }
      if (this.el.connectionDot) {
        this.el.connectionDot.className = 'relative inline-flex rounded-full h-2 w-2 bg-rose-500 animate-ping';
      }
      if (this.el.connectionText) {
        this.el.connectionText.textContent = 'Servidor Inacessível';
      }
      if (this.el.errorBanner) {
        this.el.errorBanner.classList.remove('hidden');
        if (this.el.errorMessage) {
          this.el.errorMessage.textContent = message || 'Não foi possível comunicar com o backend Flask na porta 5000.';
        }
      }
    }
  }

  renderOverviewMetrics() {
    if (!this.el.statTotalSalas) return;

    const totalSalas = this.roomSummaries.length;
    this.el.statTotalSalas.textContent = totalSalas;

    if (this.readings.length === 0) {
      this.el.statMediaTemp.textContent = '—';
      this.el.statMediaHum.textContent = '—';
      this.el.statSalasIdeais.textContent = '—';
      return;
    }

    const temps = this.readings.map(r => Number(r.temperatura)).filter(t => !isNaN(t));
    const hums = this.readings.map(r => r.umidade !== null ? Number(r.umidade) : null).filter(h => h !== null && !isNaN(h));
    
    const mediaGeralTemp = (temps.reduce((a, b) => a + b, 0) / temps.length).toFixed(1);
    const mediaGeralHum = hums.length ? (hums.reduce((a, b) => a + b, 0) / hums.length).toFixed(1) + '%' : '—';
    const salasIdeaisCount = this.roomSummaries.filter(s => s.conforto.status === 'ideal').length;

    this.el.statMediaTemp.textContent = `${mediaGeralTemp} °C`;
    this.el.statMediaHum.textContent = mediaGeralHum;
    this.el.statSalasIdeais.textContent = `${salasIdeaisCount} / ${totalSalas}`;
  }

  renderRoomCards() {
    if (!this.el.roomsGrid) return;

    if (this.roomSummaries.length === 0) {
      this.el.roomsGrid.innerHTML = '';
      if (this.el.emptyState) this.el.emptyState.classList.remove('hidden');
      return;
    }

    if (this.el.emptyState) this.el.emptyState.classList.add('hidden');

    this.el.roomsGrid.innerHTML = this.roomSummaries.map(room => {
      const { conforto } = room;
      const umidadeDisplay = room.ultima_umidade !== null ? `${room.ultima_umidade.toFixed(1)}%` : '—';
      const dataHoraFormatada = formatDate(room.data_ultima_leitura);

      return `
        <div class="bg-white dark:bg-slate-900 rounded-2xl border ${conforto.bgClass} p-5 shadow-card hover:shadow-card-hover hover:-translate-y-1 transition-all duration-300 relative group">
          <div class="flex items-start justify-between gap-2">
            <div>
              <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500">Ambiente</span>
              <h3 class="text-base font-bold text-slate-900 dark:text-white tracking-tight group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">${room.sala_id}</h3>
            </div>
            <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-semibold border ${conforto.badgeClass} shadow-2xs shrink-0">
              <span class="w-1.5 h-1.5 rounded-full ${conforto.dotClass}"></span>
              ${conforto.shortLabel}
            </span>
          </div>

          <div class="grid grid-cols-2 gap-4 my-4 pt-3.5 border-t border-slate-100 dark:border-slate-800">
            <div>
              <p class="text-[11px] text-slate-400 dark:text-slate-500 font-semibold uppercase tracking-wider">Temperatura</p>
              <div class="flex items-baseline gap-1 mt-1">
                <span class="text-3xl font-black tracking-tight text-slate-900 dark:text-white">${room.ultima_temperatura.toFixed(1)}</span>
                <span class="text-xs font-semibold text-slate-400 dark:text-slate-500">°C</span>
              </div>
              <p class="text-[11px] text-slate-400 dark:text-slate-500 mt-1">Média: <span class="font-medium text-slate-600 dark:text-slate-300">${room.media_temperatura}°C</span></p>
            </div>
            <div>
              <p class="text-[11px] text-slate-400 dark:text-slate-500 font-semibold uppercase tracking-wider">Umidade</p>
              <div class="flex items-baseline gap-1 mt-1">
                <span class="text-3xl font-black tracking-tight text-slate-900 dark:text-white">${umidadeDisplay}</span>
              </div>
              <p class="text-[11px] text-slate-400 dark:text-slate-500 mt-1">${room.media_umidade !== null ? `Média: <span class="font-medium text-slate-600 dark:text-slate-300">${room.media_umidade}%</span>` : 'Sem sensor higrométrico'}</p>
            </div>
          </div>

          <div class="flex items-center justify-between pt-3 border-t border-slate-100 dark:border-slate-800 text-[11px] text-slate-400 dark:text-slate-500">
            <span class="flex items-center gap-1">
              <svg class="w-3.5 h-3.5 text-slate-300 dark:text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <span>Último envio:</span>
            </span>
            <span class="font-semibold text-slate-600 dark:text-slate-300 font-mono text-[10px]">${dataHoraFormatada}</span>
          </div>
        </div>
      `;
    }).join('');
  }

  populateRoomSelects() {
    const rooms = this.roomSummaries.map(s => s.sala_id);
    
    // Select do gráfico
    if (this.el.selectChartRoom) {
      const currentVal = this.el.selectChartRoom.value;
      this.el.selectChartRoom.innerHTML = '<option value="all">Todas as Salas (Média Global)</option>' +
        rooms.map(r => `<option value="${r}">${r}</option>`).join('');
      if (rooms.includes(currentVal) || currentVal === 'all') {
        this.el.selectChartRoom.value = currentVal;
      }
    }

    // Select da tabela
    if (this.el.filterTableRoom) {
      const currentVal = this.el.filterTableRoom.value;
      this.el.filterTableRoom.innerHTML = '<option value="all">Todas as Salas</option>' +
        rooms.map(r => `<option value="${r}">${r}</option>`).join('');
      if (rooms.includes(currentVal) || currentVal === 'all') {
        this.el.filterTableRoom.value = currentVal;
      }
    }
  }

  renderTable() {
    if (!this.el.tableBody) return;

    const searchTerm = (this.el.searchInput?.value || '').toLowerCase().trim();
    const selectedRoom = this.el.filterTableRoom?.value || 'all';
    const statusFilter = this.selectedStatusFilter || 'all';

    let filtered = this.readings;

    if (selectedRoom !== 'all') {
      filtered = filtered.filter(r => r.sala_id === selectedRoom);
    }

    if (searchTerm) {
      filtered = filtered.filter(r => {
        return (
          r.sala_id?.toLowerCase().includes(searchTerm) ||
          String(r.id).includes(searchTerm) ||
          String(r.temperatura).includes(searchTerm)
        );
      });
    }

    if (statusFilter !== 'all') {
      filtered = filtered.filter(r => {
        const conf = classifyThermalComfort(r.temperatura);
        return conf.status === statusFilter;
      });
    }

    if (filtered.length === 0) {
      this.el.tableBody.innerHTML = `
        <tr>
          <td colspan="6" class="px-4 py-8 text-center text-slate-400 dark:text-slate-500 text-xs">
            Nenhuma leitura encontrada com os filtros selecionados.
          </td>
        </tr>
      `;
      return;
    }

    this.el.tableBody.innerHTML = filtered.map(item => {
      const conforto = classifyThermalComfort(item.temperatura);
      const humDisplay = item.umidade !== null ? `${Number(item.umidade).toFixed(1)}%` : '—';
      const formattedDate = formatDate(item.data_registro);

      return `
        <tr class="hover:bg-slate-50/80 dark:hover:bg-slate-800/50 transition-colors">
          <td class="px-4 py-3 font-mono text-[11px] text-slate-400 dark:text-slate-500">#${item.id}</td>
          <td class="px-4 py-3 font-bold text-slate-800 dark:text-slate-200">${item.sala_id}</td>
          <td class="px-4 py-3 font-semibold text-slate-900 dark:text-white">${Number(item.temperatura).toFixed(2)} °C</td>
          <td class="px-4 py-3 font-medium text-slate-600 dark:text-slate-300">${humDisplay}</td>
          <td class="px-4 py-3">
            <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-semibold border ${conforto.badgeClass}">
              <span class="w-1.5 h-1.5 rounded-full ${conforto.dotClass}"></span>
              ${conforto.label}
            </span>
          </td>
          <td class="px-4 py-3 text-slate-500 dark:text-slate-400 font-mono text-[11px]">${formattedDate}</td>
        </tr>
      `;
    }).join('');
  }

  async handleSimulateQuickReading() {
    try {
      const result = await emitSingleReading();
      this.showToast(
        'Transmissão IoT Simulada',
        `Nova medição registrada para ${result.sala_id}: ${result.temperatura}°C / ${result.umidade}%.`,
        'success'
      );
      await this.refreshData(false);
    } catch (err) {
      this.showToast('Falha na Simulação', err.message, 'error');
    }
  }

  showToast(title, message, type = 'info') {
    if (!this.el.toastContainer) return;

    const toast = document.createElement('div');
    toast.className = 'pointer-events-auto bg-white dark:bg-slate-900 rounded-2xl p-4 border shadow-card-hover flex items-start gap-3 transform transition-all duration-300 translate-y-4 opacity-0';

    let iconHtml = '';
    if (type === 'success') {
      toast.classList.add('border-emerald-500/30', 'dark:border-emerald-500/40');
      iconHtml = `
        <div class="w-7 h-7 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400 flex items-center justify-center shrink-0 border border-emerald-100 dark:border-emerald-800/60">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
        </div>`;
    } else if (type === 'error') {
      toast.classList.add('border-rose-500/30', 'dark:border-rose-500/40');
      iconHtml = `
        <div class="w-7 h-7 rounded-xl bg-rose-50 dark:bg-rose-950/60 text-rose-600 dark:text-rose-400 flex items-center justify-center shrink-0 border border-rose-100 dark:border-rose-800/60">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </div>`;
    } else {
      toast.classList.add('border-indigo-500/30', 'dark:border-indigo-500/40');
      iconHtml = `
        <div class="w-7 h-7 rounded-xl bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400 flex items-center justify-center shrink-0 border border-indigo-100 dark:border-indigo-800/60">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        </div>`;
    }

    toast.innerHTML = `
      ${iconHtml}
      <div class="flex-1 text-xs">
        <p class="font-bold text-slate-900 dark:text-white">${title}</p>
        <p class="text-slate-500 dark:text-slate-400 mt-0.5 leading-relaxed">${message}</p>
      </div>
      <button class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 text-sm font-bold ml-1">✕</button>
    `;

    const closeBtn = toast.querySelector('button');
    closeBtn?.addEventListener('click', () => {
      toast.classList.add('opacity-0', 'translate-y-2');
      setTimeout(() => toast.remove(), 250);
    });

    this.el.toastContainer.appendChild(toast);

    // Fade in
    requestAnimationFrame(() => {
      toast.classList.remove('translate-y-4', 'opacity-0');
    });

    // Auto dismiss
    setTimeout(() => {
      if (toast.parentElement) {
        toast.classList.add('opacity-0', 'translate-y-2');
        setTimeout(() => toast.remove(), 250);
      }
    }, 4500);
  }
}

// Inicializa a aplicação ao carregar o DOM
document.addEventListener('DOMContentLoaded', () => {
  window.dashboardApp = new SmartClassDashboard();
});
