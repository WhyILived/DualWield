// Main Application Controller
class HT6ixApp {
    constructor() {
        this.audioVisualizer = null;
        this.textBox = null;
        this.currentView = 'full'; // 'full' or 'mini'
        this.isVisualizerFocused = false;
        this.circularButton = null;
        this.teachingButton = null;
        this.bufferEmpty = true;
        this.logEmpty = true;
        this.teachingActive = false;
        this.bufferCheckInterval = null;
        this.logCheckInterval = null;
        
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
        
        // Start log monitoring
        this.startLogMonitoring();
        
        console.log('HT6ix AI Teaching Bot frontend initialized');
    }
    
    setupCircularButton() {
        this.circularButton = document.getElementById('circular-button');
        this.teachingButton = document.getElementById('teaching-button');
        
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
        
        if (this.teachingButton) {
            this.teachingButton.addEventListener('click', () => {
                this.handleTeachingButtonClick();
            });
            
            this.teachingButton.addEventListener('mouseenter', () => {
                this.enableButtonClicks();
            });
            
            this.teachingButton.addEventListener('mouseleave', () => {
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
        if (!this.circularButton || !this.teachingButton) return;
        
        const buttonRect = this.circularButton.getBoundingClientRect();
        const teachingButtonRect = this.teachingButton.getBoundingClientRect();
        const mouseX = event.clientX;
        const mouseY = event.clientY;
        
        // Check if mouse is over either button
        const isOverCircularButton = (
            mouseX >= buttonRect.left &&
            mouseX <= buttonRect.right &&
            mouseY >= buttonRect.top &&
            mouseY <= buttonRect.bottom
        );
        
        const isOverTeachingButton = (
            mouseX >= teachingButtonRect.left &&
            mouseX <= teachingButtonRect.right &&
            mouseY >= teachingButtonRect.top &&
            mouseY <= teachingButtonRect.bottom
        );
        
        if (isOverCircularButton || isOverTeachingButton) {
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
        
        // Hide button immediately for better UX
        this.hideBufferButton();
        
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
                // Button already hidden in handleButtonClick()
            } else {
                this.textBox.error('❌ Buffer is empty, nothing to commit');
                // Show button again if commit failed
                this.showBufferButtonIfBufferHasContent();
            }
        } catch (error) {
            console.error('Error committing buffer:', error);
            this.textBox.error('❌ Failed to commit buffer');
            // Show button again if commit failed
            this.showBufferButtonIfBufferHasContent();
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
    
    hideBufferButton() {
        if (this.circularButton) {
            this.circularButton.style.display = 'none';
        }
    }
    
    showBufferButtonIfBufferHasContent() {
        // Check if buffer has content and show button if it does
        this.checkBufferStatus();
    }
    
    async clearBuffer() {
        try {
            // Clear buffer by committing it to log (which clears it)
            const response = await fetch('http://localhost:5001/commit_buffer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const result = await response.json();
            
            if (result.success) {
                console.log('✅ Buffer cleared successfully');
            } else {
                console.log('ℹ️ Buffer was already empty');
            }
        } catch (error) {
            console.error('Error clearing buffer:', error);
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
    
    handleTeachingButtonClick() {
        console.log('🎓 Teaching button clicked!');
        
        if (this.teachingActive) {
            this.stopTeachingSession();
        } else {
            // Hide button immediately for better UX
            this.hideTeachingButton();
            // Also hide buffer button and clear buffer since teaching is starting
            this.hideBufferButton();
            this.clearBuffer();
            this.startTeachingSession();
        }
    }
    
    async startTeachingSession() {
        try {
            this.textBox.info('🚀 Starting teaching session...');
            
            const response = await fetch('http://localhost:5001/start_teaching', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.teachingActive = true;
                this.textBox.success('✅ Teaching session started!');
                this.textBox.info(`📚 Topic: ${result.topic}`);
                this.textBox.info(`📝 Subtopics: ${result.subtopics}`);
                this.textBox.info(`📖 Bullet points: ${result.bullet_points}`);
                this.textBox.info('🛑 Content processing stopped');
                this.updateTeachingButtonState(true);
                // Button already hidden in handleTeachingButtonClick()
            } else {
                this.textBox.error(`❌ ${result.message}`);
                // Show button again if teaching failed
                this.showTeachingButtonIfLogHasContent();
            }
        } catch (error) {
            console.error('Error starting teaching session:', error);
            this.textBox.error('❌ Failed to start teaching session');
            // Show button again if teaching failed
            this.showTeachingButtonIfLogHasContent();
        }
    }
    
    async stopTeachingSession() {
        try {
            this.textBox.info('⏹️ Stopping teaching session...');
            
            const response = await fetch('http://localhost:5001/stop_teaching', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.teachingActive = false;
                this.textBox.success('✅ Teaching session stopped!');
                this.textBox.info('🔄 Content processing re-enabled');
                this.updateTeachingButtonState(false);
                this.showTeachingButtonIfLogHasContent(); // Show button again if log has content
            } else {
                this.textBox.error(`❌ ${result.message}`);
            }
        } catch (error) {
            console.error('Error stopping teaching session:', error);
            this.textBox.error('❌ Failed to stop teaching session');
        }
    }
    
    updateTeachingButtonState(active) {
        if (this.teachingButton) {
            if (active) {
                this.teachingButton.classList.add('active');
            } else {
                this.teachingButton.classList.remove('active');
            }
        }
    }
    
    async checkLogStatus() {
        try {
            const response = await fetch('http://localhost:5001/log_status');
            const result = await response.json();
            
            const wasEmpty = this.logEmpty;
            this.logEmpty = result.log_empty;
            
            // Update teaching button visibility if log state changed
            if (wasEmpty !== this.logEmpty) {
                this.updateTeachingButtonVisibility(this.logEmpty);
                
                if (!this.logEmpty) {
                    this.textBox.info('📚 New content available for teaching');
                } else {
                    this.textBox.info('📚 No content available for teaching');
                }
            }
        } catch (error) {
            console.error('Error checking log status:', error);
            // Don't show error messages for server connection issues to avoid spam
        }
    }
    
    updateTeachingButtonVisibility(logEmpty) {
        if (this.teachingButton) {
            if (logEmpty) {
                this.teachingButton.style.display = 'none';
            } else {
                this.teachingButton.style.display = 'flex';
            }
        }
    }
    
    hideTeachingButton() {
        if (this.teachingButton) {
            this.teachingButton.style.display = 'none';
        }
    }
    
    showTeachingButtonIfLogHasContent() {
        // Check if log has content and show button if it does
        this.checkLogStatus();
    }
    
    startLogMonitoring() {
        // Check log status every 3 seconds
        this.logCheckInterval = setInterval(() => {
            this.checkLogStatus();
        }, 3000);
        
        // Initial check
        this.checkLogStatus();
    }
    
    stopLogMonitoring() {
        if (this.logCheckInterval) {
            clearInterval(this.logCheckInterval);
            this.logCheckInterval = null;
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