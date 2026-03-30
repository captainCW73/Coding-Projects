import cv2
import numpy as np
import sys

try:
    import mediapipe as mp
    from mediapipe import solutions
    print("MediaPipe loaded successfully!")
except Exception as e:
    print(f"Error loading MediaPipe: {e}")
    sys.exit(1)

# Initialize MediaPipe solutions
mp_hands = solutions.hands
mp_pose = solutions.pose
mp_face_mesh = solutions.face_mesh
mp_drawing = solutions.drawing_utils
mp_drawing_styles = solutions.drawing_styles

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    print("Error: Cannot open camera")
    sys.exit(1)

print("=" * 60)
print("FULL BODY TRACKING STARTED!")
print("=" * 60)
print("\nTracking:")
print("- Hands (21 landmarks each)")
print("- Upper body pose (shoulders, arms, torso)")
print("- Face mesh (468 landmarks)")
print("\nPress 'q' to quit\n")

# Configure tracking
with mp_hands.Hands(
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_hands=2) as hands, \
    mp_pose.Pose(
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose, \
    mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        # Flip horizontally for selfie view
        image = cv2.flip(image, 1)
        h, w, c = image.shape
        
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        
        # Process all detections
        hand_results = hands.process(image_rgb)
        pose_results = pose.process(image_rgb)
        face_results = face_mesh.process(image_rgb)
        
        image_rgb.flags.writeable = True
        
        # Draw POSE (upper body only - no legs)
        if pose_results.pose_landmarks:
            # Only draw upper body landmarks (0-16, excluding legs)
            # 0: nose, 1-10: eyes/ears/mouth, 11-16: shoulders/elbows/wrists
            for idx, landmark in enumerate(pose_results.pose_landmarks.landmark):
                if idx <= 16:  # Upper body only
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)
                    
                    # Different colors for different body parts
                    if idx <= 10:  # Head/face area
                        color = (255, 200, 0)
                        radius = 4
                    else:  # Shoulders/arms
                        color = (0, 200, 255)
                        radius = 6
                    
                    cv2.circle(image, (x, y), radius, color, -1)
            
            # Draw upper body connections
            upper_body_connections = [
                (11, 12),  # Shoulders
                (11, 13), (13, 15),  # Left arm
                (12, 14), (14, 16),  # Right arm
                (11, 23), (12, 24),  # Torso to hips (partial)
                (0, 1), (1, 2), (2, 3), (3, 7),  # Face right
                (0, 4), (4, 5), (5, 6), (6, 8),  # Face left
            ]
            
            for connection in upper_body_connections:
                start_idx, end_idx = connection
                if start_idx <= 24 and end_idx <= 24:  # Only upper body
                    start = pose_results.pose_landmarks.landmark[start_idx]
                    end = pose_results.pose_landmarks.landmark[end_idx]
                    
                    start_point = (int(start.x * w), int(start.y * h))
                    end_point = (int(end.x * w), int(end.y * h))
                    
                    cv2.line(image, start_point, end_point, (0, 255, 255), 2)
        
        # Draw FACE MESH
        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                # Draw face mesh with thin lines
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())
                
                # Draw contours (thicker)
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())
                
                # Draw irises (eyes)
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style())
        
        # Draw HANDS
        if hand_results.multi_hand_landmarks:
            for hand_idx, hand_landmarks in enumerate(hand_results.multi_hand_landmarks):
                # Get handedness
                handedness = hand_results.multi_handedness[hand_idx].classification[0]
                hand_label = handedness.label
                
                # FIX: Flip the label since image is flipped
                if hand_label == "Left":
                    hand_label = "Right"
                elif hand_label == "Right":
                    hand_label = "Left"
                
                # Draw hand connections
                for connection in mp_hands.HAND_CONNECTIONS:
                    start_idx = connection[0]
                    end_idx = connection[1]
                    
                    start = hand_landmarks.landmark[start_idx]
                    end = hand_landmarks.landmark[end_idx]
                    
                    start_point = (int(start.x * w), int(start.y * h))
                    end_point = (int(end.x * w), int(end.y * h))
                    
                    # Thick green lines for fingers
                    cv2.line(image, start_point, end_point, (0, 255, 0), 3)
                
                # Draw hand landmarks
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)
                    
                    if idx == 0:  # Wrist
                        color = (255, 0, 255)
                        radius = 8
                    elif idx in [4, 8, 12, 16, 20]:  # Fingertips
                        color = (0, 0, 255)
                        radius = 10
                    else:  # Other joints
                        color = (0, 255, 255)
                        radius = 6
                    
                    cv2.circle(image, (x, y), radius, color, -1)
                    cv2.circle(image, (x, y), radius + 2, (255, 255, 255), 2)
                
                # Display hand label
                wrist = hand_landmarks.landmark[0]
                label_x = int(wrist.x * w)
                label_y = int(wrist.y * h) - 30
                
                cv2.putText(image, f"{hand_label} Hand", 
                           (label_x - 80, label_y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 3)
                cv2.putText(image, f"{hand_label} Hand", 
                           (label_x - 80, label_y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                # Count extended fingers
                fingers_up = []
                
                # Thumb (fixed for flipped image)
                if hand_label == "Right":
                    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
                        fingers_up.append(1)
                    else:
                        fingers_up.append(0)
                else:
                    if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x:
                        fingers_up.append(1)
                    else:
                        fingers_up.append(0)
                
                # Other fingers
                finger_tips = [8, 12, 16, 20]
                finger_pips = [6, 10, 14, 18]
                
                for tip, pip in zip(finger_tips, finger_pips):
                    if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
                        fingers_up.append(1)
                    else:
                        fingers_up.append(0)
                
                finger_count = sum(fingers_up)
                
                # Display finger count
                cv2.putText(image, f"Fingers: {finger_count}", 
                           (label_x - 80, label_y - 40),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 3)
                cv2.putText(image, f"Fingers: {finger_count}", 
                           (label_x - 80, label_y - 40),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)
        
        # Display status and legend
        cv2.putText(image, "Full Body Tracking - Press 'q' to quit", (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 4)
        cv2.putText(image, "Full Body Tracking - Press 'q' to quit", (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Legend
        cv2.putText(image, "Green=Hands | Cyan=Face | Yellow/Cyan=Body | Red=Fingertips", 
                   (20, h - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Show image
        cv2.imshow('Full Body Tracking', image)
        
        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Cleanup
cap.release()
cv2.destroyAllWindows()
print("\nBody tracking stopped.")