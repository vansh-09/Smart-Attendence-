import cv2


def draw_box(frame_bgr, box, color=(0, 255, 0), thickness=2):
    x, y, w, h = box
    cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), color, thickness)


def draw_label(frame_bgr, text, box, color=(0, 255, 0)):
    x, y, w, h = box
    label_bg_color = (0, 0, 0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    thickness = 1
    # Compute text size
    (tw, th), _ = cv2.getTextSize(text, font, font_scale, thickness)
    # Draw background rectangle above the box
    cv2.rectangle(frame_bgr, (x, max(0, y - th - 10)), (x + tw + 10, y), label_bg_color, -1)
    # Put text
    cv2.putText(frame_bgr, text, (x + 5, y - 5), font, font_scale, color, thickness, cv2.LINE_AA)
