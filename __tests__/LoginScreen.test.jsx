import { render, screen } from '@testing-library/react';
import LoginScreen from '../src/components/LoginScreen';

// Mock firebase
jest.mock('../src/firebase', () => ({ auth: {} }));
jest.mock('firebase/auth', () => ({
  signInWithEmailAndPassword: jest.fn(),
  createUserWithEmailAndPassword: jest.fn(),
}));

test('renders login form with email and password fields', () => {
  render(<LoginScreen />);
  expect(screen.getByLabelText(/email address/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
});
