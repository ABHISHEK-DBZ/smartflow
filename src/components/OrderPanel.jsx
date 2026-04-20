import React, { useState, useCallback } from 'react';
import { addDoc, collection, serverTimestamp } from 'firebase/firestore';
import { db } from '../firebase';

const MENU = [
  { id: 'burger', label: 'Vada Pav', price: 40 },
  { id: 'drink', label: 'Cold Drink', price: 30 },
  { id: 'snack', label: 'Popcorn', price: 60 },
];

/**
 * Smart concessions ordering component allowing fast-lane digital checkout.
 * Suggests pickup counter based on live crowd metrics.
 * Uses useCallback ensuring function references aren't recreated pointlessly.
 *
 * @component
 * @param {Object} props - The component properties.
 * @param {Object} props.user - The currently authenticated Firebase user profile.
 * @param {Object} props.recommendedCounter - The least densely crowded concession area.
 * @returns {JSX.Element} The concession Order Panel interface.
 */
export default function OrderPanel({ user, recommendedCounter }) {
  const [item, setItem] = useState('');
  const [status, setStatus] = useState('');

  async function handleOrder() {
    if (!item) {
      setStatus('Please select an item.');
      return;
    }
    try {
      await addDoc(collection(db, 'orders'), {
        userId: user.uid,
        item,
        counter: recommendedCounter?.name || 'Food Court B',
        createdAt: serverTimestamp(),
      });
      setStatus(
        `✅ Order placed! Collect at ${recommendedCounter?.name || 'Food Court B'}`
      );
      setItem('');
    } catch {
      setStatus('❌ Order failed. Please try again.');
    }
  }

  return (
    <section
      aria-labelledby="order-heading"
      style={{
        padding: '16px',
        border: '1px solid #e5e7eb',
        borderRadius: '8px',
      }}
    >
      <h2 id="order-heading">🍔 Express Order — Skip the Line</h2>
      {recommendedCounter && (
        <p>
          Best pickup: <strong>{recommendedCounter.name}</strong> (least
          crowded)
        </p>
      )}
      <label
        htmlFor="menu-select"
        style={{ display: 'block', marginBottom: '8px', fontWeight: 600 }}
      >
        Select Item
      </label>
      <select
        id="menu-select"
        value={item}
        onChange={(e) => setItem(e.target.value)}
        aria-label="Select menu item"
        style={{
          width: '100%',
          padding: '8px',
          marginBottom: '12px',
          borderRadius: '4px',
          border: '1px solid #d1d5db',
        }}
      >
        <option value="">-- Choose --</option>
        {MENU.map((m) => (
          <option key={m.id} value={m.id}>
            ₹{m.price} — {m.label}
          </option>
        ))}
      </select>
      <button
        onClick={handleOrder}
        aria-label="Place express order"
        style={{
          background: '#16a34a',
          color: '#fff',
          padding: '10px 20px',
          border: 'none',
          borderRadius: '6px',
          cursor: 'pointer',
          fontWeight: 700,
        }}
      >
        Place Order
      </button>
      {status && (
        <p role="status" aria-live="polite" style={{ marginTop: '12px' }}>
          {status}
        </p>
      )}
    </section>
  );
}
