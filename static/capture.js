// static/capture.js - browser-side camera + speech capture (needs HTTPS or localhost; use Chrome)
(function () {
  const W = 320, H = 240;                         // frames are downscaled before upload
  const video = document.getElementById("cam") || document.createElement("video");
  video.autoplay = true; video.muted = true; video.playsInline = true;

  const grab = document.createElement("canvas");
  grab.width = W; grab.height = H;
  const gctx = grab.getContext("2d");

  let transcript = "";
  let camReady = false;

  async function startCamera() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 }, audio: false });
      video.srcObject = stream;
      await video.play();
      camReady = true;
    } catch (e) {
      console.error("Camera error:", e);
    }
  }

  function startSpeech() {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { console.warn("Web Speech API not supported - use Chrome."); return; }
    const rec = new SR();
    let allowed = true;
    rec.continuous = true;
    rec.interimResults = false;
    rec.lang = "en-US";
    rec.onresult = (e) => { transcript = e.results[e.results.length - 1][0].transcript.trim(); };
    rec.onerror = (e) => { if (e.error === "not-allowed" || e.error === "service-not-allowed") allowed = false; };
    rec.onend = () => { if (allowed) { try { rec.start(); } catch (_) {} } };
    try { rec.start(); } catch (_) {}
  }

  // Call this inside your existing fetch('/analyze') body
  function getPayload() {
    let frame = null;
    if (camReady && video.videoWidth) {
      gctx.drawImage(video, 0, 0, W, H);
      frame = grab.toDataURL("image/jpeg", 0.7);
    }
    return { frame: frame, speech: transcript };
  }

  // Optional: draws the face box on <canvas id="overlay"> stacked above the <video id="cam">
  function drawBox(face) {
    const c = document.getElementById("overlay");
    if (!c) return;
    c.width = video.clientWidth || c.width;
    c.height = video.clientHeight || c.height;
    const ctx = c.getContext("2d");
    ctx.clearRect(0, 0, c.width, c.height);
    if (!face || !face.box) return;
    const sx = c.width / W, sy = c.height / H;
    const colors = { happy: "#00ff00", sad: "#ff0000", neutral: "#808080" };
    const color = colors[face.emotion] || "#808080";
    ctx.lineWidth = 2; ctx.strokeStyle = color; ctx.fillStyle = color;
    ctx.strokeRect(face.box.x * sx, face.box.y * sy, face.box.w * sx, face.box.h * sy);
    ctx.font = "16px sans-serif";
    ctx.fillText(face.emotion.charAt(0).toUpperCase() + face.emotion.slice(1), face.box.x * sx, face.box.y * sy - 6);
  }

  window.CloudCapture = { startCamera, startSpeech, getPayload, drawBox };
  document.addEventListener("DOMContentLoaded", () => { startCamera(); startSpeech(); });
})();
