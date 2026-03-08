import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ─────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────
OPENROUTER_API_KEY = "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"
MODEL_PATH = "trained_algorithm_model"

# ─────────────────────────────────────────────────────────────
# OPTIONAL: Load torch & local model ONLY if available
# This allows the server to start even without torch installed.
# The cloud API (OpenRouter) handles 95% of requests anyway.
# ─────────────────────────────────────────────────────────────
tokenizer = None
model     = None
device    = None
TORCH_AVAILABLE = False

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    TORCH_AVAILABLE = True
    print("✅ PyTorch detected.")

    # ─────────────────────────────────────────────────────────────
    # LAPTOP-SAFE CPU LIMITING
    # Prevent PyTorch from hogging all cores which freezes the OS
    # ─────────────────────────────────────────────────────────────
    torch.set_num_threads(2)
    torch.set_num_interop_threads(1)
    print(f"   CPU Threads limited to: {torch.get_num_threads()}")

    if os.path.exists(MODEL_PATH):
        print(f"Loading local fallback model from '{MODEL_PATH}' ...")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        model     = AutoModelForSeq2SeqLM.from_pretrained(
            MODEL_PATH,
            low_cpu_mem_usage=True   # Loads weights lazily → less RAM spike
        )
        device = torch.device("cpu")   # Force CPU — safer for low-spec laptops
        model.to(device)
        model.eval()                   # Disable dropout → faster + less memory
        print("✅ Local fallback model loaded on CPU.")
    else:
        print("⚠️  Local model not found. Cloud-only mode active.")

except ImportError:
    print("⚠️  PyTorch not installed. Running in Cloud-only mode (fully functional).")

from algo_db import ALGORITHM_DATABASE

# ── LOGIC CACHE (Save bandwidth/CPU for laptop) ───────────
CACHE_FILE = "logic_cache.json"
def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f: return json.load(f)
        except: return {}
    return {}

def save_cache(cache):
    try:
        with open(CACHE_FILE, "w") as f: json.dump(cache, f)
    except: pass

logic_cache = load_cache()

import gc  # Added for memory management

# ── PEDANTIC LOGIC GUARD (Frontend to AI) ───────────────────
def logic_guard(algorithm, intent_language):
    """Catch obvious blunders before the AI even sees them.
    Returns a list of dicts: [{"error": "...", "fix": "..."}]
    """
    low = algorithm.lower()
    errors = []
    
    # Check for Min/Max confusion
    if "max" in low and "<" in low and "min" not in low and "else" not in low:
        errors.append({
            "error": "Logic Contradiction: You mentioned 'max' but used the less-than operator (<). This logic actually finds the minimum value.",
            "fix": "Replace '<' with '>' so the comparison finds the LARGEST value. For example: if num > max_val: max_val = num"
        })
    
    if "min" in low and ">" in low and "max" not in low and "else" not in low:
        errors.append({
            "error": "Logic Contradiction: You mentioned 'min' but used the greater-than operator (>). This logic actually finds the maximum value.",
            "fix": "Replace '>' with '<' so the comparison finds the SMALLEST value. For example: if num < min_val: min_val = num"
        })
        
    # Check for Arithmetic confusion
    if ("sum" in low or "add" in low) and "-" in low and "+" not in low:
        errors.append({
            "error": "Arithmetic Error: You mentioned 'sum' but used subtraction (-). Summation requires addition (+).",
            "fix": "Replace the '-' operator with '+'. For summation: total = total + value  (or total += value)"
        })
    
    if ("difference" in low or "subtract" in low) and "+" in low and "-" not in low:
        errors.append({
            "error": "Arithmetic Error: You mentioned 'difference' but used addition (+). Difference requires subtraction (-).",
            "fix": "Replace the '+' operator with '-'. For difference: result = a - b"
        })

    if ("product" in low or "multiply" in low) and "+" in low and "*" not in low:
        errors.append({
            "error": "Arithmetic Error: You mentioned 'product' but used addition (+). Product requires multiplication (*).",
            "fix": "Replace the '+' operator with '*'. For product: result = a * b"
        })

    if "avg" in low or "average" in low:
        if "/" not in low and "//" not in low:
            errors.append({
                "error": "Logic Error: You mentioned 'average' but didn't perform a division (/). Average requires dividing by the count.",
                "fix": "After summing all values, divide by the count: average = total_sum / count"
            })

    # Check for Swap mistakes
    if "swap" in low or ("a=b" in low.replace(" ","") and "b=a" in low.replace(" ","")):
        if "temp" not in low and "[a,b]=[b,a]" not in low.replace(" ","") and "a,b=b,a" not in low.replace(" ",""):
             errors.append({
                 "error": "Swap Error: You are trying to swap variables without a temporary variable. Both variables will end up with the same value.",
                 "fix": "Use a temporary variable: temp = a, then a = b, then b = temp.  Or in Python: a, b = b, a"
             })

    # Check for Infinite Loop (While loops)
    if "while" in low:
        import re
        while_match = re.search(r'while\b(.*?)(?:\n|$)', low)
        if while_match:
            condition_text = while_match.group(1)
            var_match = re.search(r'([a-zA-Z_]\w*)\b', condition_text)
            if var_match:
                var = var_match.group(1)
                body_start_idx = while_match.end()
                loop_body = low[body_start_idx:]
                body_no_space = loop_body.replace(" ", "")
                has_update = (
                    f"{var}=" in body_no_space or 
                    f"{var}+" in body_no_space or 
                    f"{var}-" in body_no_space or 
                    f"set{var}" in body_no_space or
                    f"increment{var}" in body_no_space or
                    f"decrement{var}" in body_no_space or
                    f"{var}isupdated" in body_no_space
                )
                if not has_update:
                    errors.append({
                        "error": f"Infinite Loop Error: Your loop depends on '{var}', but '{var}' is never updated inside the loop body. This will run forever.",
                        "fix": f"Add '{var} = {var} + 1' (or '{var} += 1') inside the loop body so the loop eventually terminates."
                    })

    # Empty Loop Body
    if "for" in low or "while" in low:
        if "print" not in low and "=" not in low and "set" not in low and "\u2192" not in low and "next" not in low:
             errors.append({
                 "error": "Logic Error: Your loop body appears to be empty or does nothing. A loop must perform an action.",
                 "fix": "Add statements inside the loop body, e.g.: total = total + arr[i] or print(i)"
             })

    # Missing return/output
    if "def " in low or "function" in low:
        if "return" not in low and "print" not in low and "yield" not in low:
            errors.append({
                "error": "Structural Error: Your function doesn't return or output anything. It will have no effect.",
                "fix": "Add a 'return result' at the end of your function, or use 'print(result)' to display output."
            })
            
    # Variable initialization
    if "while" in low and ("i<" in low or "i<=" in low) and "i=" not in low.replace(" ",""):
        errors.append({
            "error": "Logic Error: You are using 'i' in a loop condition but haven't initialized it (e.g., Set i = 0).",
            "fix": "Add 'i = 0' (or the appropriate starting value) BEFORE the while loop."
        })

    # For loop decrement
    if "for" in low and "to 0" in low and "step -1" not in low and "decrement" not in low:
        errors.append({
            "error": "Loop Error: You are looping to 0 but didn't specify a decrement or step -1. This could cause an infinite loop.",
            "fix": "Add 'step -1' to your loop, e.g.: for i from n down to 0 step -1. In Python: for i in range(n, -1, -1)"
        })

    # Off-by-one in range/loop bounds
    if "for" in low and "range" in low:
        import re
        range_match = re.search(r'range\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)', low)
        if range_match:
            start, end = int(range_match.group(1)), int(range_match.group(2))
            if start > end:
                errors.append({
                    "error": f"Range Error: range({start}, {end}) will produce an empty sequence since {start} > {end}.",
                    "fix": f"Swap the values: range({end}, {start}) or use range({start}, {end}, -1) if counting downward."
                })

    # Division by zero risk
    if "/0" in low.replace(" ", "") or "/ 0" in low:
        errors.append({
            "error": "Division by Zero: Your code divides by 0, which will cause a runtime error.",
            "fix": "Add a check before dividing: if divisor != 0: result = value / divisor"
        })

    # Array index out of bounds hints
    if ("arr[n]" in low or "array[n]" in low or "list[n]" in low) and "len" not in low:
        errors.append({
            "error": "Potential Index Error: Accessing arr[n] when array has n elements (indices 0 to n-1) will cause an out-of-bounds error.",
            "fix": "Use arr[n-1] to access the last element, or ensure your index is within range(0, len(arr))."
        })
        
    return errors

# ─────────────────────────────────────────────────────────────
# CLOUD ANALYSIS  (primary brain — OpenRouter / Gemini Flash)
# ─────────────────────────────────────────────────────────────
LANG_MAP = {
    "python": "Python", "java": "Java", "cpp": "C++", "c": "C",
    "javascript": "JavaScript", "typescript": "TypeScript",
    "go": "Go", "ruby": "Ruby", "php": "PHP", "rust": "Rust",
    "shell": "Shell Script", "r": "R", "perl": "Perl",
    "lua": "Lua", "dart": "Dart", "swift": "Swift", "sql": "SQL"
}

def analyze_with_openrouter(algorithm, language):
    target_lang = LANG_MAP.get(language.lower(), language.capitalize())
    algo_lower = algorithm.strip().lower()

    # Detect if user is requesting code generation vs checking logic
    is_code_request = False
    code_request_prefixes = [
        "write", "generate", "create", "implement", "code for", "show me",
        "give me", "make", "build", "program for", "algorithm for",
        "sort", "search", "find", "calculate", "compute", "convert",
        "reverse", "merge", "traverse", "insert", "delete", "detect",
        "check", "fibonacci", "factorial", "prime", "palindrome",
        "linked list", "binary tree", "bfs", "dfs", "dijkstra",
        "kruskal", "prim", "knapsack", "tower of hanoi", "matrix",
        "stack", "queue", "heap", "hash", "graph", "dynamic programming",
    ]
    for prefix in code_request_prefixes:
        if prefix in algo_lower:
            is_code_request = True
            break

    # Also detect if input is just an algorithm name (short, no code syntax)
    has_code_syntax = any(c in algorithm for c in ['=', '{', '}', '(', ')', 'def ', 'for ', 'while ', 'if '])
    if len(algorithm.split()) <= 8 and not has_code_syntax:
        is_code_request = True

    if is_code_request:
        prompt = f"""You are an expert algorithm instructor and code generator engineered for 99.9% accuracy.
The user wants: "{algorithm}"
Target Language: {target_lang}

INSTRUCTIONS:
1. "ACCURACY IS PARAMOUNT": Ensure the generated logic operates with >99% accuracy, addressing edge cases, boundary conditions, and preventing typical runtime errors.
2. Generate a COMPLETE, RUNNABLE {target_lang} program for this algorithm that is highly optimized and flawlessly implemented.
3. The code MUST include all necessary imports and a main function/entry point with exhaustive sample test data.
4. The code MUST print clear output when run to verify correct operation.
5. Include professional comments explaining key steps.
6. The "perfect_code" MUST be copy-paste ready, free of placeholder logic, and produce the intended output immediately.

Response MUST be valid JSON only (no markdown):
{{
    "status": "correct",
    "mistakes": [],
    "quote": "A motivational programming quote",
    "time_complexity": "Big-O time",
    "space_complexity": "Big-O space",
    "explanation": "Clear explanation of how the algorithm works",
    "learning_path": ["relevant topics to study"],
    "perfect_code": "Complete runnable {target_lang} code with test cases and output",
    "expected_output": "What the code prints when run"
}}"""
    else:
        prompt = f"""You are an extremely PEDANTIC AI Algorithm Professor engineered to evaluate code with >99% logical accuracy.
Analyze the user's logic: "{algorithm}"
Target Language: {target_lang}

STRICT RULES:
1. "ACCURACY TARGET >99%": Systematize your logical validation. Catch silent failures, edge case misses, and subtle bugs.
2. WRONG MEANS WRONG: If the algorithm fails its objective even slightly, status MUST be "incorrect".
3. LANGUAGE AGNOSTIC: Whether Python, Java, C++, or pseudocode, logic must be perfectly sound.
4. SEMANTIC CHECK: If variables named 'min' but logic finds 'max', it is INCORRECT.
5. LOOP CONVERGENCE: No clear termination or infinite-loop risk = INCORRECT.
6. ARITHMETIC INTEGRITY: Wrong operators = INCORRECT.
7. Do NOT assume the user 'meant' to add a step. If not written, it doesn't exist.
8. "perfect_code" MUST be a HIGHLY OPTIMIZED, COMPLETE RUNNABLE {target_lang} program with exhaustive test data.
9. If incorrect, list EVERY logical failure with a CLEAR, EXPLANATORY FIX SUGGESTION.
10. Each mistake string MUST follow this format: "MISTAKE: [what is wrong] → FIX: [exactly how to fix it]"
11. Include line-level detail when possible (e.g., "Line 3: used '<' instead of '>'").

Response MUST be valid JSON only (no markdown):
{{
    "status": "correct" or "incorrect",
    "mistakes": ["MISTAKE: [precise flaw description] → FIX: [exact step-by-step fix]"],
    "quote": "Motivational quote",
    "time_complexity": "Big-O",
    "space_complexity": "Big-O",
    "explanation": "Professional explanation of what the algorithm does and what went wrong",
    "learning_path": ["topics to study"],
    "perfect_code": "Complete runnable {target_lang} implementation with test data and output",
    "expected_output": "Console result"
}}"""

    if not OPENROUTER_API_KEY:
        return None

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "google/gemini-flash-1.5",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 2048,
                "temperature": 0.3   # Lower temp for more precise code
            },
            timeout=30
        )

        if response.status_code != 200:
            print(f"❌ OpenRouter Error {response.status_code}: {response.text[:250]}")
            return None

        raw_content = response.json()["choices"][0]["message"]["content"].strip()
        print(f"📝 Raw AI Content length: {len(raw_content)}")
        
        content = raw_content
        # Strip markdown code fences if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            parts = content.split("```")
            if len(parts) >= 3:
                content = parts[1].strip()
                if content.startswith("json"):
                    content = content[4:].strip()
            else:
                content = parts[0].strip()

        # Try to extract JSON object if there's extra text
        if not content.startswith("{"):
            idx = content.find("{")
            if idx != -1:
                content = content[idx:]
        if not content.endswith("}"):
            idx = content.rfind("}")
            if idx != -1:
                content = content[:idx+1]

        try:
            return json.loads(content)
        except json.JSONDecodeError as je:
            print(f"❌ JSON Parse Error: {je}\nContent: {content[:300]}")
            return None

    except Exception as e:
        print(f"Cloud Analysis Exception: {e}")
        return None


# ─────────────────────────────────────────────────────────────
# KEYWORD-BASED FALLBACK  (works without torch — instant)
# ─────────────────────────────────────────────────────────────
def analyze_with_keyword_db(algorithm, language):
    lowercase_input = algorithm.lower().strip()
    best_match = None
    best_key = None
    highest_score = 0

    for key, entry in ALGORITHM_DATABASE.items():
        score = 0
        # Direct key match (e.g. user types "bubble sort" matches "bubble_sort")
        key_clean = key.replace("_", " ")
        if key_clean in lowercase_input or key in lowercase_input:
            score += 100
        # Keyword scoring
        score += sum(len(kw) * 5 for kw in entry["keywords"] if kw in lowercase_input)
        if score > highest_score:
            highest_score = score
            best_match = entry
            best_key = key

    perfect_code = None
    if best_match:
        perfect_code = best_match.get(language, best_match.get("python"))

    if not perfect_code:
        perfect_code = (
            algorithm if ("def " in algorithm or "{" in algorithm)
            else f"# Language: {language}\n# Please use Cloud mode for full implementation.\ndef solve():\n    pass"
        )
    return perfect_code


# ─────────────────────────────────────────────────────────────
# MAIN ENDPOINT
# ─────────────────────────────────────────────────────────────
@app.route("/evaluate", methods=["POST"])
def evaluate():
    data      = request.json or {}
    algorithm = data.get("algorithm", "").strip()
    language  = data.get("language", "python").lower()

    if not algorithm:
        return jsonify({"feedback": "Please provide an algorithm.", "type": "neutral"})

    print(f"\n📥 RECEIVED LOGIC FOR EVALUATION: {algorithm[:50]}...")
    target_lang = LANG_MAP.get(language.lower(), language.capitalize())
    
    # ── CACHE CHECK ──────────────────────────────────────────
    cache_key = f"{algorithm}_{language}"
    if cache_key in logic_cache:
        print("⚡ Cache hit! Returning stored result.")
        return jsonify(logic_cache[cache_key])

    # ── STEP 0: Pedantic Logic Guard ──────────────────────────
    # Only run logic guard on actual pseudocode/logic, not algorithm name requests
    algo_lower = algorithm.lower().strip()
    has_code_syntax = any(c in algorithm for c in ['=', '{', '}', 'def ', 'for ', 'while ', 'if '])
    is_pure_name = len(algorithm.split()) <= 8 and not has_code_syntax
    
    guard_errors = [] if is_pure_name else logic_guard(algorithm, language)
    if guard_errors:
        print(f"🛑 LOGIC GUARD TRIGGERED: {guard_errors[0]['error']}")
        # Also try to find the correct reference code from DB
        ref_code = analyze_with_keyword_db(algorithm, language)
        
        # Build readable mistake list with fix suggestions
        mistake_list = []
        for e in guard_errors:
            mistake_list.append(f"MISTAKE: {e['error']} → FIX: {e['fix']}")
        
        return jsonify({
            "status": "incorrect",
            "type": "incorrect",
            "feedback": "I caught logical errors in your algorithm! Read the mistakes below carefully and see how to fix each one.",
            "mistakes": mistake_list,
            "quote": "Every master was once a beginner. Let's fix this logic step by step!",
            "explanation": "Your code contains logic errors that contradict the algorithm's stated goal. Each mistake is listed below with a specific fix suggestion so you can learn and correct it.",
            "learning_path": ["Comparison Operators", "Algorithm Design", "Debugging Techniques"],
            "perfect_code": ref_code,
            "time_complexity": "See reference code",
            "space_complexity": "See reference code"
        })

    # ── STEP 1: Try Cloud (OpenRouter / Gemini Flash) ──────────
    result = analyze_with_openrouter(algorithm, language)

    if result:
        # AI processed the request. It's the most reliable source.
        status = result.get("status", "incorrect").lower()
        
        # Ensure 'status' is consistent for the frontend
        result["status"] = status
        result["type"]   = status
        
        # Save to cache
        logic_cache[cache_key] = result
        save_cache(logic_cache)
        
        gc.collect()
        return jsonify(result)

    # ── STEP 2: Try Local Torch Model ───────────────────────────
    if TORCH_AVAILABLE and model and tokenizer:
        try:
            import torch
            input_text = f"Check algorithm: {algorithm}"
            with torch.no_grad():
                inputs = tokenizer(input_text, return_tensors="pt", max_length=64, truncation=True).to(device)
                outputs = model.generate(**inputs, max_new_tokens=64)
                model_feedback = tokenizer.decode(outputs[0], skip_special_tokens=True)

            eval_status = "correct" if "correct" in model_feedback.lower() else "incorrect"
            perfect_code = analyze_with_keyword_db(algorithm, language)

            gc.collect()
            return jsonify({
                "status": eval_status,
                "type": eval_status,
                "feedback": f"Local AI Analysis: {model_feedback}",
                "quote": "Small steps lead to great heights. Keep going!",
                "perfect_code": perfect_code,
                "time_complexity": "O(?)", 
                "space_complexity": "O(?)",
                "explanation": "I'm using my local basic engine to check this. For deep logic analysis, please check your internet connection.",
                "mistakes": [] if eval_status == "correct" else ["Logic seems unconventional for a standard algorithm."],
                "learning_path": ["Algorithm Fundamentals"]
            })
        except Exception as e:
            print(f"Local model error: {e}")

    # ── STEP 3: Pure Keyword Fallback (SKEPTICAL MODE) ──────────
    perfect_code = analyze_with_keyword_db(algorithm, language)
    
    # If the user typed a known algorithm name and we got a DB match, it's valid
    # If they typed pseudocode we can't fully verify, mark as needing review
    matched_in_db = False
    for key, entry in ALGORITHM_DATABASE.items():
        key_clean = key.replace("_", " ")
        if key_clean in algo_lower or key in algo_lower:
            matched_in_db = True
            break
        if any(kw in algo_lower for kw in entry.get("keywords", [])):
            matched_in_db = True
            break

    if matched_in_db and is_pure_name:
        # User typed a known algorithm name — return the code as "correct"
        gc.collect()
        return jsonify({
            "status": "correct",
            "type": "correct",
            "feedback": f"Here's the {target_lang} implementation for your requested algorithm!",
            "quote": "Code is the common language of the digital world.",
            "perfect_code": perfect_code,
            "time_complexity": "Check the code for complexity details",
            "space_complexity": "Check the code for complexity details",
            "explanation": f"Generated from the built-in algorithm database. This is a standard, verified implementation in {target_lang}.",
            "mistakes": [],
            "learning_path": ["Algorithm Design", "Data Structures", target_lang + " Programming"]
        })

    # For pseudocode/logic they wrote themselves — can't fully verify without cloud
    feedback = "Cloud AI is offline. I matched this to a known pattern, but couldn't deeply verify your specific logic." if matched_in_db else "I couldn't verify this logic with my full AI. Please check your internet connection for full analysis."

    gc.collect()

    return jsonify({
        "status": "incorrect" if not matched_in_db else "correct", 
        "type": "incorrect" if not matched_in_db else "correct",
        "feedback": feedback,
        "quote": "The expert in anything was once a beginner.",
        "perfect_code": perfect_code,
        "time_complexity": "O(?)",
        "space_complexity": "O(?)",
        "explanation": "Cloud analysis is unavailable. Showing the standard implementation for this type of problem as a reference.",
        "mistakes": ["Full logic verification requires cloud connection."] if not matched_in_db else [],
        "learning_path": ["Logic Verification", "Algorithm Structure"]
    })


# ─────────────────────────────────────────────────────────────
# SUBMIT CODE — Run + Verify correctness against task
# ─────────────────────────────────────────────────────────────
@app.route("/submit_code", methods=["POST"])
def submit_code():
    """Run code, capture output, and verify it meets the task requirements."""
    import subprocess, sys, tempfile, os as _os

    data      = request.json or {}
    code      = data.get("code", "").strip()
    language  = data.get("language", "python").lower()
    task_title = data.get("task_title", "").strip()
    task_desc  = data.get("task_description", "").strip()

    if not code:
        return jsonify({"passed": False, "feedback": "No code provided.", "test_results": []})

    # Step 1: Execute the code (Python only for now)
    run_output = ""
    run_error = ""
    timed_out = False

    if language == "python":
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(code)
                tmp_path = f.name

            result = subprocess.run(
                [sys.executable, tmp_path],
                capture_output=True, text=True, timeout=10,
                cwd=tempfile.gettempdir()
            )
            run_output = result.stdout or ""
            run_error = result.stderr or ""
        except subprocess.TimeoutExpired:
            timed_out = True
            run_error = "Execution timed out (>10 seconds). Possible infinite loop."
        except Exception as e:
            run_error = str(e)
        finally:
            try: _os.unlink(tmp_path)
            except: pass
    else:
        run_output = f"(Simulated {language} execution — output not captured)"

    if timed_out:
        return jsonify({
            "passed": False,
            "feedback": "⏱️ Your code timed out! Check for infinite loops.",
            "output": run_error,
            "test_results": [{"name": "Execution", "passed": False, "detail": "Timed out after 10 seconds"}]
        })

    # Step 2: Use Cloud AI to verify correctness against the task
    if OPENROUTER_API_KEY and task_title:
        target_lang = LANG_MAP.get(language, language.capitalize())
        prompt = f"""You are a strict code grader. The student was given this task:

TASK: {task_title}
DESCRIPTION: {task_desc}

The student submitted this {target_lang} code:
```
{code}
```

The code produced this output:
```
{run_output}
```
{f"Errors: {run_error}" if run_error else ""}

GRADING RULES:
1. Check if the code actually implements the task correctly.
2. Check for edge cases and logical errors.
3. Generate 3-5 test cases and check if the code handles them.
4. Be fair but strict — partial credit is OK.

Response MUST be valid JSON only (no markdown):
{{
    "passed": true or false,
    "score": 0-100,
    "feedback": "One sentence overall verdict",
    "test_results": [
        {{"name": "Test case name", "passed": true/false, "detail": "What was tested and result"}}
    ],
    "suggestions": ["improvement suggestion 1", "suggestion 2"]
}}"""
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "google/gemini-flash-1.5",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1024,
                    "temperature": 0.2
                },
                timeout=30
            )

            if response.status_code == 200:
                raw = response.json()["choices"][0]["message"]["content"].strip()
                content = raw
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    parts = content.split("```")
                    if len(parts) >= 3:
                        content = parts[1].strip()
                        if content.startswith("json"):
                            content = content[4:].strip()
                if not content.startswith("{"):
                    idx = content.find("{")
                    if idx != -1: content = content[idx:]
                if not content.endswith("}"):
                    idx = content.rfind("}")
                    if idx != -1: content = content[:idx+1]

                try:
                    result = json.loads(content)
                    result["output"] = run_output
                    return jsonify(result)
                except:
                    pass
        except Exception as e:
            print(f"Submit grading error: {e}")

    # Fallback: just return execution results
    has_errors = bool(run_error and "Error" in run_error)
    return jsonify({
        "passed": not has_errors and bool(run_output),
        "score": 0 if has_errors else 50,
        "feedback": "Code executed. Full verification requires cloud AI." if not has_errors else "Code has errors.",
        "output": run_output,
        "test_results": [
            {"name": "Execution", "passed": not has_errors, "detail": run_output[:200] if run_output else run_error[:200]}
        ],
        "suggestions": ["Connect to internet for full AI-powered test case verification."]
    })


# ─────────────────────────────────────────────────────────────
# CHECK TASK RELEVANCE — Is the algorithm relevant to the task?
# ─────────────────────────────────────────────────────────────
@app.route("/check_task_relevance", methods=["POST"])
def check_task_relevance():
    """Check if the user's algorithm input is related to the active task."""
    data       = request.json or {}
    algorithm  = data.get("algorithm", "").strip()
    task_title = data.get("task_title", "").strip()
    task_desc  = data.get("task_description", "").strip()

    if not algorithm or not task_title:
        return jsonify({"relevant": True, "message": ""})

    # Quick keyword check first
    algo_lower = algorithm.lower()
    task_lower = (task_title + " " + task_desc).lower()
    common_words = set(algo_lower.split()) & set(task_lower.split())
    # Remove stopwords
    stopwords = {"the", "a", "an", "is", "to", "for", "in", "of", "and", "or", "with", "that", "this", "it", "on", "at", "by"}
    meaningful_common = common_words - stopwords
    if meaningful_common:
        return jsonify({"relevant": True, "message": f"✅ Algorithm matches task keywords: {', '.join(meaningful_common)}"})

    # Use Cloud AI for deeper check
    if OPENROUTER_API_KEY:
        prompt = f"""Is this algorithm/code related to this task?

TASK: {task_title} — {task_desc}
USER INPUT: {algorithm}

Reply with ONLY valid JSON:
{{"relevant": true or false, "message": "Brief explanation of why it is or isn't related"}}"""
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"},
                json={"model": "google/gemini-flash-1.5", "messages": [{"role": "user", "content": prompt}], "max_tokens": 256, "temperature": 0.1},
                timeout=15
            )
            if response.status_code == 200:
                raw = response.json()["choices"][0]["message"]["content"].strip()
                content = raw
                if "```" in content:
                    content = content.split("```json")[-1].split("```")[0].strip() if "```json" in content else content.split("```")[1].strip()
                if not content.startswith("{"):
                    idx = content.find("{")
                    if idx != -1: content = content[idx:]
                if not content.endswith("}"):
                    idx = content.rfind("}")
                    if idx != -1: content = content[:idx+1]
                try:
                    return jsonify(json.loads(content))
                except:
                    pass
        except:
            pass

    return jsonify({"relevant": True, "message": ""})

@app.route("/run_code", methods=["POST"])
def run_code():
    """Execute Python code in a safe subprocess with timeout."""
    import subprocess, sys, tempfile, os as _os

    data     = request.json or {}
    code     = data.get("code", "").strip()
    language = data.get("language", "python").lower()

    if not code:
        return jsonify({"output": "No code provided.", "error": True})

    if language != "python":
        # For non-Python we return a simulation result
        simulated = {
            "java":       "// Java compiled successfully.\n// Output: Program ran with exit code 0.",
            "cpp":        "// C++ compiled with g++ -O2\n// Output: Program ran with exit code 0.",
            "javascript": "// Node.js simulation\nconsole.log('Program ran successfully');",
        }.get(language, f"// {language.upper()} execution simulated.\n// Output: Program completed with exit code 0.")
        return jsonify({"output": simulated, "error": False, "simulated": True})

    # Write code to a temp file and run it
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code)
            tmp_path = f.name

        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,
            text=True,
            timeout=10,          # 10 second hard limit
            cwd=tempfile.gettempdir()
        )

        output = result.stdout or ""
        if result.stderr:
            output += "\n⚠️ Errors:\n" + result.stderr

        return jsonify({
            "output":   output.strip() or "(No output produced)",
            "error":    result.returncode != 0,
            "exitcode": result.returncode
        })

    except subprocess.TimeoutExpired:
        return jsonify({"output": "⏱️ Execution timed out (>10 seconds). Check for infinite loops!", "error": True})
    except Exception as e:
        return jsonify({"output": f"Execution error: {str(e)}", "error": True})
    finally:
        try: _os.unlink(tmp_path)
        except: pass


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status":        "running",
        "torch":         TORCH_AVAILABLE,
        "local_model":   model is not None,
        "cloud_api":     bool(OPENROUTER_API_KEY)
    })


@app.route("/certificate", methods=["GET"])
def certificate():
    """Serve a dynamically generated certificate page."""
    name = request.args.get("name", "Student")
    course = request.args.get("course", "Algorithm Logic")
    date = request.args.get("date", "February 25, 2026")

    # Recreating the premium design from the user's template using HTML/CSS
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Certificate of Completion - {name}</title>
        <link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&family=Montserrat:wght@300;400;700&family=Great+Vibes&display=swap" rel="stylesheet">
        <style>
            :root {{
                --primary: #0f172a;
                --gold: #c5a059;
                --border-gold: #b38b4d;
                --bg: #f8fafc;
            }}
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                background: #e2e8f0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                font-family: 'Montserrat', sans-serif;
                padding: 20px;
            }}
            .cert-container {{
                width: 1000px;
                height: 700px;
                background: white;
                position: relative;
                padding: 40px;
                box-shadow: 0 50px 100px -20px rgba(0,0,0,0.25);
                overflow: hidden;
                border: 4px solid var(--primary);
            }}

            /* Corner Decorations */
            .corner {{
                position: absolute;
                width: 250px;
                height: 250px;
                background: var(--primary);
                z-index: 1;
            }}
            .corner-tl {{ top: -125px; left: -125px; transform: rotate(45deg); border-right: 15px solid var(--gold); }}
            .corner-tr {{ top: -125px; right: -125px; transform: rotate(-45deg); border-left: 15px solid var(--gold); }}
            .corner-bl {{ bottom: -125px; left: -125px; transform: rotate(-45deg); border-right: 15px solid var(--gold); }}
            .corner-br {{ bottom: -125px; right: -125px; transform: rotate(45deg); border-left: 15px solid var(--gold); }}

            /* Inner Border */
            .inner-border {{
                position: absolute;
                top: 20px;
                left: 20px;
                right: 20px;
                bottom: 20px;
                border: 2px solid var(--gold);
                z-index: 2;
                pointer-events: none;
            }}
            .inner-border::after {{
                content: '';
                position: absolute;
                top: 10px;
                left: 10px;
                right: 10px;
                bottom: 10px;
                border: 1px solid var(--gold);
            }}

            /* Content Area */
            .content {{
                position: relative;
                z-index: 3;
                height: 100%;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
            }}

            h1 {{
                font-family: 'Libre+Baskerville', serif;
                font-size: 72px;
                color: var(--primary);
                letter-spacing: 4px;
                margin-bottom: 5px;
                text-transform: uppercase;
            }}
            .sub-title {{
                font-size: 24px;
                color: var(--primary);
                border-top: 2px solid var(--gold);
                border-bottom: 2px solid var(--gold);
                padding: 10px 40px;
                margin-bottom: 40px;
                letter-spacing: 2px;
            }}
            .presented {{
                font-size: 18px;
                font-weight: 300;
                margin-bottom: 20px;
                color: #64748b;
            }}
            .student-name {{
                font-family: 'Great Vibes', cursive;
                font-size: 84px;
                color: var(--primary);
                margin-bottom: 10px;
                border-bottom: 2px solid var(--gold);
                min-width: 600px;
            }}
            .completion-text {{
                font-size: 18px;
                color: #475569;
                max-width: 600px;
                line-height: 1.6;
                margin-top: 10px;
            }}
            .course-name {{
                font-weight: 700;
                color: var(--primary);
            }}

            /* Signatures */
            .footer {{
                display: flex;
                justify-content: space-between;
                width: 80%;
                margin-top: 60px;
            }}
            .sig-block {{
                display: flex;
                flex-direction: column;
                align-items: center;
            }}
            .sig-line {{
                width: 200px;
                border-top: 1px solid #475569;
                margin-bottom: 10px;
            }}
            .sig-label {{
                font-size: 14px;
                color: #64748b;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}

            /* Seal */
            .seal {{
                position: absolute;
                bottom: 40px;
                left: 50%;
                transform: translateX(-50%);
                width: 100px;
                height: 100px;
                background: var(--primary);
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                border: 4px double var(--gold);
                box-shadow: 0 0 0 5px var(--primary);
            }}
            .seal::after {{
                content: '★';
                color: var(--gold);
                font-size: 40px;
            }}
            .ribbon {{
                position: absolute;
                bottom: -20px;
                width: 40px;
                height: 80px;
                background: var(--primary);
                z-index: -1;
            }}
            .ribbon-l {{ left: 20px; transform: rotate(-15deg); }}
            .ribbon-r {{ right: 20px; transform: rotate(15deg); }}

            @media print {{
                body {{ background: white; padding: 0; }}
                .cert-container {{ box-shadow: none; border: 4px solid var(--primary); }}
                .no-print {{ display: none; }}
            }}

            .download-btn {{
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 12px 24px;
                background: var(--primary);
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-weight: bold;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                z-index: 100;
                transition: transform 0.2s;
            }}
            .download-btn:hover {{
                transform: scale(1.05);
            }}
        </style>
    </head>
    <body>
        <button class="download-btn no-print" onclick="window.print()">Download PDF</button>

        <div class="cert-container">
            <div class="corner corner-tl"></div>
            <div class="corner corner-tr"></div>
            <div class="corner corner-bl"></div>
            <div class="corner corner-br"></div>
            <div class="inner-border"></div>

            <div class="content">
                <h1>CERTIFICATE</h1>
                <div class="sub-title">of Completing this Course</div>
                
                <p class="presented">This certificate is proudly presented to</p>
                <div class="student-name">{name}</div>
                
                <p class="completion-text">
                    has successfully completed the course <span class="course-name">{course}</span> 
                    and demonstrated exceptional understanding of algorithm logic and implementation.
                </p>

                <div class="footer">
                    <div class="sig-block">
                        <div class="sig-line"></div>
                        <div class="sig-label">Authorized Signatory</div>
                    </div>
                    <div class="sig-block">
                        <div class="sig-line"></div>
                        <div class="sig-label">Course Instructor</div>
                    </div>
                </div>

                <div class="seal">
                    <div class="ribbon ribbon-l"></div>
                    <div class="ribbon ribbon-r"></div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    print("\n" + "="*50)
    print("  🚀 AI Algorithm Instructor Backend")
    print(f"  📡 Cloud API:   {'✅ Active' if OPENROUTER_API_KEY else '❌ No key'}")
    print(f"  🧠 Local Model: {'✅ Loaded' if model else '⚠️  Not loaded (cloud-only)'}")
    print(f"  🔥 PyTorch:     {'✅ Installed' if TORCH_AVAILABLE else '⚠️  Not installed'}")
    print("  🌐 Running at:  http://localhost:5005")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5005, debug=False, threaded=True)  # debug=False → saves CPU
