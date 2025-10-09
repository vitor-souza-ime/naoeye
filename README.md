# 🤖 NAO Eye Detection

This project detects whether a person's eyes are **open or closed** in real time using the **NAO robot’s camera**.  
The detection is powered by **MediaPipe FaceMesh**, while communication with the robot is handled through the **Qi Framework (qi)**.  
The NAO can also **speak the eye status** using its text-to-speech service (`ALTextToSpeech`).

---

## 🧠 Overview

The system captures images directly from the NAO’s camera and processes each frame using **MediaPipe FaceMesh** to locate the eyes.  
Based on the **facial landmarks**, it computes the **Eye Aspect Ratio (EAR)** to determine whether the eyes are open or closed.

- EAR ≥ 0.2 → 👁️ **EYES OPEN**
- EAR < 0.2 → 😴 **EYES CLOSED**

The result is displayed on the screen and can optionally be spoken by the NAO.

---

## 📂 Project Structure

```

naoeye/
│
├── main.py          # Main Python script
├── requirements.txt # Project dependencies (optional)
└── README.md        # This file

````
## ⚙️ Requirements

### Hardware
- **NAO robot** (connected to the same network)
- Functional **NAO camera**

### Software
- **Python 3.8+**
- Required Python packages:
  ```bash
  pip install qi opencv-python mediapipe numpy scipy
````

### Optional `requirements.txt`

```txt
qi
opencv-python
mediapipe
numpy
scipy
```

---

## 🚀 How to Run

1. **Clone the repository**

   ```bash
   git clone https://github.com/vitor-souza-ime/naoeye
   cd naoeye
   ```

2. **Set your NAO’s IP address**
   Edit `main.py` and replace:

   ```python
   NAO_IP = "172.15.4.178"   # Replace with your NAO’s IP address
   ```

3. **Run the program**

   ```bash
   python main.py
   ```

4. **Controls**

   * Press `q` → Quit the program
   * Press `s` → Save the current frame as an image

---

## 🧩 How It Works

The program performs the following steps:

1. Connects to the NAO using `qi.Session`.
2. Subscribes to the robot’s camera via `ALVideoDevice`.
3. Processes each frame with `mediapipe.solutions.face_mesh`.
4. Computes the **Eye Aspect Ratio (EAR)** for both eyes.
5. Displays the result and optionally makes the NAO speak.

---

## 🧠 EAR Formula

The **Eye Aspect Ratio (EAR)** is defined as:

[
EAR = \frac{||p2 - p6|| + ||p3 - p5||}{2 \times ||p1 - p4||}
]

Where:

* p1–p6 are the landmark points outlining each eye in the **FaceMesh** model.

A smaller EAR value indicates **closed eyes**.

---

## 🗣️ NAO Interaction

The script uses several NAO services:

* **`ALTextToSpeech`** – allows the robot to speak (“EYES OPEN” or “EYES CLOSED”)
* **`ALMotion`** – sets the robot’s body stiffness to `0.0` (relaxed state)

> 💡 To enable speech output, uncomment the line:
>
> ```python
> # tts_service.say(status)
> ```

---

## 📸 Example Output

In the video window:

```
EYES OPEN (EAR: 0.26)
```

or, when closed:

```
EYES CLOSED (EAR: 0.12)
```

Each detected eye is marked with green dots for visualization.

---

## 🧑‍💻 Author

**Prof. Vitor Amadeu Souza**
📍 [GitHub](https://github.com/vitor-souza-ime)

---

## 📜 License

This project is released under the **MIT License**.
You are free to use, modify, and distribute it with proper attribution.

---

## 💬 Notes

* Tested with **MediaPipe 0.10+** and **Python 3.11**.
* You may need to adjust the camera index in `subscribeCamera()` depending on your NAO version.
* Detection accuracy depends on lighting conditions and face positioning.

---
