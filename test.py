import numpy as np
# Load the image
import cv2
from PIL import Image
import matplotlib.pyplot as plt
image_path = r"C:\Users\Morning\Desktop\_20231020181255.png"
# image = Image.open(image_path)
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Further reduce the threshold value to include even more gray as white
# Further reduce the threshold value to include even more gray as white

_, white_thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)

black_thresh = cv2.bitwise_not(white_thresh)

# Find contours in the thresholded images
white_contours, _ = cv2.findContours(white_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
black_contours, _ = cv2.findContours(black_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Sort the contours by area to find the largest ones
white_contours = sorted(white_contours, key=cv2.contourArea, reverse=True)
black_contours = sorted(black_contours, key=cv2.contourArea, reverse=True)

# Draw the largest contours on the original image
# if white_contours:
#     cv2.drawContours(image, [white_contours[0]], -1, (0, 0, 255), 2)
#
# if black_contours:
#     cv2.drawContours(image, [black_contours[0]], -1, (0, 0, 255), 2)

# Convert the image back to RGB for visualization
image_rgb_even_lower_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

leftmost = tuple(white_contours[0][white_contours[0][:,:,0].argmin()][0])
rightmost = tuple(white_contours[0][white_contours[0][:,:,0].argmax()][0])
topmost = tuple(white_contours[0][white_contours[0][:,:,1].argmin()][0])
bottommost = tuple(white_contours[0][white_contours[0][:,:,1].argmax()][0])

# Draw horizontal and vertical lines connecting these extremal points
# cv2.line(image, (leftmost[0], (topmost[1] + bottommost[1]) // 2), (rightmost[0], (topmost[1] + bottommost[1]) // 2), (0, 255, 0), 2)
# cv2.line(image, ((leftmost[0] + rightmost[0]) // 2, topmost[1]), ((leftmost[0] + rightmost[0]) // 2, bottommost[1]), (0, 255, 0), 2)

# Convert the image back to RGB for visualization
image_rgb_with_lines = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
circle_center = ((leftmost[0] + rightmost[0]) // 2, (topmost[1] + bottommost[1]) // 2)

# Find the maximum distance from the circle center to the contour points
# distances = [cv2.pointPolygonTest(white_contours[0], circle_center, True)]
# max_distance = max(distances)

# Display the result
# Calculate distances from the circle center to all the points in the contour
distances = [cv2.norm(np.array(circle_center) - point[0]) for point in white_contours[0]]

# Get the maximum distance
max_distance = max(distances)

# Draw the circle using the calculated center and radius
cv2.circle(image, circle_center, int(max_distance), (255, 0, 0), 2)

# Convert the image back to RGB for visualization
image_rgb_with_circle_fixed = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Display the result
mask = np.zeros_like(gray)

# Draw the circle on the mask

# Apply the mask to the image
masked_image = cv2.bitwise_and(image, image, mask=mask)

# Convert the masked image back to RGB for visualization
masked_image_rgb = cv2.cvtColor(masked_image, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(masked_image_rgb, cv2.COLOR_BGR2GRAY)
ret, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# Display the result

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))

# Apply morphological opening to smooth the edges
smoothed_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)
cv2.circle(smoothed_image, circle_center, int(max_distance), (255), -1)

# Display the smoothed image
plt.figure(figsize=(6, 6))
plt.imshow(smoothed_image, cmap='gray')
plt.axis('off')
plt.title('Smoothed Image using Morphological Opening')
plt.show()