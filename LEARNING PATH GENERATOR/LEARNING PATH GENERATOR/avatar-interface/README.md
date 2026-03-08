# AI Algorithm Instructor - 3D Interface (AI Optimized)

This is a premium, 3D AI teaching avatar interface designed for the Algorithm Learning Path Generator. It features a realistic 3D avatar that interacts with users through natural speech, facial expressions, and real-time feedback driven by a locally trained AI model.

## Features
- **Professional Male Avatar**: Upgraded to a high-fidelity male instructor (Real-time Human-like mode).
- **Dual AI Brain**:
  - **Local Model**: Fallback mode for basic analysis.
  - **Gemini Pro Integration**: High-fidelity analysis providing "Perfect Code", "Mistake Breakdown", and "Concept Explanations".
- **Dynamic Feedback System**:
  - Prints "Perfect Code" for correct algorithms.
  - Explains the target problem in simple terms.
  - Pinpoints specific logic errors.
- **Lip Synchronization**: Real-time mouth movement while speaking.
- **Glassmorphic UI**: Cinematic studio background with responsive code highlighting.

## How to Run
To run the full intelligent platform, you need to start two systems:

1.  **Start the AI Brain (Backend)**:
    ```bash
    # In the main folder
    python app.py
    ```
2.  **Start the 3D Interface (Frontend)**:
    ```bash
    # In the avatar-interface folder
    python -m http.server 8000
    ```
    Then open **[http://localhost:8000](http://:8000)** in your browser.

## Accuracy & Training
The AI is trained on `dataset.csv`. To improve itlocalhosts accuracy:
1.  Add more examples to `dataset.csv`.
2.  Run `python train_model.py` to update the model weights.
3.  Restart `app.py`.

## Environment Variables
For premium AI features, set your Gemini API key:
```bash
set GEMINI_API_KEY=your_key_here
python app.py
```

## Integration with Backend
The frontend connects to the AI backend at `http://localhost:5000/evaluate`. It expects an enhanced JSON response:
```json
{
  "feedback": "Spoken feedback string",
  "type": "correct/incorrect",
  "perfect_code": "The ideal Python implementation",
  "explanation": "Detailed breakdown of mistakes/logic",
  "question_explanation": "Simple explanation of what the problem is"
}
```
Possible types: `"correct"`, `"incorrect"`, `"thinking"`, `"neutral"`.

