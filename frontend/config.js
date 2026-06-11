// 后端地址。如果后端不在本机 8000 端口，改这里即可。
// 也支持通过 URL 参数覆盖：  index.html?api=http://192.168.1.10:8000
window.API_BASE = (function () {
  const p = new URLSearchParams(location.search).get("api");
  if (p) return p.replace(/\/$/, "");
  // 若本页面就是被后端 /ui 托管的，则用同源；否则默认本机 8000
  if (location.pathname.startsWith("/ui")) return location.origin;
  return "http://127.0.0.1:8000";
})();
