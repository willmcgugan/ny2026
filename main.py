#!/usr/bin/env python3
"""
Fireworks simulation using Braille canvas.
"""

import math
import random
import time
import os
import sys
from datetime import datetime, timezone
from typing import List, Tuple
from braille_canvas import BrailleCanvas

# Cross-platform keyboard input handling
if sys.platform == "win32":
    import msvcrt
else:
    import select
    import termios
    import tty


# Digit segments as pixel patterns for braille canvas
# Classic 7-segment display style
# Each digit is represented as a grid of pixels (1 = on, 0 = off)
DIGIT_PATTERNS = {
    "0": [
        "███████████",
        "███████████",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "███████████",
        "███████████",
    ],
    "1": [
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
    ],
    "2": [
        "███████████",
        "███████████",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "███████████",
        "███████████",
        "██         ",
        "██         ",
        "██         ",
        "██         ",
        "██         ",
        "██         ",
        "██         ",
        "██         ",
        "███████████",
        "███████████",
    ],
    "3": [
        "███████████",
        "███████████",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "███████████",
        "███████████",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "███████████",
        "███████████",
    ],
    "4": [
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "███████████",
        "███████████",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
    ],
    "5": [
        "███████████",
        "███████████",
        "██         ",
        "██         ",
        "██         ",
        "██         ",
        "██         ",
        "██         ",
        "██         ",
        "██         ",
        "███████████",
        "███████████",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "███████████",
        "███████████",
    ],
    "6": [
        "███████████",
        "███████████",
        "██         ",
        "██         ",
        "██         ",
        "██         ",
        "██         ",
        "██         ",
        "██         ",
        "██         ",
        "███████████",
        "███████████",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "███████████",
        "███████████",
    ],
    "7": [
        "███████████",
        "███████████",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
    ],
    "8": [
        "███████████",
        "███████████",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "███████████",
        "███████████",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "███████████",
        "███████████",
    ],
    "9": [
        "███████████",
        "███████████",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "██       ██",
        "███████████",
        "███████████",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "         ██",
        "███████████",
        "███████████",
    ],
    ":": [
        "    ",
        "    ",
        "    ",
        "    ",
        "    ",
        " ██ ",
        " ██ ",
        "    ",
        "    ",
        "    ",
        "    ",
        "    ",
        "    ",
        " ██ ",
        " ██ ",
        "    ",
        "    ",
        "    ",
        "    ",
        "    ",
        "    ",
        "    ",
    ],
}


def get_countdown_to_newyear_2026() -> Tuple[str, bool]:
    """
    Calculate time remaining until New Year's Day 2026 (2026-01-01 00:00:00 UTC).

    Returns:
        Tuple of (countdown string in format "HH:MM:SS", midnight_reached bool)
    """
    # New Year's Day 2026 UTC
    target = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)

    # Calculate difference
    diff = target - now

    # If we've passed the target, show 00:00:00
    if diff.total_seconds() <= 0:
        return "2026", True

    # Calculate hours, minutes, seconds
    total_seconds = int(diff.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}", False


def render_countdown_on_canvas(canvas: BrailleCanvas, text: str, color: str):
    """
    Render countdown text on the braille canvas at the center.

    Args:
        canvas: BrailleCanvas to render to
        text: String to render (e.g., "12:34:56")
        color: Color to use for the digits
    """
    # Calculate total width needed
    total_width = 0
    char_widths = []
    for char in text:
        if char in DIGIT_PATTERNS:
            pattern = DIGIT_PATTERNS[char]
            width = len(pattern[0]) if pattern else 0
            char_widths.append(width)
            total_width += width + 3  # 3 pixels spacing between digits
        else:
            # For characters not in patterns, append 0 width to keep lists aligned
            char_widths.append(0)

    if total_width == 0:
        return

    # Calculate starting position to center the text
    digit_height = 22
    start_x = (canvas.width - total_width) // 2
    start_y = (canvas.height - digit_height) // 2

    # Render each character
    current_x = start_x
    for char, width in zip(text, char_widths):
        if char in DIGIT_PATTERNS:
            pattern = DIGIT_PATTERNS[char]
            points = []

            # Convert pattern to pixel coordinates
            for y, line in enumerate(pattern):
                for x, pixel in enumerate(line):
                    if pixel != " ":
                        px = current_x + x
                        py = start_y + y
                        if 0 <= px < canvas.width and 0 <= py < canvas.height:
                            points.append((px, py))

            # Plot all pixels for this digit
            if points:
                canvas.plot(color, points)

            # Move to next character position
            current_x += width + 3


class Particle:
    """A 3D particle with position, velocity, and lifetime."""

    def __init__(
        self,
        x: float,
        y: float,
        z: float,
        vx: float,
        vy: float,
        vz: float,
        color: str,
        lifetime: float,
    ):
        """
        Initialize a particle.

        Args:
            x, y, z: Initial 3D position
            vx, vy, vz: Initial 3D velocity
            color: RGB color string
            lifetime: Time in seconds before particle disappears
        """
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.color = color
        self.lifetime = lifetime
        self.age = 0.0

    def update(self, dt: float, gravity: float = 20.0, air_resistance: float = 0.95):
        """
        Update particle position and age.

        Args:
            dt: Time delta in seconds
            gravity: Gravity acceleration (pixels/s^2)
            air_resistance: Air resistance factor (0-1, closer to 1 = less resistance)
        """
        # Apply gravity to vertical velocity
        self.vy += gravity * dt

        # Apply air resistance (damping) to all velocities
        # This causes particles to slow down over time
        # Use per-frame damping for more noticeable effect
        self.vx *= air_resistance
        self.vy *= air_resistance
        self.vz *= air_resistance

        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt

        # Update age
        self.age += dt

    def is_alive(self) -> bool:
        """Check if particle is still alive."""
        return self.age < self.lifetime

    def get_2d_position(
        self,
        camera_distance: float = 200.0,
        center_x: float = 0.0,
        center_y: float = 0.0,
    ) -> Tuple[int, int]:
        """
        Get 2D screen position with perspective projection.

        Args:
            camera_distance: Distance of camera from z=0 plane
            center_x: X coordinate of screen center (camera looks at this point)
            center_y: Y coordinate of screen center (camera looks at this point)

        Returns:
            (x, y) screen coordinates
        """
        # Perspective projection: closer objects (negative z) appear larger
        # Objects at z=0 are at the "screen" plane
        # Objects with positive z are behind the screen (appear smaller)
        z_offset = self.z + camera_distance

        if z_offset <= 0:
            # Particle is behind camera, don't render
            return (-1, -1)

        # Apply perspective scaling relative to screen center
        scale = camera_distance / z_offset

        # Project relative to center, then add center back
        screen_x = center_x + (self.x - center_x) * scale
        screen_y = center_y + (self.y - center_y) * scale

        return (int(screen_x), int(screen_y))


class Firework:
    """A firework that launches, arcs, and explodes."""

    def __init__(self, canvas_width: int, canvas_height: int, camera_z: float = 0.0):
        """
        Initialize a firework.

        Args:
            canvas_width: Width of the canvas in pixels
            canvas_height: Height of the canvas in pixels
            camera_z: Current Z position of the camera
        """
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        # Random neon color
        self.color = self._random_neon_color()

        # Launch from bottom of screen, always ahead of the camera
        self.x = random.uniform(canvas_width * 0.2, canvas_width * 0.8)
        self.y = canvas_height - 1
        # Spawn at camera position plus some forward distance
        self.z = camera_z + random.uniform(50.0, 300.0)

        # Calculate target explosion height (top quarter to top half of screen)
        self.target_y = random.uniform(canvas_height * 0.15, canvas_height * 0.4)

        # Launch velocity (upward with slight horizontal drift)
        self.vx = random.uniform(-20, 20)
        self.vy = random.uniform(-150, -120) * 1.3  # Strong upward velocity
        self.vz = 0.0

        # Explosion parameters
        self.exploded = False
        self.particles: List[Particle] = []
        self.apex_reached = False
        self.time_since_apex = 0.0

        # Trail particle for launch phase
        self.launch_trail: List[Tuple[float, float]] = []

    def _random_neon_color(self) -> str:
        """Generate a random neon color."""
        neon_colors = [
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Cyan
            (255, 255, 0),  # Yellow
            (255, 0, 128),  # Hot pink
            (0, 255, 128),  # Spring green
            (255, 128, 0),  # Orange
            (128, 0, 255),  # Purple
            (255, 0, 0),  # Red
            (0, 255, 0),  # Green
            (0, 128, 255),  # Light blue
        ]
        r, g, b = random.choice(neon_colors)
        return BrailleCanvas.rgb_color(r, g, b)

    def update(self, dt: float):
        """
        Update firework state.

        Args:
            dt: Time delta in seconds
        """
        if not self.exploded:
            # Update launch phase
            gravity = 100.0
            self.vy += gravity * dt
            self.x += self.vx * dt
            self.y += self.vy * dt

            # Store trail position
            self.launch_trail.append((self.x, self.y))
            if len(self.launch_trail) > 15:
                self.launch_trail.pop(0)

            # Check if firework has reached apex (velocity becomes positive/downward)
            if self.vy > 0 and not self.apex_reached:
                self.apex_reached = True

            # If apex reached, wait about 1 second before exploding
            if self.apex_reached:
                self.time_since_apex += dt
                if self.time_since_apex >= 1.0:
                    self.explode()
        else:
            # Update explosion particles with reduced gravity for better spread
            for particle in self.particles:
                particle.update(dt, gravity=10.0, air_resistance=0.97)

            # Remove dead particles
            self.particles = [p for p in self.particles if p.is_alive()]

    def explode(self):
        """Create explosion particles."""
        self.exploded = True

        # Generate particles in all directions with higher speed for more dramatic effect
        num_particles = random.randint(450, 750)
        speed = random.uniform(140, 210)

        for i in range(num_particles):
            # Random direction on a sphere
            theta = random.uniform(0, 2 * math.pi)  # Azimuthal angle
            phi = random.uniform(0, math.pi)  # Polar angle

            # Convert to Cartesian coordinates
            vx = speed * math.sin(phi) * math.cos(theta)
            vy = speed * math.cos(phi)
            vz = speed * math.sin(phi) * math.sin(theta)

            # Random lifetime with some variation (around 2-3 seconds)
            base_lifetime = random.uniform(1.8, 2.5)
            lifetime_variation = random.uniform(-0.2, 0.2)
            lifetime = base_lifetime + lifetime_variation

            particle = Particle(
                self.x, self.y, self.z, vx, vy, vz, self.color, lifetime
            )
            self.particles.append(particle)

    def render(self, canvas: BrailleCanvas, camera_z: float = 0.0):
        """
        Render firework to canvas.

        Args:
            canvas: BrailleCanvas to render to
            camera_z: Z position of the camera
        """
        if not self.exploded:
            # Render launch trail with perspective
            if self.launch_trail:
                points = []
                canvas_w = canvas.width
                canvas_h = canvas.height
                center_x = canvas_w / 2.0
                center_y = canvas_h / 2.0
                camera_distance = 200.0

                for x, y in self.launch_trail:
                    # Apply perspective projection to trail points
                    z_relative = self.z - camera_z
                    z_offset = z_relative + camera_distance

                    if z_offset > 0:
                        scale = camera_distance / z_offset
                        screen_x = center_x + (x - center_x) * scale
                        screen_y = center_y + (y - center_y) * scale

                        if 0 <= screen_x < canvas_w and 0 <= screen_y < canvas_h:
                            points.append((int(screen_x), int(screen_y)))

                if points:
                    canvas.plot(self.color, points)
        else:
            # Render explosion particles with perspective - batch processing
            # Pre-allocate list with estimated size for better performance
            points = []
            canvas_w = canvas.width
            canvas_h = canvas.height
            center_x = canvas_w / 2.0
            center_y = canvas_h / 2.0
            camera_distance = 200.0

            for particle in self.particles:
                # Adjust particle Z position relative to camera
                z_relative = particle.z - camera_z
                z_offset = z_relative + camera_distance

                if z_offset <= 0:
                    # Particle is behind camera, don't render
                    continue

                # Apply perspective scaling
                scale = camera_distance / z_offset
                screen_x = center_x + (particle.x - center_x) * scale
                screen_y = center_y + (particle.y - center_y) * scale

                x, y = int(screen_x), int(screen_y)
                if 0 <= x < canvas_w and 0 <= y < canvas_h:
                    points.append((x, y))

            if points:
                canvas.plot(self.color, points)

    def is_finished(self) -> bool:
        """Check if firework is finished (exploded and all particles dead)."""
        return self.exploded and len(self.particles) == 0


def is_key_pressed() -> str:
    """
    Check if a key has been pressed (non-blocking).

    Returns:
        The key character if pressed, empty string otherwise
    """
    if sys.platform == "win32":
        # Windows implementation using msvcrt
        if msvcrt.kbhit():
            key = msvcrt.getch()
            # Convert bytes to string
            try:
                return key.decode("utf-8")
            except:
                return ""
        return ""
    else:
        # Unix implementation using select
        if select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.read(1)
        return ""


def fireworks():
    """Main fireworks simulation loop."""
    # Get terminal size
    try:
        columns, rows = os.get_terminal_size()
    except OSError:
        columns, rows = 80, 24

    # Canvas dimensions (pixels)
    # Each braille character represents 2x4 pixels
    # We need to leave one row for the cursor and ensure exact fit
    # Use (columns - 1) to account for BrailleCanvas's ceiling division: (width + 1) // 2
    canvas_width = (columns - 1) * 2
    canvas_height = (rows - 1) * 4  # Subtract 1 row to prevent wrapping

    # Create canvas
    canvas = BrailleCanvas(canvas_width, canvas_height, default_color=0)

    # Fireworks list
    fireworks: List[Firework] = []

    # Camera animation
    camera_z = 0.0
    camera_speed = 15.0  # Camera moves forward at 15 pixels/second through Z space

    # Timing
    target_fps = 60
    frame_time = 1.0 / target_fps
    last_spawn_time = 0.0
    spawn_interval = random.uniform(
        0.5, 1.5
    )  # Spawn new firework every 0.5-1.5 seconds

    # Midnight tracking
    midnight_reached = False

    # Enter alternate screen mode, hide cursor
    print("\033[?1049h\033[?25l\033[2J", end="", flush=True)

    # Save terminal settings (Unix only)
    old_settings = None
    if sys.platform != "win32":
        old_settings = termios.tcgetattr(sys.stdin)

    try:
        # Set terminal to raw mode for non-blocking input (Unix only)
        if sys.platform != "win32":
            tty.setraw(sys.stdin.fileno())

        start_time = time.time()
        last_frame_time = start_time

        while True:
            current_time = time.time()
            dt = current_time - last_frame_time

            # Limit frame rate
            if dt < frame_time:
                time.sleep(frame_time - dt)
                current_time = time.time()
                dt = current_time - last_frame_time

            last_frame_time = current_time
            elapsed = current_time - start_time

            # Check for space key press
            key = is_key_pressed()
            if key == " ":
                # Launch a single firework on space press
                fireworks.append(Firework(canvas_width, canvas_height, camera_z))
            elif key == "q" or key == "\x03":  # 'q' or Ctrl+C
                break

            # Check if midnight has been reached
            countdown, midnight_reached = get_countdown_to_newyear_2026()

            # Animate camera moving forward
            camera_z += camera_speed * dt

            # Spawn new fireworks automatically only after midnight
            if midnight_reached and elapsed - last_spawn_time > spawn_interval:
                fireworks.append(Firework(canvas_width, canvas_height, camera_z))
                last_spawn_time = elapsed
                spawn_interval = random.uniform(0.2, 0.8)

            # Update all fireworks
            for firework in fireworks:
                firework.update(dt)

            # Remove finished fireworks (and those that passed behind camera)
            fireworks = [
                f for f in fireworks if not f.is_finished() and f.z - camera_z > -50.0
            ]

            # Clear canvas
            canvas.clear(0)

            # Render all fireworks with camera position
            for firework in fireworks:
                firework.render(canvas, camera_z)

            # Render countdown on canvas
            # Use bright green when countdown has finished, default color otherwise
            if midnight_reached:
                countdown_color = BrailleCanvas.rgb_color(0, 255, 0)  # Bright green
            else:
                countdown_color = "\033[39m"  # Default foreground color
            render_countdown_on_canvas(canvas, countdown, countdown_color)

            # Render to screen (single write operation is faster)
            # Use \033[H to position cursor at top-left and overwrite
            output = "\033[H" + canvas.render()
            print(output, end="", flush=True)

    except KeyboardInterrupt:
        pass
    finally:
        # Restore terminal settings (Unix only)
        if old_settings is not None:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        # Exit alternate screen mode, show cursor
        print("\033[?1049l\033[?25h", flush=True)


def main():
    from rich.console import Console
    from rich.panel import Panel

    console = Console()

    console.print(
        Panel(
            "Wait for 2026 (or press SPACE for a firework)",
            padding=(1, 2),
            style="magenta",
            border_style="cyan",
            expand=False,
            title="Instructions",
        )
    )

    input("Enter to continue")

    fireworks()

    MESSAGE = """Thanks for watching!

Toad is a unified interface for AI in the terminal.    

https://github.com/batrachianai/toad"""

    console.print(
        Panel(
            MESSAGE,
            style="magenta",
            border_style="bright_green",
            title="🐸 Built with Toad 🐸",
            expand=False,
            padding=(1, 4),
        )
    )


if __name__ == "__main__":
    main()
