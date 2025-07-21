// 비동기 JS (fetch로 최신 온습도 데이터 가져오기)
setInterval(() => {
  fetch('/api/sensor/latest')
    .then(res => res.json())
    .then(data => {
      document.getElementById('temp').innerText = data.temperature;
      document.getElementById('humid').innerText = data.humidity;
      document.getElementById('status').innerText = data.status;
    });
}, 6000);
