import random
import threading
import time
import turtle

# --- Fixed Winsound Audio Engine ---
try:
    import winsound

    HAS_SOUND = True
except ImportError:
    HAS_SOUND = False

# Happy Birthday Frequencies
NOTES = {
    "C4": 262,
    "D4": 294,
    "E4": 330,
    "F4": 349,
    "G4": 392,
    "A4": 440,
    "A#4": 466,
    "B4": 494,
    "C5": 523,
    "D5": 587,
    "E5": 659,
    "F5": 698,
}

# (Note, Note Length in Milliseconds)
MELODY = [
    ("C4", 250),
    ("C4", 250),
    ("D4", 500),
    ("C4", 500),
    ("F4", 500),
    ("E4", 1000),
    ("C4", 250),
    ("C4", 250),
    ("D4", 500),
    ("C4", 500),
    ("G4", 500),
    ("F4", 1000),
    ("C4", 250),
    ("C4", 250),
    ("C5", 500),
    ("A4", 500),
    ("F4", 500),
    ("E4", 500),
    ("D4", 500),
    ("A#4", 250),
    ("A#4", 250),
    ("A4", 500),
    ("F4", 500),
    ("G4", 500),
    ("F4", 1000),
]


def audio_thread_worker():
    """Loops the music track in a separate thread to completely prevent animation lag."""
    if not HAS_SOUND:
        return
    while True:
        for note, duration in MELODY:
            # Play note frequency for the specified duration
            winsound.Beep(NOTES[note], duration)
            # Short break between notes so they sound clean
            time.sleep(0.05)
        time.sleep(2.0)  # Pause before repeating the song


# Launch audio thread safely right away
if HAS_SOUND:
    audio_thread = threading.Thread(target=audio_thread_worker, daemon=True)
    audio_thread.start()

# --- Screen & Canvas Setup ---
screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.bgcolor("#080816")
screen.title("Fixed & Smooth Winsound Birthday App")
screen.tracer(0)  # Handles high performance frame refreshes manually

particles = []

static_drawer = turtle.Turtle()
static_drawer.hideturtle()
static_drawer.speed(0)


def draw_rectangle(t, color, x, y, width, height):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)
    t.begin_fill()
    for _ in range(2):
        t.forward(width)
        t.left(90)
        t.forward(height)
        t.left(90)
    t.end_fill()


def draw_scene():
    # Base Cake Design
    draw_rectangle(static_drawer, "#e03e52", -150, -200, 300, 80)
    draw_rectangle(static_drawer, "#ff6b4a", -100, -120, 200, 70)
    draw_rectangle(static_drawer, "#f7cb45", -60, -50, 120, 60)

    # Candles
    for x in [-40, 0, 40]:
        draw_rectangle(static_drawer, "#ffffff", x - 4, 10, 8, 30)

    # Information Display text
    static_drawer.penup()
    static_drawer.color("#ffffff")
    static_drawer.goto(0, 220)
    static_drawer.write(
        "🎂 Happy Birthday 🎂",
        align="center",
        font=("Arial", 22, "bold"),
    )
    static_drawer.goto(0, -260)
    static_drawer.color("#00ffcc")
    static_drawer.write(
        "Happy Birthday to Anyone celebrating today!",
        align="center",
        font=("Courier New", 18, "bold"),
    )


# --- Candle Flame Flickering ---
flame_drawer = turtle.Turtle()
flame_drawer.hideturtle()
flame_drawer.speed(0)


def draw_flames():
    flame_drawer.clear()
    for x in [-40, 0, 40]:
        flame_drawer.penup()
        flame_drawer.goto(x, 43)
        flame_drawer.pendown()
        size = random.uniform(6, 11)
        flame_drawer.color("#ff9233", "#ffd31d")
        flame_drawer.begin_fill()
        flame_drawer.circle(size)
        flame_drawer.end_fill()


# --- Firework System ---
class Spark:

    def __init__(self, x, y, color):
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.penup()
        self.t.goto(x, y)
        self.t.shape("circle")
        self.t.shapesize(random.uniform(0.2, 0.45))
        self.t.color(color)
        self.t.setheading(random.randint(0, 360))
        self.speed = random.uniform(4, 9)
        self.life = random.randint(20, 35)

    def move(self):
        self.t.forward(self.speed)
        self.speed *= 0.94  # Simulates deceleration in the sky
        self.life -= 1
        if self.life <= 0:
            self.t.clear()
            return False
        return True


def burst(x, y):
    colors = [
        "#ff0055",
        "#00ffcc",
        "#ffcc00",
        "#ff6600",
        "#9933ff",
        "#33ccff",
        "#ff00aa",
    ]
    c = random.choice(colors)
    for _ in range(30):
        particles.append(Spark(x, y, c))


def user_click(x, y):
    if y > -80:
        burst(x, y)


# Initialize and render background
draw_scene()
screen.listen()
screen.onclick(user_click)


# --- Core Smooth Loop ---
def app_loop():
    # 1. Randomly auto-trigger a fireworks burst in the sky
    if random.random() < 0.04:
        auto_x = random.randint(-300, 300)
        auto_y = random.randint(60, 180)
        burst(auto_x, auto_y)

    # 2. Keep the candle flames flickering smoothly
    draw_flames()

    # 3. Step forward the animations for active particles
    for p in particles[:]:
        alive = p.move()
        if not alive:
            particles.remove(p)

    # 4. Refresh screen and queue next frame (runs cleanly at ~40 FPS)
    screen.update()
    screen.ontimer(app_loop, 25)


# Start display loop
app_loop()
screen.mainloop()
