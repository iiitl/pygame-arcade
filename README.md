# Pygame Arcade 

Pygame Arcade is a collection of three simple games built using Pygame.

---

## About Pygame

Pygame is a free and open-source library used for building 2D games. It provides simple tools to handle graphics, sounds, and user input (like keyboard and mouse), so you can focus on game logic without dealing with low-level details.

--- 

## Games Included 

- Snake
- Flappy Bird
- Space Shooter

Each game is kept separate under games folder so it's easier to read the code and make changes if you want to experiment.
--- 

## Repository Structure

```
pygame-arcade/
├── launcher.py # Main menu to select games
├── games/
│   ├── snake/ # Snake game implementation
│   ├── flappy/ # Flappy Bird game implementation
│   └── shooter/ # Space Shooter game implementation
├── common/
├── assets/ # used images and other resources
├── requirements.txt #Project dependencies
```

--- 

## Prerequisites 

- python 3.x installed
- Basic understanding of python (recommended)

--- 

## Setup

Install the required dependencies:

```
pip install -r requirements.txt
```
---

## Run the project

Run the launcher to choose a game:
```
python launcher.py
```
This will open a simple menu where you can pick a game.


## Contributing

If you want to contribute, feel free to:

- Fix bugs
- Improve code structure
- Add small features
- Improve documentation 

Please follow the steps in [CONTRIBUTING.md](./CONTRIBUTING.md) to contribute to this project.
