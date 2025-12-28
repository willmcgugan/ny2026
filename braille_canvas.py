"""
High-performance Braille canvas for terminal graphics.

Braille characters use a 2x4 dot pattern, allowing 8 dots per character:
    0 3
    1 4
    2 5
    6 7
Each dot can be individually controlled using Unicode Braille patterns (U+2800-U+28FF).
"""

from typing import Iterable, Tuple


class BrailleCanvas:
    """A high-performance canvas using Braille characters for terminal graphics."""
    
    # Braille Unicode offset
    BRAILLE_OFFSET = 0x2800
    
    # Braille dot bit positions (2x4 grid per character)
    BRAILLE_DOTS = [
        [0, 3],  # Row 0
        [1, 4],  # Row 1
        [2, 5],  # Row 2
        [6, 7],  # Row 3
    ]
    
    # ANSI color codes (standard 8 colors)
    COLORS = {
        0: '\033[30m',  # Black
        1: '\033[31m',  # Red
        2: '\033[32m',  # Green
        3: '\033[33m',  # Yellow
        4: '\033[34m',  # Blue
        5: '\033[35m',  # Magenta
        6: '\033[36m',  # Cyan
        7: '\033[37m',  # White
    }
    RESET = '\033[0m'
    
    @staticmethod
    def rgb_color(r: int, g: int, b: int) -> str:
        """Generate ANSI 24-bit RGB color code."""
        return f'\033[38;2;{r};{g};{b}m'
    
    def __init__(self, width: int, height: int, default_color: int = 7):
        """
        Initialize a Braille canvas.
        
        Args:
            width: Width in pixels (not characters)
            height: Height in pixels (not characters)
            default_color: Default color index (0-7)
        """
        self.width = width
        self.height = height
        self.default_color = default_color
        
        # Calculate character grid dimensions (each character is 2x4 pixels)
        self.char_width = (width + 1) // 2
        self.char_height = (height + 3) // 4
        
        # Storage: 2D array of (braille_value, color) tuples
        self.clear(default_color)
    
    def clear(self, color: int = 7):
        """
        Clear the canvas with a single color.
        
        Args:
            color: Color index (0-7) to clear with
        """
        self.buffer = [
            [(0, color) for _ in range(self.char_width)]
            for _ in range(self.char_height)
        ]
        self.default_color = color
    
    def plot(self, color, points: Iterable[Tuple[int, int]]):
        """
        Plot multiple points with the given color.
        
        Args:
            color: Color index (0-7) or RGB color string from rgb_color()
            points: Iterable of (x, y) coordinate tuples
        """
        # Cache frequently accessed values for better performance
        width = self.width
        height = self.height
        buffer = self.buffer
        braille_dots = self.BRAILLE_DOTS
        
        for x, y in points:
            if 0 <= x < width and 0 <= y < height:
                # Calculate character position using bit shifts (faster than division)
                char_x = x >> 1  # x // 2
                char_y = y >> 2  # y // 4
                
                # Calculate dot position within character using bitwise AND
                dot_x = x & 1  # x % 2
                dot_y = y & 3  # y % 4
                
                # Get bit position for this dot
                bit_pos = braille_dots[dot_y][dot_x]
                
                # Update the character's braille pattern
                current_val, _ = buffer[char_y][char_x]
                new_val = current_val | (1 << bit_pos)
                buffer[char_y][char_x] = (new_val, color)
    
    def line(self, x0: int, y0: int, x1: int, y1: int, color):
        """
        Draw a line from (x0, y0) to (x1, y1) using Bresenham's algorithm.
        
        Args:
            x0, y0: Starting point coordinates
            x1, y1: Ending point coordinates
            color: Color index (0-7) or RGB color string from rgb_color()
        """
        points = self._bresenham_line(x0, y0, x1, y1)
        self.plot(color, points)
    
    def _bresenham_line(self, x0: int, y0: int, x1: int, y1: int) -> Iterable[Tuple[int, int]]:
        """
        Generate points along a line using Bresenham's algorithm.
        
        Args:
            x0, y0: Starting point
            x1, y1: Ending point
            
        Yields:
            (x, y) tuples along the line
        """
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        x, y = x0, y0
        
        while True:
            yield (x, y)
            
            if x == x1 and y == y1:
                break
            
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
    
    def render(self) -> str:
        """
        Render the canvas to a string with ANSI color codes.
        
        Returns:
            String representation of the canvas
        """
        # Pre-allocate list with estimated size for better performance
        lines = []
        braille_offset = self.BRAILLE_OFFSET
        colors = self.COLORS
        reset = self.RESET
        
        for row in self.buffer:
            line_parts = []
            current_color = None
            
            for braille_val, color in row:
                # Only change color if needed
                if color != current_color:
                    if current_color is not None:
                        line_parts.append(reset)
                    # Support both integer colors and RGB string colors
                    if isinstance(color, int):
                        line_parts.append(colors[color])
                    else:
                        line_parts.append(color)
                    current_color = color
                
                # Convert braille value to Unicode character
                line_parts.append(chr(braille_offset + braille_val))
            
            # Reset color at end of line
            if current_color is not None:
                line_parts.append(reset)
            
            lines.append(''.join(line_parts))
        
        return '\r\033[B'.join(lines)
    
    def __str__(self) -> str:
        """Return the rendered canvas."""
        return self.render()
