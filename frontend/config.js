// 后端地址。如果后端不在本机 8000 端口，改这里即可。
// 也支持通过 URL 参数覆盖：  index.html?api=http://192.168.1.10:8000
window.API_BASE = (function () {
  const p = new URLSearchParams(location.search).get("api");
  if (p) return p.replace(/\/$/, "");
  // 若本页面就是被后端 /ui 托管的，则用同源
  if (location.pathname.startsWith("/ui")) return location.origin;
  // 否则（前端单独起静态服务器，方式 B）：用「当前访问页面的主机名」+ 8000 端口。
  // 这样局域网里别人用 http://192.168.x.x:8080/ 打开时，会自动连到同一台机器的 :8000，
  // 而不是连到访问者自己的 127.0.0.1。file:// 直接打开时退回本机 8000。
  if (location.hostname) return location.protocol + "//" + location.hostname + ":8000";
  return "http://127.0.0.1:8000";
})();
