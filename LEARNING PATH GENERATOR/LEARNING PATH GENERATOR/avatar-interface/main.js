// =====================================================================
//  AlgoAI Instructor – main.js (Maximum Robustness)
// =====================================================================

'use strict';

const API_URL = (hostname) => {
    const h = (!hostname || hostname === 'localhost' || hostname === '127.0.0.1') ? '127.0.0.1' : hostname;
    return `http://${h}:5000`;
};

const BACKEND = `${API_URL(window.location.hostname)}/evaluate`;
const RUN_ENDPOINT = `${API_URL(window.location.hostname)}/run_code`;

// ── DOM references ───────────────────────────────────────────────────
const $ = id => document.getElementById(id);

let state = {
    latestResponse: null,
    recognition: null,
    isListening: false,
    isSpeaking: false,
    elements: {},
    courseData: [],
    currentModuleIndex: 0,
    completedModules: new Set(JSON.parse(localStorage.getItem('completedModules') || '[]'))
};

// ── Speech Synthesis ──────────────────────────────────────────────────
const synth = window.speechSynthesis;

function speak(text, onDone) {
    if (!synth) return;
    synth.cancel();
    const chunks = text.match(/.{1,160}(?:\s|$)/g) || [text];
    state.isSpeaking = true;
    setAvatarState('speaking');

    function speakChunk(i) {
        if (i >= chunks.length) {
            state.isSpeaking = false;
            setAvatarState('idle');
            if (onDone) onDone();
            return;
        }
        const u = new SpeechSynthesisUtterance(chunks[i].trim());
        u.rate = 0.95;
        const voices = synth.getVoices();
        const v = voices.find(v => v.lang.startsWith('en') && (v.name.includes('Male') || v.name.includes('Natural')));
        if (v) u.voice = v;
        u.onend = () => speakChunk(i + 1);
        u.onerror = () => speakChunk(i + 1);
        synth.speak(u);
    }
    speakChunk(0);
}

// ── Avatar States ─────────────────────────────────────────────────────
function setAvatarState(avatarState) {
    const el = state.elements;
    if (!el.avatarFrame) return;
    el.avatarFrame.className = 'avatar-frame';
    el.avatarFrame.classList.add(`avatar-${avatarState}`);
    const labels = {
        idle: 'Teacher is ready',
        speaking: '🔊 Explaining...',
        thinking: '🧠 Analyzing...',
        correct: '✅ Great Logic!',
        incorrect: '⚠️ Logic Check',
        listening: '🎤 Listening...'
    };
    if (el.avatarLabel) el.avatarLabel.textContent = labels[avatarState] || 'Ready';
}

// ── Course Logic ──────────────────────────────────────────────────────
async function loadCourse() {
    try {
        // Since we are running in a static way or via flask, we fetch from the backend or direct file
        // For simplicity, we define a fallback or fetch course_data.json
        const res = await fetch('/course_data.json');
        state.courseData = await res.json();
    } catch (e) {
        // Fallback Course Data if file fetch fails
        state.courseData = [
            { id: 1, type: "video", title: "Introduction to Algorithms", description: "Learn what algorithms are and why they matter.", videoUrl: "https://www.youtube.com/embed/0IAPZzGSbME" },
            { id: 2, type: "video", title: "Time Complexity & Big O", description: "Understanding how to measure algorithm efficiency.", videoUrl: "https://www.youtube.com/embed/v4cd1O4zkGw" },
            { id: 3, type: "exam", title: "Basic Logic Challenge", description: "Create an algorithm to find the maximum of two numbers.", required_algorithm: "find_max" },
            { id: 4, type: "video", title: "Linear Search Explained", description: "How to search through a list sequentially.", videoUrl: "https://www.youtube.com/embed/4gpqV_itMTo" },
            { id: 5, type: "exam", title: "Search Logic Challenge", description: "Write a pseudocode for a Linear Search algorithm.", required_algorithm: "linear_search" }
        ];
    }
    renderModuleList();
    updateProgress();
}

function renderModuleList() {
    const list = $('module-list');
    list.innerHTML = state.courseData.map((m, i) => `
        <div class="module-item ${state.completedModules.has(m.id) ? 'completed' : ''} ${state.currentModuleIndex === i ? 'active' : ''}" onclick="openModule(${i})">
            <span class="module-status-icon">${m.type === 'video' ? '📽️' : '📝'}</span>
            <div class="module-info">
                <h4>${m.title}</h4>
                <p>${m.type.toUpperCase()}</p>
            </div>
            ${state.completedModules.has(m.id) ? '<span class="module-check">L</span>' : ''}
        </div>
    `).join('');
}

function openModule(index) {
    state.currentModuleIndex = index;
    const module = state.courseData[index];
    const modal = $('module-modal');
    modal.classList.remove('hidden');

    if (module.type === 'video') {
        $('video-player-container').classList.remove('hidden');
        $('exam-container').classList.add('hidden');
        $('video-iframe').src = module.videoUrl;
    } else {
        $('video-player-container').classList.add('hidden');
        $('exam-container').classList.remove('hidden');
        $('exam-title').textContent = module.title;
        $('exam-desc').textContent = module.description;
        // Reset exam feedback
        $('exam-feedback').textContent = "Submit your algorithm below to pass this exam.";
    }
    renderModuleList();
}

$('close-modal').onclick = () => {
    $('module-modal').classList.add('hidden');
    $('video-iframe').src = '';
};

$('mark-complete-btn').onclick = () => {
    const module = state.courseData[state.currentModuleIndex];
    state.completedModules.add(module.id);
    localStorage.setItem('completedModules', JSON.stringify([...state.completedModules]));
    updateProgress();
    renderModuleList();
    $('module-modal').classList.add('hidden');
    checkCourseCompletion();
};

function updateProgress() {
    const percent = Math.round((state.completedModules.size / state.courseData.length) * 100);
    $('course-progress-bar').style.width = percent + '%';
    $('progress-text').textContent = percent + '% Complete';
}

function checkCourseCompletion() {
    if (state.completedModules.size === state.courseData.length) {
        $('cert-modal').classList.remove('hidden');
        speak("Congratulations! You have completed the entire course. You can now download your certificate.");
    }
}

// ── Main Submission (Updated for Exams) ───────────────────────────────
async function handleSubmission() {
    const el = state.elements;
    const input = el.algorithmInput.value.trim();

    if (!input) {
        speak("Please enter an algorithm first.");
        return;
    }

    setAvatarState('thinking');
    el.submitBtn.disabled = true;
    el.submitBtn.textContent = '⏳ Thinking...';

    try {
        const res = await fetch(BACKEND, {
            method: 'POST',
            mode: 'cors',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                algorithm: input,
                language: el.languageSelect.value
            })
        });

        const data = await res.json();
        state.latestResponse = data;
        updateUI(data);

        // Check if this is an active exam
        const module = state.courseData[state.currentModuleIndex];
        if (module && module.type === 'exam' && data.status === 'correct') {
            state.completedModules.add(module.id);
            localStorage.setItem('completedModules', JSON.stringify([...state.completedModules]));
            updateProgress();
            renderModuleList();
            setTimeout(() => {
                speak("Excellent! You passed the exam.");
                checkCourseCompletion();
            }, 1000);
        }

    } catch (err) {
        setAvatarState('incorrect');
        speak("I couldn't reach the server.");
    } finally {
        el.submitBtn.disabled = false;
        el.submitBtn.textContent = '⚡ Evaluate';
    }
}

function updateUI(data) {
    const el = state.elements;
    const { status, feedback, perfect_code, quote } = data;
    const isCorrect = (status === 'correct');

    setAvatarState(isCorrect ? 'correct' : 'incorrect');

    if (el.perfectCodeEl && perfect_code) {
        el.codePlaceholder.classList.add('hidden');
        el.codePre.classList.remove('hidden');
        el.perfectCodeEl.textContent = perfect_code;
        if (window.hljs) window.hljs.highlightElement(el.perfectCodeEl);
    }

    speak(`${feedback || "Logic check complete."} ${quote || ""}`);
    triggerEmoji(isCorrect);
}

function triggerEmoji(isCorrect) {
    const emoji = $('emoji-overlay');
    const content = $('emoji-content');
    content.textContent = isCorrect ? '👏' : '😟';
    emoji.classList.remove('hidden');
    emoji.classList.add('active');
    setTimeout(() => emoji.classList.remove('active', 'hidden'), 1500);
}

// ── Initialization ────────────────────────────────────────────────────
function init() {
    const ids = [
        'start-overlay', 'start-btn', 'submit-btn', 'run-btn', 'listen-btn',
        'algorithm-input', 'language-select', 'avatar-frame', 'avatar-label',
        'code-placeholder', 'code-pre', 'perfect-code', 'claim-cert-btn'
    ];

    ids.forEach(id => {
        const el = $(id);
        let camelId = id.replace(/-([a-z])/g, g => g[1].toUpperCase());
        if (id === 'perfect-code') camelId = 'perfectCodeEl';
        state.elements[camelId] = el;
    });

    const el = state.elements;
    if (el.startBtn) el.startBtn.onclick = () => { el.startOverlay.style.display = 'none'; loadCourse(); };
    if (el.submitBtn) el.submitBtn.onclick = handleSubmission;

    if (el.claimCertBtn) el.claimCertBtn.onclick = () => {
        const name = prompt("Enter your full name for the certificate:", "Student");
        if (name) {
            window.open(`http://127.0.0.1:5000/certificate?name=${encodeURIComponent(name)}&course=Algorithm Logic Mastery`, '_blank');
        }
    };

    setAvatarState('idle');
}

document.addEventListener('DOMContentLoaded', init);
