import React from 'react';

/**
 * Functional component that displays real-time high-priority alerts to the user.
 * Built with accessibility features to ensure screen readers announce updates immediately.
 *
 * @component
 * @param {Object} props - The component properties.
 * @param {Array<Object>} props.alerts - Array of alert objects containing a message and ID.
 * @returns {JSX.Element|null} A styled alert banner or null if no alerts exist.
 */
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
