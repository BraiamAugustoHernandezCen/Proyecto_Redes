import { useState, useEffect } from 'react'
import axios from 'axios'

function App() {
  const [datos, setDatos] = useState([])

  const fetchDatos = async () => {
    try {
      const response = await axios.get('https://proyecto-redes-50om.onrender.com/api/datos')
      setDatos(response.data)
    } catch (error) {
      console.error("Error al conectar con la API:", error)
    }
  }

  useEffect(() => {
    fetchDatos()
    const intervalo = setInterval(fetchDatos, 5000)
    return () => clearInterval(intervalo)
  }, [])

  const tcp = datos.filter(d => d.protocolo === 'TCP').length
  const udp = datos.filter(d => d.protocolo === 'UDP').length
  const total = datos.length
  const tcpPct = total ? Math.round((tcp / total) * 100) : 0
  const udpPct = total ? Math.round((udp / total) * 100) : 0

  const tagStyle = (proto) => ({
    fontFamily: "'Press Start 2P', monospace",
    fontSize: '7px', padding: '3px 6px',
    background: proto === 'TCP' ? '#e94560' : '#4fc3f7',
    color: proto === 'TCP' ? '#fff' : '#1a1a2e',
  })

  const s = {
    wrap: { background: '#1a1a2e', minHeight: '100vh', fontFamily: "'Noto Sans JP', sans-serif", color: '#fff' },
    topbar: { background: '#16213e', borderBottom: '4px solid #e94560', padding: '10px 20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' },
    topbarTitle: { fontFamily: "'Press Start 2P', monospace", fontSize: '11px', color: '#fff', display: 'flex', alignItems: 'center', gap: '10px' },
    vhsBadge: { fontFamily: "'Press Start 2P', monospace", fontSize: '8px', background: '#e94560', color: '#fff', padding: '4px 8px' },
    body: { padding: '16px 20px' },
    sectionTitle: { fontFamily: "'Press Start 2P', monospace", fontSize: '9px', color: '#f5a623', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' },
    metrics: { display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '10px', marginBottom: '20px' },
    panels: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '20px' },
    tableWrap: { background: '#16213e', border: '3px solid #e94560' },
    tableHeader: { background: '#e94560', padding: '8px 14px', fontFamily: "'Press Start 2P', monospace", fontSize: '8px', color: '#fff', display: 'flex', justifyContent: 'space-between' },
  }

  const cards = [
    { jp: '合計', label: 'TOTAL REGISTROS', value: total, sub: '↑ en tiempo real', color: '#e94560', border: '#e94560' },
    { jp: '制御転送', label: 'PROTOCOLO TCP', value: tcp, sub: `${tcpPct}% del tráfico`, color: '#4fc3f7', border: '#0f3460' },
    { jp: 'データグラム', label: 'PROTOCOLO UDP', value: udp, sub: `${udpPct}% del tráfico`, color: '#f5a623', border: '#f5a623' },
    { jp: '最終更新', label: 'ULTIMA INSERCION', value: '● LIVE', sub: 'sistema activo', color: '#ff6b9d', border: '#ff6b9d', small: true },
  ]

  const tcpPixels = Math.round((tcpPct / 100) * 20)

  return (
    <>
      <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Noto+Sans+JP:wght@400;700&display=swap" rel="stylesheet" />
      <style>{`
        @keyframes blink { 50% { opacity: 0; } }
        .live-dot { animation: blink 0.8s step-end infinite; }
        tr:hover td { background: #0f1a30; }
        .bar-fill-tcp { background: repeating-linear-gradient(90deg,#e94560 0px,#e94560 6px,#c73652 6px,#c73652 8px); }
        .bar-fill-udp { background: repeating-linear-gradient(90deg,#4fc3f7 0px,#4fc3f7 6px,#3aa8d8 6px,#3aa8d8 8px); }
        .scanlines { position: fixed; top:0; left:0; width:100%; height:100%; background: repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.1) 2px,rgba(0,0,0,0.1) 4px); pointer-events:none; z-index:999; }
      `}</style>

      <div style={s.wrap}>
        <div className="scanlines"></div>

        {/* Topbar */}
        <div style={s.topbar}>
          <div style={s.topbarTitle}>
            <span className="live-dot" style={{ width: '8px', height: '8px', background: '#f5a623', display: 'inline-block', borderRadius: '0' }}></span>
            Monitor de Red
            <span style={{ color: '#444', fontSize: '9px' }}>ネットワーク</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span style={{ fontSize: '13px', color: '#e94560', fontWeight: 700 }}>Fase 3 フェーズ</span>
            <span style={s.vhsBadge}>● REC</span>
          </div>
        </div>

        <div style={s.body}>

          {/* Métricas */}
          <div style={s.sectionTitle}>
            <span style={{ color: '#e94560' }}>►</span>
            Estado del Sistema
            <span style={{ fontSize: '10px', color: '#444' }}>システム状態</span>
          </div>
          <div style={s.metrics}>
            {cards.map((c, i) => (
              <div key={i} style={{ background: '#16213e', border: `3px solid ${c.border}`, padding: '12px', position: 'relative', overflow: 'hidden' }}>
                <div style={{ position: 'absolute', top: 0, right: 0, width: 0, height: 0, borderStyle: 'solid', borderWidth: '0 16px 16px 0', borderColor: `transparent ${c.border} transparent transparent` }}></div>
                <div style={{ fontSize: '9px', color: '#444', marginBottom: '2px' }}>{c.jp}</div>
                <div style={{ fontFamily: "'Press Start 2P', monospace", fontSize: '7px', color: '#aaa', marginBottom: '8px' }}>{c.label}</div>
                <div style={{ fontFamily: "'Press Start 2P', monospace", fontSize: c.small ? '11px' : '20px', color: c.color, marginTop: c.small ? '6px' : '0' }}>{c.value}</div>
                <div style={{ fontSize: '10px', color: '#666', marginTop: '6px' }}>{c.sub}</div>
              </div>
            ))}
          </div>

          {/* Paneles */}
          <div style={s.sectionTitle}>
            <span style={{ color: '#e94560' }}>►</span>
            Análisis de Protocolos
            <span style={{ fontSize: '10px', color: '#444' }}>プロトコル</span>
          </div>
          <div style={s.panels}>
            <div style={{ background: '#16213e', border: '3px solid #0f3460' }}>
              <div style={{ background: '#0f3460', padding: '8px 12px', fontFamily: "'Press Start 2P', monospace", fontSize: '8px', color: '#4fc3f7', display: 'flex', justifyContent: 'space-between' }}>
                <span>Mensajes por Protocolo</span>
                <span style={{ color: '#333', fontSize: '9px' }}>バーチャート</span>
              </div>
              <div style={{ padding: '14px' }}>
                {[{ proto: 'TCP', count: tcp, pct: tcpPct }, { proto: 'UDP', count: udp, pct: udpPct }].map(({ proto, count, pct }) => (
                  <div key={proto} style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
                    <div style={{ fontFamily: "'Press Start 2P', monospace", fontSize: '7px', width: '30px', color: proto === 'TCP' ? '#e94560' : '#4fc3f7' }}>{proto}</div>
                    <div style={{ flex: 1, height: '16px', background: '#1a1a2e', border: '2px solid #0f3460', overflow: 'hidden' }}>
                      <div className={`bar-fill-${proto.toLowerCase()}`} style={{ width: `${pct}%`, height: '100%' }}></div>
                    </div>
                    <div style={{ fontFamily: "'Press Start 2P', monospace", fontSize: '8px', width: '28px', textAlign: 'right', color: proto === 'TCP' ? '#e94560' : '#4fc3f7' }}>{count}</div>
                  </div>
                ))}
                <div style={{ fontFamily: "'Press Start 2P', monospace", fontSize: '7px', color: '#444', marginTop: '8px' }}>
                  <span style={{ color: '#e94560' }}>████</span> TCP &nbsp; <span style={{ color: '#4fc3f7' }}>████</span> UDP
                </div>
              </div>
            </div>

            <div style={{ background: '#16213e', border: '3px solid #0f3460' }}>
              <div style={{ background: '#0f3460', padding: '8px 12px', fontFamily: "'Press Start 2P', monospace", fontSize: '8px', color: '#4fc3f7', display: 'flex', justifyContent: 'space-between' }}>
                <span>Distribución de Tráfico</span>
                <span style={{ color: '#333', fontSize: '9px' }}>ピクセル</span>
              </div>
              <div style={{ padding: '14px' }}>
                <div style={{ fontFamily: "'Press Start 2P', monospace", fontSize: '7px', color: '#888', marginBottom: '10px' }}>
                  <span style={{ color: '#e94560' }}>■</span> TCP &nbsp; <span style={{ color: '#4fc3f7' }}>■</span> UDP
                </div>
                <div style={{ display: 'flex', gap: '3px', flexWrap: 'wrap', padding: '4px 0' }}>
                  {Array.from({ length: 20 }, (_, i) => (
                    <div key={i} style={{ width: '8px', height: '8px', background: i < tcpPixels ? '#e94560' : '#4fc3f7', display: 'inline-block' }}></div>
                  ))}
                </div>
                <div style={{ marginTop: '12px' }}>
                  <div style={{ color: '#e94560', fontFamily: "'Press Start 2P', monospace", fontSize: '9px' }}>TCP — {tcpPct}%</div>
                  <div style={{ color: '#4fc3f7', fontFamily: "'Press Start 2P', monospace", fontSize: '9px', marginTop: '6px' }}>UDP — {udpPct}%</div>
                </div>
              </div>
            </div>
          </div>

          {/* Tabla */}
          <div style={s.sectionTitle}>
            <span style={{ color: '#e94560' }}>►</span>
            Registros en Base de Datos
            <span style={{ fontSize: '10px', color: '#444' }}>データベース</span>
          </div>
          <div style={s.tableWrap}>
            <div style={s.tableHeader}>
              <span>Supabase DB — スパベース</span>
              <span style={{ color: '#ffe066' }}>↓ más recientes primero</span>
            </div>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '11px' }}>
              <thead>
                <tr>
                  {['ID', 'Protocolo', 'IP Origen', 'Mensaje', 'Fecha y Hora'].map(h => (
                    <th key={h} style={{ padding: '8px 12px', textAlign: 'left', fontFamily: "'Press Start 2P', monospace", fontSize: '7px', color: '#f5a623', borderBottom: '2px solid #0f3460', background: '#1a1a2e' }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {[...datos].reverse().map((reg) => (
                  <tr key={reg.id}>
                    <td style={{ padding: '8px 12px', borderBottom: '1px solid #0f3460', color: '#ccc' }}>{reg.id}</td>
                    <td style={{ padding: '8px 12px', borderBottom: '1px solid #0f3460' }}><span style={tagStyle(reg.protocolo)}>{reg.protocolo}</span></td>
                    <td style={{ padding: '8px 12px', borderBottom: '1px solid #0f3460', color: '#ccc' }}>{reg.agente_ip}</td>
                    <td style={{ padding: '8px 12px', borderBottom: '1px solid #0f3460', color: '#ccc', fontFamily: 'monospace', fontSize: '10px' }}>{reg.mensaje?.length > 40 ? reg.mensaje.slice(0, 40) + '...' : reg.mensaje}</td>
                    <td style={{ padding: '8px 12px', borderBottom: '1px solid #0f3460', color: '#555', fontSize: '10px' }}>{new Date(reg.fecha_hora).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

        </div>
        <div style={{ textAlign: 'center', padding: '16px', fontFamily: "'Press Start 2P', monospace", fontSize: '7px', color: '#333' }}>
          © 1994 <span style={{ color: '#e94560' }}>PROYECTO REDES</span> — FASE 3 COMPLETADA — フェーズ３完了
        </div>
      </div>
    </>
  )
}

export default App