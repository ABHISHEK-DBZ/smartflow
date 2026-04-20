import { useEffect, useState } from 'react';
import { collection, onSnapshot } from 'firebase/firestore';
import { db } from '../firebase';

export function useCrowdData() {
  const [zones, setZones] = useState([]);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const unsubZones = onSnapshot(collection(db, 'zones'), (snap) => {
      setZones(snap.docs.map((d) => ({ id: d.id, ...d.data() })));
    });
    const unsubAlerts = onSnapshot(collection(db, 'alerts'), (snap) => {
      setAlerts(
        snap.docs
          .map((d) => ({ id: d.id, ...d.data() }))
          .filter((a) => a.active)
      );
    });
    return () => {
      unsubZones();
      unsubAlerts();
    };
  }, []);

  return { zones, alerts };
}
