// Formulario multi-paso completamente funcional
document.addEventListener('DOMContentLoaded', function() {
    console.log('Inicializando formulario de startup...');
    
    // Verificar que Alpine está disponible
    if (typeof Alpine === 'undefined') {
        console.error('Alpine.js no está disponible');
        return;
    }
    
    Alpine.data('startupForm', () => ({
        currentStep: 1,
        totalSteps: 3,
        
        init() {
            console.log('Formulario inicializado correctamente');
        },
        
        nextStep() {
            if (this.currentStep < this.totalSteps) {
                this.currentStep++;
                console.log('Avanzando al paso:', this.currentStep);
            }
        },
        
        prevStep() {
            if (this.currentStep > 1) {
                this.currentStep--;
                console.log('Retrocediendo al paso:', this.currentStep);
            }
        },
        
        goToStep(step) {
            if (step >= 1 && step <= this.totalSteps) {
                this.currentStep = step;
                console.log('Saltando al paso:', step);
            }
        },
        
        getProgress() {
            return Math.round((this.currentStep / this.totalSteps) * 100);
        },
        
        isFirstStep() {
            return this.currentStep === 1;
        },
        
        isLastStep() {
            return this.currentStep === this.totalSteps;
        },
        
        canProceed() {
            // Validación básica por paso
            switch(this.currentStep) {
                case 1:
                    const companyName = document.querySelector('[name="company_name"]');
                    const tagline = document.querySelector('[name="tagline"]');
                    return companyName && companyName.value.trim() !== '' && 
                           tagline && tagline.value.trim() !== '';
                case 2:
                    const industry = document.querySelector('[name="industry"]');
                    return industry && industry.value !== '';
                case 3:
                    return true; // Último paso, siempre puede proceder
                default:
                    return true;
            }
        },
        
        submitForm() {
            console.log('Enviando formulario...');
            const form = document.getElementById('startup-form');
            if (form) {
                form.submit();
            }
        }
    }));
    
    console.log('Alpine data registrado exitosamente');
});
