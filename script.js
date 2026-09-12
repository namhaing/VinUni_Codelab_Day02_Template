const recommendationList = document.querySelector('.recommendation-list');

const zones = [
  { name: 'Zone B2-C', occupancy: 0.48, walk: '2 min walk', confidence: 89 },
  { name: 'Zone B2-A', occupancy: 0.52, walk: '3 min walk', confidence: 85 },
  { name: 'Zone B3-D', occupancy: 0.61, walk: '5 min walk', confidence: 81 }
];

if (recommendationList) {
  recommendationList.innerHTML = zones
    .map(
      (zone) => `
        <li>
          <div>
            <strong>${zone.name}</strong>
            <small>${zone.walk} • ${zone.occupancy.toFixed(2)} occupancy</small>
          </div>
          <span>${zone.confidence}%</span>
        </li>
      `
    )
    .join('');
}

const pulse = document.querySelector('.status-dot');
if (pulse) {
  let visible = true;
  setInterval(() => {
    visible = !visible;
    pulse.style.opacity = visible ? '1' : '0.35';
  }, 800);
}
