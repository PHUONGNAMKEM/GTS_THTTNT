const map = L.map('map').setView([10.776075, 106.694288], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

fetch('/api/locations')
    .then(response => response.json())
    .then(data => {
        const dropdown = document.getElementById('startingPoint');
        data.forEach((location, index) => {
            const option = document.createElement('option');
            option.value = index;
            option.textContent = location.name;
            dropdown.appendChild(option);
        });
    });

document.getElementById('startJourney').addEventListener('click', () => {
    const startIndex = parseInt(document.getElementById('startingPoint').value);
    fetch('/api/journey', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ start_index: startIndex })
    })
    .then(response => response.json())
    .then(path => {
        map.eachLayer(layer => {
            if (layer instanceof L.Marker || layer instanceof L.Polyline) {
                map.removeLayer(layer);
            }
        });

        const coordinates = path.map(location => [location.latitude, location.longitude]);
        L.polyline(coordinates, { color: 'blue' }).addTo(map);

        path.forEach(location => {
            L.marker([location.latitude, location.longitude]).addTo(map)
                .bindPopup(`${location.name}<br>${location.address}`);
        });
    });
});
