import cv2
import numpy as np

def preprocess_image(image):
    """
    Preprocess the image by converting it to grayscale and applying Gaussian blur.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    return blur

def detect_edges(image):
    """
    Detect edges in the image using the Canny edge detection algorithm.
    """
    edges = cv2.Canny(image, 50, 150)
    return edges

def region_of_interest(image):
    """
    Apply a mask to focus on the region of interest (ROI).
    """
    height, width = image.shape
    mask = np.zeros_like(image)

    # Define a trapezoidal ROI (adjust vertices as needed)
    polygon = np.array([[
        (0, height),  # Bottom-left corner
        (width // 2, height // 2),  # Center-top
        (width, height),  # Bottom-right corner
    ]], np.int32)

    cv2.fillPoly(mask, polygon, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def detect_lines(image):
    """
    Detect lines using the Hough Transform.
    """
    lines = cv2.HoughLinesP(image, rho=2, theta=np.pi/180, threshold=100, minLineLength=40, maxLineGap=5)
    return lines

def draw_lines(image, lines):
    """
    Draw detected lines on the original image.
    """
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)
    return image

def process_image(image):
    """
    Process the image to detect and draw lanes.
    """
    # Step 1: Preprocess the image
    blur = preprocess_image(image)

    # Step 2: Detect edges
    edges = detect_edges(blur)

    # Step 3: Apply ROI mask
    masked_edges = region_of_interest(edges)

    # Step 4: Detect lines
    lines = detect_lines(masked_edges)

    # Step 5: Draw lines on the original image
    output_image = draw_lines(image, lines)

    return output_image

def process_video(video_path, output_path=None):
    """
    Process a video to detect lanes.
    """
    cap = cv2.VideoCapture(video_path)

    if output_path:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process the frame
        processed_frame = process_image(frame)

        # Display the frame
        cv2.imshow('Lane Detection', processed_frame)

        # Save the frame if output path is provided
        if output_path:
            out.write(processed_frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    if output_path:
        out.release()
    cv2.destroyAllWindows()

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Lane Detection in Images or Videos")
    parser.add_argument('--image', type=str, help="Path to the input image")
    parser.add_argument('--video', type=str, help="Path to the input video")
    parser.add_argument('--real-time', action='store_true', help="Enable real-time lane detection using webcam")
    parser.add_argument('--output', type=str, help="Path to save the output video")

    args = parser.parse_args()

    if args.image:
        # Process an image
        image = cv2.imread(args.image)
        output_image = process_image(image)
        cv2.imshow('Lane Detection', output_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif args.video:
        # Process a video
        process_video(args.video, args.output)

    elif args.real_time:
        # Real-time lane detection using webcam
        process_video(0)  # 0 for webcam

    else:
        print("Please provide an input image or video using --image or --video.")

if __name__ == "__main__":
    main()