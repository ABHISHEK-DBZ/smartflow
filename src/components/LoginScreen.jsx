import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
} from 'firebase/auth';
import { useState } from 'react';
import { auth } from '../firebase';

export default function LoginScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  async function handleLogin() {
    try {
      await signInWithEmailAndPassword(auth, email, password);
    } catch {
      try {
        await createUserWithEmailAndPassword(auth, email, password);
      } catch (e) {
        setError(e.message);
      }
    }
  }

  return (
    <main
      aria-label="Login screen"
      style={{
        maxWidth: '360px',
        margin: '80px auto',
        padding: '32px',
        border: '1px solid #e5e7eb',
        borderRadius: '12px',
      }}
    >
      <h1 style={{ marginBottom: '24px' }}>🏟️ SmartFlow</h1>
      <label
        htmlFor="email-input"
        style={{ display: 'block', marginBottom: '4px', fontWeight: 600 }}
      >
        Email
      </label>
      <input
        id="email-input"
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        aria-label="Email address"
        placeholder="you@example.com"
        style={{
          width: '100%',
          padding: '8px',
          marginBottom: '16px',
          borderRadius: '4px',
          border: '1px solid #d1d5db',
        }}
      />
      <label
        htmlFor="password-input"
        style={{ display: 'block', marginBottom: '4px', fontWeight: 600 }}
      >
        Password
      </label>
      <input
        id="password-input"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        aria-label="Password"
        placeholder="••••••••"
        style={{
          width: '100%',
          padding: '8px',
          marginBottom: '20px',
          borderRadius: '4px',
          border: '1px solid #d1d5db',
        }}
      />
      {error && (
        <p role="alert" style={{ color: '#dc2626', marginBottom: '12px' }}>
          {error}
        </p>
      )}
      <button
        onClick={handleLogin}
        aria-label="Sign in or register"
        style={{
          width: '100%',
          background: '#1d4ed8',
          color: '#fff',
          padding: '12px',
          border: 'none',
          borderRadius: '6px',
          cursor: 'pointer',
          fontWeight: 700,
          fontSize: '16px',
        }}
      >
        Sign In / Register
      </button>
    </main>
  );
}
