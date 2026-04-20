import React, { useEffect, useState } from 'react';
import { onAuthStateChanged } from 'firebase/auth';
import { auth } from './firebase';
import { useCrowdData } from './hooks/useCrowdData';
import { getBestZone } from './utils/routing';
import HeatmapOverlay from './components/HeatmapOverlay';
import AlertBanner from './components/AlertBanner';
import OrderPanel from './components/OrderPanel';
import LoginScreen from './components/LoginScreen';
import SOSButton from './components/dashboard/SOSButton';

export default function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const { zones, alerts } = useCrowdData();

  useEffect(() => {
    return onAuthStateChanged(auth, (u) => {
      setUser(u);
      setLoading(false);
    });
  }, []);

  if (loading)
    return (
      <div role="status" aria-label="Loading application">
        Loading…
      </div>
    );
  if (!user) return <LoginScreen />;

  const bestGate = getBestZone(zones, 'gate');
  const bestConcession = getBestZone(zones, 'concession');

  return (
    <main
      style={{
        maxWidth: '768px',
        margin: '0 auto',
        padding: '16px',
        fontFamily: 'Georgia, serif',
      }}
    >
      <header
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '16px',
        }}
      >
        <h1 style={{ margin: 0 }}>🏟️ SmartFlow</h1>
        <button
          onClick={() => auth.signOut()}
          aria-label="Sign out"
          style={{
            background: 'none',
            border: '1px solid #d1d5db',
            padding: '6px 12px',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Sign Out
        </button>
      </header>

      <div style={{ marginBottom: '16px' }}>
        <SOSButton />
      </div>

      <AlertBanner alerts={alerts} />

      {bestGate && (
        <div
          role="region"
          aria-label="Gate recommendation"
          style={{
            background: '#dcfce7',
            padding: '12px',
            borderRadius: '8px',
            marginBottom: '16px',
          }}
        >
          ✅ <strong>Recommended Gate:</strong> {bestGate.name} (least crowded
          right now)
        </div>
      )}

      <section aria-labelledby="map-heading">
        <h2 id="map-heading">Live Crowd Density Map</h2>
        <HeatmapOverlay zones={zones} />
        <p style={{ fontSize: '13px', color: '#6b7280' }}>
          🟢 Low &nbsp; 🟡 Medium &nbsp; 🔴 High
        </p>
      </section>

      <hr style={{ margin: '24px 0' }} />

      <OrderPanel user={user} recommendedCounter={bestConcession} />
    </main>
  );
}
