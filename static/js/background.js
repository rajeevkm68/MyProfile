// ===== Canvas setup =====
const canvas = document.getElementById("bg-canvas");
const ctx = canvas.getContext("2d");

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener("resize", resizeCanvas);

// ===== Mouse tracking =====
let mouseX = canvas.width / 2;

window.addEventListener("mousemove", (e) => {
    mouseX = e.clientX;
});

// ===== Physics constants =====
const GRAVITY = 0.35;
const BOUNCE = 0.6;
const AIR_RESISTANCE = 0.98;
const MAX_TILT = 0.5;

// ===== Helpers =====
function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
}

// ===== Single color (CHANGE THIS ONE LINE) =====
const BALL_COLOR = "yellowgreen"; // soft white

// ===== Ball creation =====
const BALL_COUNT = 30;

let balls = Array.from({ length: BALL_COUNT }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height * 0.5,
    r: 6 + Math.random() * 6,
    vx: 0,
    vy: 0
}));

// ===== Animation loop =====
function animate() {
    // Paint background
    ctx.fillStyle = "#0f172a"; // dark slate
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Mouse-based gravity tilt
    const rawTiltX = (mouseX - canvas.width / 2) * 0.0001;
    const tiltX = clamp(rawTiltX, -MAX_TILT, MAX_TILT);

    balls.forEach(b => {
        // Gravity
        b.vy += GRAVITY;

        // Horizontal influence
        b.vx += tiltX;

        // Friction
        b.vx *= AIR_RESISTANCE;

        // Position update
        b.x += b.vx;
        b.y += b.vy;

        // Floor collision
        if (b.y + b.r > canvas.height) {
            b.y = canvas.height - b.r;
            b.vy *= -BOUNCE;
        }

        // Left wall
        if (b.x - b.r < 0) {
            b.x = b.r;
            b.vx *= -BOUNCE;
        }

        // Right wall
        if (b.x + b.r > canvas.width) {
            b.x = canvas.width - b.r;
            b.vx *= -BOUNCE;
        }

        // Draw ball (single color)
        ctx.beginPath();
        ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
        ctx.fillStyle = BALL_COLOR;
        ctx.fill();
    });

    requestAnimationFrame(animate);
}

animate();
