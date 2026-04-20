import { getBestZone, getDensityColor, haversineDistance } from '../src/utils/routing';

const mockZones = [
  { id: '1', type: 'gate', density: 'high', name: 'Gate A' },
  { id: '2', type: 'gate', density: 'low', name: 'Gate B' },
  { id: '3', type: 'concession', density: 'medium', name: 'Food Court' },
];

test('getBestZone returns lowest density zone of given type', () => {
  const best = getBestZone(mockZones, 'gate');
  expect(best.name).toBe('Gate B');
});

test('getDensityColor returns correct colors', () => {
  expect(getDensityColor('low')).toBe('#22c55e');
  expect(getDensityColor('high')).toBe('#ef4444');
});

test('haversineDistance returns a positive number', () => {
  const dist = haversineDistance(18.5204, 73.8567, 18.5214, 73.8577);
  expect(dist).toBeGreaterThan(0);
});
