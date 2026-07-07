import assert from "node:assert/strict";
import { countFingers, compute, reduce, initialState, isValidPose, OPERATORS } from "./calc.mjs";

let passed = 0;
function test(name, fn) {
  fn();
  passed++;
  console.log("  ✓ " + name);
}

// --- helpers to build fake landmarks -------------------------------------
// 21 landmarks. y grows downward. A finger is "up" when tip.y < pip.y.
// Thumb uses x: Right hand up when tip.x > ip.x; Left hand up when tip.x < ip.x.
function makeHand({ fingersUp = 0, thumbUp = false, handedness = "Right" } = {}) {
  const lm = Array.from({ length: 21 }, () => ({ x: 0.5, y: 0.5, z: 0 }));
  // four fingers: [tip, pip]
  const fingers = [[8, 6], [12, 10], [16, 14], [20, 18]];
  fingers.forEach(([tip, pip], i) => {
    const up = i < fingersUp;
    lm[pip].y = 0.5;
    lm[tip].y = up ? 0.2 : 0.8; // up => tip above pip
  });
  // thumb: index 4 tip, 3 ip
  lm[3].x = 0.5;
  if (handedness === "Right") {
    lm[4].x = thumbUp ? 0.7 : 0.3;
  } else {
    lm[4].x = thumbUp ? 0.3 : 0.7;
  }
  return lm;
}

console.log("countFingers:");
test("0 fingers", () => assert.equal(countFingers(makeHand({ fingersUp: 0, thumbUp: false }), "Right"), 0));
test("2 fingers no thumb", () => assert.equal(countFingers(makeHand({ fingersUp: 2, thumbUp: false }), "Right"), 2));
test("4 fingers + thumb (Right) = 5", () => assert.equal(countFingers(makeHand({ fingersUp: 4, thumbUp: true }), "Right"), 5));
test("thumb only (Right)", () => assert.equal(countFingers(makeHand({ fingersUp: 0, thumbUp: true }), "Right"), 1));
test("thumb only (Left) mirrors x", () => assert.equal(countFingers(makeHand({ fingersUp: 0, thumbUp: true, handedness: "Left" }), "Left"), 1));
test("Left hand: wrong thumb x does not count", () => assert.equal(countFingers(makeHand({ fingersUp: 3, thumbUp: false, handedness: "Left" }), "Left"), 3));

console.log("compute:");
test("addition", () => assert.equal(compute(2, 3, "+"), 5));
test("subtraction", () => assert.equal(compute(2, 5, "−"), -3));
test("multiplication", () => assert.equal(compute(3, 4, "×"), 12));
test("division rounds to 2dp", () => assert.equal(compute(10, 3, "÷"), 3.33));
test("division by zero => ∞", () => assert.equal(compute(4, 0, "÷"), "∞"));
test("unknown operator => ?", () => assert.equal(compute(1, 1, "?"), "?"));

console.log("operator mapping (1=− 2=+ 3=× 4=÷):");
test("1 => −", () => assert.equal(OPERATORS[1], "−"));
test("2 => +", () => assert.equal(OPERATORS[2], "+"));
test("3 => ×", () => assert.equal(OPERATORS[3], "×"));
test("4 => ÷", () => assert.equal(OPERATORS[4], "÷"));

console.log("isValidPose:");
test("op step rejects 0", () => assert.equal(isValidPose("op", 0), false));
test("op step rejects 5", () => assert.equal(isValidPose("op", 5), false));
test("op step accepts 2", () => assert.equal(isValidPose("op", 2), true));
test("num1 accepts 0", () => assert.equal(isValidPose("num1", 0), true));
test("null pose is invalid", () => assert.equal(isValidPose("num1", null), false));

console.log("reduce (full flow 3 + 2 = 5):");
test("full sequence", () => {
  let s = initialState();
  assert.equal(s.state, "num1");
  s = reduce(s, 3);
  assert.deepEqual([s.state, s.num1], ["op", 3]);
  s = reduce(s, 2); // 2 => +
  assert.deepEqual([s.state, s.operator], ["num2", "+"]);
  s = reduce(s, 2);
  assert.deepEqual([s.state, s.num2], ["result", 2]);
  s = reduce(s, 1); // any pose reveals result
  assert.deepEqual([s.state, s.result], ["done", 5]);
});

test("reduce is pure (does not mutate input)", () => {
  const s = initialState();
  reduce(s, 4);
  assert.equal(s.state, "num1"); // original unchanged
});

test("op step with invalid gesture stays in op", () => {
  let s = reduce(initialState(), 5); // num1 = 5 -> op
  const before = s.state;
  s = reduce(s, 9); // no operator maps to 9
  assert.equal(before, "op");
  assert.equal(s.state, "op");
  assert.equal(s.operator, "");
});

console.log(`\nAll ${passed} tests passed ✅`);
