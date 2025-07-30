# Computer Vision Lab
def get_Imgae_code():
    code = """
    import cv2
import numpy as np
import matplotlib.pyplot as plt

def image_processing():
    #Demonstrates various image processing techniques using OpenCV.
    #Requires an input image file named 'input_image.jpg'.
    # Load an image
    img = cv2.imread('input_image.jpg')
    if img is None:
        print("Error: Could not load image.")
        return

    # 1a. Display original image
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.axis('off')
    plt.show()

    # 1b. Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plt.imshow(gray, cmap='gray')
    plt.title('Grayscale Image')
    plt.axis('off')
    plt.show()

    # 1c. Image transformations
    # Resize to 30% of original size
    height, width = img.shape[:2]
    resized = cv2.resize(img, (int(width * 0.3), int(height * 0.3)))
    plt.imshow(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
    plt.title('Resized Image (30%)')
    plt.axis('off')
    plt.show()

    # Crop a region (e.g., from (100, 100) to (300, 300))
    cropped = img[100:300, 100:300]
    plt.imshow(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
    plt.title('Cropped Image')
    plt.axis('off')
    plt.show()

    # Rotate by 90 degrees
    rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    plt.imshow(cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB))
    plt.title('Rotated Image (90°)')
    plt.axis('off')
    plt.show()

    # 1d. Filtering
    # Gaussian blur
    blurred = cv2.GaussianBlur(img, (7, 7), 0)
    plt.imshow(cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB))
    plt.title('Gaussian Blurred Image')
    plt.axis('off')
    plt.show()

    # Sharpening
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(img, -1, sharpen_kernel)
    plt.imshow(cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB))
    plt.title('Sharpened Image')
    plt.axis('off')
    plt.show()

    # 1e. Edge detection
    # Sobel
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
    sobel = cv2.magnitude(sobelx, sobely)
    plt.imshow(sobel, cmap='gray')
    plt.title('Sobel Edge Detection')
    plt.axis('off')
    plt.show()

    # Canny
    edges = cv2.Canny(gray, 100, 200)
    plt.imshow(edges, cmap='gray')
    plt.title('Canny Edge Detection')
    plt.axis('off')
    plt.show()

    # 1f. Thresholding
    # Global
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    plt.imshow(thresh, cmap='gray')
    plt.title('Global Thresholding')
    plt.axis('off')
    plt.show()

    # Adaptive
    adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                            cv2.THRESH_BINARY, 11, 2)
    plt.imshow(adaptive_thresh, cmap='gray')
    plt.title('Adaptive Thresholding')
    plt.axis('off')
    plt.show()

    # 1g. Contour detection
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_with_contours = img.copy()
    cv2.drawContours(img_with_contours, contours, -1, (0, 255, 0), 3)
    plt.imshow(cv2.cvtColor(img_with_contours, cv2.COLOR_BGR2RGB))
    plt.title('Contour Detection')
    plt.axis('off')
    plt.show()

    # 1h. Face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Face Detection')
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    image_processing()
    """
    return code

def get_MNIST_code():
    code = """
    import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import pandas as pd
from torchvision import transforms

class MNISTCSVLoader(Dataset):
    #Custom Dataset to load MNIST data from CSV.
    def __init__(self, csv_file, transform=None):
        data = pd.read_csv(csv_file)
        self.labels = torch.tensor(data.iloc[:, 0].values, dtype=torch.long)
        self.images = data.iloc[:, 1:].values.reshape(-1, 28, 28).astype("float32") / 255.0
        self.transform = transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        image = torch.tensor(self.images[idx], dtype=torch.float32).unsqueeze(0)  # Shape: (1, 28, 28)
        if self.transform:
            image = self.transform(image)
        return image, self.labels[idx]

class SimpleCNN(nn.Module):
    #Simple Convolutional Neural Network for MNIST classification.
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, 3, padding=1)  # Output: (16, 28, 28)
        self.pool = nn.MaxPool2d(2, 2)               # Output: (16, 14, 14)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1) # Output: (32, 14, 14) -> (32, 7, 7)
        self.fc1 = nn.Linear(32 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)                # 10 classes

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 32 * 7 * 7)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def train_mnist():
    #Trains a CNN on the MNIST dataset loaded from a CSV file.
    #Requires 'mnist_train.csv' with labels in column 0 and pixels in columns 1-784.
    # Define transforms
    transform = transforms.Normalize((0.5,), (0.5,))

    # Load dataset
    try:
        train_dataset = MNISTCSVLoader("mnist_train.csv", transform=transform)
    except FileNotFoundError:
        print("Error: 'mnist_train.csv' not found.")
        return
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Initialize model, loss, and optimizer
    model = SimpleCNN().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Training loop
    num_epochs = 5
    for epoch in range(num_epochs):
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            # Forward pass
            outputs = model(images)
            loss = criterion(outputs, labels)

            # Backward pass and optimization
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # Statistics
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        accuracy = 100 * correct / total
        print(f"Epoch {epoch+1}/{num_epochs}, Loss: {running_loss:.4f}, Accuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    train_mnist()
    """
    return code

def get_basic_cnn_code():
    code = """
    import torch
import torch.nn as nn

class MediumCNN(nn.Module):
    def __init__(self):
        super(MediumCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 64, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(64)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(128)
        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(256)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(256 * 3 * 3, 128)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(128, 10)
        
    def forward(self, x):
        x = self.pool(torch.relu(self.bn1(self.conv1(x))))
        x = self.pool(torch.relu(self.bn2(self.conv2(x))))
        x = self.pool(torch.relu(self.bn3(self.conv3(x))))
        x = x.view(-1, 256 * 3 * 3)
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x
    """
    return code


def get_advance_cnn_code():
    code = """
    import torch
import torch.nn as nn

class AdvancedCNN(nn.Module):
    def __init__(self):
        super(AdvancedCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 128, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(128)
        self.conv2 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(256)
        self.conv3 = nn.Conv2d(256, 512, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(512)
        self.conv4 = nn.Conv2d(512, 1024, kernel_size=3, padding=1)
        self.bn4 = nn.BatchNorm2d(1024)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(1024 * 1 * 1, 128)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(128, 10)
        
    def forward(self, x):
        x = self.pool(torch.relu(self.bn1(self.conv1(x))))
        x = self.pool(torch.relu(self.bn2(self.conv2(x))))
        x = self.pool(torch.relu(self.bn3(self.conv3(x))))
        x = self.pool(torch.relu(self.bn4(self.conv4(x))))
        x = x.view(-1, 1024 * 1 * 1)
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x
    """
    return code

def get_calculator_code():
    code = """

# --- 🔰 Library Imports ---
import cv2             # OpenCV library for image processing and webcam integration
import mediapipe as mp # MediaPipe for hand tracking
import time            # For handling button cooldown and time-based operations
import math            # For math operations (e.g., sqrt, sin, cos, etc.)
import re              # Regular expression support for expression sanitization
import numpy as np     # NumPy for array handling and image creation

# ---------------- Hand Tracking Setup ----------------
# Initialize the MediaPipe Hands solution for real-time hand landmark detection.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,     # Use video stream (not static images)
    max_num_hands=1,             # Track only one hand for simplicity
    min_detection_confidence=0.8,  # High detection confidence for accurate recognition
    min_tracking_confidence=0.8    # High tracking confidence to reduce jitter
)

# ---------------- Enhanced Button Class ----------------
class Button:
    def __init__(self, pos, text, size=(100, 100), color=(60, 60, 200)):
        self.pos = pos
        self.size = size
        self.text = text
        self.color = color
        self.last_click = 0   # Time of the last valid click for cooldown enforcement
        self.active = False   # True when button is pressed
        self.hover = False    # True when index finger is hovering

    def draw(self, img):
        x, y = self.pos
        w, h = self.size
        
        # Button glow effect: Increase brightness if hovering, decrease if active.
        base_color = tuple(min(255, c + (40 if self.hover else 0) - (40 if self.active else 0)) for c in self.color)
        
        # Shadow effect for a 3D appearance
        shadow_offset = 4
        cv2.rectangle(img, (x + shadow_offset, y + shadow_offset), 
                      (x + w + shadow_offset, y + h + shadow_offset), (30, 30, 30), cv2.FILLED)
        
        # Draw the primary button rectangle with adjusted brightness
        cv2.rectangle(img, (x, y), (x + w, y + h), base_color, cv2.FILLED)
        
        # Draw border with a glow effect when hovered
        border_color = (255, 255, 255) if self.hover else (120, 120, 120)
        cv2.rectangle(img, (x, y), (x + w, y + h), border_color, 2)
        
        # Dynamic font scaling based on the text length
        font_scale = 0.7 if len(self.text) > 2 else 1
        text_size = cv2.getTextSize(self.text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2
        cv2.putText(img, self.text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale, (255, 255, 255), 2)

    def is_clicked(self, cursor_pos, cooldown=0.5):
        x, y = self.pos
        w, h = self.size
        # Check if the cursor is within the button boundaries
        in_bound = x < cursor_pos[0] < x + w and y < cursor_pos[1] < y + h
        # Check if enough time has passed since last click to avoid accidental multi-clicks
        ready = (time.time() - self.last_click) > cooldown
        return in_bound and ready

# ---------------- Instructions Popup ----------------
def show_instructions():
    instructions = [
        "Welcome to the Futuristic Virtual Calculator!",
        "",
        "Instructions:",
        "- Hover over a button with your INDEX finger.",
        "- Pinch using your INDEX and MIDDLE finger to press the button.",
        "",
        "Supported functions and constants:",
        "+, -, *, /, ^, sqrt, sin, cos, tan, log, ln, %",
        "pi, e, (, )",
        "",
        "Other keys:",
        "- 'C': Clear the current expression.",
        "- '<-': Backspace (delete last character).",
        "- '=': Evaluate the expression.",
        "",
        "Press any key to start..."
    ]
    # Create a white background image for the popup
    popup = 255 * np.ones((600, 800, 3), dtype=np.uint8)
    y0, dy = 40, 40  # Starting y position and line spacing
    for i, line in enumerate(instructions):
        y = y0 + i * dy
        cv2.putText(popup, line, (40, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    cv2.imshow("Instructions", popup)
    cv2.waitKey(0)
    cv2.destroyWindow("Instructions")

# ---------------- Virtual Keyboard Layout and Button Initialization ----------------
# Define the keys layout as a 2D list; empty strings represent gaps in the layout.
keys = [
    ['7', '8', '9', '/', 'sqrt'],
    ['4', '5', '6', '*', '^'],
    ['1', '2', '3', '-', '<-'],
    ['0', '.', '=', '+', 'C'],
    ['(', ')', '%', 'log', 'ln'],
    ['pi', 'e', '', '', ''],
    ['sin', 'cos', 'tan', '', '']
]

buttons = []
sx, sy = 50, 170       # Starting (x,y) position for the keyboard area
bw, bh = 100, 100      # Width and height for each button
gap = 15               # Gap between buttons

# Create button objects for non-empty keys
for i, row in enumerate(keys):
    for j, key in enumerate(row):
        if key == '':
            continue  # Skip empty cells to keep layout organized
        x = sx + j * (bw + gap)
        y = sy + i * (bh + gap)
        
        # Determine color: differentiate operators from numeric keys
        # Regular expression checks for operators or functions
        is_operator = re.match(r'[+\-*/^%()]|log|ln|sqrt|sin|cos|tan|C|<-|=', key)
        color = (0, 120, 215) if is_operator else (60, 200, 100)
        buttons.append(Button((x, y), key, (bw, bh), color))

# Initialize expression and result strings
expr = ""
result = ""

# Show the instruction popup before starting the calculator
show_instructions()

# ---------------- Webcam Capture Setup ----------------
cap = cv2.VideoCapture(0)  # Open default webcam
cap.set(3, 1280)          # Set webcam resolution width to 1280
cap.set(4, 720)           # Set webcam resolution height to 720

# ---------------- Main Application Loop ----------------
while True:
    success, frame = cap.read()   # Read a frame from the webcam
    if not success:
        continue    # Skip frame if there was an error in reading
    
    frame = cv2.flip(frame, 1)      # Mirror the frame for a natural user experience
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB for MediaPipe processing
    results = hands.process(rgb)    # Get hand landmark predictions from MediaPipe
    
    # Reset visual states for all buttons for the new frame
    for btn in buttons:
        btn.hover = False
        btn.active = False

    # ---------------- Process Hand Landmarks ----------------
    if results.multi_hand_landmarks:
        # Consider only the first detected hand for simplicity
        hand = results.multi_hand_landmarks[0]
        h, w, _ = frame.shape
        
        # Retrieve the coordinates for the index finger tip and middle finger tip
        ix = int(hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * w)
        iy = int(hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * h)
        mx = int(hand.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * w)
        my = int(hand.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * h)
        # Calculate distance between index and middle finger tips for "pinch" detection
        pinch_dist = math.hypot(ix - mx, iy - my)
        
        # Draw hand landmarks and connections for visual feedback (from MediaPipe documentation)
        mp.solutions.drawing_utils.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
        
        # ---------------- Button Interaction Handling ----------------
        for btn in buttons:
            # Check if the index finger tip is hovering over the button
            if btn.is_clicked((ix, iy), cooldown=0.5):
                btn.hover = True
                # When pinch distance is small (<40 pixels), consider it a click
                if pinch_dist < 40:
                    btn.last_click = time.time()  # Update last clicked time for debounce
                    key = btn.text
                    btn.active = True             # Change button color to show active state
                    
                    # Process the button press
                    if key == 'C':
                        expr = ""
                        result = ""
                    elif key == '<-':
                        expr = expr[:-1]
                    elif key == '=':
                        try:
                            # Preprocess the expression:
                            safe_expr = expr.replace('^', '**')  # Replace caret operator with Python exponentiation
                            safe_expr = safe_expr.replace('sqrt', 'math.sqrt')
                            mapping = {
                                'sin': 'math.sin',
                                'cos': 'math.cos',
                                'tan': 'math.tan',
                                'log': 'math.log10',
                                'ln': 'math.log',
                                'pi': 'math.pi',
                                'e': 'math.e'
                            }
                            pattern = r'sin|cos|tan|log|ln|pi|e'
                            safe_expr = re.sub(pattern, lambda m: mapping[m.group()], safe_expr)
                            safe_expr = safe_expr.replace('%', '/100')
                            # Remove any disallowed characters for added safety
                            safe_expr = re.sub(r'[^0-9+\-*/().a-zA-Z_]', '', safe_expr)
                            # Evaluate the expression safely with limited builtins and using math module
                            result = str(round(eval(safe_expr, {"math": math, "__builtins__": None}), 10))
                            expr = result  # Allow continuous calculation with the result as new input
                        except Exception:
                            result = "Error"
                    else:
                        expr += key  # Append number/operator to the expression
    
    # ---------------- Drawing the Interface ----------------
    # Draw the display area background for the expression/result
    display_x = sx
    display_y = 30
    display_width = 5 * (bw + gap) - gap  # Adjust width to span the top row of keys
    display_height = 120
    cv2.rectangle(frame, (display_x, display_y), (display_x + display_width, display_y + display_height), (20, 20, 30), cv2.FILLED)
    cv2.putText(frame, f"Expr: {expr}", (display_x + 10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (200, 255, 255), 2)
    cv2.putText(frame, f"Result: {result}", (display_x + 10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (200, 255, 200), 2)
    
    # Draw every button onto the frame
    for btn in buttons:
        btn.draw(frame)
    
    # ---------------- Show the Final Output ----------------
    cv2.imshow("Futuristic Calculator", frame)
    # Exit when the user presses the ESC key (ASCII 27)
    if cv2.waitKey(1) & 0xFF == 27:
        break

# ---------------- Cleanup ----------------
cap.release()               # Release the webcam resource
cv2.destroyAllWindows()     # Close all OpenCV windows

    """
    return code
