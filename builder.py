import os

base_dir = r'C:\Users\Abhishek\Downloads\lifescan\smartflow\src'
files = {
    'index.css': '''
:root {
  --bg: #0a0e1a;
  --surface: rgba(17, 24, 39, 0.85);
  --surface-solid: #111827;
  --border: rgba(255,255,255,0.08);
  --cyan: #00d4ff;
  --green: #00ff88;
  --amber: #ffb700;
  --red: #ff4757;
  --text: #f1f5f9;
  --text-muted: #64748b;
  --font-display: 'Barlow Condensed', sans-serif;
  --font-body: 'DM Sans', sans-serif;
  --radius: 12px;
  --shadow: 0 8px 32px rgba(0,0,0,0.4);
  --glow-cyan: 0 0 20px rgba(0,212,255,0.3);
  --glow-green: 0 0 20px rgba(0,255,136,0.3);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-body);
  min-height: 100vh;
  overflow-x: hidden;
}

body::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
  z-index: 0;
}

.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: var(--cyan);
  color: #000;
  padding: 8px 16px;
  text-decoration: none;
  font-weight: 700;
  z-index: 9999;
  border-radius: 0 0 8px 0;
}
.skip-link:focus { top: 0; }

.glass {
  background: var(--surface);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--border);
  border-radius: var(--radius);
}

@keyframes pulse-ring {
  0% { transform: scale(1); opacity: 1; }
  100% { transform: scale(2.5); opacity: 0; }
}
@keyframes pulse-dot {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.15); }
}
.pulse-dot {
  position: relative;
  border-radius: 50%;
  animation: pulse-dot 2s ease-in-out infinite;
}
.pulse-dot::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 50%;
  animation: pulse-ring 2s ease-out infinite;
}
.pulse-red { background: var(--red); }
.pulse-red::after { border: 2px solid var(--red); }
.pulse-amber { background: var(--amber); }
.pulse-amber::after { border: 2px solid var(--amber); }
.pulse-green { background: var(--green); }
.pulse-green::after { border: 2px solid var(--green); }

@keyframes slideUp {
  from { transform: translateY(100%); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
.slide-up { animation: slideUp 0.3s cubic-bezier(0.4,0,0.2,1); }

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.stagger-1 { animation: fadeInUp 0.4s ease 0.1s both; }
.stagger-2 { animation: fadeInUp 0.4s ease 0.2s both; }
.stagger-3 { animation: fadeInUp 0.4s ease 0.3s both; }
.stagger-4 { animation: fadeInUp 0.4s ease 0.4s both; }
.stagger-5 { animation: fadeInUp 0.4s ease 0.5s both; }

button:focus-visible, select:focus-visible, input:focus-visible, a:focus-visible {
  outline: 2px solid var(--cyan);
  outline-offset: 3px;
}
''',
    
    'utils/mapStyles.js': '''
export const DARK_MAP_STYLES = [
  { elementType: "geometry", stylers: [{ color: "#0a0e1a" }] },
  { elementType: "labels.text.fill", stylers: [{ color: "#64748b" }] },
  { elementType: "labels.text.stroke", stylers: [{ color: "#0a0e1a" }] },
  { featureType: "road", elementType: "geometry", stylers: [{ color: "#1e293b" }] },
  { featureType: "road", elementType: "geometry.stroke", stylers: [{ color: "#0f172a" }] },
  { featureType: "road.highway", elementType: "geometry", stylers: [{ color: "#1e3a5f" }] },
  { featureType: "water", elementType: "geometry", stylers: [{ color: "#0f172a" }] },
  { featureType: "poi", stylers: [{ visibility: "off" }] },
  { featureType: "transit", stylers: [{ visibility: "off" }] },
];
''',
    
    'utils/routing.js': '''
export const DENSITY_WEIGHT = { low: 1, medium: 2, high: 3 };

export function getBestZone(zones, type) {
  return zones
    .filter((z) => z.type === type)
    .sort((a, b) => DENSITY_WEIGHT[a.density] - DENSITY_WEIGHT[b.density])[0] || null;
}

export function getDensityColor(density) {
  return { low: '#00ff88', medium: '#ffb700', high: '#ff4757' }[density] || '#64748b';
}

export function getDensityClass(density) {
  return { low: 'pulse-green', medium: 'pulse-amber', high: 'pulse-red' }[density] || '';
}

export function haversineDistance(lat1, lng1, lat2, lng2) {
  const R = 6371;
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLng = ((lng2 - lng1) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos((lat1 * Math.PI) / 180) * Math.cos((lat2 * Math.PI) / 180) * Math.sin(dLng / 2) ** 2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

export function getCapacityPercent(density) {
  return { low: 22, medium: 58, high: 89 }[density] || 50;
}
''',
    
    'components/layout/TopBar.jsx': '''
import React, { useState, useEffect } from 'react';
import { auth } from '../../firebase';

export default function TopBar({ user }) {
  const [time, setTime] = useState(new Date());
  const [weather, setWeather] = useState(null);

  useEffect(() => {
    const t = setInterval(() => setTime(new Date()), 1000);
    // Fetch weather (Pune coords)
    fetch(https://api.openweathermap.org/data/2.5/weather?lat=18.5204&lon=73.8567&appid=&units=metric)
      .then(r => r.json())
      .then(d => setWeather({ temp: Math.round(d.main?.temp), desc: d.weather?.[0]?.main }))
      .catch(() => {});
    return () => clearInterval(t);
  }, []);

  return (
    <header role="banner" style={{
      background: 'rgba(10,14,26,0.95)',
      backdropFilter: 'blur(20px)',
      borderBottom: '1px solid rgba(255,255,255,0.06)',
      padding: '12px 20px',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      position: 'sticky',
      top: 0,
      zIndex: 100,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <div style={{
          width: 36, height: 36, borderRadius: '8px',
          background: 'linear-gradient(135deg, #00d4ff, #0066ff)',
          display: 'grid', placeItems: 'center', fontSize: '18px'
        }} aria-hidden="true">🏟️</div>
        <div>
          <div style={{ fontFamily: 'var(--font-display)', fontSize: '20px', fontWeight: 900, letterSpacing: '1px', color: 'var(--cyan)', lineHeight: 1 }}>
            SMARTFLOW
          </div>
          <div style={{ fontSize: '10px', color: 'var(--text-muted)', letterSpacing: '2px' }}>STADIUM COMPANION</div>
        </div>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        {weather && (
          <div aria-label={Weather:  degrees, }
            style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
            🌤 {weather.temp}°C · {weather.desc}
          </div>
        )}
        <div style={{ fontFamily: 'var(--font-display)', fontSize: '18px', fontWeight: 700, color: 'var(--cyan)', letterSpacing: '2px' }}
          aria-label={Current time: }>
          {time.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
        </div>
        <button onClick={() => auth.signOut()} aria-label="Sign out of SmartFlow"
          style={{ background: 'none', border: '1px solid rgba(255,255,255,0.15)', color: 'var(--text-muted)', padding: '6px 12px', borderRadius: '6px', cursor: 'pointer', fontSize: '12px' }}>
          Sign Out
        </button>
      </div>
    </header>
  );
}
''',

    'components/dashboard/ZoneCards.jsx': '''
import React from 'react';
import { getDensityColor, getDensityClass, getCapacityPercent } from '../../utils/routing';

const ICONS = { gate: '🚪', restroom: '🚻', concession: '🍔' };

export default function ZoneCards({ zones }) {
  if (!zones) return null;
  return (
    <section aria-labelledby="zones-heading" style={{ marginBottom: '24px' }}>
      <h2 id="zones-heading" style={{
        fontFamily: 'var(--font-display)', fontSize: '13px', letterSpacing: '3px',
        color: 'var(--text-muted)', marginBottom: '12px', textTransform: 'uppercase'
      }}>Live Zone Status</h2>
      <div role="list" style={{ display: 'flex', gap: '12px', overflowX: 'auto', paddingBottom: '8px', scrollSnapType: 'x mandatory' }}>
        {zones.map((zone, i) => {
          const pct = getCapacityPercent(zone.density);
          const color = getDensityColor(zone.density);
          return (
            <div key={zone.id} role="listitem" className={glass stagger-}
              aria-label={${zone.name}:  density,  minute wait}
              style={{ minWidth: '160px', padding: '16px', scrollSnapAlign: 'start', flexShrink: 0 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                <span style={{ fontSize: '24px' }} aria-hidden="true">{ICONS[zone.type] || '📍'}</span>
                <div className={pulse-dot }
                  style={{ width: 10, height: 10, marginTop: '6px' }} />
              </div>
              <div style={{ fontFamily: 'var(--font-display)', fontSize: '16px', fontWeight: 700, marginBottom: '4px' }}>
                {zone.name}
              </div>
              <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '10px' }}>
                ⏱ {zone.waitMin} min wait
              </div>
              <div style={{ background: 'rgba(255,255,255,0.08)', borderRadius: '4px', height: '4px', overflow: 'hidden' }}>
                <div style={{
                  height: '100%', width: ${pct}%, borderRadius: '4px',
                  background: color,
                  transition: 'width 1s ease',
                  boxShadow:   0 8px ,
                }} aria-label={${pct}% capacity} />
              </div>
              <div style={{ fontSize: '11px', color, marginTop: '4px', textTransform: 'uppercase', fontWeight: 700 }}>
                {zone.density} · {pct}%
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
''',

    'components/map/StadiumMap.jsx': '''
import React, { useState } from 'react';
import { GoogleMap, useJsApiLoader, OverlayView } from '@react-google-maps/api';
import { getDensityColor, getDensityClass } from '../../utils/routing';
import { DARK_MAP_STYLES } from '../../utils/mapStyles';

const CENTER = { lat: 18.5204, lng: 73.8567 };

export default function StadiumMap({ zones }) {
  const [selected, setSelected] = useState(null);
  const { isLoaded } = useJsApiLoader({ googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY });

  if (!isLoaded) return (
    <div role="status" aria-label="Loading stadium map" style={{ height: 320, display: 'grid', placeItems: 'center', background: 'var(--surface-solid)', borderRadius: 'var(--radius)', color: 'var(--text-muted)' }}>
      Loading map…
    </div>
  );

  return (
    <section aria-labelledby="map-heading" className="glass" style={{ overflow: 'hidden', marginBottom: '24px' }}>
      <div style={{ padding: '14px 16px', borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2 id="map-heading" style={{ fontFamily: 'var(--font-display)', fontSize: '13px', letterSpacing: '3px', color: 'var(--text-muted)', textTransform: 'uppercase', margin: 0 }}>
          Live Crowd Map
        </h2>
        <div style={{ display: 'flex', gap: '12px', fontSize: '11px' }}>
          {[['#00ff88','Low'],['#ffb700','Medium'],['#ff4757','High']].map(([c,l]) => (
            <span key={l} style={{ display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--text-muted)' }}>
              <span style={{ width: 8, height: 8, borderRadius: '50%', background: c, display: 'inline-block' }} />
              {l}
            </span>
          ))}
        </div>
      </div>
      <GoogleMap
        mapContainerStyle={{ width: '100%', height: '300px' }}
        center={CENTER} zoom={17}
        options={{ styles: DARK_MAP_STYLES, disableDefaultUI: true, zoomControl: true }}
        aria-label="Interactive stadium crowd density map"
      >
        {zones?.map((zone) => (
          <OverlayView key={zone.id} position={{ lat: zone.lat, lng: zone.lng }} mapPaneName={OverlayView.OVERLAY_MOUSE_TARGET}>
            <button
              onClick={() => setSelected(selected?.id === zone.id ? null : zone)}
              aria-label={${zone.name}:  crowd density,  min wait}
              style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 0, transform: 'translate(-50%, -50%)' }}
            >
              <div className={pulse-dot }
                style={{ width: 20, height: 20, border: 2px solid  }} />
            </button>
          </OverlayView>
        ))}
        {selected && (
          <OverlayView position={{ lat: selected.lat, lng: selected.lng }} mapPaneName={OverlayView.FLOAT_PANE}>
            <div className="glass" style={{ padding: '10px 14px', minWidth: '140px', transform: 'translate(-50%, -130%)', fontSize: '13px' }}>
              <strong style={{ fontFamily: 'var(--font-display)', fontSize: '15px' }}>{selected.name}</strong>
              <p style={{ color: getDensityColor(selected.density), margin: '4px 0 0', fontWeight: 700, textTransform: 'uppercase', fontSize: '11px' }}>
                {selected.density} · {selected.waitMin} min
              </p>
            </div>
          </OverlayView>
        )}
      </GoogleMap>
    </section>
  );
}
''',

    'components/alerts/ToastNotification.jsx': '''
import React, { useState } from 'react';

export default function ToastStack({ alerts }) {
  const [dismissed, setDismissed] = useState(new Set());
  if (!alerts) return null;
  const visible = alerts.filter(a => !dismissed.has(a.id));

  if (!visible.length) return null;

  return (
    <div role="region" aria-label="Live alerts" aria-live="assertive" aria-atomic="false"
      style={{ position: 'fixed', top: 70, right: 16, zIndex: 200, display: 'flex', flexDirection: 'column', gap: '8px', maxWidth: '340px' }}>
      {visible.map((alert) => (
        <div key={alert.id} role="alert" className="glass slide-up"
          style={{ padding: '12px 16px', borderLeft: 3px solid var(--amber), display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '10px' }}>
          <div>
            <div style={{ fontSize: '11px', letterSpacing: '2px', color: 'var(--amber)', fontWeight: 700, marginBottom: '4px' }}>⚠ VENUE ALERT</div>
            <p style={{ fontSize: '13px', color: 'var(--text)', margin: 0 }}>{alert.message}</p>
          </div>
          <button onClick={() => setDismissed(d => new Set([...d, alert.id]))}
            aria-label="Dismiss alert"
            style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: '18px', lineHeight: 1, padding: 0 }}>
            ×
          </button>
        </div>
      ))}
    </div>
  );
}
''',

    'components/order/MenuDrawer.jsx': '''
import React, { useState } from 'react';
import { addDoc, collection, serverTimestamp } from 'firebase/firestore';
import { db } from '../../firebase';

const MENU = [
  { id: 'vadapav', emoji: '🌮', label: 'Vada Pav', price: 40, time: 3 },
  { id: 'samosa', emoji: '🥟', label: 'Samosa (2pc)', price: 30, time: 2 },
  { id: 'popcorn', emoji: '🍿', label: 'Popcorn (Lg)', price: 60, time: 1 },
  { id: 'coke', emoji: '🥤', label: 'Cold Drink', price: 35, time: 1 },
  { id: 'chai', emoji: '☕', label: 'Cutting Chai', price: 20, time: 4 },
  { id: 'icecream', emoji: '🍦', label: 'Ice Cream', price: 50, time: 2 },
];

export default function MenuDrawer({ user, recommendedCounter, onOrderPlaced }) {
  const [open, setOpen] = useState(false);
  const [cart, setCart] = useState({});
  const [status, setStatus] = useState('');
  const [ordering, setOrdering] = useState(false);

  const totalItems = Object.values(cart).reduce((a, b) => a + b, 0);
  const totalPrice = MENU.reduce((acc, m) => acc + (cart[m.id] || 0) * m.price, 0);

  function addItem(id) { setCart(c => ({ ...c, [id]: (c[id] || 0) + 1 })); }
  function removeItem(id) { setCart(c => { const n = { ...c }; if (n[id] > 1) n[id]--; else delete n[id]; return n; }); }

  async function placeOrder() {
    if (!totalItems) { setStatus('Add items to your cart first.'); return; }
    setOrdering(true);
    try {
      await addDoc(collection(db, 'orders'), {
        userId: user.uid,
        items: cart,
        total: totalPrice,
        counter: recommendedCounter?.name || 'Food Court B',
        createdAt: serverTimestamp(),
      });
      setStatus(✅ Order placed! Collect at  (~ min));
      setCart({});
      onOrderPlaced?.();
    } catch { setStatus('❌ Failed. Try again.'); }
    finally { setOrdering(false); }
  }

  return (
    <>
      <button onClick={() => setOpen(true)} aria-label={Open food order menu.  items in cart}
        style={{
          position: 'fixed', bottom: 24, right: 24, zIndex: 150,
          background: 'linear-gradient(135deg, #00d4ff, #0066ff)',
          border: 'none', borderRadius: '50px', padding: '14px 22px',
          color: '#000', fontFamily: 'var(--font-display)', fontWeight: 900,
          fontSize: '15px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px',
          boxShadow: '0 4px 24px rgba(0,212,255,0.4)',
        }}>
        🍔 ORDER FOOD
        {totalItems > 0 && (
          <span aria-label={${totalItems} items} style={{
            background: '#ff4757', color: '#fff', borderRadius: '50%',
            width: 22, height: 22, display: 'grid', placeItems: 'center', fontSize: '12px', fontWeight: 900,
          }}>{totalItems}</span>
        )}
      </button>

      {open && (
        <div role="dialog" aria-modal="true" aria-label="Food order menu"
          style={{ position: 'fixed', inset: 0, zIndex: 300, display: 'flex', flexDirection: 'column', background: 'var(--bg)' }}>
          <div style={{ padding: '16px 20px', borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '22px', fontWeight: 900, letterSpacing: '1px' }}>
              🍔 EXPRESS ORDER
            </h2>
            <button onClick={() => setOpen(false)} aria-label="Close menu"
              style={{ background: 'none', border: '1px solid var(--border)', color: 'var(--text)', padding: '6px 14px', borderRadius: '6px', cursor: 'pointer' }}>
              Close
            </button>
          </div>

          {recommendedCounter && (
            <div style={{ padding: '10px 20px', background: 'rgba(0,255,136,0.08)', borderBottom: '1px solid rgba(0,255,136,0.15)', fontSize: '13px', color: 'var(--green)' }}>
              📍 Pickup at <strong>{recommendedCounter.name}</strong> — {recommendedCounter.waitMin} min wait (least crowded)
            </div>
          )}

          <div style={{ flex: 1, overflowY: 'auto', padding: '16px 20px', display: 'grid', gap: '10px' }}>
            {MENU.map((item) => (
              <div key={item.id} className="glass" style={{ padding: '14px 16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                  <span style={{ fontSize: '28px' }} aria-hidden="true">{item.emoji}</span>
                  <div>
                    <div style={{ fontWeight: 600 }}>{item.label}</div>
                    <div style={{ color: 'var(--text-muted)', fontSize: '12px' }}>₹{item.price} · ~{item.time} min</div>
                  </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  {cart[item.id] > 0 && (
                    <>
                      <button onClick={() => removeItem(item.id)} aria-label={Remove one }
                        style={{ width: 30, height: 30, borderRadius: '50%', border: '1px solid var(--border)', background: 'none', color: 'var(--text)', cursor: 'pointer', fontSize: '18px' }}>−</button>
                      <span style={{ minWidth: '20px', textAlign: 'center', fontWeight: 700 }}>{cart[item.id]}</span>
                    </>
                  )}
                  <button onClick={() => addItem(item.id)} aria-label={Add  to cart}
                    style={{ width: 30, height: 30, borderRadius: '50%', background: 'var(--cyan)', border: 'none', color: '#000', cursor: 'pointer', fontSize: '18px', fontWeight: 900 }}>+</button>
                </div>
              </div>
            ))}
          </div>

          <div style={{ padding: '16px 20px', borderTop: '1px solid var(--border)', background: 'var(--surface-solid)' }}>
            {status && <p role="status" aria-live="polite" style={{ marginBottom: '10px', fontSize: '14px', color: status.startsWith('✅') ? 'var(--green)' : 'var(--red)' }}>{status}</p>}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
              <span style={{ color: 'var(--text-muted)' }}>{totalItems} items</span>
              <span style={{ fontFamily: 'var(--font-display)', fontSize: '24px', fontWeight: 900, color: 'var(--cyan)' }}>₹{totalPrice}</span>
            </div>
            <button onClick={placeOrder} disabled={ordering || !totalItems}
              aria-label={Place order for ₹}
              style={{
                width: '100%', padding: '14px', background: totalItems ? 'linear-gradient(135deg, #00ff88, #00d4ff)' : 'rgba(255,255,255,0.1)',
                border: 'none', borderRadius: '10px', color: totalItems ? '#000' : 'var(--text-muted)',
                fontFamily: 'var(--font-display)', fontSize: '18px', fontWeight: 900, cursor: totalItems ? 'pointer' : 'not-allowed',
                letterSpacing: '1px',
              }}>
              {ordering ? 'PLACING ORDER…' : 'PLACE ORDER →'}
            </button>
          </div>
        </div>
      )}
    </>
  );
}
''',

    'components/finder/SeatFinder.jsx': '''
import React, { useState } from 'react';
import { getBestZone } from '../../utils/routing';

const SECTIONS = ['A', 'B', 'C', 'D', 'E', 'F'];
const GATE_MAP = { A: 'Gate A', B: 'Gate A', C: 'Gate B', D: 'Gate B', E: 'Gate C', F: 'Gate C' };

export default function SeatFinder({ zones }) {
  const [section, setSection] = useState('');
  const [row, setRow] = useState('');
  const [seat, setSeat] = useState('');
  const [result, setResult] = useState(null);

  function findSeat() {
    if (!section || !zones) return;
    const recommendedGate = GATE_MAP[section];
    const gateZone = zones.find(z => z.name === recommendedGate);
    const bestGate = getBestZone(zones, 'gate');
    setResult({ recommendedGate, gateZone, bestGate, section, row, seat });
  }

  return (
    <section aria-labelledby="seat-heading" className="glass stagger-4" style={{ padding: '20px', marginBottom: '24px' }}>
      <h2 id="seat-heading" style={{ fontFamily: 'var(--font-display)', fontSize: '13px', letterSpacing: '3px', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '16px' }}>
        🎫 Find Your Seat
      </h2>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '10px', marginBottom: '12px' }}>
        <div>
          <label htmlFor="section-select" style={{ fontSize: '11px', color: 'var(--text-muted)', display: 'block', marginBottom: '4px', letterSpacing: '1px' }}>SECTION</label>
          <select id="section-select" value={section} onChange={e => { setSection(e.target.value); setResult(null); }}
            aria-label="Select seating section"
            style={{ width: '100%', padding: '10px', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border)', borderRadius: '8px', color: 'var(--text)', fontSize: '14px' }}>
            <option value="">--</option>
            {SECTIONS.map(s => <option key={s} value={s}>{s}</option>)}
          </select>
        </div>
        <div>
          <label htmlFor="row-input" style={{ fontSize: '11px', color: 'var(--text-muted)', display: 'block', marginBottom: '4px', letterSpacing: '1px' }}>ROW</label>
          <input id="row-input" type="number" min="1" max="30" value={row} onChange={e => setRow(e.target.value)}
            aria-label="Row number" placeholder="e.g. 12"
            style={{ width: '100%', padding: '10px', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border)', borderRadius: '8px', color: 'var(--text)', fontSize: '14px' }} />
        </div>
        <div>
          <label htmlFor="seat-input" style={{ fontSize: '11px', color: 'var(--text-muted)', display: 'block', marginBottom: '4px', letterSpacing: '1px' }}>SEAT</label>
          <input id="seat-input" type="number" min="1" max="50" value={seat} onChange={e => setSeat(e.target.value)}
            aria-label="Seat number" placeholder="e.g. 7"
            style={{ width: '100%', padding: '10px', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border)', borderRadius: '8px', color: 'var(--text)', fontSize: '14px' }} />
        </div>
      </div>
      <button onClick={findSeat} aria-label="Find route to my seat"
        style={{ width: '100%', padding: '11px', background: 'rgba(0,212,255,0.15)', border: '1px solid var(--cyan)', borderRadius: '8px', color: 'var(--cyan)', fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: '14px', letterSpacing: '1px', cursor: 'pointer' }}>
        FIND MY SEAT →
      </button>

      {result && (
        <div role="region" aria-label="Seat finder result" aria-live="polite"
          style={{ marginTop: '14px', padding: '14px', background: 'rgba(0,255,136,0.06)', borderRadius: '8px', border: '1px solid rgba(0,255,136,0.2)' }}>
          <p style={{ color: 'var(--green)', fontWeight: 700, marginBottom: '6px' }}>
            📍 Section {result.section}{result.row ? , Row  : ''}{result.seat ? , Seat  : ''}
          </p>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
            Your gate: <strong style={{ color: 'var(--text)' }}>{result.recommendedGate}</strong>
            {result.gateZone &&  —  min wait}
          </p>
          {result.bestGate?.name !== result.recommendedGate && (
            <p style={{ fontSize: '12px', color: 'var(--amber)', marginTop: '6px' }}>
              ⚡ Tip: {result.bestGate?.name} is less crowded right now ({result.bestGate?.waitMin} min)
            </p>
          )}
        </div>
      )}
    </section>
  );
}
''',

    'components/dashboard/FanScore.jsx': '''
import React, { useEffect, useState } from 'react';

export default function FanScore({ orders }) {
  const [score, setScore] = useState(0);
  const target = 50 + orders * 25;

  useEffect(() => {
    let current = 0;
    const step = target / 40;
    const timer = setInterval(() => {
      current = Math.min(current + step, target);
      setScore(Math.round(current));
      if (current >= target) clearInterval(timer);
    }, 30);
    return () => clearInterval(timer);
  }, [target]);

  const pct = Math.min((score / 200) * 100, 100);

  return (
    <div className="glass stagger-5" aria-label={Fan score:  out of 200}
      style={{ padding: '16px 20px', display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '24px' }}>
      <div style={{ fontSize: '32px' }} aria-hidden="true">⭐</div>
      <div style={{ flex: 1 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
          <span style={{ fontFamily: 'var(--font-display)', fontSize: '13px', letterSpacing: '2px', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Fan Score</span>
          <span style={{ fontFamily: 'var(--font-display)', fontSize: '20px', fontWeight: 900, color: 'var(--cyan)' }}>{score}</span>
        </div>
        <div style={{ background: 'rgba(255,255,255,0.08)', borderRadius: '4px', height: '6px', overflow: 'hidden' }}>
          <div style={{ height: '100%', width: ${pct}%, background: 'linear-gradient(90deg, var(--cyan), var(--green))', borderRadius: '4px', transition: 'width 0.5s ease', boxShadow: 'var(--glow-cyan)' }} />
        </div>
        <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>Order food & explore zones to earn more</div>
      </div>
    </div>
  );
}
''',

    'components/auth/LoginScreen.jsx': '''
import React, { useState } from 'react';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../../firebase';

export default function LoginScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleAuth() {
    setLoading(true); setError('');
    try {
      await signInWithEmailAndPassword(auth, email, password);
    } catch {
      try { await createUserWithEmailAndPassword(auth, email, password); }
      catch (e) { setError(e.message.replace('Firebase: ', '')); }
    } finally { setLoading(false); }
  }

  return (
    <main aria-label="SmartFlow login" style={{ minHeight: '100vh', display: 'grid', placeItems: 'center', padding: '20px', position: 'relative' }}>
      <div aria-hidden="true" style={{ position: 'fixed', top: '20%', left: '50%', transform: 'translateX(-50%)', width: 400, height: 400, background: 'radial-gradient(circle, rgba(0,212,255,0.12) 0%, transparent 70%)', pointerEvents: 'none' }} />

      <div className="glass" style={{ width: '100%', maxWidth: '380px', padding: '40px 32px' }}>
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <div style={{ fontSize: '48px', marginBottom: '12px' }} aria-hidden="true">🏟️</div>
          <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '36px', fontWeight: 900, letterSpacing: '3px', color: 'var(--cyan)', margin: 0 }}>SMARTFLOW</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '13px', letterSpacing: '2px', marginTop: '4px' }}>STADIUM COMPANION</p>
        </div>

        {[['email-input','email','Email','you@example.com',email,setEmail],['pass-input','password','Password','••••••••',password,setPassword]].map(([id,type,label,ph,val,set]) => (
          <div key={id} style={{ marginBottom: '16px' }}>
            <label htmlFor={id} style={{ display: 'block', fontSize: '11px', letterSpacing: '2px', color: 'var(--text-muted)', marginBottom: '6px', textTransform: 'uppercase' }}>{label}</label>
            <input id={id} type={type} value={val} onChange={e => set(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleAuth()}
              aria-label={label} placeholder={ph}
              style={{ width: '100%', padding: '12px 14px', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border)', borderRadius: '8px', color: 'var(--text)', fontSize: '14px' }} />
          </div>
        ))}

        {error && <p role="alert" style={{ color: 'var(--red)', fontSize: '13px', marginBottom: '12px' }}>{error}</p>}

        <button onClick={handleAuth} disabled={loading} aria-label="Sign in or create account"
          style={{ width: '100%', padding: '14px', background: 'linear-gradient(135deg, #00d4ff, #0066ff)', border: 'none', borderRadius: '10px', color: '#000', fontFamily: 'var(--font-display)', fontSize: '18px', fontWeight: 900, letterSpacing: '2px', cursor: 'pointer', marginTop: '4px' }}>
          {loading ? 'SIGNING IN…' : 'ENTER STADIUM →'}
        </button>
        <p style={{ fontSize: '11px', color: 'var(--text-muted)', textAlign: 'center', marginTop: '16px' }}>New user? An account will be created automatically.</p>
      </div>
    </main>
  );
}
''',

    'App.jsx': '''
import React, { useEffect, useState } from 'react';
import { onAuthStateChanged } from 'firebase/auth';
import { auth } from './firebase';
import { useCrowdData } from './hooks/useCrowdData';
import { getBestZone } from './utils/routing';
import TopBar from './components/layout/TopBar';
import ZoneCards from './components/dashboard/ZoneCards';
import StadiumMap from './components/map/StadiumMap';
import ToastStack from './components/alerts/ToastNotification';
import MenuDrawer from './components/order/MenuDrawer';
import SeatFinder from './components/finder/SeatFinder';
import FanScore from './components/dashboard/FanScore';
import LoginScreen from './components/auth/LoginScreen';

export default function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [orderCount, setOrderCount] = useState(0);
  const { zones, alerts } = useCrowdData();

  useEffect(() => {
    return onAuthStateChanged(auth, (u) => { setUser(u); setLoading(false); });
  }, []);

  if (loading) return (
    <div role="status" aria-label="Loading SmartFlow" style={{ minHeight: '100vh', display: 'grid', placeItems: 'center', fontFamily: 'var(--font-display)', fontSize: '20px', color: 'var(--cyan)', letterSpacing: '4px' }}>
      LOADING…
    </div>
  );

  if (!user) return <LoginScreen />;

  const bestGate = getBestZone(zones || [], 'gate');
  const bestConcession = getBestZone(zones || [], 'concession');

  return (
    <>
      <a href="#main-content" className="skip-link">Skip to main content</a>
      <TopBar user={user} />
      <ToastStack alerts={alerts} />

      <main id="main-content" style={{ maxWidth: '768px', margin: '0 auto', padding: '20px 16px 100px' }}>

        {bestGate && (
          <div className="glass stagger-1" role="region" aria-label="Gate recommendation"
            style={{ padding: '14px 18px', marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderLeft: '3px solid var(--green)' }}>
            <div>
              <div style={{ fontSize: '11px', letterSpacing: '2px', color: 'var(--green)', fontWeight: 700 }}>RECOMMENDED ENTRY</div>
              <div style={{ fontFamily: 'var(--font-display)', fontSize: '20px', fontWeight: 900 }}>{bestGate.name} — {bestGate.waitMin} min wait</div>
            </div>
            <div style={{ fontFamily: 'var(--font-display)', fontSize: '36px', fontWeight: 900, color: 'var(--green)' }}>{bestGate.waitMin}m</div>
          </div>
        )}

        <div className="stagger-2"><ZoneCards zones={zones} /></div>
        <div className="stagger-3"><StadiumMap zones={zones} /></div>
        <SeatFinder zones={zones} />
        <FanScore orders={orderCount} />
      </main>

      <MenuDrawer user={user} recommendedCounter={bestConcession} onOrderPlaced={() => setOrderCount(c => c + 1)} />
    </>
  );
}
'''
}

for rel_path, content in files.items():
    full_path = os.path.join(base_dir, rel_path.replace('/', os.sep))
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Successfully wrote {len(files)} files to {base_dir}")
