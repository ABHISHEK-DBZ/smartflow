import { calculateCrowdDensity, formatWaitTime } from '../src/utils/densityUtils.js';

describe('Utility: densityUtils', () => {
    describe('calculateCrowdDensity', () => {
        it('should return Unknown if capacity is 0 or negative', () => {
            expect(calculateCrowdDensity(100, 0)).toBe('Unknown');
            expect(calculateCrowdDensity(50, -10)).toBe('Unknown');
        });

        it('should return Dangerous when at or above 85% capacity', () => {
            expect(calculateCrowdDensity(85, 100)).toBe('Dangerous');
            expect(calculateCrowdDensity(90, 100)).toBe('Dangerous');
            expect(calculateCrowdDensity(100, 100)).toBe('Dangerous');
            expect(calculateCrowdDensity(200, 100)).toBe('Dangerous');
        });

        it('should return Moderate when at or above 60% capacity but below 85%', () => {
            expect(calculateCrowdDensity(60, 100)).toBe('Moderate');
            expect(calculateCrowdDensity(70, 100)).toBe('Moderate');
            expect(calculateCrowdDensity(84, 100)).toBe('Moderate');
        });

        it('should return Safe when below 60% capacity', () => {
            expect(calculateCrowdDensity(0, 100)).toBe('Safe');
            expect(calculateCrowdDensity(30, 100)).toBe('Safe');
            expect(calculateCrowdDensity(59, 100)).toBe('Safe');
        });
    });

    describe('formatWaitTime', () => {
        it('should return format for ready state', () => {
            expect(formatWaitTime(0)).toBe('Ready');
            expect(formatWaitTime(-5)).toBe('Ready');
        });

        it('should return format for singleton', () => {
            expect(formatWaitTime(1)).toBe('1 min');
        });

        it('should handle multiples mins', () => {
            expect(formatWaitTime(5)).toBe('5 mins');
        });
    });
});
