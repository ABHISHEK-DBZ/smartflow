import React, { useState } from 'react';
import { db, auth } from '../../firebase';
import { collection, addDoc, serverTimestamp } from 'firebase/firestore';

/**
 * Renders an emergency SOS button for crowd crush or medical emergency scenarios.
 * It instantly pings Firebase with geolocation and alert status.
 *
 * @component
 * @returns {JSX.Element} The rendered SOS action button component.
 */
export default function SOSButton() {
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);

  /**
   * Handles the SOS trigger event, captures user coordinates if available,
   * and sends a high-priority alert to the database.
   */
  const handleSOS = async () => {
    if (!window.confirm("EMERGENCY: Are you sure you want to trigger Stadium Security Protocol?")) return;

    setLoading(true);
    try {
      const payload = {
        userId: auth.currentUser?.uid || 'anonymous',
        timestamp: serverTimestamp(),
        type: 'crowd_crush_or_medical',
        status: 'active'
      };

      if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(async (position) => {
          payload.location = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };
          await addDoc(collection(db, 'emergencies'), payload);
          setSent(true);
          setLoading(false);
        }, async () => {
          await addDoc(collection(db, 'emergencies'), payload);
          setSent(true);
          setLoading(false);
        });
      } else {
        await addDoc(collection(db, 'emergencies'), payload);
        setSent(true);
        setLoading(false);
      }
    } catch (e) {
      console.error("SOS Ping Failed", e);
      setLoading(false);
    }
  };

  return (
    <div className="bg-red-900/40 border border-red-500/50 p-4 rounded-xl flex items-center justify-between mb-6 shadow-red-900/20 shadow-lg">
      <div>
        <h3 className="text-red-400 font-bold text-lg flex items-center gap-2">
          <span aria-hidden="true">🚨</span> Emergency SOS
        </h3>
        <p className="text-red-200/70 text-sm">Trigger immediate security & medical dispatch.</p>
      </div>
      <button 
        onClick={handleSOS}
        disabled={loading || sent}
        aria-label="Trigger Emergency SOS Protocol"
        className={`px-6 py-3 rounded-full font-black tracking-wider transition-all shadow-md ${
          sent ? 'bg-red-500/20 text-red-300 border border-red-500/30' : 'bg-red-600 hover:bg-red-500 text-white hover:scale-105 shadow-red-600/30'
        }`}
      >
        {sent ? 'DISPATCHED' : loading ? 'SENDING...' : 'SOS ACTION'}
      </button>
    </div>
  );
}
