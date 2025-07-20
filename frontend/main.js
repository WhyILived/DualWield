// Main Application Controller
class HT6ixApp {
    constructor() {
        this.audioVisualizer = null;
        this.textBox = null;
        this.currentView = 'full'; // 'full' or 'mini'
        this.isVisualizerFocused = false;
        this.circularButton = null;
        this.bufferEmpty = true;
        this.bufferCheckInterval = null;
        
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
        
        // Set up circular button
        this.setupCircularButton();
        
        // Set up IPC listeners
        this.setupIPCListeners();
        
        // Set up keyboard shortcuts
        this.setupKeyboardShortcuts();
        
        // Set up mouse tracking for click-through
        this.setupMouseTracking();
        
        // Start buffer monitoring
        this.startBufferMonitoring();
        
        console.log('HT6ix AI Teaching Bot frontend initialized');
    }
    
    setupCircularButton() {
        this.circularButton = document.getElementById('circular-button');
        if (this.circularButton) {
            this.circularButton.addEventListener('click', () => {
                this.handleButtonClick();
            });
            
            this.circularButton.addEventListener('mouseenter', () => {
                this.enableButtonClicks();
            });
            
            this.circularButton.addEventListener('mouseleave', () => {
                this.disableButtonClicks();
            });
        }
    }
    
    setupMouseTracking() {
        // Track mouse movement to enable/disable click-through
        document.addEventListener('mousemove', (event) => {
            this.handleMouseMove(event);
        });
    }
    
    handleMouseMove(event) {
        if (!this.circularButton) return;
        
        const buttonRect = this.circularButton.getBoundingClientRect();
        const mouseX = event.clientX;
        const mouseY = event.clientY;
        
        // Check if mouse is over the button
        const isOverButton = (
            mouseX >= buttonRect.left &&
            mouseX <= buttonRect.right &&
            mouseY >= buttonRect.top &&
            mouseY <= buttonRect.bottom
        );
        
        if (isOverButton) {
            this.enableButtonClicks();
        } else {
            this.disableButtonClicks();
        }
    }
    
    enableButtonClicks() {
        if (window.require) {
            const { ipcRenderer } = require('electron');
            ipcRenderer.invoke('set-mouse-events', true);
        }
    }
    
    disableButtonClicks() {
        if (window.require) {
            const { ipcRenderer } = require('electron');
            ipcRenderer.invoke('set-mouse-events', false);
        }
    }
    
    handleButtonClick() {
        console.log('🔘 Circular button clicked!');
        this.textBox.success('Committing buffer to log...');
        
        // Commit buffer to log
        this.commitBuffer();
    }
    
    async commitBuffer() {
        try {
            const response = await fetch('http://localhost:5001/commit_buffer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.textBox.success('✅ Buffer committed to log successfully!');
                this.updateButtonVisibility(true); // Hide button
            } else {
                this.textBox.error('❌ Buffer is empty, nothing to commit');
            }
        } catch (error) {
            console.error('Error committing buffer:', error);
            this.textBox.error('❌ Failed to commit buffer');
        }
    }
    
    async checkBufferStatus() {
        try {
            const response = await fetch('http://localhost:5001/buffer_status');
            const result = await response.json();
            
            const wasEmpty = this.bufferEmpty;
            this.bufferEmpty = result.buffer_empty;
            
            // Update button visibility if buffer state changed
            if (wasEmpty !== this.bufferEmpty) {
                this.updateButtonVisibility(this.bufferEmpty);
                
                if (!this.bufferEmpty) {
                    this.textBox.info('📝 New content detected in buffer');
                } else {
                    this.textBox.info('📝 Buffer is now empty');
                }
            }
        } catch (error) {
            console.error('Error checking buffer status:', error);
            // Don't show error messages for server connection issues to avoid spam
            // The button will remain hidden if server is not available
        }
    }
    
    updateButtonVisibility(bufferEmpty) {
        if (this.circularButton) {
            if (bufferEmpty) {
                this.circularButton.style.display = 'none';
            } else {
                this.circularButton.style.display = 'flex';
            }
        }
    }
    
    startBufferMonitoring() {
        // Check buffer status every 2 seconds
        this.bufferCheckInterval = setInterval(() => {
            this.checkBufferStatus();
        }, 2000);
        
        // Initial check
        this.checkBufferStatus();
    }
    
    stopBufferMonitoring() {
        if (this.bufferCheckInterval) {
            clearInterval(this.bufferCheckInterval);
            this.bufferCheckInterval = null;
        }
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