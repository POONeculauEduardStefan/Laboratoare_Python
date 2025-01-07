# Advanced Connect 4 Game with AI Integration

## Overview

This project presents an advanced implementation of Connect 4, enhanced with artificial intelligence (AI) capabilities, designed to provide an engaging and adaptable gameplay experience. The system supports multiplayer functionality over a network, as well as competition against an AI opponent, featuring a scalable difficulty model. The project employs Python as the core programming language, leveraging Tkinter for the graphical user interface (GUI) and socket programming for robust client-server communication.

## Features

- **Multiplayer Mode**: Facilitates head-to-head matches between two players over a network connection.
- **AI-Driven Gameplay**: Allows players to challenge an AI opponent with three distinct difficulty levels: Easy, Medium, and Hard.
- **Customizable Board Dimensions**: Users can define the number of rows and columns to tailor the gameplay experience.
- **Client GUI**: Provides an intuitive and visually appealing interface powered by Tkinter.
- **Real-Time State Synchronization**: Ensures that game states are updated instantaneously across all participants.
- **Strategic AI**: Implements advanced board evaluation and decision-making algorithms to enhance competitive play.

## Installation

### Prerequisites

Ensure that Python 3.9 or a later version is installed on your system. Since the required libraries are part of Python's standard library, no additional dependencies need to be installed.

### Setup Instructions

1. Clone the project repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Launch the server:

   ```bash
   python server.py <mode> <rows> <columns> <first>
   ```

   - `<mode>`: Specify `human` for Player vs Player or `ai` for Player vs AI gameplay.
   - `<rows>` and `<columns>`: Define the dimensions of the game board.
   - `<first>`: For AI mode, indicate the starting player (`player` or `ai`).

3. Initialize the client(s):

   ```bash
   python client.py
   ```

   Launch two clients for Player vs Player mode, or one client for Player vs AI mode.

## Gameplay Instructions

### Player vs Player Mode

1. Configure and start the server in `human` mode.
2. Connect two clients to the server.
3. Players alternate turns, selecting a column to drop their pieces by clicking on it.
4. The match concludes when one player achieves a line of four or the board is entirely filled (resulting in a draw).

### Player vs AI Mode

1. Configure and start the server in `ai` mode, specifying the starting player.
2. Select the AI difficulty level: Easy, Medium, or Hard.
3. Take turns with the AI, observing its calculated responses.

### Controls

- **Hover Functionality**: Preview the drop location of your piece.
- **Click to Place**: Finalize your move by clicking on the desired column.

## System Architecture

### Server

The server orchestrates the game logic, including board updates, win condition checks, and draw detection. It employs socket programming to facilitate:

- **Player Synchronization**: Ensuring real-time consistency between connected clients.
- **AI Integration**: Seamlessly integrating the AI module for solo gameplay.

### Client

The client manages the user interface and player interactions. Key functionalities include:

- Rendering board updates from the server.
- Sending player moves to the server.
- Displaying game outcomes and status messages.

### AI Engine

The AI engine, implemented in `aiscript.py`, employs heuristic evaluation to determine optimal moves:

- **Easy Level**: Executes random moves.
- **Medium Level**: Considers immediate consequences of potential moves.
- **Hard Level**: Simulates multiple turns ahead, leveraging strategic foresight (minmax algorithm).

### Graphical User Interface

Developed using Tkinter, the GUI comprises:

- A dynamically generated Connect 4 board.
- Real-time visual updates for player and AI moves.
- Interactive hover effects to guide player actions.

## Code Overview

### Server Initialization

```python
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 4444))
server_socket.listen(2)
```

### AI Decision-Making

```python
def solve(gametable, difficulty):
    # Implements the AI's logic to evaluate board states and select optimal moves.
    return gametable
```

### GUI Setup

```python
def create_gui(rows, cols, set_move_function, player_number):
    window = tk.Tk()
    canvas = tk.Canvas(window, width=cols * 80, height=(rows * 80 + 100), bg="blue")
    canvas.pack()
```

## Project Directory Structure

```
project-directory/
|-- aiscript.py         # AI logic
|-- client.py           # Client-side logic
|-- client_gui.py       # GUI implementation
|-- difficult_gui.py    # Difficulty selection GUI
|-- server.py           # Server-side logic
```

## Potential Enhancements

- Integrate a leaderboard to track player statistics.
- Advance AI capabilities using machine learning models.
- Enrich user experience with sound effects and animations.

