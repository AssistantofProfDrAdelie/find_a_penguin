#!/usr/bin/env python3
"""Prepare the authentic Professor Adelie portrait as a transparent PNG.

This is deterministic foreground segmentation and alpha cleanup. It never
generates, redraws, fills, or reconstructs character pixels.
"""

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "source" / "professor-adelie-portrait.jpg"
OUTPUT = ROOT / "assets" / "professor-adelie-transparent.png"
WORKING_HEIGHT = 1760


def build_mask(image: np.ndarray) -> np.ndarray:
    """Segment the supplied portrait using fixed masks tied to that source."""
    height, width = image.shape[:2]
    if (width, height) != (990, 1760):
        raise ValueError(f"Unexpected source dimensions: {width}x{height}")

    def point(x: int, y: int) -> tuple[int, int]:
        return round(x / 2), round(y / 2)

    mask = np.full((height, width), cv2.GC_BGD, dtype=np.uint8)
    mask[:480, :] = cv2.GC_BGD
    mask[:, :18] = cv2.GC_BGD

    silhouette = np.array(
        [
            point(390, 1030), point(1510, 1020), point(1460, 1570),
            point(1600, 1740), point(1810, 2210), point(1979, 2820),
            point(1979, 3519), point(75, 3519), point(135, 3100),
            point(300, 2520), point(520, 2180), point(560, 2040),
            point(500, 1980), point(500, 1800), point(520, 1640),
            point(410, 1560), point(395, 1300),
        ],
        dtype=np.int32,
    )
    cv2.fillPoly(mask, [silhouette], cv2.GC_PR_FGD)
    # Known pockets of wall enclosed by the broad silhouette.
    cv2.rectangle(mask, point(350, 1150), point(720, 1760), cv2.GC_BGD, -1)
    cv2.rectangle(mask, point(1230, 1150), point(1530, 1700), cv2.GC_BGD, -1)

    cv2.rectangle(mask, point(520, 1110), point(1390, 1480), cv2.GC_FGD, -1)
    cv2.ellipse(mask, point(1050, 1940), point(430, 330), 0, 0, 360, cv2.GC_FGD, -1)
    cv2.ellipse(mask, point(1030, 2860), point(560, 620), 0, 0, 360, cv2.GC_FGD, -1)
    cv2.rectangle(mask, point(445, 1450), point(535, 1790), cv2.GC_FGD, -1)

    bg_model = np.zeros((1, 65), np.float64)
    fg_model = np.zeros((1, 65), np.float64)
    cv2.setRNGSeed(0)
    cv2.grabCut(image, mask, None, bg_model, fg_model, 5, cv2.GC_INIT_WITH_MASK)
    alpha = np.where(
        (mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0
    ).astype(np.uint8)
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))

    # GrabCut can leave pinholes in dark woven fabric. Fill only small enclosed
    # holes; open background and deliberate gaps remain transparent.
    inverse = cv2.bitwise_not(alpha)
    hole_count, hole_labels, hole_stats, _ = cv2.connectedComponentsWithStats(inverse, 8)
    for label in range(1, hole_count):
        x, y, w, h, area = hole_stats[label]
        touches_edge = x == 0 or y == 0 or x + w == width or y + h == height
        if not touches_edge and area < 180:
            alpha[hole_labels == label] = 255

    # Preserve the fine gold tassel and its dark cord directly from the source.
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    luminance = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cap_region = np.zeros_like(alpha)
    brim = np.array(
        [[90, 500], [770, 490], [720, 650], [660, 655], [640, 700],
         [315, 700], [300, 655], [180, 640]],
        dtype=np.int32,
    )
    crown = np.array(
        [[315, 575], [665, 575], [650, 795], [325, 795]],
        dtype=np.int32,
    )
    cv2.fillPoly(cap_region, [brim, crown], 1)
    cap = (luminance < 76) & (cap_region == 1)
    cap = cv2.morphologyEx(
        np.where(cap, 255, 0).astype(np.uint8),
        cv2.MORPH_CLOSE,
        np.ones((5, 5), np.uint8),
    )

    tassel_region = np.zeros_like(alpha)
    tassel_region[600:980, 170:335] = 1
    yellow = ((hsv[:, :, 1] > 155) & (hsv[:, :, 2] > 75) & (tassel_region == 1))
    cord_region = np.zeros_like(alpha)
    cord_region[600:810, 220:310] = 1
    cord = (luminance < 72) & (cord_region == 1)
    accents = np.where(yellow | cord, 255, 0).astype(np.uint8)
    accents = cv2.morphologyEx(accents, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))

    count, labels, stats, _ = cv2.connectedComponentsWithStats(alpha, 8)
    if count > 1:
        keep = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        alpha = np.where(labels == keep, 255, 0).astype(np.uint8)
    result = cv2.bitwise_or(alpha, accents)
    # Remove two dark wall-shadow pockets beneath the mortarboard. Restore the
    # source tassel afterward so its fine strands remain intact.
    result[650:900, 145:220] = 0
    result[650:800, 220:300] = 0
    result[650:800, 660:785] = 0
    right_wall = np.array(
        [[940, 1300], [989, 1300], [989, 1759], [970, 1759], [925, 1450]],
        dtype=np.int32,
    )
    cv2.fillPoly(result, [right_wall], 0)
    return cv2.bitwise_or(cv2.bitwise_or(result, accents), cap)


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Missing preserved source: {SOURCE}")

    oriented = ImageOps.exif_transpose(Image.open(SOURCE)).convert("RGB")
    scale = WORKING_HEIGHT / oriented.height
    oriented = oriented.resize(
        (round(oriented.width * scale), WORKING_HEIGHT), Image.Resampling.LANCZOS
    )
    rgb = np.asarray(oriented)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    alpha = build_mask(bgr)

    alpha_image = Image.fromarray(alpha, "L").filter(ImageFilter.MinFilter(3))
    alpha_image = alpha_image.filter(ImageFilter.GaussianBlur(0.8))

    rgba = oriented.convert("RGBA")
    rgba.putalpha(alpha_image)
    bbox = alpha_image.getbbox()
    if not bbox:
        raise RuntimeError("Foreground segmentation produced an empty mask")
    padding = 18
    left = max(0, bbox[0] - padding)
    top = max(0, bbox[1] - padding)
    right = min(rgba.width, bbox[2] + padding)
    bottom = min(rgba.height, bbox[3] + padding)
    rgba = rgba.crop((left, top, right, bottom))
    if rgba.height > 1120:
        rgba = rgba.crop((0, 0, rgba.width, 1120))

    OUTPUT.parent.mkdir(exist_ok=True)
    rgba.save(OUTPUT, optimize=True)
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({rgba.width}x{rgba.height})")


if __name__ == "__main__":
    main()
