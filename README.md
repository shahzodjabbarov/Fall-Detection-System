# Fall Detection Program

This project is a computer vision-based Fall Detection system designed to monitor and detect if a person has fallen in a home environment. Upon detecting a fall, it sends a notification to a designated person's phone to alert them.

![CareGuard_Team3](https://github.com/user-attachments/assets/ed308981-1756-4642-bfe5-738e80a80821)


## Features

- **Fall Detection:** Utilizes computer vision to detect falls based on contour analysis and angle measurement.
- **Real-Time Monitoring:** Continuously processes video frames to identify potential falls.
- **Notification System:** Sends push notifications to a user's mobile device via Pushover.
- **Video Recording:** Saves the output video with the fall detection overlay.

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- NumPy
- pushover (`pushover`)

To install the required dependencies, run:
```bash
pip install opencv-python-headless numpy pushover-python
```

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd fall-detection-program
   ```

2. Install the necessary packages:
   ```bash
   pip install opencv-python-headless numpy pushover-python
   ```

3. Update your Pushover credentials in the code:
   ```python
   api_token = 'your_api_token'
   user_key = 'your_user_key'
   ```

4. Place the input video file in the project directory and specify the file path:
   ```python
   cap = cv2.VideoCapture("path_to_your_video.MOV")
   ```

## Usage

1. Run the program:
   ```bash
   python fall_detection.py
   ```

2. The system will process the video frames, detect falls, and overlay notifications on the frame when a fall is detected.

3. A push notification is sent to the configured phone with an alert message when a fall is detected.

## Notifications

The program integrates with the [Pushover API](https://pushover.net/) to send mobile notifications. A sample message format is:
> "Our computer vision system has detected on [timestamp] that your grandpa might need help! Be sure to check on them! (This could be a false alarm)."

## Customization

- **Threshold Values:** Adjust parameters such as `minArea`, `minAngle`, and `maxAngle` to fine-tune the fall detection logic.
- **Notification Message:** Modify the `message` variable to customize the alert text.

## Output

- The modified video with detection overlays is saved as `output.mp4`.
- Notifications are sent when a fall is detected.

## Example Output

![Sample Fall Detection Frame](image.jpg)

## License

This project is open-source and available under the [MIT License](LICENSE).

## Acknowledgements

This project was built using:
- [OpenCV](https://opencv.org/) for computer vision processing
- [NumPy](https://numpy.org/) for numerical computations
- [Pushover](https://pushover.net/) for notification services

