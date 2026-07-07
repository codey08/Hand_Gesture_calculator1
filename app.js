import {
  HandLandmarker,
  FilesetResolver,
} from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/vision_bundle.mjs";
import { countFingers, reduce, initialState, isValidPose } from "./calc.mjs";

// ---------- DOM ----------
const video = document.getElementById("video");
const overlay = document.getElementById("overlay");
const ctx = overlay.getContext("2d");
const loader = document.getElementById("loader");
const loaderText = document.getElementById("loaderText");
const startScreen = document.getElementById("startScreen");
const startBtn = document.getElementById("startBtn");
const startError = document.getElementById("startError");
const stopBtn = document.getElementById("stopBtn");
const resetBtn = document.getElementById("resetBtn");
const countdownEl = document.getElementById("countdown");
const ring = document.getElementById("ring");
const fingerCountEl = document.getElementById("fingerCount");

const stateBadge = document.getElementById("stateBadge");
const num1El = document.getElementById("num1");
const opEl = document.getElementById("op");
const num2El = document.getElementById("num2");
const resultEl = document.getElementById("result");
const slots = {
  num1: document.querySelector('[data-slot="num1"]'),
  op: document.querySelector('[data-slot="op"]'),
  num2: document.querySelector('[data-slot="num2"]'),
};

const RING_LEN = 327; // 2 * PI * 52

// ---------- State machine ----------
const STATES = {
  num1: "Show fingers for the first number",
  op: "Choose an operator (1=− 2=+ 3=× 4=÷)",
  num2: "Show fingers for the second number",
  result: "Hold to reveal the result",
  done: "Done! Press Reset to start again",
};

let calc = initialState(); // { state, num1, num2, operator, result }

const HOLD_MS = 2000; // hold a steady pose this long to commit
let holdValue = null; // the finger-count currently being held
let holdStart = 0;

let handLandmarker = null;
let running = false;
let rafId = null;
let lastVideoTime = -1;

// ---------- Landmark connections for drawing ----------
const CONNECTIONS = [
  [0, 1], [1, 2], [2, 3], [3, 4],
  [0, 5], [5, 6], [6, 7], [7, 8],
  [5, 9], [9, 10], [10, 11], [11, 12],
  [9, 13], [13, 14], [14, 15], [15, 16],
  [13, 17], [17, 18], [18, 19], [19, 20],
  [0, 17],
];

// ---------- Model load ----------
const MODEL_URL =
  "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task";

async function createLandmarker(vision, delegate) {
  return HandLandmarker.createFromOptions(vision, {
    baseOptions: { modelAssetPath: MODEL_URL, delegate },
    runningMode: "VIDEO",
    numHands: 2,
    minHandDetectionConfidence: 0.6,
    minTrackingConfidence: 0.5,
  });
}

async function init() {
  try {
    const vision = await FilesetResolver.forVisionTasks(
      "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/wasm"
    );
    try {
      handLandmarker = await createLandmarker(vision, "GPU");
    } catch (gpuErr) {
      console.warn("GPU delegate unavailable, falling back to CPU.", gpuErr);
      handLandmarker = await createLandmarker(vision, "CPU");
    }
    loader.hidden = true;
    startScreen.hidden = false;
  } catch (err) {
    loaderText.textContent = "Failed to load hand-tracking model. Check your connection and refresh.";
    console.error(err);
  }
}

// ---------- Camera ----------
async function startCamera() {
  startError.textContent = "";
  if (!navigator.mediaDevices?.getUserMedia) {
    startError.textContent = "This browser does not support camera access.";
    return;
  }
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "user", width: { ideal: 960 }, height: { ideal: 720 } },
      audio: false,
    });
    video.srcObject = stream;
    await video.play();
    overlay.width = video.videoWidth;
    overlay.height = video.videoHeight;
    startScreen.hidden = true;
    countdownEl.hidden = false;
    running = true;
    stopBtn.disabled = false;
    resetState();
    loop();
  } catch (err) {
    if (err.name === "NotAllowedError") {
      startError.textContent = "Camera permission denied. Allow access and try again.";
    } else if (err.name === "NotFoundError") {
      startError.textContent = "No camera found on this device.";
    } else {
      startError.textContent = "Could not start the camera: " + err.message;
    }
    console.error(err);
  }
}

function stopCamera() {
  running = false;
  if (rafId) cancelAnimationFrame(rafId);
  const stream = video.srcObject;
  if (stream) stream.getTracks().forEach((t) => t.stop());
  video.srcObject = null;
  ctx.clearRect(0, 0, overlay.width, overlay.height);
  countdownEl.hidden = true;
  startScreen.hidden = false;
  stopBtn.disabled = true;
}

// ---------- Main loop ----------
function loop() {
  if (!running) return;
  rafId = requestAnimationFrame(loop);

  if (video.readyState < 2 || video.currentTime === lastVideoTime) return;
  lastVideoTime = video.currentTime;

  const results = handLandmarker.detectForVideo(video, performance.now());
  ctx.clearRect(0, 0, overlay.width, overlay.height);

  let totalFingers = 0;
  let handsSeen = 0;

  if (results.landmarks && results.landmarks.length) {
    for (let i = 0; i < results.landmarks.length; i++) {
      const lm = results.landmarks[i];
      const handedness = results.handedness?.[i]?.[0]?.categoryName ?? "Right";
      drawHand(lm);
      totalFingers += countFingers(lm, handedness);
      handsSeen++;
    }
  }

  fingerCountEl.textContent = handsSeen ? totalFingers : "–";
  updateStateMachine(handsSeen ? totalFingers : null);
}

// ---------- Drawing ----------
function drawHand(lm) {
  const w = overlay.width;
  const h = overlay.height;
  ctx.lineWidth = 3;
  ctx.strokeStyle = "rgba(110, 168, 254, 0.85)";
  for (const [a, b] of CONNECTIONS) {
    ctx.beginPath();
    ctx.moveTo(lm[a].x * w, lm[a].y * h);
    ctx.lineTo(lm[b].x * w, lm[b].y * h);
    ctx.stroke();
  }
  for (const p of lm) {
    ctx.beginPath();
    ctx.arc(p.x * w, p.y * h, 4, 0, Math.PI * 2);
    ctx.fillStyle = "#8b7cff";
    ctx.fill();
  }
}

// ---------- State machine ----------
function updateStateMachine(fingers) {
  if (calc.state === "done") {
    setRing(0);
    return;
  }

  // No stable / valid pose -> reset the hold timer.
  if (!isValidPose(calc.state, fingers)) {
    holdValue = null;
    setRing(0);
    return;
  }

  const now = performance.now();
  if (fingers !== holdValue) {
    holdValue = fingers;
    holdStart = now;
  }

  const elapsed = now - holdStart;
  setRing(Math.min(elapsed / HOLD_MS, 1));

  if (elapsed >= HOLD_MS) {
    calc = reduce(calc, fingers);
    render();
    holdValue = null;
    holdStart = now;
    setRing(0);
  }
}

// ---------- Rendering ----------
function setRing(fraction) {
  ring.style.strokeDashoffset = String(RING_LEN * (1 - fraction));
}

function render() {
  const { state, num1, num2, operator, result } = calc;
  stateBadge.textContent = STATES[state];

  num1El.textContent = num1 === null ? "–" : num1;
  opEl.textContent = operator || "–";
  num2El.textContent = num2 === null ? "–" : num2;
  resultEl.textContent = result === null ? "?" : result;

  // active + filled styling
  slots.num1.classList.toggle("filled", num1 !== null);
  slots.op.classList.toggle("filled", !!operator);
  slots.num2.classList.toggle("filled", num2 !== null);

  const activeSlot = state === "op" ? "op" : state === "num2" ? "num2" : state === "num1" ? "num1" : null;
  for (const key of Object.keys(slots)) {
    slots[key].classList.toggle("active", key === activeSlot);
  }

  if (result !== null) {
    resultEl.classList.remove("show");
    void resultEl.offsetWidth; // restart animation
    resultEl.classList.add("show");
  }
}

function resetState() {
  calc = initialState();
  holdValue = null;
  setRing(0);
  render();
}

// ---------- Events ----------
startBtn.addEventListener("click", startCamera);
stopBtn.addEventListener("click", stopCamera);
resetBtn.addEventListener("click", resetState);

resetState();
init();
