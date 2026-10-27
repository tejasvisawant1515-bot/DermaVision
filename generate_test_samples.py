"""
Generate realistic synthetic face images for testing DermaVisionAI
without requiring an immediate live webcam or manual photo upload.
"""

import os
import cv2
import numpy as np

def create_sample_face(filename, skin_type='Combination', add_acne=True, add_pigment=True):
    # Canvas size
    width, height = 480, 560
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # Soft gradient background
    for y in range(height):
        ratio = y / height
        img[y, :] = [int(235 - ratio * 20), int(240 - ratio * 15), int(245 - ratio * 10)]

    # Center coordinates
    cx = width // 2
    cy = int(height * 0.48)

    # Face base skin color (Indian / warm wheatish skin tone: BGR)
    # R=215, G=175, B=145 -> BGR: (145, 175, 215)
    base_color = (145, 175, 215)
    face_w = 140
    face_h = 185

    # Draw Face Oval
    cv2.ellipse(img, (cx, cy), (face_w, face_h), 0, 0, 360, base_color, -1)

    # Forehead shading
    cv2.ellipse(img, (cx, cy - 60), (face_w - 15, 80), 0, 0, 360, (140, 170, 212), -1)

    # Eyes (Left & Right)
    eye_y = cy - 25
    eye_offset = 55
    cv2.ellipse(img, (cx - eye_offset, eye_y), (22, 11), 0, 0, 360, (245, 245, 248), -1)
    cv2.ellipse(img, (cx + eye_offset, eye_y), (22, 11), 0, 0, 360, (245, 245, 248), -1)
    # Irises
    cv2.circle(img, (cx - eye_offset, eye_y), 8, (35, 45, 60), -1)
    cv2.circle(img, (cx + eye_offset, eye_y), 8, (35, 45, 60), -1)

    # Eyebrows
    cv2.ellipse(img, (cx - eye_offset, eye_y - 18), (28, 5), -8, 0, 180, (40, 45, 55), 4)
    cv2.ellipse(img, (cx + eye_offset, eye_y - 18), (28, 5), 8, 0, 180, (40, 45, 55), 4)

    # Nose
    nose_pts = np.array([
        [cx, cy - 15],
        [cx - 14, cy + 35],
        [cx + 14, cy + 35]
    ], np.int32)
    cv2.polylines(img, [nose_pts], False, (125, 150, 190), 2)
    # Nostrils
    cv2.circle(img, (cx - 9, cy + 36), 3, (110, 135, 175), -1)
    cv2.circle(img, (cx + 9, cy + 36), 3, (110, 135, 175), -1)

    # Lips
    lip_y = cy + 85
    cv2.ellipse(img, (cx, lip_y), (36, 12), 0, 0, 360, (115, 120, 190), -1)

    # Hair on top
    cv2.ellipse(img, (cx, cy - 120), (face_w + 10, 75), 0, 180, 360, (25, 30, 35), -1)

    # Skin type specific modifications:
    if skin_type in ['Oily', 'Combination']:
        # Specular shine on forehead and nose bridge (high V, lower S)
        shine_color = (205, 225, 250)
        cv2.ellipse(img, (cx, cy - 70), (45, 22), 0, 0, 360, shine_color, -1)
        cv2.ellipse(img, (cx, cy + 10), (12, 28), 0, 0, 360, shine_color, -1)

        if skin_type == 'Oily':
            # Also shine on cheeks
            cv2.ellipse(img, (cx - 70, cy + 35), (28, 16), 15, 0, 360, shine_color, -1)
            cv2.ellipse(img, (cx + 70, cy + 35), (28, 16), -15, 0, 360, shine_color, -1)

    # Add Acne / Red Blemishes
    if add_acne:
        # High redness in BGR: low B, medium G, high R -> (70, 75, 220)
        acne_color = (65, 75, 225)
        spots = [
            (cx - 50, cy + 20, 5),
            (cx - 65, cy + 45, 6),
            (cx + 45, cy + 15, 5),
            (cx + 60, cy + 40, 7),
            (cx - 15, cy - 50, 4),
            (cx + 25, cy - 40, 5),
            (cx, cy + 120, 6) # chin
        ]
        for sx, sy, sr in spots:
            cv2.circle(img, (sx, sy), sr, acne_color, -1)
            # Center papule head
            cv2.circle(img, (sx, sy), 2, (120, 130, 245), -1)

    # Add Hyperpigmentation / Dark spots
    if add_pigment:
        # Dark melanin spots in BGR: (100, 125, 160)
        pigment_color = (95, 120, 155)
        patches = [
            (cx - 75, cy + 60, 14, 9),
            (cx + 70, cy + 65, 16, 10),
            (cx - 35, cy - 75, 12, 7),
            (cx + 40, cy - 80, 10, 8)
        ]
        for px, py, pw, ph in patches:
            cv2.ellipse(img, (px, py), (pw, ph), 12, 0, 360, pigment_color, -1)

    # Smooth blur for realistic skin texture
    smoothed = cv2.GaussianBlur(img, (3, 3), 0)

    # Save image
    out_dir = os.path.join(os.path.dirname(__file__), 'static', 'samples')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename)
    cv2.imwrite(out_path, smoothed)
    print(f"Generated sample image: {out_path}")
    return out_path

if __name__ == '__main__':
    create_sample_face('sample_combination_acne.jpg', skin_type='Combination', add_acne=True, add_pigment=True)
    create_sample_face('sample_oily_skin.jpg', skin_type='Oily', add_acne=True, add_pigment=False)
    create_sample_face('sample_dry_normal.jpg', skin_type='Normal', add_acne=False, add_pigment=False)
