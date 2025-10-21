document.addEventListener('DOMContentLoaded', function() {
    console.log('Alpine script loading...');
    
    // Ensure Alpine is loaded
    if (typeof Alpine === 'undefined') {
        console.error('Alpine.js not loaded!');
        return;
    }
    
    console.log('Alpine found, registering component...');
    
    Alpine.data('startupWizard', () => ({
        currentStep: 1,
        totalSteps: 3,
        isLoading: false,
        errors: {},
        form: {},

        init() {
            console.log('startupWizard component initialized!');
        },

        nextStep() {
            console.log('nextStep called, current:', this.currentStep);
            if (this.currentStep < this.totalSteps) {
                this.currentStep++;
                console.log('Moved to step:', this.currentStep);
            }
        },

        prevStep() {
            console.log('prevStep called, current:', this.currentStep);
            if (this.currentStep > 1) {
                this.currentStep--;
                console.log('Moved to step:', this.currentStep);
            }
        },

        getFieldValue(fieldName) {
            const element = document.querySelector(`[name="${fieldName}"]`);
            return element ? element.value : '';
        },

        getOverallProgress() {
            return Math.round((this.currentStep / this.totalSteps) * 100);
        },

        getStepProgress() {
            return Math.round((this.currentStep / this.totalSteps) * 100);
        },

        validateField(fieldName) {
            // Simple validation for now
            const value = this.getFieldValue(fieldName);
            if (!value) {
                this.errors[fieldName] = 'Este campo es requerido';
            } else {
                delete this.errors[fieldName];
            }
        },

        showToast(message, type = 'info') {
            console.log('Toast:', message, type);
        },

        async submitForm() {
            console.log('Submit form called');
            this.showToast('Funcionalidad en desarrollo', 'info');
        }
    }));
    
    console.log('Component registered successfully');
});
