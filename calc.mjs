// Pure, DOM-free logic for the hand-gesture calculator.
// Kept separate from app.js so it can be unit-tested in Node.

// Count raised fingers from 21 MediaPipe hand landmarks.
// Four fingers: tip above its PIP joint (smaller y) => extended.
// Thumb: horizontal check, direction flipped by handedness.
export function countFingers(lm, handedness) {
  let count = 0;
  const fingers = [
    [8, 6],
    [12, 10],
    [16, 14],
    [20, 18],
  ];
  for (const [tip, pip] of fingers) {
    if (lm[tip].y < lm[pip].y) count++;
  }
  const thumbTip = lm[4];
  const thumbIp = lm[3];
  if (handedness === "Right") {
    if (thumbTip.x > thumbIp.x) count++;
  } else {
    if (thumbTip.x < thumbIp.x) count++;
  }
  return count;
}

export const OPERATORS = { 1: "−", 2: "+", 3: "×", 4: "÷" };

export function compute(a, b, op) {
  switch (op) {
    case "+": return a + b;
    case "−": return a - b;
    case "×": return a * b;
    case "÷": return b === 0 ? "∞" : Math.round((a / b) * 100) / 100;
    default: return "?";
  }
}

// Advance the calculator given a committed finger count.
// `s` is { state, num1, num2, operator, result }; returns a new state object.
export function reduce(s, fingers) {
  const next = { ...s };
  switch (s.state) {
    case "num1":
      next.num1 = fingers;
      next.state = "op";
      break;
    case "op": {
      const operator = OPERATORS[fingers] || "";
      if (operator) {
        next.operator = operator;
        next.state = "num2";
      }
      break;
    }
    case "num2":
      next.num2 = fingers;
      next.state = "result";
      break;
    case "result":
      next.result = compute(s.num1, s.num2, s.operator);
      next.state = "done";
      break;
  }
  return next;
}

export function initialState() {
  return { state: "num1", num1: null, num2: null, operator: "", result: null };
}

// Whether a given finger count is a valid pose to commit in the current state.
export function isValidPose(state, fingers) {
  if (fingers === null) return false;
  if (state === "op") return fingers >= 1 && fingers <= 4;
  return true;
}
