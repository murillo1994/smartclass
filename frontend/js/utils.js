/**
 * SmartClass - Funções Utilitárias e Classificação de Conforto Térmico (NR-17)
 * Compatível com Modo Claro e Modo Escuro (Dark Mode).
 */

export function classifyThermalComfort(temperatura) {
  const temp = Number(temperatura);
  if (temp < 19.5) {
    return {
      status: "frio",
      label: "Abaixo do Ideal (Frio)",
      shortLabel: "Frio",
      bgClass: "border-sky-200/80 hover:border-sky-400/60 bg-gradient-to-b from-sky-500/[0.03] to-white dark:border-sky-500/30 dark:hover:border-sky-500/60 dark:from-sky-950/30 dark:to-slate-900",
      dotClass: "bg-sky-500 shadow-[0_0_8px_rgba(14,165,233,0.6)]",
      badgeClass: "bg-sky-500/10 text-sky-700 dark:text-sky-400 border-sky-500/20 dark:border-sky-500/30",
      accentColor: "#0284c7"
    };
  } else if (temp <= 24.5) {
    return {
      status: "ideal",
      label: "Confortável (Ideal)",
      shortLabel: "Ideal",
      bgClass: "border-emerald-200/80 hover:border-emerald-400/60 bg-gradient-to-b from-emerald-500/[0.03] to-white dark:border-emerald-500/30 dark:hover:border-emerald-500/60 dark:from-emerald-950/30 dark:to-slate-900",
      dotClass: "bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.6)]",
      badgeClass: "bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border-emerald-500/20 dark:border-emerald-500/30",
      accentColor: "#10b981"
    };
  } else if (temp <= 27.0) {
    return {
      status: "atencao",
      label: "Atenção: Aquecido",
      shortLabel: "Aquecido",
      bgClass: "border-amber-200/80 hover:border-amber-400/60 bg-gradient-to-b from-amber-500/[0.03] to-white dark:border-amber-500/30 dark:hover:border-amber-500/60 dark:from-amber-950/30 dark:to-slate-900",
      dotClass: "bg-amber-500 shadow-[0_0_8px_rgba(245,158,11,0.6)]",
      badgeClass: "bg-amber-500/10 text-amber-700 dark:text-amber-400 border-amber-500/20 dark:border-amber-500/30",
      accentColor: "#f59e0b"
    };
  } else {
    return {
      status: "quente",
      label: "Calor Excessivo",
      shortLabel: "Calor",
      bgClass: "border-rose-200/80 hover:border-rose-400/60 bg-gradient-to-b from-rose-500/[0.03] to-white dark:border-rose-500/30 dark:hover:border-rose-500/60 dark:from-rose-950/30 dark:to-slate-900",
      dotClass: "bg-rose-500 shadow-[0_0_8px_rgba(244,63,94,0.6)]",
      badgeClass: "bg-rose-500/10 text-rose-700 dark:text-rose-400 border-rose-500/20 dark:border-rose-500/30",
      accentColor: "#f43f5e"
    };
  }
}

export function formatDate(isoString) {
  if (!isoString) return "—";
  try {
    const d = new Date(isoString);
    return d.toLocaleString("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit"
    });
  } catch {
    return isoString;
  }
}

export function formatShortTime(isoString) {
  if (!isoString) return "";
  try {
    const d = new Date(isoString);
    return d.toLocaleTimeString("pt-BR", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit"
    });
  } catch {
    return "";
  }
}

export function aggregateByRoom(readings) {
  const roomsMap = new Map();

  for (const item of readings) {
    const salaId = item.sala_id || "Desconhecida";
    if (!roomsMap.has(salaId)) {
      roomsMap.set(salaId, {
        sala_id: salaId,
        readings: [],
        ultima_leitura: null
      });
    }
    const room = roomsMap.get(salaId);
    room.readings.push(item);
    if (!room.ultima_leitura || new Date(item.data_registro) > new Date(room.ultima_leitura.data_registro)) {
      room.ultima_leitura = item;
    }
  }

  const summaries = [];
  roomsMap.forEach((room) => {
    const temps = room.readings.map(r => Number(r.temperatura)).filter(t => !isNaN(t));
    const hums = room.readings.map(r => r.umidade !== null ? Number(r.umidade) : null).filter(h => h !== null && !isNaN(h));
    
    const mediaTemp = temps.length ? (temps.reduce((a, b) => a + b, 0) / temps.length).toFixed(1) : "0.0";
    const mediaHum = hums.length ? (hums.reduce((a, b) => a + b, 0) / hums.length).toFixed(1) : null;
    const ultimaTemp = room.ultima_leitura ? Number(room.ultima_leitura.temperatura) : 0;
    const ultimaHum = (room.ultima_leitura && room.ultima_leitura.umidade !== null) ? Number(room.ultima_leitura.umidade) : null;

    summaries.push({
      sala_id: room.sala_id,
      total_leituras: room.readings.length,
      ultima_temperatura: ultimaTemp,
      ultima_umidade: ultimaHum,
      data_ultima_leitura: room.ultima_leitura ? room.ultima_leitura.data_registro : null,
      media_temperatura: mediaTemp,
      media_umidade: mediaHum,
      conforto: classifyThermalComfort(ultimaTemp)
    });
  });

  return summaries.sort((a, b) => a.sala_id.localeCompare(b.sala_id));
}
