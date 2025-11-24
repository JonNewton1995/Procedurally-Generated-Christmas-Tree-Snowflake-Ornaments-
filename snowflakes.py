import math
import random

def rotate_point(point, angle, center):
    """Rotate a point around a center by a given angle in degrees."""
    angle_rad = math.radians(angle)
    ox, oy = center
    px, py = point
    qx = ox + math.cos(angle_rad) * (px - ox) - math.sin(angle_rad) * (py - oy)
    qy = oy + math.sin(angle_rad) * (px - ox) + math.cos(angle_rad) * (py - oy)
    return (qx, qy)

def make_trapezoid(start, end, start_width, end_width):
    """Create a filled trapezoid for a branch segment to give tapered body."""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.sqrt(dx**2 + dy**2)
    if length == 0:
        return []
    perp_x = -dy / length
    perp_y = dx / length
    p1 = (start[0] + perp_x * (start_width / 2), start[1] + perp_y * (start_width / 2))
    p2 = (start[0] - perp_x * (start_width / 2), start[1] - perp_y * (start_width / 2))
    p3 = (end[0] - perp_x * (end_width / 2), end[1] - perp_y * (end_width / 2))
    p4 = (end[0] + perp_x * (end_width / 2), end[1] + perp_y * (end_width / 2))
    return [p1, p4, p3, p2]

def elongated_diamond(tip, direction_angle, width, elong_length):
    """Create an elongated diamond starting at tip, overlaying back along stem."""
    rad = math.radians(direction_angle)
    norm_dir = (math.cos(rad), math.sin(rad))
    back_point = (tip[0] - norm_dir[0] * elong_length, tip[1] - norm_dir[1] * elong_length)
    mid_point = ((tip[0] + back_point[0]) / 2, (tip[1] + back_point[1]) / 2)
    perp_dir = (-norm_dir[1], norm_dir[0])
    width *= random.uniform(0.9, 1.1)
    elong_length *= random.uniform(0.9, 1.1)
    left = (mid_point[0] + perp_dir[0] * (width / 2) + random.uniform(-0.72, 0.72),
            mid_point[1] + perp_dir[1] * (width / 2) + random.uniform(-0.72, 0.72))
    right = (mid_point[0] - perp_dir[0] * (width / 2) + random.uniform(-0.72, 0.72),
             mid_point[1] - perp_dir[1] * (width / 2) + random.uniform(-0.72, 0.72))
    back_point = (back_point[0] + random.uniform(-0.72, 0.72), back_point[1] + random.uniform(-0.72, 0.72))
    tip = (tip[0] + random.uniform(-0.72, 0.72), tip[1] + random.uniform(-0.72, 0.72))
    return [tip, left, back_point, right]

def diamond_shape(center, radius, rotation=0):
    """Fallback diamond for core or non-elongated uses with slight distortions."""
    points = []
    angles = [0, 90, 180, 270]
    for a in angles:
        ang = math.radians(a + rotation + random.uniform(-7.2, 7.2))
        adj_radius = radius * random.uniform(0.9, 1.1)
        px = center[0] + adj_radius * math.cos(ang)
        py = center[1] + adj_radius * math.sin(ang)
        points.append((px, py))
    return points

def draw_branch(start, length, angle, depth, max_depth, polys, start_width, terminals):
    """Recursively collect branch trapezoids and elongated diamond plates with variation."""
    if depth == 0:
        return
    end_x = start[0] + length * math.cos(math.radians(angle))
    end_y = start[1] + length * math.sin(math.radians(angle))
    end = (end_x, end_y)
    end_width = start_width * random.uniform(0.6, 0.8)
    trap = make_trapezoid(start, end, start_width, end_width)
    if trap:
        polys.append(trap)
    
    elong_length = random.uniform(0.3, 0.8) * length
    plate_width = end_width * random.uniform(2.0, 3.0)
    diamond_poly = elongated_diamond(end, angle, plate_width, elong_length)
    polys.append(diamond_poly)
    
    if depth == max_depth:
        num_protrusions = random.randint(1, 3)
        for _ in range(num_protrusions):
            prot_pos = random.uniform(0.3, 0.7)
            prot_start = (start[0] + (end_x - start[0]) * prot_pos, start[1] + (end_y - start[1]) * prot_pos)
            prot_angle = angle + random.choice([-1, 1]) * random.uniform(40, 60)
            prot_length = length * random.uniform(0.1, 0.3)
            prot_end_x = prot_start[0] + prot_length * math.cos(math.radians(prot_angle))
            prot_end_y = prot_start[1] + prot_length * math.sin(math.radians(prot_angle))
            prot_end = (prot_end_x, prot_end_y)
            prot_width = start_width * random.uniform(0.4, 0.6)
            prot_end_width = prot_width * 0.5
            prot_trap = make_trapezoid(prot_start, prot_end, prot_width, prot_end_width)
            if prot_trap:
                polys.append(prot_trap)
            prot_elong = random.uniform(0.3, 0.8) * prot_length
            prot_plate_width = prot_end_width * random.uniform(2.0, 3.0)
            prot_diamond = elongated_diamond(prot_end, prot_angle, prot_plate_width, prot_elong)
            polys.append(prot_diamond)
    
    new_length = length * random.uniform(0.5, 0.7)
    branch_angle_var = random.uniform(35, 55)
    draw_branch(end, new_length, angle + branch_angle_var, depth - 1, max_depth, polys, end_width, terminals)
    draw_branch(end, new_length, angle - branch_angle_var, depth - 1, max_depth, polys, end_width, terminals)
    
    if depth == 1:
        terminals.append(end)

def generate_snowflake(filename, size=180, max_depth=5, initial_length=50.4, initial_width=14.4, center_radius=9):
    """Generate a unique robust elongated diamond-plated snowflake SVG with dead-end protrusions and oversized teardrop hanging loop."""
    center = (size // 2, size // 2)
    
    # Central diamond for core
    all_polygons = [diamond_shape(center, center_radius * random.uniform(0.8, 1.2))]
    
    # Generate one arm's polygons and terminals with random depth
    depth = random.randint(3, max_depth)
    arm_polys = []
    arm_terminals = []
    draw_branch(center, initial_length, 270, depth, depth, arm_polys, initial_width, arm_terminals)  # Start upward (screen top)
    
    # Rotate and add symmetric arms
    for rot in range(0, 360, 60):
        for poly in arm_polys:
            rot_poly = [rotate_point(p, rot, center) for p in poly]
            all_polygons.append(rot_poly)
    
    # Add oversized teardrop hanging loop on one branch end (top arm, furthest terminal)
    if arm_terminals:
        chosen_terminal = min(arm_terminals, key=lambda p: p[1])  # Smallest y for screen top
        direction = (chosen_terminal[0] - center[0], chosen_terminal[1] - center[1])
        dist = math.sqrt(direction[0]**2 + direction[1]**2)
        if dist > 0:
            norm_dir = (direction[0] / dist, direction[1] / dist)
            direction_angle = math.degrees(math.atan2(direction[1], direction[0]))
            rot_angle = direction_angle - 90
            transform = f'translate({chosen_terminal[0]:.2f} {chosen_terminal[1]:.2f}) rotate({rot_angle:.2f})'
            outer_side_x = 50.0
            outer_r = 50.0
            side_y = 75.0
            loop_path = f"M0 0 L-{outer_side_x} {side_y} A{outer_r} {outer_r} 0 1 0 {outer_side_x} {side_y} L0 0 z"
    
    # Write SVG
    with open(filename, 'w') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">\n')
        for poly in all_polygons:
            points_str = ' '.join(f'{x:.2f},{y:.2f}' for x, y in poly)
            f.write(f'<polygon points="{points_str}" fill="white" stroke="none" />\n')
        if 'loop_path' in locals():
            f.write(f'<g transform="{transform}">\n')
            f.write(f'<path d="{loop_path}" fill="none" stroke="white" stroke-width="2" />\n')
            f.write('</g>\n')
        f.write('</svg>')

# Generate 10 unique thickened snowflakes
for i in range(1, 11):
    generate_snowflake(f'thickened_snowflake_{i}.svg')
    print(f'Generated thickened_snowflake_{i}.svg')