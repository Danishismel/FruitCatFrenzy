# Fruit Cat Frenzy 🐱🍉

A 2D arcade catching game developed in Python using Pygame-CE. Players control a basket to catch falling fruit cats within a 60-second timer while avoiding dangerous bombs.

---

## 🎮 Game Features
- **Object-Oriented Architecture (OOP):** Modular design utilizing dedicated classes (`Player`, `Item`, `ScoreFeedback`, `LevelMessage`, `Countdown`).
- **Dynamic Difficulty:** 3 difficulty levels with increasing fall speed and spawn rates at 40s and 20s remaining.
- **Bilingual Interface (EN / BM):** Real-time language toggle switching between English and Bahasa Melayu across all menus, HUD, and dialogs.
- **Visual Feedback & Polish:** 
  - Dynamic visual stack of caught fruit cats inside the basket.
  - Floating score indicators (`+10`, `+15`, `+20`, `-1 LIFE`).
  - Pre-round countdown timer (`3, 2, 1, GO!`).
- **Audio-Safe Architecture:** Failsafe audio system that gracefully handles environments without connected audio output devices.

---

## 🍎 Scoring & Rules

| Entity | Action | Points / Effect |
| :--- | :--- | :--- |
| **Watermelon** | Caught | +10 Points |
| **Pineapple** | Caught | +10 Points |
| **Grape** | Caught | +15 Points |
| **Strawberry** | Caught | +20 Points |
| **Bomb** | Caught | -1 Life |
| **Any Fruit** | Missed (Falls off screen) | -1 Life |
| **Bomb** | Missed (Falls off screen) | No Penalty |

- **Starting Lives:** 5 Lives
- **Round Duration:** 60 Seconds
- **Win Condition:** Survive the full 60 seconds with at least 1 life remaining.
- **Loss Condition:** Reach 0 lives.

---

## 🕹️ Controls

| Key | Action |
| :--- | :--- |
| `LEFT ARROW` | Move Basket Left |
| `RIGHT ARROW` | Move Basket Right |
| `P` | Pause / Resume Game |
| `R` | Restart Round (After Game Over) |
| `Q` | Quit Game (After Game Over) |

---

## 📁 Project Structure

```text
FruitCatFrenzy/
├── assets/
│   ├── background.jpg
│   ├── basket.png
│   ├── watermelon.png
│   ├── pineapple.png
│   ├── grape.png
│   ├── strawberry.png
│   ├── bomb.png
│   ├── meow.wav
│   ├── bomb.wav
│   ├── miss.wav
│   └── gameover.wav
├── main.py
├── requirements.txt
├── .gitignore
└── README.md