import React from 'react';
import { render, screen } from '@testing-library/react';
import SOSButton from '../src/components/dashboard/SOSButton';

// Mock firebase
jest.mock('../src/firebase', () => ({
    db: {},
    auth: { currentUser: { uid: '123' } }
}));

jest.mock('firebase/firestore', () => ({
    collection: jest.fn(),
    addDoc: jest.fn(),
    serverTimestamp: jest.fn()
}));

describe('SOSButton', () => {
    it('renders the SOS action area', () => {
        render(<SOSButton />);
        expect(screen.getByRole('heading', { name: /Emergency SOS/i })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /Trigger Emergency SOS Protocol/i })).toBeInTheDocument();
    });
});
