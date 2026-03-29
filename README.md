
A 2D space shooter game built using Python and Pygame, featuring real-time gameplay, enemy AI, particle effects, and a structured multi-file architecture
Overview:
This project is a classic arcade-style space shooter where the player controls a spaceship, shoots enemies, and survives as long as possible while maximizing score.
The game was built to explore:
* Game development fundamentals
* Object-oriented programming
* Real-time event handling
* Modular software design
  
Features:
Core Gameplay
* Smooth player movement
* Shooting mechanics with cooldown system
* Enemy spawning and movement patterns
* Collision detection system
* Score tracking
Visual Effects
* Particle explosion effects
* Dynamic starfield background
* Clean 2D rendering using Pygame
Game Systems
* Multiple game states (Menu, Playing, Pause)
* Difficulty scaling through enemy behavior
* High score saving using JSON
Architecture
* Modular code structure (multiple files)
* Separation of concerns (player, enemies, effects, config)
* Maintainable and scalable design
Tech Stack
* **Python 3**
* **Pygame**
* **JSON** (for persistent storage)
Project Structure

## Space-Shooter/

* ├── config.py          # Constants and settings
* ├── effects.py         # Particles and visual effects
* ├── game.py            # Game state and core logic
* ├── game_objects.py    # Enemies and bullets
* ├──high_score.json    # Persistent high score
* ├── main.py            # Entry point and game loop
* ├── player.py          # Player mechanics
* ├── game.py            # Game state and core logic
* ├── player.py          # Player mechanics
* ├── requirements.txt   # Dependencies
* └──sound.py           # Sound system (experimental)


---

##  How to Run

### 1. Clone the repository

```bash
git clone https://github.com/HarsitCH/Space-Shooter.git
cd Space-Shooter
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the game

```bash
python main.py
```

---

## Controls

* ⬅️ / ➡️ → Move
* SPACE → Shoot
* P → Pause / Resume
* ENTER → Start Game

---

##  Screenshots

<img width="600" height="835" alt="image" src="https://github.com/user-attachments/assets/79a85665-0fef-4b79-87b5-07209ab44a0e" />
<img width="595" height="843" alt="image" src="https://github.com/user-attachments/assets/d5e6cba8-ea12-4842-8cf2-b424a104b8b2" />
<img width="597" height="835" alt="image" src="https://github.com/user-attachments/assets/ec0aa4ef-4ed4-40a9-a5c4-a1ddb6e24fcc" />
<img width="597" height="832" alt="image" src="https://github.com/user-attachments/assets/36bdd5aa-b5dc-4088-a4fe-cf73d038d26c" />

---

##  Future Improvements

* Improved enemy AI
* Boss battles
* Sound system enhancements
* Power-ups and abilities
* UI improvements

---

##  Author

Developed as a personal project to strengthen skills in:

* Game development
* Object-oriented programming
* Software design

---

## Notes

This project focuses on clean and simple structure and gameplay systems rather than complex graphics, making it a strong foundation for future game development projects.

