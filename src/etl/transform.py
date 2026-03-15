import cv2
import numpy as np

def transform_video_to_sequences(video_path, seq_length=10, target_fps=15):
    cap = cv2.VideoCapture(video_path)
    src_fps = cap.get(cv2.CAP_PROP_FPS)
    skip_rate = max(1, int(src_fps / target_fps))
    
    frames = []
    sequences = []
    
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        if count % skip_rate == 0:
            # Resize and normalize for MobileNetV2/CNN backbone
            frame = cv2.resize(frame, (224, 224)) / 255.0
            frames.append(frame)
            
            if len(frames) == seq_length:
                sequences.append(np.array(frames))
                frames = frames[seq_length // 2:] # 50% overlap for smoother temporal learning
        count += 1
    cap.release()
    return np.array(sequences) # Shape: (Num_Seqs, 10, 224, 224, 3)