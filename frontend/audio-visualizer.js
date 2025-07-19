// Audio Visualizer Component
class AudioVisualizer {
    constructor() {
        this.canvas = null;
        this.ctx = null;
        this.audioContext = null;
        this.analyser = null;
        this.dataArray = null;
        this.bufferLength = 0;
        this.isAudioInitialized = false;
        this.frame = 0;
        this.isFocused = false;
        
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
        this.canvas = document.getElementById('canvas-center');
        if (!this.canvas) {
            console.error('Canvas not found');
            return;
        }
        
        this.ctx = this.canvas.getContext('2d');
        this.setupCanvas();
        this.initAudio();
        this.animate();
        
        console.log('Audio visualizer created');
    }
    
    setupCanvas() {
        const resizeCanvas = () => {
            const rect = this.canvas.getBoundingClientRect();
            this.canvas.width = rect.width;
            this.canvas.height = rect.height;
        };
        
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);
    }
    
    async initAudio() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.analyser = this.audioContext.createAnalyser();
            this.analyser.fftSize = 256;
            this.bufferLength = this.analyser.frequencyBinCount;
            this.dataArray = new Uint8Array(this.bufferLength);
            
            const source = this.audioContext.createMediaStreamSource(stream);
            source.connect(this.analyser);
            this.isAudioInitialized = true;
            
            console.log('Audio initialized successfully');
        } catch (error) {
            console.error('Failed to initialize audio:', error);
            this.isAudioInitialized = false;
        }
    }
    
    animate() {
        this.frame += 0.05;
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        const baseRadius = Math.min(this.canvas.width, this.canvas.height) * 0.3;
        
        // Get audio data
        let audioLevel = 0;
        if (this.isAudioInitialized && this.analyser) {
            this.analyser.getByteTimeDomainData(this.dataArray);
            
            // Calculate RMS (root mean square) for volume
            let sum = 0;
            for (let i = 0; i < this.bufferLength; i++) {
                let v = (this.dataArray[i] - 128) / 128;
                sum += v * v;
            }
            audioLevel = Math.sqrt(sum / this.bufferLength);
        } else {
            // Fallback idle animation
            audioLevel = Math.sin(this.frame) * 0.1;
        }
        
        // Draw animated ring
        this.drawRing(centerX, centerY, baseRadius, audioLevel);
        
        // Draw frequency bars if focused
        if (this.isFocused) {
            this.drawFrequencyBars(audioLevel);
        }
        
        requestAnimationFrame(() => this.animate());
    }
    
    drawRing(centerX, centerY, baseRadius, audioLevel) {
        const dynamicRadius = baseRadius + (audioLevel * baseRadius * 0.5);
        
        this.ctx.save();
        this.ctx.strokeStyle = this.getRingColor(audioLevel);
        this.ctx.lineWidth = 3;
        this.ctx.globalAlpha = 0.8;
        
        // Draw main ring
        this.ctx.beginPath();
        this.ctx.arc(centerX, centerY, dynamicRadius, 0, Math.PI * 2);
        this.ctx.stroke();
        
        // Draw inner ring
        this.ctx.strokeStyle = this.getRingColor(audioLevel * 0.5);
        this.ctx.lineWidth = 1;
        this.ctx.beginPath();
        this.ctx.arc(centerX, centerY, dynamicRadius * 0.7, 0, Math.PI * 2);
        this.ctx.stroke();
        
        // Draw pulsing dots
        for (let i = 0; i < 8; i++) {
            const angle = (i / 8) * Math.PI * 2 + this.frame;
            const x = centerX + Math.cos(angle) * dynamicRadius;
            const y = centerY + Math.sin(angle) * dynamicRadius;
            
            this.ctx.fillStyle = this.getRingColor(audioLevel);
            this.ctx.globalAlpha = 0.6 + Math.sin(this.frame * 2 + i) * 0.4;
            this.ctx.beginPath();
            this.ctx.arc(x, y, 3, 0, Math.PI * 2);
            this.ctx.fill();
        }
        
        this.ctx.restore();
    }
    
    drawFrequencyBars(audioLevel) {
        if (!this.isAudioInitialized || !this.analyser) return;
        
        this.analyser.getByteFrequencyData(this.dataArray);
        
        const barCount = 32;
        const barWidth = this.canvas.width / barCount;
        const maxBarHeight = this.canvas.height * 0.3;
        
        this.ctx.save();
        this.ctx.fillStyle = '#00aaff';
        this.ctx.globalAlpha = 0.7;
        
        for (let i = 0; i < barCount; i++) {
            const dataIndex = Math.floor((i / barCount) * this.bufferLength);
            const barHeight = (this.dataArray[dataIndex] / 255) * maxBarHeight;
            
            const x = (this.canvas.width / 2) - (barCount * barWidth / 2) + (i * barWidth);
            const y = this.canvas.height / 2 + maxBarHeight / 2;
            
            this.ctx.fillRect(x + 2, y - barHeight, barWidth - 4, barHeight);
        }
        
        this.ctx.restore();
    }
    
    getRingColor(audioLevel) {
        if (audioLevel > 0.3) {
            return '#00ff88'; // Green for high activity
        } else if (audioLevel > 0.1) {
            return '#ff6b00'; // Orange for medium activity
        } else {
            return '#00aaff'; // Blue for low/idle activity
        }
    }
    
    setFocus(focused) {
        this.isFocused = focused;
        const visualizer = document.querySelector('.center-visualizer');
        if (focused) {
            visualizer.classList.add('focused');
        } else {
            visualizer.classList.remove('focused');
        }
    }
    
    getAudioLevel() {
        if (!this.isAudioInitialized || !this.analyser) return 0;
        
        this.analyser.getByteTimeDomainData(this.dataArray);
        let sum = 0;
        for (let i = 0; i < this.bufferLength; i++) {
            let v = (this.dataArray[i] - 128) / 128;
            sum += v * v;
        }
        return Math.sqrt(sum / this.bufferLength);
    }
} 