import cv2
import time

# Open the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error opening video stream")

# Loop over the video stream
while True:
    # Read the next frame
    ret, frame = cap.read()

    # Check if the frame is empty
    if not ret:
        print("Error reading video stream")
        break

    # Create a timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")

    # Save the frame to a file
    cv2.imwrite(f"./data/input/{timestamp}.png", frame)

    # Display the frame in a window
    cv2.imshow('frame', frame)

    # Wait for a key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the webcam
cap.release()

# Destroy all windows
cv2.destroyAllWindows()