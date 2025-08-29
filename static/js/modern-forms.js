// Modern Forms JavaScript - Interacciones avanzadas para formularios
class ModernFormHandler {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 3;
        this.form = document.getElementById('startup-form');
        this.init();
    }

    init() {
        this.setupStepNavigation();
        this.setupFormValidation();
        this.setupFileUploads();
        this.setupProgressIndicator();
        this.setupAnimations();
        this.setupFloatingLabels();
        this.setupTooltips();
    }

    setupStepNavigation() {
        const nextButtons = document.querySelectorAll('[data-next-step]');
        const prevButtons = document.querySelectorAll('[data-prev-step]');

        nextButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const nextStep = parseInt(button.dataset.nextStep);
                if (this.validateCurrentStep()) {
                    this.goToStep(nextStep);
                }
            });
        });

        prevButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const prevStep = parseInt(button.dataset.prevStep);
                this.goToStep(prevStep);
            });
        });
    }

    setupFormValidation() {
        const inputs = this.form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            // Real-time validation
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearFieldError(input));
            
            // Enhanced UX for different input types
            if (input.type === 'email') {
                input.addEventListener('input', () => this.validateEmail(input));
            }
            
            if (input.type === 'url') {
                input.addEventListener('input', () => this.validateUrl(input));
            }
        });
    }

    setupFileUploads() {
        const uploadAreas = document.querySelectorAll('.upload-area');
        
        uploadAreas.forEach(area => {
            const input = area.querySelector('input[type="file"]');
            const preview = area.querySelector('.file-preview');
            
            // Drag and drop functionality
            area.addEventListener('dragover', (e) => {
                e.preventDefault();
                area.classList.add('drag-over');
            });
            
            area.addEventListener('dragleave', () => {
                area.classList.remove('drag-over');
            });
            
            area.addEventListener('drop', (e) => {
                e.preventDefault();
                area.classList.remove('drag-over');
                const files = e.dataTransfer.files;
                this.handleFileUpload(input, files, preview);
            });
            
            // Click to upload
            area.addEventListener('click', () => input.click());
            
            // File input change
            input.addEventListener('change', (e) => {
                this.handleFileUpload(input, e.target.files, preview);
            });
        });
    }

    setupProgressIndicator() {
        this.updateProgress();
    }

    setupAnimations() {
        // Add smooth transitions to form steps
        const steps = document.querySelectorAll('.form-step');
        steps.forEach((step, index) => {
            if (index + 1 !== this.currentStep) {
                step.classList.remove('active');
            }
        });
    }

    setupFloatingLabels() {
        const floatingInputs = document.querySelectorAll('.floating-label input');
        
        floatingInputs.forEach(input => {
            // Set initial state
            if (input.value) {
                input.classList.add('has-value');
            }
            
            input.addEventListener('focus', () => {
                input.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', () => {
                input.parentElement.classList.remove('focused');
                if (input.value) {
                    input.classList.add('has-value');
                } else {
                    input.classList.remove('has-value');
                }
            });
        });
    }

    setupTooltips() {
        const tooltipElements = document.querySelectorAll('[data-tooltip]');
        
        tooltipElements.forEach(element => {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = element.dataset.tooltip;
            
            element.addEventListener('mouseenter', () => {
                document.body.appendChild(tooltip);
                this.positionTooltip(element, tooltip);
                tooltip.classList.add('visible');
            });
            
            element.addEventListener('mouseleave', () => {
                if (tooltip.parentNode) {
                    document.body.removeChild(tooltip);
                }
            });
        });
    }

    goToStep(stepNumber) {
        if (stepNumber < 1 || stepNumber > this.totalSteps) return;
        
        const currentStepElement = document.querySelector(`#step-${this.currentStep}`);
        const nextStepElement = document.querySelector(`#step-${stepNumber}`);
        
        if (currentStepElement && nextStepElement) {
            // Animate out current step
            currentStepElement.classList.remove('active');
            
            // Animate in next step
            setTimeout(() => {
                nextStepElement.classList.add('active');
            }, 200);
            
            this.currentStep = stepNumber;
            this.updateStepIndicator();
            this.updateProgress();
            this.scrollToTop();
        }
    }

    validateCurrentStep() {
        const currentStepElement = document.querySelector(`#step-${this.currentStep}`);
        const inputs = currentStepElement.querySelectorAll('input, textarea, select');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!this.validateField(input)) {
                isValid = false;
            }
        });
        
        return isValid;
    }

    validateField(field) {
        let isValid = true;
        const value = field.value.trim();
        
        // Required field validation
        if (field.hasAttribute('required') && !value) {
            this.showFieldError(field, 'Este campo es requerido');
            isValid = false;
        }
        
        // Email validation
        else if (field.type === 'email' && value && !this.isValidEmail(value)) {
            this.showFieldError(field, 'Introduce un email válido');
            isValid = false;
        }
        
        // URL validation
        else if (field.type === 'url' && value && !this.isValidUrl(value)) {
            this.showFieldError(field, 'Introduce una URL válida');
            isValid = false;
        }
        
        // Minimum length validation
        else if (field.hasAttribute('minlength') && value.length < parseInt(field.getAttribute('minlength'))) {
            this.showFieldError(field, `Mínimo ${field.getAttribute('minlength')} caracteres`);
            isValid = false;
        }
        
        if (isValid) {
            this.clearFieldError(field);
            field.classList.add('input-success');
            setTimeout(() => field.classList.remove('input-success'), 2000);
        }
        
        return isValid;
    }

    showFieldError(field, message) {
        field.classList.add('input-error');
        
        let errorElement = field.parentNode.querySelector('.error-message');
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.className = 'error-message';
            field.parentNode.appendChild(errorElement);
        }
        
        errorElement.innerHTML = `
            <svg fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
            </svg>
            ${message}
        `;
    }

    clearFieldError(field) {
        field.classList.remove('input-error');
        const errorElement = field.parentNode.querySelector('.error-message');
        if (errorElement) {
            errorElement.remove();
        }
    }

    updateStepIndicator() {
        const stepItems = document.querySelectorAll('.step-item');
        
        stepItems.forEach((item, index) => {
            const stepNumber = index + 1;
            item.classList.remove('active', 'completed');
            
            if (stepNumber < this.currentStep) {
                item.classList.add('completed');
            } else if (stepNumber === this.currentStep) {
                item.classList.add('active');
            }
        });
    }

    updateProgress() {
        const progressBar = document.querySelector('.progress-bar-fill');
        if (progressBar) {
            const percentage = (this.currentStep / this.totalSteps) * 100;
            progressBar.style.width = `${percentage}%`;
        }
    }

    handleFileUpload(input, files, preview) {
        if (files.length > 0) {
            const file = files[0];
            const maxSize = 5 * 1024 * 1024; // 5MB
            
            // Validate file size
            if (file.size > maxSize) {
                this.showNotification('El archivo es demasiado grande. Máximo 5MB.', 'error');
                return;
            }
            
            // Validate file type for images
            if (input.accept && input.accept.includes('image/')) {
                if (!file.type.startsWith('image/')) {
                    this.showNotification('Solo se permiten archivos de imagen.', 'error');
                    return;
                }
            }
            
            // Create preview for images
            if (file.type.startsWith('image/') && preview) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    preview.innerHTML = `
                        <img src="${e.target.result}" alt="Preview" class="w-full h-32 object-cover rounded-lg">
                        <p class="text-sm text-gray-600 mt-2">${file.name}</p>
                    `;
                };
                reader.readAsDataURL(file);
            } else if (preview) {
                preview.innerHTML = `
                    <div class="flex items-center space-x-2">
                        <svg class="w-8 h-8 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 0v12h8V4H6z" clip-rule="evenodd"/>
                        </svg>
                        <span class="text-sm text-gray-700">${file.name}</span>
                    </div>
                `;
            }
            
            this.showNotification('Archivo subido correctamente', 'success');
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="flex items-center space-x-2">
                ${this.getNotificationIcon(type)}
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => notification.classList.add('show'), 100);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentNode) {
                    document.body.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    getNotificationIcon(type) {
        const icons = {
            success: `<svg class="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>`,
            error: `<svg class="w-5 h-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
            </svg>`,
            info: `<svg class="w-5 h-5 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
            </svg>`
        };
        return icons[type] || icons.info;
    }

    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    isValidUrl(url) {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    }

    scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }

    positionTooltip(element, tooltip) {
        const rect = element.getBoundingClientRect();
        tooltip.style.position = 'absolute';
        tooltip.style.left = `${rect.left + (rect.width / 2)}px`;
        tooltip.style.top = `${rect.top - 40}px`;
        tooltip.style.transform = 'translateX(-50%)';
    }
}

// CSS for notifications and tooltips
const notificationStyles = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #3b82f6;
        z-index: 1000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 400px;
    }
    
    .notification.show {
        transform: translateX(0);
    }
    
    .notification-success {
        border-left-color: #10b981;
    }
    
    .notification-error {
        border-left-color: #ef4444;
    }
    
    .tooltip {
        background: #1f2937;
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 500;
        z-index: 1000;
        opacity: 0;
        transition: opacity 0.2s ease;
        pointer-events: none;
    }
    
    .tooltip.visible {
        opacity: 1;
    }
    
    .tooltip::after {
        content: '';
        position: absolute;
        bottom: -4px;
        left: 50%;
        transform: translateX(-50%);
        width: 0;
        height: 0;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 4px solid #1f2937;
    }
    
    .drag-over {
        background: rgba(14, 165, 233, 0.05) !important;
        border-color: #0ea5e9 !important;
        transform: scale(1.02);
    }
`;

// Inject styles
const styleSheet = document.createElement('style');
styleSheet.textContent = notificationStyles;
document.head.appendChild(styleSheet);

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ModernFormHandler();
});

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ModernFormHandler;
}
