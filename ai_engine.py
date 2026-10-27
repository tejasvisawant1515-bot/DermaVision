"""
DermaVisionAI - Advanced Computer Vision & AI Skin Analysis Engine
Integrates OpenCV Face Detection, Multi-Spectrum Skin Analysis,
Color-Space Transformations, Feature Extraction, and CNN Deep Learning.
"""

import os
import cv2
import numpy as np
from skin_model import skin_cnn

class SkinAnalyzer:
    def __init__(self):
        # Load Haar Cascade for face detection from OpenCV data
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

    def analyze_image(self, image_path, upload_folder):
        """
        Main pipeline:
        1. Loads image from file.
        2. Detects face and isolates facial skin.
        3. Extracts Region Of Interests (T-Zone, Cheeks, Forehead, Chin).
        4. Performs multi-spectrum Computer Vision analysis.
        5. Combines with CNN deep learning classifier.
        6. Generates visual diagnostic heatmap overlay.
        7. Returns detailed clinical metrics dictionary.
        """
        image_bgr = cv2.imread(image_path)
        if image_bgr is None:
            raise ValueError(f"Could not load image at path: {image_path}")

        img_h, img_w = image_bgr.shape[:2]

        # 1. Detect Face
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100)
        )

        face_detected = True
        if len(faces) > 0:
            # Pick largest detected face
            faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
            fx, fy, fw, fh = faces[0]
        else:
            # Fallback: assume image is a close-up skin shot
            face_detected = False
            fx = int(img_w * 0.1)
            fy = int(img_h * 0.1)
            fw = int(img_w * 0.8)
            fh = int(img_h * 0.8)

        # Crop face region
        face_roi_bgr = image_bgr[fy:fy+fh, fx:fx+fw]
        face_roi_rgb = cv2.cvtColor(face_roi_bgr, cv2.COLOR_BGR2RGB)

        # 2. Skin Segmentation (YCrCb + HSV)
        skin_mask = self._extract_skin_mask(face_roi_bgr)

        # 3. Extract Facial Sub-Zones (Forehead, T-Zone, Cheeks)
        zones = self._extract_zones(face_roi_bgr, fw, fh)

        # 4. Computer Vision Feature Analysis
        sebum_score, tzone_shine, cheek_shine = self._analyze_sebum_and_shine(zones, skin_mask)
        acne_score, acne_spots = self._detect_acne_and_blemishes(face_roi_bgr, skin_mask)
        pigment_score, dark_spots_score, dark_spots = self._detect_pigmentation_and_dark_spots(face_roi_bgr, skin_mask)
        redness_score = self._detect_erythema_redness(face_roi_bgr, skin_mask)
        texture_score = self._analyze_skin_texture(face_roi_bgr, skin_mask)

        # 5. Determine Skin Type (Consensus between CV Sebum/Shine & CNN)
        cnn_result = skin_cnn.predict_patch(face_roi_rgb)
        skin_type, confidence = self._classify_skin_type(
            sebum_score, tzone_shine, cheek_shine, texture_score, cnn_result
        )

        # 6. Identify Primary Skin Concerns
        concerns = self._identify_concerns(
            acne_score, pigment_score, dark_spots_score, redness_score, texture_score, sebum_score
        )

        # 7. Generate Annotated Diagnostic Image Overlay
        annotated_filename = "annotated_" + os.path.basename(image_path)
        annotated_full_path = os.path.join(upload_folder, annotated_filename)
        self._generate_diagnostic_overlay(
            image_bgr, fx, fy, fw, fh, acne_spots, dark_spots, zones,
            skin_type, concerns, annotated_full_path, face_detected
        )

        # Format Scores (0 to 100)
        scores = {
            'sebum': round(float(sebum_score), 1),
            'acne': round(float(acne_score), 1),
            'pigmentation': round(float(pigment_score), 1),
            'dark_spots': round(float(dark_spots_score), 1),
            'texture': round(float(texture_score), 1),
            'redness': round(float(redness_score), 1)
        }

        # Human-friendly descriptions
        interpretations = self._generate_interpretations(skin_type, scores)

        return {
            'face_detected': face_detected,
            'skin_type': skin_type,
            'confidence': int(confidence * 100),
            'concerns': concerns,
            'scores': scores,
            'interpretations': interpretations,
            'annotated_image': annotated_filename,
            'cnn_details': cnn_result
        }

    def _extract_skin_mask(self, bgr_img):
        """Generates binary mask of skin pixels using YCrCb and HSV."""
        ycrcb = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2YCrCb)
        hsv = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)

        # Skin tone range in YCrCb
        lower_ycrcb = np.array([0, 133, 77], dtype=np.uint8)
        upper_ycrcb = np.array([255, 173, 127], dtype=np.uint8)
        mask_ycrcb = cv2.inRange(ycrcb, lower_ycrcb, upper_ycrcb)

        # Skin tone range in HSV
        lower_hsv = np.array([0, 20, 70], dtype=np.uint8)
        upper_hsv = np.array([25, 255, 255], dtype=np.uint8)
        mask_hsv = cv2.inRange(hsv, lower_hsv, upper_hsv)

        # Combine masks
        combined = cv2.bitwise_and(mask_ycrcb, mask_hsv)

        # Morphological opening and closing to clean noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        cleaned = cv2.morphologyEx(combined, cv2.MORPH_OPEN, kernel, iterations=2)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel, iterations=2)

        # If mask is too empty, fall back to entire face ROI
        if np.count_nonzero(cleaned) < 0.1 * bgr_img.shape[0] * bgr_img.shape[1]:
            cleaned = np.ones((bgr_img.shape[0], bgr_img.shape[1]), dtype=np.uint8) * 255

        return cleaned

    def _extract_zones(self, face_bgr, fw, fh):
        """Extracts T-zone, Forehead, Cheeks, and Chin ROIs."""
        # Relative coordinates
        tzone = face_bgr[int(fh * 0.15):int(fh * 0.65), int(fw * 0.35):int(fw * 0.65)]
        left_cheek = face_bgr[int(fh * 0.45):int(fh * 0.75), int(fw * 0.10):int(fw * 0.38)]
        right_cheek = face_bgr[int(fh * 0.45):int(fh * 0.75), int(fw * 0.62):int(fw * 0.90)]
        forehead = face_bgr[int(fh * 0.10):int(fh * 0.35), int(fw * 0.20):int(fw * 0.80)]
        chin = face_bgr[int(fh * 0.75):int(fh * 0.95), int(fw * 0.30):int(fw * 0.70)]

        return {
            'tzone': tzone,
            'left_cheek': left_cheek,
            'right_cheek': right_cheek,
            'forehead': forehead,
            'chin': chin,
            'coords': {
                'tzone': (int(fw * 0.35), int(fh * 0.15), int(fw * 0.30), int(fh * 0.50)),
                'left_cheek': (int(fw * 0.10), int(fh * 0.45), int(fw * 0.28), int(fh * 0.30)),
                'right_cheek': (int(fw * 0.62), int(fh * 0.45), int(fw * 0.28), int(fh * 0.30))
            }
        }

    def _analyze_sebum_and_shine(self, zones, skin_mask):
        """Computes shine / specular reflections in T-zone vs Cheeks."""
        def get_shine_ratio(bgr_patch):
            if bgr_patch is None or bgr_patch.size == 0:
                return 0.0
            hsv = cv2.cvtColor(bgr_patch, cv2.COLOR_BGR2HSV)
            # Specular shine: high brightness (V > 210) and low-to-medium saturation (S < 90)
            shine_mask = (hsv[:, :, 2] > 210) & (hsv[:, :, 1] < 90)
            return float(np.sum(shine_mask)) / float(bgr_patch.shape[0] * bgr_patch.shape[1])

        t_shine = get_shine_ratio(zones['tzone']) * 100.0
        lc_shine = get_shine_ratio(zones['left_cheek']) * 100.0
        rc_shine = get_shine_ratio(zones['right_cheek']) * 100.0
        cheek_shine = (lc_shine + rc_shine) / 2.0

        # General sebum score (0 to 100)
        overall_shine = (t_shine * 0.6) + (cheek_shine * 0.4)
        sebum_score = min(100.0, max(5.0, overall_shine * 7.5))

        return sebum_score, t_shine, cheek_shine

    def _detect_acne_and_blemishes(self, face_bgr, skin_mask):
        """Detects erythematous acne papules, pustules, and inflamed comedones."""
        h, w = face_bgr.shape[:2]
        lab = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2LAB)
        l_chan, a_chan, b_chan = cv2.split(lab)

        # In LAB, 'a' represents Red-Green. Elevated 'a' within skin means redness/acne.
        # Apply skin mask
        a_skin = cv2.bitwise_and(a_chan, a_chan, mask=skin_mask)
        mean_a = np.mean(a_skin[skin_mask > 0]) if np.count_nonzero(skin_mask) > 0 else 128
        std_a = np.std(a_skin[skin_mask > 0]) if np.count_nonzero(skin_mask) > 0 else 10

        # Threshold for red inflamed spots (mean + 1.25 std)
        red_threshold = int(mean_a + 1.25 * std_a)
        _, red_mask = cv2.threshold(a_chan, red_threshold, 255, cv2.THRESH_BINARY)
        red_mask = cv2.bitwise_and(red_mask, skin_mask)

        # Remove eyes/lips region roughly by height/margins
        cv2.circle(red_mask, (int(w * 0.33), int(h * 0.38)), int(w * 0.12), 0, -1) # left eye
        cv2.circle(red_mask, (int(w * 0.67), int(h * 0.38)), int(w * 0.12), 0, -1) # right eye
        cv2.ellipse(red_mask, (int(w * 0.5), int(h * 0.78)), (int(w * 0.18), int(h * 0.08)), 0, 0, 360, 0, -1) # lips

        # Find contours of acne spots
        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        acne_spots = []
        for c in contours:
            area = cv2.contourArea(c)
            # Filter by reasonable pimple size (radius ~ 3px to 25px depending on image size)
            if 8 <= area <= 400:
                (x, y), radius = cv2.minEnclosingCircle(c)
                acne_spots.append((int(x), int(y), int(radius)))

        # Severity score based on spot count and density
        spot_count = len(acne_spots)
        if spot_count == 0:
            score = 12.0
        elif spot_count <= 4:
            score = 25.0 + spot_count * 5.0
        elif spot_count <= 10:
            score = 45.0 + spot_count * 3.0
        else:
            score = min(98.0, 75.0 + (spot_count - 10) * 1.5)

        return score, acne_spots

    def _detect_pigmentation_and_dark_spots(self, face_bgr, skin_mask):
        """Detects hyperpigmentation patches, dark spots, and post-acne marks."""
        h, w = face_bgr.shape[:2]
        lab = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2LAB)
        l_chan = lab[:, :, 0]

        # Use Gaussian blur to compute local background skin luminance
        blurred_l = cv2.GaussianBlur(l_chan, (35, 35), 0)
        # Compute local luminance deficit (darker than surroundings)
        dark_diff = cv2.subtract(blurred_l, l_chan)
        dark_diff = cv2.bitwise_and(dark_diff, dark_diff, mask=skin_mask)

        # Threshold for dark spots
        _, dark_thresh = cv2.threshold(dark_diff, 18, 255, cv2.THRESH_BINARY)

        # Mask out eyebrows, eyes, and mouth
        cv2.circle(dark_thresh, (int(w * 0.33), int(h * 0.38)), int(w * 0.14), 0, -1)
        cv2.circle(dark_thresh, (int(w * 0.67), int(h * 0.38)), int(w * 0.14), 0, -1)
        cv2.ellipse(dark_thresh, (int(w * 0.5), int(h * 0.78)), (int(w * 0.20), int(h * 0.10)), 0, 0, 360, 0, -1)
        # Forehead hairline mask
        dark_thresh[0:int(h * 0.12), :] = 0

        contours, _ = cv2.findContours(dark_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        dark_spots = []
        total_dark_area = 0
        for c in contours:
            area = cv2.contourArea(c)
            if 15 <= area <= 600:
                x, y, cw, ch = cv2.boundingRect(c)
                dark_spots.append((x, y, cw, ch))
                total_dark_area += area

        skin_area = max(1.0, float(np.count_nonzero(skin_mask)))
        dark_ratio = (total_dark_area / skin_area) * 100.0

        pigment_score = min(95.0, max(10.0, dark_ratio * 12.0 + len(dark_spots) * 2.5))
        dark_spots_score = min(96.0, max(8.0, len(dark_spots) * 4.5 + dark_ratio * 6.0))

        return pigment_score, dark_spots_score, dark_spots

    def _detect_erythema_redness(self, face_bgr, skin_mask):
        """Measures diffuse redness / erythema on cheeks and nose."""
        b, g, r = cv2.split(face_bgr.astype(np.float32))
        # Erythema index: (r - g) normalized
        erythema = np.clip(r - g, 0, 255)
        masked_erythema = erythema[skin_mask > 0]
        if len(masked_erythema) == 0:
            return 20.0
        mean_erythema = np.mean(masked_erythema)
        score = min(95.0, max(10.0, (mean_erythema / 40.0) * 50.0))
        return score

    def _analyze_skin_texture(self, face_bgr, skin_mask):
        """Calculates micro-texture roughness and pore visibility."""
        gray = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        laplacian_sq = np.square(laplacian)
        masked_lap = laplacian_sq[skin_mask > 0]
        if len(masked_lap) == 0:
            return 30.0
        var_lap = np.mean(masked_lap)
        # Moderate texture is smooth; very high variance indicates roughness or large pores
        score = min(92.0, max(15.0, np.log1p(var_lap) * 10.0))
        return score

    def _classify_skin_type(self, sebum_score, tzone_shine, cheek_shine, texture_score, cnn_result):
        """
        Synthesizes CV metrics and CNN deep learning predictions
        to classify into: Oily, Dry, Normal, Combination.
        """
        # Rule-based CV heuristic
        diff = tzone_shine - cheek_shine

        if sebum_score >= 58.0 and cheek_shine >= 2.5:
            cv_type = 'Oily'
            cv_conf = min(0.95, 0.70 + (sebum_score / 200.0))
        elif diff >= 2.2 and tzone_shine >= 3.0 and cheek_shine < 2.5:
            cv_type = 'Combination'
            cv_conf = min(0.94, 0.72 + (diff / 15.0))
        elif sebum_score < 30.0 and texture_score >= 45.0:
            cv_type = 'Dry'
            cv_conf = min(0.92, 0.70 + ((50.0 - sebum_score) / 100.0))
        else:
            cv_type = 'Normal'
            cv_conf = 0.85

        # CNN agreement boost
        final_type = cv_type
        final_conf = cv_conf
        if cnn_result:
            cnn_type = cnn_result['predicted_class']
            cnn_conf = cnn_result['confidence']
            if cnn_type == cv_type:
                final_conf = min(0.98, max(cv_conf, cnn_conf) + 0.05)
            else:
                # If slight discrepancy, weight CV 60% and CNN 40%
                if cnn_conf > 0.80 and cv_conf < 0.75:
                    final_type = cnn_type
                    final_conf = cnn_conf

        return final_type, final_conf

    def _identify_concerns(self, acne_score, pigment_score, dark_spots_score, redness_score, texture_score, sebum_score):
        """Identifies primary skin concerns sorted by severity."""
        concern_candidates = []
        if acne_score >= 35.0:
            concern_candidates.append(('Acne & Blemishes', acne_score))
        if dark_spots_score >= 32.0 or pigment_score >= 38.0:
            concern_candidates.append(('Pigmentation & Dark Spots', max(dark_spots_score, pigment_score)))
        if sebum_score >= 60.0:
            concern_candidates.append(('Excess Sebum & Oiliness', sebum_score))
        if redness_score >= 45.0:
            concern_candidates.append(('Redness & Sensitivity', redness_score))
        if texture_score >= 50.0:
            concern_candidates.append(('Enlarged Pores & Texture', texture_score))
        elif sebum_score <= 25.0:
            concern_candidates.append(('Dryness & Dehydration', 100.0 - sebum_score))

        # Sort by score descending
        concern_candidates.sort(key=lambda x: x[1], reverse=True)

        if not concern_candidates:
            return ['Even Texture', 'General Maintenance']

        return [c[0] for c in concern_candidates[:3]]

    def _generate_diagnostic_overlay(self, img_bgr, fx, fy, fw, fh, acne_spots, dark_spots,
                                    zones, skin_type, concerns, output_path, face_detected):
        """Draws visual diagnostic markers, HUD overlays, and annotations."""
        overlay = img_bgr.copy()
        h, w = img_bgr.shape[:2]

        # 1. Draw glowing face bounding box
        box_color = (255, 191, 0) # Deep sky cyan in BGR: (0, 215, 255) -> (255, 191, 0)
        cv2.rectangle(overlay, (fx, fy), (fx + fw, fy + fh), (0, 220, 255), 2)

        # Draw aesthetic corner brackets
        corner_len = int(min(fw, fh) * 0.15)
        thick = 3
        c_col = (0, 255, 180) # neon mint
        # Top-left
        cv2.line(overlay, (fx, fy), (fx + corner_len, fy), c_col, thick)
        cv2.line(overlay, (fx, fy), (fx, fy + corner_len), c_col, thick)
        # Top-right
        cv2.line(overlay, (fx + fw, fy), (fx + fw - corner_len, fy), c_col, thick)
        cv2.line(overlay, (fx + fw, fy), (fx + fw, fy + corner_len), c_col, thick)
        # Bottom-left
        cv2.line(overlay, (fx, fy + fh), (fx + corner_len, fy + fh), c_col, thick)
        cv2.line(overlay, (fx, fy + fh), (fx, fy + fh - corner_len), c_col, thick)
        # Bottom-right
        cv2.line(overlay, (fx + fw, fy + fh), (fx + fw - corner_len, fy + fh), c_col, thick)
        cv2.line(overlay, (fx + fw, fy + fh), (fx + fw, fy + fh - corner_len), c_col, thick)

        # 2. Mark detected Acne spots (Neon Red circles)
        for (ax, ay, ar) in acne_spots:
            global_x = fx + ax
            global_y = fy + ay
            cv2.circle(overlay, (global_x, global_y), max(6, ar + 3), (40, 40, 255), 2)
            cv2.circle(overlay, (global_x, global_y), 2, (0, 0, 255), -1)

        # 3. Mark detected Hyperpigmentation / Dark spots (Golden Amber rectangles)
        for (dx, dy, dw, dh) in dark_spots:
            global_x = fx + dx
            global_y = fy + dy
            cv2.rectangle(overlay, (global_x, global_y), (global_x + dw, global_y + dh), (0, 165, 255), 1)

        # Blend overlay with original for a smooth glow
        blended = cv2.addWeighted(overlay, 0.85, img_bgr, 0.15, 0)

        # 4. Add Sleek Clinical HUD Header / Banner
        hud_bar_height = max(56, int(h * 0.10))
        hud_bar = np.zeros((hud_bar_height, w, 3), dtype=np.uint8)
        # Deep clinical slate blue
        hud_bar[:] = (35, 25, 20)

        # Combine banner at top
        final_canvas = np.vstack([hud_bar, blended])

        # Dynamic font scale based on width
        scale = max(0.40, min(0.70, w / 800.0))
        thick = 1 if scale < 0.55 else 2

        # Render HUD text
        title_text = f"DermaVisionAI | Skin: {skin_type.upper()}"
        concerns_text = f"Concerns: {', '.join(concerns[:2])}"
        cv2.putText(final_canvas, title_text, (15, int(hud_bar_height * 0.42)), cv2.FONT_HERSHEY_SIMPLEX, scale, (0, 255, 200), thick)
        cv2.putText(final_canvas, concerns_text, (15, int(hud_bar_height * 0.82)), cv2.FONT_HERSHEY_SIMPLEX, max(0.35, scale * 0.8), (220, 220, 220), 1)

        # Legend on right side (only if width allows)
        if w >= 450:
            legend_scale = max(0.35, scale * 0.75)
            # Acne indicator
            acne_x = w - 165
            cv2.circle(final_canvas, (acne_x, int(hud_bar_height * 0.42)), 4, (40, 40, 255), -1)
            cv2.putText(final_canvas, "Acne", (acne_x + 8, int(hud_bar_height * 0.48)), cv2.FONT_HERSHEY_SIMPLEX, legend_scale, (255, 255, 255), 1)

            # Dark Spot indicator
            spot_x = w - 95
            cv2.circle(final_canvas, (spot_x, int(hud_bar_height * 0.42)), 4, (0, 165, 255), -1)
            cv2.putText(final_canvas, "Spots", (spot_x + 8, int(hud_bar_height * 0.48)), cv2.FONT_HERSHEY_SIMPLEX, legend_scale, (255, 255, 255), 1)

        # Save to static uploads
        cv2.imwrite(output_path, final_canvas)

    def _generate_interpretations(self, skin_type, scores):
        """Generates clinical interpretations for each score."""
        res = {}
        # Sebum
        if scores['sebum'] > 60:
            res['sebum'] = "Elevated sebum activity detected across forehead and nose. Pores are actively producing lipid shine."
        elif scores['sebum'] < 30:
            res['sebum'] = "Low lipid secretion observed. Dermal barrier shows reduced oil levels, prone to tightness."
        else:
            res['sebum'] = "Well-balanced sebum equilibrium. Optimal skin lipid barrier maintained."

        # Acne
        if scores['acne'] > 50:
            res['acne'] = "Moderate to active erythematous blemishes detected. Gentle clarifying actives recommended."
        elif scores['acne'] > 25:
            res['acne'] = "Mild blemish activity observed. Preventive pore-unclogging measures advised."
        else:
            res['acne'] = "Minimal or zero active inflammatory breakouts detected."

        # Pigmentation
        if scores['pigmentation'] > 50 or scores['dark_spots'] > 50:
            res['pigmentation'] = "Visible localized hyperpigmentation and UV melanin clusters detected. Melanin inhibitors recommended."
        else:
            res['pigmentation'] = "Even complexion with low overall melanin discoloration."

        # Texture
        if scores['texture'] > 50:
            res['texture'] = "Noticeable epidermal micro-roughness or visible follicular pore dilation."
        else:
            res['texture'] = "Smooth skin surface with refined pore structure."

        return res


# Global singleton instance
skin_analyzer = SkinAnalyzer()
