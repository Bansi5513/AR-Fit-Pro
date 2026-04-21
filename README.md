# AR-Fit-Pro

An AI-powered fitness tracking desktop app built with Python and Flet.  
Uses computer vision to count exercise reps in real time and visualizes workout progress across daily, weekly, and monthly timelines.

---

## What it does

AR-Fit-Pro tracks your workouts using your camera — no wearables needed.  
It detects body pose in real time, counts repetitions automatically, and logs your progress over time with interactive charts.

**Supported exercises:**
- Bicep curls
- Squats

**Dashboard views:**
- Today's session summary
- Weekly progress charts
- Monthly performance trends

---

## Tech stack

| Layer | Technology |
|---|---|
| UI / Desktop app | [Flet](https://flet.dev) (Flutter-based Python framework) |
| Computer vision | OpenCV · MediaPipe |
| Data visualization | Matplotlib |
| Language | Python 3.x |

---

## Project structure

```
AR-Fit-Pro/
├── app.py           # App entry point
├── main.py          # Core logic
├── views.py         # UI views
├── pages/           # Multi-page Flet screens
├── assets/          # Images, audio, badges
└── README.md
```

---

## How to run

```bash
# Clone the repo
git clone https://github.com/Bansi5513/AR-Fit-Pro.git
cd AR-Fit-Pro

# Install dependencies
pip install flet opencv-python mediapipe matplotlib

# Run the app
python app.py
```

---

## Key learnings

- Integrating real-time computer vision into a desktop Python app
- Building multi-page UI layouts with Flet
- Tracking and visualizing time-series workout data with Matplotlib

---

## Developer

**Bansi Patel** · [LinkedIn](https://www.linkedin.com/in/bansi-patel-43809226a) · [GitHub](https://github.com/Bansi5513)
