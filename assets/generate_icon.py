#!/usr/bin/env python3
"""Generate a simple PPM icon for CyberLab Pro"""
# PPM is a simple format tkinter can read

WIDTH, HEIGHT = 64, 64

def generate():
    pixels = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            # Shield shape
            cx, cy = 32, 32
            # Simple shield: triangle top, rectangle bottom
            in_shield = False
            
            # Top triangle
            if 10 <= y <= 45:
                half_width = int(20 - (y - 10) * 0.3) if y <= 30 else 20
                if cx - half_width <= x <= cx + half_width:
                    in_shield = True
            
            if in_shield:
                # Green shield with dark border
                if abs(x - (cx - 20)) <= 1 or abs(x - (cx + 20)) <= 1 or abs(y - 10) <= 1 or abs(y - 45) <= 1:
                    row.extend([0, 200, 100])  # Border green
                else:
                    row.extend([10, 30, 20])  # Dark bg
            else:
                row.extend([5, 10, 20])  # Background
        
        pixels.append(row)
    
    # Write PPM file
    path = os.path.join(os.path.dirname(__file__), 'icon.ppm')
    with open(path, 'w') as f:
        f.write(f'P3\n{WIDTH} {HEIGHT}\n255\n')
        for row in pixels:
            f.write(' '.join(str(v) for v in row) + '\n')
    
    print(f"Icon saved to {path}")

import os
generate()
