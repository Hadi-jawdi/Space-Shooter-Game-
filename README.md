# Space Shooter Game

A classic space shooter game built with Python and Pygame. Defend Earth from alien invaders by shooting down enemies, collecting power-ups, and achieving the highest score possible!

## Features

- **Player Controls**: Move left and right, shoot bullets at enemies
- **Enemies**: Randomly spawning alien ships that shoot back
- **Power-ups**:
  - **Life**: Increases your lives
  - **Rapid Fire**: Temporarily increases shooting speed
  - **Shield**: Provides temporary invincibility
- **Scoring System**: Earn points by destroying enemies and collecting power-ups
- **Lives System**: Start with 3 lives, lose one when hit by enemies or bullets
- **Game Over & Restart**: Restart the game after losing all lives
- **Animated Background**: Scrolling stars for immersive space atmosphere

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   Or install Pygame directly:

   ```bash
   pip install pygame
   ```

## How to Run

Run the game using Python:

```bash
python space_shooter.py
```

## Controls

- **Left Arrow**: Move player left
- **Right Arrow**: Move player right
- **Spacebar**: Shoot bullets
- **R**: Restart game (when game over)

## Gameplay

- Your goal is to survive as long as possible and achieve the highest score.
- Move your blue spaceship to avoid enemy bullets and collisions.
- Shoot yellow bullets to destroy red enemy ships.
- Collect falling power-ups to gain advantages:
  - Green squares: Extra life
  - Yellow squares: Rapid fire (5 seconds)
  - Blue squares: Shield protection (5 seconds)
- The game ends when you lose all 3 lives.
- Press R to restart and try for a better score!

## Game Mechanics

- **Enemies**: Spawn every second, move downward at varying speeds, and shoot red bullets randomly.
- **Collisions**:
  - Player bullets destroy enemies (+10 points)
  - Enemy bullets or collisions reduce player lives
  - Player can collect power-ups for bonuses
- **Power-up Effects**:
  - Life: +1 life, +5 points
  - Rapid Fire: Faster shooting for 5 seconds, +5 points
  - Shield: Invincibility for 5 seconds, +5 points

## Screenshots

*(Add screenshots here if available)*

## Contributing

Feel free to fork this project and submit pull requests with improvements!

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

Created with ❤️ using Python and Pygame.
# Space-Shooter-Game-
