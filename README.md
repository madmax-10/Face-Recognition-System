# Face Recognition System

A Python-based personal assistant and real-time face recognition application. Leverages OpenCV and the `face_recognition` library for live camera capture, identification, and user enrollment—augmented with voice interaction via `pyttsx3` and `SpeechRecognition`.

---

## 🚀 Features

* **Real-time face detection & recognition** from your webcam
* **Voice-driven interface**: text-to-speech prompts and speech-to-text commands
* **Dynamic user enrollment**: add new profiles on the fly
* **Configurable admin credentials & IDs** via a simple text file
* **Modular scripts** for encoding management, ID mapping, and the main assistant

---

## 📂 Repository Structure

```
Face-Recognition-System/
├── AdminInfos.txt          # Admin password & last used ID
├── Photos/                 # Folder of face images (one file per person, named <ID>.jpg/.png)
├── knownEncodings.pkl      # Serialized face-encoding dictionary
├── knownIDs.pkl            # Serialized ID→name mapping
├── updateEncodings.py      # Build or refresh `knownEncodings.pkl` from `Photos/`
├── updateIDs.py            # Initialize or reset `knownIDs.pkl`
├── camera.py               # Core Camera class for capture, detection, and enrollment
├── main.py                 # Voice-assistant entry point—handles verification & command flow
└── requirements.txt        # Python dependencies
```

---

## 🛠️ Prerequisites

* Python 3.7+
* pip
* PortAudio (for PyAudio; e.g., `brew install portaudio` on macOS)

---

## 📥 Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/madmax-10/Face-Recognition-System.git
   cd Face-Recognition-System
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare your dataset**

   * Create a `Photos/` directory.
   * Add one image per person, named with a unique numeric ID (e.g., `1001.jpg`, `1002.png`).

4. **Configure admin credentials**

   * Open `AdminInfos.txt` and set:

     ```text
     your_secure_password
     10000
     ```

     * Line 1: Admin password for identity verification.
     * Line 2: Last assigned numeric ID; increments automatically on enrollment.

---

## ⚙️ Initialization

Before running the assistant for the first time:

1. **Generate face encodings**

   ```bash
   python updateEncodings.py
   ```

   Scans `Photos/` and creates `knownEncodings.pkl`.

2. **Initialize ID mappings**

   ```bash
   python updateIDs.py
   ```

   Creates an empty `knownIDs.pkl` for storing ID → name pairs.

---

## 🎬 Usage

1. **Launch the Assistant**

   ```bash
   python main.py
   ```

2. **Verification**

   * You’ll be prompted (via voice) to verify your identity.
   * The camera window appears—press **c** to capture your image.
   * If recognized, you’re greeted by name and real-time recognition begins.

3. **Adding New Users**

   * If no face is recognized, you’ll be asked if you’d like to enroll.
   * Say **yes** or **no**.
   * For **yes**, specify how many profiles to create (spoken number), then type each person’s name.
   * The camera feed returns to let you capture each new face (press **c** for each).

4. **Live Recognition Mode**

   * After verification or enrollment, the app continuously detects faces.
   * Bounding boxes and confidence scores appear on the video feed.
   * Speak commands at any time: e.g., “stop” to exit.

---

## ⚙️ Configuration Details

**AdminInfos.txt**

```text
your_secure_password
10000
```

* Line 1: Admin password for identity verification.
* Line 2: Last assigned numeric ID; increments automatically on enrollment.

**requirements.txt**
Lists all Python libraries (e.g., `face_recognition`, `pyttsx3`, `SpeechRecognition`, etc.).

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch:

   ```bash
   ```

git checkout -b feature/YourFeature

````
3. Commit your changes:
```bash
git commit -m "Add awesome feature"
````

4. Push your branch:

   ```bash
   ```

git push origin feature/YourFeature

```
5. Open a Pull Request

Please update `requirements.txt` and document any new scripts or modules in this `README.md`.

---

## 📄 License

This project is currently unlicensed. To open-source it, add an OSI-approved license (e.g., MIT) in a `LICENSE` file and update this section accordingly.

```
