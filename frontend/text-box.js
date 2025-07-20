// Text Box Component
class TextBox {
    constructor() {
        this.container = null;
        this.content = null;
        this.messages = [];
        this.maxMessages = 50;
        
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
        this.container = document.querySelector('.text-box');
        this.content = document.getElementById('text-box-content');
        
        if (!this.container || !this.content) {
            console.error('Text box elements not found');
            return;
        }
        
        // Add initial message
        this.addMessage('System initialized. Press / to toggle view, = to focus visualizer.', 'info');
        
        console.log('Text box created');
    }
    
    addMessage(text, type = 'info') {
        const message = {
            text: text,
            type: type,
            timestamp: new Date().toLocaleTimeString()
        };
        
        this.messages.push(message);
        
        // Keep only the last maxMessages
        if (this.messages.length > this.maxMessages) {
            this.messages.shift();
        }
        
        this.render();
    }
    
    addTTSMessage(text) {
        const message = {
            text: text,
            type: 'tts',
            timestamp: new Date().toLocaleTimeString()
        };
        
        this.messages.push(message);
        
        // Keep only the last maxMessages
        if (this.messages.length > this.maxMessages) {
            this.messages.shift();
        }
        
        this.render();
    }
    
    render() {
        if (!this.content) return;
        
        this.content.innerHTML = '';
        
        this.messages.forEach(message => {
            const messageElement = document.createElement('div');
            messageElement.className = `message ${message.type}`;
            
            if (message.type === 'tts') {
                // Bold the "Section:" text in TTS messages
                const formattedText = message.text.replace(/^(Section:)/, '<strong>$1</strong>');
                messageElement.innerHTML = `
                    <span class="message-arrow">→</span>
                    <span class="message-text">${formattedText}</span>
                `;
            } else {
                messageElement.innerHTML = `
                    <span class="message-arrow">→</span>
                    <span class="message-text">${message.text}</span>
                `;
            }
            
            this.content.appendChild(messageElement);
        });
        
        this.scrollToBottom();
    }
    
    scrollToBottom() {
        if (this.content) {
            this.content.scrollTop = this.content.scrollHeight;
        }
    }
    
    clear() {
        this.messages = [];
        this.render();
        this.addMessage('Messages cleared.', 'info');
    }
    
    // Convenience methods for different message types
    info(text) {
        this.addMessage(text, 'info');
    }
    
    success(text) {
        this.addMessage(text, 'success');
    }
    
    warning(text) {
        this.addMessage(text, 'warning');
    }
    
    error(text) {
        this.addMessage(text, 'error');
    }
    
    // Method to add learning content
    addLearningContent(content) {
        this.addMessage('📚 New learning content detected!', 'success');
        this.addMessage(content, 'info');
    }
    
    // Method to add quiz content
    addQuizContent(question, options) {
        this.addMessage('❓ Quiz Question:', 'warning');
        this.addMessage(question, 'info');
        
        if (options && options.length > 0) {
            options.forEach((option, index) => {
                this.addMessage(`${String.fromCharCode(65 + index)}. ${option}`, 'info');
            });
        }
    }
    
    // Method to show system status
    showStatus(status) {
        this.addMessage(`🔄 System Status: ${status}`, 'info');
    }
} 