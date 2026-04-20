import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import App from '../src/App';
import * as useCrowdDataHook from '../src/hooks/useCrowdData';

// Mock the CSS module import and other dependencies
jest.mock('../src/firebase', () => ({
  auth: {
    signOut: jest.fn(),
  },
}));

jest.mock('../src/components/HeatmapOverlay', () => () => <div data-testid="heatmap-mock" />);
jest.mock('../src/components/dashboard/SmartAssistant', () => () => <div data-testid="smart-assistant-mock" />)

jest.mock('firebase/auth', () => ({
  onAuthStateChanged: (auth, callback) => {
    callback({ uid: 'mockuser', email: 'test@example.com' });
    return jest.fn(); // Unsubscribe mock
  },
}));

// Mock hook returning fake crowd data to avoid real fetches during tests
jest.spyOn(useCrowdDataHook, 'useCrowdData').mockReturnValue({
  zones: [
    { id: 'z1', name: 'Gate A', type: 'gate', density: 'low' },
    { id: 'z2', name: 'Concession 1', type: 'concession', density: 'medium' }
  ],
  alerts: []
});

describe('App Root Component', () => {
  it('renders the main app component successfully when authenticated', async () => {
    render(<App />);

    // Fast Forward through the 'Loading...' suspense boundary using waitFor
    await waitFor(() => {
      expect(screen.getByRole('main')).toBeInTheDocument();
    });

    // Assert that basic headers and UI are present
    expect(screen.getByText(/SmartFlow/i)).toBeInTheDocument();
    expect(screen.getByText(/Live Crowd Density Map/i)).toBeInTheDocument();
    
    // Assert that the Google Service Gemini Drop-In renders
    expect(screen.getByTestId('smart-assistant-mock')).toBeInTheDocument();
  });
});
