# 🤖 Robot Adventures

**Robot Adventures** is a beginner-friendly 2D platformer game built with Python and Pygame.  
This project is designed to help learners understand the fundamentals of how games work, including input handling, physics, animation, and basic AI.

## 🕹️ Gameplay Overview

You control a robot on a coin-collecting mission across an increasingly dangerous platform world.  
Avoid explosives, dodge poison, and outsmart enemy bots. As levels progress, new challenges arise — but so do your powers!

**Abilities:**

- Move: `←` and `→` arrow keys  
- Jump: `↑` arrow key  
- Kick attack: `A` (only after acquiring the ability)  
- Pause/Resume: `Left Ctrl`

## 📦 Requirements

- Python 3.10+
- [Pygame](https://www.pygame.org/)

You can install all dependencies using the provided `requirements.txt`.

---

## 🔧 Setup Instructions

1. **Download the game source code**

   If you're not familiar with Git, follow these steps to download the project manually:

   - Click the green **Code** button
   - Select **Download ZIP**
   - Extract the ZIP file to your computer

   Then open the extracted folder in your terminal or command prompt and continue with the steps below.


2. **Create a virtual environment (recommended)**
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**

   - On **Windows**:
     - If using **Command Prompt**:
       ```bash
       venv\Scripts\activate.bat
       ```
     - If using **PowerShell**:
       ```powershell
       .\venv\Scripts\Activate.ps1
       ```

   - On **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
5. **Run the game**
    ```bash
    python main.py
    ```


## 📚 Educational Purpose
This game was created as part of a book project to teach beginners the basics of game development using Python.
If you're following the book, use this project to explore how different components work together to create a full game.

## 🎨 Credits
Sprites and tilesets: Kenney.nl

Sound effects: Pixabay

Example assets: Bundled with Pygame