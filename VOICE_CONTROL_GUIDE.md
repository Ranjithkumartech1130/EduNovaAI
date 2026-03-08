# Voice-Controlled IDE - User Guide

## 🎤 Overview

The SkillGPS IDE now features **fully voice-controlled coding** that allows you to dictate code line by line with intelligent syntax handling. The system automatically converts spoken words into proper code syntax, preventing common errors with punctuation, operators, and keywords.

## 🚀 Getting Started

### Activating Voice Control

1. Navigate to the **IDE & Tasks** tab in your dashboard
2. Click the red **"Voice Control"** button in the toolbar
3. Allow microphone access when prompted by your browser
4. The button will turn green and show "Listening..." when active
5. Start speaking your code!

### Deactivating Voice Control

- Click the **"Stop Voice"** button (same button, now green)
- Or say **"stop listening"** (voice command)

## 🗣️ How to Dictate Code

### Basic Syntax

The voice control system intelligently converts spoken words to code symbols:

#### Operators
- Say **"equals"** → writes ` = `
- Say **"equal to"** → writes ` == `
- Say **"not equal"** → writes ` != `
- Say **"plus"** → writes ` + `
- Say **"minus"** → writes ` - `
- Say **"times"** → writes ` * `
- Say **"divided by"** → writes ` / `
- Say **"greater than"** → writes ` > `
- Say **"less than"** → writes ` < `

#### Punctuation
- Say **"colon"** → writes `:`
- Say **"semicolon"** → writes `;`
- Say **"comma"** → writes `,`
- Say **"period"** or **"dot"** → writes `.`
- Say **"open parenthesis"** → writes `(`
- Say **"close parenthesis"** → writes `)`
- Say **"open bracket"** → writes `[`
- Say **"close bracket"** → writes `]`
- Say **"open brace"** → writes `{`
- Say **"close brace"** → writes `}`
- Say **"quote"** → writes `"`
- Say **"single quote"** → writes `'`

#### Common Keywords
- Say **"define"** → writes `def ` (Python)
- Say **"return"** → writes `return `
- Say **"print"** → writes `print(`
- Say **"console log"** → writes `console.log(`
- Say **"const"** → writes `const `
- Say **"let"** → writes `let `
- Say **"var"** → writes `var `
- Say **"true"** → writes `true`
- Say **"false"** → writes `false`
- Say **"null"** → writes `null`

## 🎯 Voice Commands

### Code Execution
- **"run code"** - Run the current code
- **"run this code"** - Run the current code
- **"execute code"** - Run the current code

### Terminal Control
- **"open terminal"** - Open/Show the terminal panel
- **"show terminal"** - Open/Show the terminal panel
- **"close terminal"** - Close/Hide the terminal panel
- **"hide terminal"** - Close/Hide the terminal panel

### Editor Control
- **"new line"** - Insert a new line
- **"indent"** or **"tab"** - Add indentation (4 spaces)
- **"delete line"** - Delete current line
- **"clear editor"** - Clear all code
- **"undo"** - Undo last change
- **"redo"** - Redo last undone change

### Navigation
- **"go to start"** - Move cursor to beginning of file
- **"go to end"** - Move cursor to end of file
- **"next line"** - Move cursor down one line
- **"previous line"** - Move cursor up one line

### Code Snippets
- **"function"** - Insert function template
- **"class"** - Insert class template
- **"if statement"** - Insert if statement
- **"for loop"** - Insert for loop
- **"while loop"** - Insert while loop
- **"try catch"** - Insert try-catch block
- **"import"** - Insert import statement

## 📝 Example Usage

### Python Example

**You say:**
```
"define calculate sum open parenthesis numbers close parenthesis colon"
"new line"
"indent total equals zero"
"new line"
"indent for num in numbers colon"
"new line"
"indent indent total plus equals num"
"new line"
"indent return total"
```

**Result:**
```python
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
```

### JavaScript Example

**You say:**
```
"const greet user equals open parenthesis name close parenthesis arrow open brace"
"new line"
"indent console log hello comma name"
"new line"
"close brace"
```

**Result:**
```javascript
const greetUser = (name) => {
    console.log("hello", name)
}
```

## 🎨 Visual Feedback

### Voice Indicator
- **Red pulsing badge** in top-right corner shows "Listening..."
- Appears when voice control is active

### Voice Preview
- **Blue preview box** shows what you're currently saying
- Updates in real-time as you speak
- Helps you verify the system is hearing you correctly

### Button States
- **Red button** = Voice control OFF
- **Green pulsing button** = Voice control ON and listening

## ⚠️ Important Tips

### For Best Accuracy

1. **Speak clearly** and at a moderate pace
2. **Pause briefly** between commands and code
3. **Use exact command phrases** (e.g., "open parenthesis" not "left paren")
4. **Specify punctuation explicitly** - don't rely on the system to guess
5. **Say "new line"** when you want to move to the next line

### Language-Specific Features

The system adapts to your selected programming language:

- **Python**: Automatically handles `def`, `class`, proper indentation
- **JavaScript**: Recognizes `const`, `let`, `function`, arrow functions
- **Java/C++/C#**: Auto-adds semicolons where appropriate

### Troubleshooting

**Voice not being recognized?**
- Check microphone permissions in browser settings
- Ensure you're using Chrome, Edge, or Safari (best support)
- Check that your microphone is working in other apps

**Wrong symbols being inserted?**
- Speak more slowly and clearly
- Use the exact command phrases listed above
- Check the preview box to see what's being heard

**Voice control button not working?**
- Make sure you're on the IDE & Tasks tab
- Refresh the page and try again
- Check browser console for errors

## 🌐 Browser Compatibility

**Fully Supported:**
- Google Chrome (recommended)
- Microsoft Edge
- Safari (macOS/iOS)

**Not Supported:**
- Firefox (limited Web Speech API support)
- Internet Explorer

## 🔒 Privacy

- All voice processing happens **locally in your browser**
- No audio is sent to external servers
- Voice recognition uses your browser's built-in Web Speech API
- No recordings are stored

## 💡 Pro Tips

1. **Practice common phrases** - The more you use it, the faster you'll get
2. **Combine with keyboard** - Use voice for structure, keyboard for quick edits
3. **Use code snippets** - Say "function" instead of dictating the entire template
4. **Review before running** - Always check the code visually before executing
5. **Start simple** - Begin with simple statements, then move to complex code

## 🎓 Learning Resources

### Recommended Practice Flow

1. Start with simple variable declarations
2. Move to basic functions
3. Practice control structures (if, for, while)
4. Try object-oriented code (classes, methods)
5. Experiment with complex algorithms

### Sample Practice Exercises

**Beginner:**
- Declare variables with different data types
- Create simple functions with parameters
- Write basic if-else statements

**Intermediate:**
- Build classes with multiple methods
- Create loops with complex conditions
- Handle exceptions with try-catch

**Advanced:**
- Implement algorithms (sorting, searching)
- Build data structures (linked lists, trees)
- Create async functions and promises

## 📞 Support

If you encounter issues:
1. Check this guide first
2. Verify browser compatibility
3. Test your microphone in browser settings
4. Clear browser cache and reload
5. Try a different browser

---

**Happy Voice Coding! 🎤💻**
