import React from 'react';

export default function AlertBanner({ alerts }) {
  if (!alerts.length) return null;
  return (
    <div
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
      style={{
        background: '#fef08a',
        borderLeft: '4px solid #f59e0b',
        padding: '12px 16px',
        marginBottom: '16px',
        borderRadius: '4px',
      }}
    >
      {alerts.map((a) => (
        <p key={a.id} style={{ margin: 0, fontWeight: 600 }}>
          📢 {a.message}
        </p>
      ))}
    </div>
  );
}
