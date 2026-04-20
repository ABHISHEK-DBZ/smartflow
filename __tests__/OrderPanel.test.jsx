import { render, screen } from '@testing-library/react';
import OrderPanel from '../src/components/OrderPanel';

jest.mock('../src/firebase', () => ({ db: {} }));
jest.mock('firebase/firestore', () => ({ addDoc: jest.fn(), collection: jest.fn(), serverTimestamp: jest.fn() }));

const mockUser = { uid: 'test-uid-123' };

test('renders order panel with heading and menu select', () => {
  render(<OrderPanel user={mockUser} recommendedCounter={{ name: 'Food Court B' }} />);
  expect(screen.getByRole('heading', { name: /express order/i })).toBeInTheDocument();
  expect(screen.getByLabelText(/select menu item/i)).toBeInTheDocument();
});
