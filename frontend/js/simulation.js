/**
 * SmartClass - Motor de Simulação de Telemetria IoT
 * Gera variações térmicas e higrométricas realistas com inércia térmica e envio assíncrono.
 */
import { sendTelemetryReading } from './api.js';

const ROOM_PROFILES = [
  { id: 'Sala 101', baseTemp: 22.4, currentTemp: 22.4, baseHum: 54.0, currentHum: 54.0 },
  { id: 'Sala 102', baseTemp: 23.8, currentTemp: 23.8, baseHum: 50.0, currentHum: 50.0 },
  { id: 'Lab 01', baseTemp: 21.2, currentTemp: 21.2, baseHum: 48.0, currentHum: 48.0 },
  { id: 'Lab 02', baseTemp: 24.6, currentTemp: 24.6, baseHum: 58.0, currentHum: 58.0 },
  { id: 'Auditório', baseTemp: 22.0, currentTemp: 22.0, baseHum: 52.0, currentHum: 52.0 },
  { id: 'Biblioteca', baseTemp: 21.8, currentTemp: 21.8, baseHum: 46.0, currentHum: 46.0 }
];

let simulationTimer = null;
let isSimulating = false;

function getNextReading(profile) {
  // Random walk com reversão à média para manter realismo
  const tempDelta = (Math.random() - 0.5) * 0.4 + (profile.baseTemp - profile.currentTemp) * 0.08;
  const humDelta = (Math.random() - 0.5) * 0.8 + (profile.baseHum - profile.currentHum) * 0.08;

  profile.currentTemp = Number((profile.currentTemp + tempDelta).toFixed(2));
  profile.currentHum = Number((profile.currentHum + humDelta).toFixed(2));

  // Limites físicos de segurança
  profile.currentTemp = Math.max(18.0, Math.min(32.0, profile.currentTemp));
  profile.currentHum = Math.max(30.0, Math.min(85.0, profile.currentHum));

  return {
    sala_id: profile.id,
    temperatura: profile.currentTemp,
    umidade: profile.currentHum
  };
}

export async function emitSingleReading(specificRoomId = null) {
  let profile;
  if (specificRoomId) {
    profile = ROOM_PROFILES.find(r => r.id === specificRoomId) || ROOM_PROFILES[0];
  } else {
    profile = ROOM_PROFILES[Math.floor(Math.random() * ROOM_PROFILES.length)];
  }

  const payload = getNextReading(profile);
  return await sendTelemetryReading(payload);
}

export async function emitBurstReadings() {
  const promises = ROOM_PROFILES.map(profile => {
    const payload = getNextReading(profile);
    return sendTelemetryReading(payload);
  });
  return await Promise.all(promises);
}

export function startContinuousSimulation(onReadingCallback, intervalMs = 6000) {
  if (simulationTimer) {
    clearInterval(simulationTimer);
  }
  isSimulating = true;

  simulationTimer = setInterval(async () => {
    try {
      const profile = ROOM_PROFILES[Math.floor(Math.random() * ROOM_PROFILES.length)];
      const payload = getNextReading(profile);
      await sendTelemetryReading(payload);
      if (typeof onReadingCallback === 'function') {
        onReadingCallback(payload);
      }
    } catch (e) {
      console.warn('Erro ao emitir telemetria simulada:', e.message);
    }
  }, intervalMs);
}

export function stopContinuousSimulation() {
  if (simulationTimer) {
    clearInterval(simulationTimer);
    simulationTimer = null;
  }
  isSimulating = false;
}

export function isSimulationActive() {
  return isSimulating;
}

export async function seedInitialDataIfLow(existingCount = 0) {
  if (existingCount < 6) {
    console.info('SmartClass: Inicializando banco de dados com lote de telemetria simulada...');
    try {
      for (const profile of ROOM_PROFILES) {
        const payload = getNextReading(profile);
        await sendTelemetryReading(payload);
      }
    } catch (err) {
      console.warn('Falha no auto-seed de telemetria:', err);
    }
  }
}
