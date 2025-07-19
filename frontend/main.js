// Main Application Controller
class HT6ixApp {
    constructor() {
        this.audioVisualizer = null;
        this.textBox = null;
        this.currentView = 'full'; // 'full' or 'mini'
        this.isVisualizerFocused = false;
        
        this.init();
    }
    
    init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.create());
        } else {
            this.create();
        }
    }
    
    create() {
        // Initialize components
        this.audioVisualizer = new AudioVisualizer();
        this.textBox = new TextBox();
        
        // Set up IPC listeners
        this.setupIPCListeners();
        
        // Set up keyboard shortcuts
        this.setupKeyboardShortcuts();
        
        // Start periodic updates
        this.startPeriodicUpdates();
        
        console.log('HT6ix AI Teaching Bot frontend initialized');
    }
    
    setupIPCListeners() {
        // Listen for toggle view mode from backend
        if (window.require) {
            const { ipcRenderer } = require('electron');
            
            ipcRenderer.on('toggle-view-mode', () => {
                this.toggleViewMode();
            });
            
            ipcRenderer.on('toggle-visualizer-focus', () => {
                this.toggleVisualizerFocus();
            });
        }
    }
    
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (event) => {
            // Prevent default behavior for our shortcuts
            if (event.key === '/' || event.key === '=') {
                event.preventDefault();
            }
        });
    }
    
    startPeriodicUpdates() {
        // Update audio level display every 2 seconds
        setInterval(() => {
            if (this.audioVisualizer && this.textBox) {
                const audioLevel = this.audioVisualizer.getAudioLevel();
                if (audioLevel > 0.05) { // Only show if there's significant audio
                    this.textBox.showAudioLevel(audioLevel);
                }
            }
        }, 2000);
        
        // Periodic status updates
        setInterval(() => {
            if (this.textBox) {
                this.textBox.showStatus(`View: ${this.currentView}, Focus: ${this.isVisualizerFocused ? 'On' : 'Off'}`);
            }
        }, 10000);
    }
    
    toggleViewMode() {
        this.currentView = this.currentView === 'full' ? 'mini' : 'full';
        
        if (this.currentView === 'mini') {
            document.body.classList.add('mini-view');
            document.body.classList.remove('full-view');
            this.textBox.info('Switched to mini view');
        } else {
            document.body.classList.add('full-view');
            document.body.classList.remove('mini-view');
            this.textBox.info('Switched to full view');
        }
        
        console.log(`View mode toggled to: ${this.currentView}`);
    }
    
    toggleVisualizerFocus() {
        this.isVisualizerFocused = !this.isVisualizerFocused;
        
        if (this.audioVisualizer) {
            this.audioVisualizer.setFocus(this.isVisualizerFocused);
        }
        
        if (this.isVisualizerFocused) {
            document.body.classList.add('focus-mode');
            this.textBox.info('Audio visualizer focused');
        } else {
            document.body.classList.remove('focus-mode');
            this.textBox.info('Audio visualizer unfocused');
        }
        
        console.log(`Visualizer focus toggled: ${this.isVisualizerFocused}`);
    }
    
    // Method to add learning content (will be used later)
    addLearningContent(content) {
        if (this.textBox) {
            this.textBox.addLearningContent(content);
        }
    }
    
    // Method to add quiz content (will be used later)
    addQuizContent(question, options) {
        if (this.textBox) {
            this.textBox.addQuizContent(question, options);
        }
    }
    
    // Method to show system status
    showStatus(status) {
        if (this.textBox) {
            this.textBox.showStatus(status);
        }
    }
}

// Initialize the application
let app;

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        app = new HT6ixApp();
    });
} else {
    app = new HT6ixApp();
}

// Make app globally available for debugging
window.HT6ixApp = app; 