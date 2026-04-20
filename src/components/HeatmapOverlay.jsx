import {
  GoogleMap,
  useJsApiLoader,
  Circle,
  InfoWindow,
} from '@react-google-maps/api';
import { useState } from 'react';
import { getDensityColor } from '../utils/routing';

const MAP_CENTER = { lat: 18.5204, lng: 73.8567 };

export default function HeatmapOverlay({ zones }) {
  const [selected, setSelected] = useState(null);
  const { isLoaded } = useJsApiLoader({
    googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY,
  });

  if (!isLoaded)
    return (
      <div role="status" aria-label="Loading map">
        Loading map…
      </div>
    );

  return (
    <GoogleMap
      mapContainerStyle={{ width: '100%', height: '400px' }}
      center={MAP_CENTER}
      zoom={17}
      aria-label="Stadium crowd density map"
    >
      {zones.map((zone) => (
        <Circle
          key={zone.id}
          center={{ lat: zone.lat, lng: zone.lng }}
          radius={30}
          options={{
            fillColor: getDensityColor(zone.density),
            fillOpacity: 0.6,
            strokeColor: getDensityColor(zone.density),
            strokeWeight: 2,
          }}
          onClick={() => setSelected(zone)}
          aria-label={`${zone.name}: ${zone.density} density`}
        />
      ))}
      {selected && (
        <InfoWindow
          position={{ lat: selected.lat, lng: selected.lng }}
          onCloseClick={() => setSelected(null)}
        >
          <div>
            <strong>{selected.name}</strong>
            <p>
              Density:{' '}
              <span style={{ color: getDensityColor(selected.density) }}>
                {selected.density.toUpperCase()}
              </span>
            </p>
          </div>
        </InfoWindow>
      )}
    </GoogleMap>
  );
}
