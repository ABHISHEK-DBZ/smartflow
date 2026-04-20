export const DENSITY_WEIGHT = { low: 1, medium: 2, high: 3 };

export function getBestZone(zones, type) {
  return (
    zones
      .filter((z) => z.type === type)
      .sort(
        (a, b) => DENSITY_WEIGHT[a.density] - DENSITY_WEIGHT[b.density]
      )[0] || null
  );
}

export function getDensityColor(density) {
  const colors = { low: '#22c55e', medium: '#f59e0b', high: '#ef4444' };
  return colors[density] || '#6b7280';
}

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
