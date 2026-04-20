/**
 * Represents the crowd density weights used for routing decisions.
 * @constant
 * @type {Object<string, number>}
 */
export const DENSITY_WEIGHT = { low: 1, medium: 2, high: 3 };

/**
 * Finds the optimal zone based on the lowest crowd density.
 *
 * @param {Array<Object>} zones - List of zones in the stadium.
 * @param {string} type - The type of zone (e.g., 'gate', 'concession').
 * @returns {Object|null} The best zone object or null if none found.
 */
export function getBestZone(zones, type) {
  return (
    zones
      .filter((z) => z.type === type)
      .sort(
        (a, b) => DENSITY_WEIGHT[a.density] - DENSITY_WEIGHT[b.density]
      )[0] || null
  );
}

/**
 * Retrieves the hexadecimal color associated with a crowd density level.
 *
 * @param {string} density - The current density status.
 * @returns {string} The hex color code representing the status.
 */
export function getDensityColor(density) {
  const colors = { low: '#22c55e', medium: '#f59e0b', high: '#ef4444' };
  return colors[density] || '#6b7280';
}

/**
 * Calculates the great-circle distance between two points on the Earth.
 *
 * @param {number} lat1 - Latitude of point 1.
 * @param {number} lng1 - Longitude of point 1.
 * @param {number} lat2 - Latitude of point 2.
 * @param {number} lng2 - Longitude of point 2.
 * @returns {number} Distance in kilometers.
 */
export function haversineDistance(lat1, lng1, lat2, lng2) {
  const R = 6371;
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLng = ((lng2 - lng1) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLng / 2) ** 2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}
