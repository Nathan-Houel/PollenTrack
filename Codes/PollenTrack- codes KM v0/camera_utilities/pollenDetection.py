import cv2

def pollen_detection(image) :
    """detect the ROI (region of interest) of the image given in parameters

    Args:
        image_path (_string_)

    Returns:
        _x, y, w, h (_int_) : coordinates of the ROI
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = (0,0,0,0)
    if len(contours) != 0 :
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
    return x,y,w,h

