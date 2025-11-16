# Projet2-RP - Knight's Tour Solver using Genetic Algorithm

## 📋 Project Description
This project solves the classic **Knight's Tour problem** using a **Genetic Algorithm**. The goal is to find a sequence of moves where a chess knight visits every square on an 8x8 chessboard exactly once.

## 🎯 Problem Overview
The knight moves in an "L-shaped" pattern. A knight's tour is a sequence of moves that visits all 64 squares without repeating any square. This project uses evolutionary computation to find such a sequence.

## 🧬 Algorithm Approach
We implement a genetic algorithm with the following components:

### Chromosome Representation
- Each chromosome represents a sequence of 63 moves
- Each gene is one of 8 possible knight moves
- Genetic operations: single-point crossover and mutation

### Knight Movement System
- Tracks position and visited squares
- Validates moves (no off-board or repeated visits)
- Calculates fitness based on number of unique squares visited

### Population Evolution
- Tournament selection for parent choice
- Generational replacement with elitism
- Fitness-based survival of the fittest

Expected Output
The program will:

Display the evolution process generation by generation

Show the best solution found with fitness score

Visualize the knight's tour path on the chessboard

Terminate when a perfect solution (fitness = 64) is found

🧪 Key Features
Move Validation: Automatically corrects illegal moves

Fitness Evaluation: Scores solutions based on unique squares visited

Tournament Selection: Selects best parents for reproduction

Visualization: Displays the final solution graphically

⚙️ Parameters
Population size: 50 individuals

Tournament size: 3 individuals

Chromosome length: 63 moves

Maximum fitness: 64 (perfect tour)

📈 Results
The genetic algorithm evolves populations over generations, gradually improving the knight's path until it finds a complete tour visiting all 64 squares.

👨‍💻 Author
[Your Name]
Master 1, Visual Computing
USTHB University
2025/2026

📄 License
This project is for educational purposes as part of the Visual Computing curriculum.

## How to Run
```bash
python knight-chess.py

