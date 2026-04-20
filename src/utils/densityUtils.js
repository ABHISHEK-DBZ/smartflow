/**
 * Calculates crowd density level.
 * @param {number} count The number of people in an area.
 * @param {number} capacity The maximum capacity of the area.
 * @returns {string} The risk level: "Safe", "Moderate", "Dangerous".
 */
export const calculateCrowdDensity = (count, capacity) => {
    if (capacity <= 0) return "Unknown";
    const ratio = count / capacity;
    if (ratio >= 0.85) return "Dangerous";
    if (ratio >= 0.6) return "Moderate";
    return "Safe";
};

/**
 * Formats a given time remaining in minutes format.
 * @param {number} minutes wait time in minutes.
 * @returns {string} Human readable formatted time remaining.
 */
export const formatWaitTime = (minutes) => {
    if (minutes <= 0) return "Ready";
    if (minutes === 1) return "1 min";
    return `${minutes} mins`;
};
