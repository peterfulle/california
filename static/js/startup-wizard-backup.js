/**
 * StartupWizard - Multi-step form with modern UI/UX
 * Enhanced with Alpine.js and modern interactions
 */

document.addEventListener('alpine:init', () => {
    Alpine.data('startupWizard', () => ({
        currentStep: 1,
        totalSteps: 5,
        isLoading: false,
        formData: {},
        errors: {},
        
        steps: [
            {
                id: 1,
                title: 'Información Básica',
                subtitle: 'Cuéntanos sobre tu startup',
                icon: 'rocket',
                fields: ['company_name', 'tagline', 'description', 'founded_date']
            },
            {
                id: 2,
                title: 'Branding & Medios',
                subtitle: 'Imagen de tu marca',
                icon: 'photo',
                fields: ['logo', 'cover_image', 'website', 'demo_url', 'pitch_deck_url']
            },
            {
                id: 3,
                title: 'Industria & Negocio',
                subtitle: 'Define tu mercado',
                icon: 'building',
                fields: ['industry', 'sub_industry', 'stage', 'employees_count', 'business_model']
            },
            {
                id: 4,
                title: 'Tesis & Métricas',
                subtitle: 'Tu propuesta de valor',
                icon: 'chart',
                fields: ['problem_statement', 'solution_description', 'market_size', 'competitive_advantage', 'monthly_revenue', 'seeking_amount']
            },
            {
                id: 5,
                title: 'Revisión Final',
                subtitle: 'Confirma tu información',
                icon: 'check',
                fields: []
            }
        ],

        init() {
            // Set up real-time validation
            this.setupRealTimeValidation();
            
            // Load from localStorage
            this.loadFromStorage();
            
            // Auto-save every 30 seconds
            setInterval(() => {
                this.saveToStorage();
            }, 30000);
        },

        setupRealTimeValidation() {
            // Add event listeners for real-time validation
            this.$nextTick(() => {
                const inputs = document.querySelectorAll('input, textarea, select');
                inputs.forEach(input => {
                    // Validate on input (for real-time feedback)
                    input.addEventListener('input', (e) => {
                        const fieldName = e.target.name;
                        if (fieldName) {
                            this.validateField(fieldName);
                        }
                    });
                    
                    // Validate on blur (when user leaves field)
                    input.addEventListener('blur', (e) => {
                        const fieldName = e.target.name;
                        if (fieldName) {
                            this.validateField(fieldName);
                        }
                    });
                });
            });
        },

        // Navigation methods
        nextStep() {
            if (this.validateCurrentStep()) {
                this.saveCurrentStep();
                if (this.currentStep < this.totalSteps) {
                    this.currentStep++;
                    this.animateStepTransition();
                }
            }
        },

        prevStep() {
            if (this.currentStep > 1) {
                this.currentStep--;
                this.animateStepTransition();
            }
        },

        goToStep(step) {
            if (step <= this.getMaxAccessibleStep()) {
                this.currentStep = step;
                this.animateStepTransition();
            }
        },

        getMaxAccessibleStep() {
            // Users can only go to steps they've completed or the next step
            let maxStep = 1;
            for (let i = 1; i < this.totalSteps; i++) {
                if (this.isStepValid(i)) {
                    maxStep = i + 1;
                } else {
                    break;
                }
            }
            return Math.min(maxStep, this.totalSteps);
        },

        // Validation methods
        validateCurrentStep() {
            const currentStepFields = this.steps[this.currentStep - 1].fields;
            let isValid = true;
            this.errors = {};

            currentStepFields.forEach(field => {
                if (this.isFieldRequired(field) && !this.getFieldValue(field)) {
                    this.errors[field] = 'Este campo es obligatorio';
                    isValid = false;
                }
            });

            return isValid;
        },

        isStepValid(stepNumber) {
            const stepFields = this.steps[stepNumber - 1].fields;
            return stepFields.every(field => 
                !this.isFieldRequired(field) || this.getFieldValue(field)
            );
        },

        isFieldRequired(field) {
            const requiredFields = ['company_name', 'tagline', 'description'];
            return requiredFields.includes(field);
        },

        validateFieldSpecific(fieldName, value) {
            // Specific validation rules
            switch (fieldName) {
                case 'company_name':
                    if (value && value.length < 2) {
                        return 'El nombre debe tener al menos 2 caracteres';
                    }
                    if (value && value.length > 100) {
                        return 'El nombre es demasiado largo (máximo 100 caracteres)';
                    }
                    break;
                
                case 'tagline':
                    if (value && value.length < 10) {
                        return 'El tagline debe ser más descriptivo (mínimo 10 caracteres)';
                    }
                    if (value && value.length > 200) {
                        return 'El tagline es demasiado largo (máximo 200 caracteres)';
                    }
                    break;
                
                case 'description':
                    if (value && value.length < 50) {
                        return 'La descripción debe ser más detallada (mínimo 50 caracteres)';
                    }
                    if (value && value.length > 2000) {
                        return 'La descripción es demasiado larga (máximo 2000 caracteres)';
                    }
                    break;
                
                case 'website':
                    if (value && !value.match(/^https?:\/\/.+/)) {
                        return 'Debe ser una URL válida (ej: https://tusite.com)';
                    }
                    break;
                
                case 'employees_count':
                    if (value && (isNaN(value) || value < 1 || value > 10000)) {
                        return 'Debe ser un número entre 1 y 10,000';
                    }
                    break;
                
                case 'monthly_revenue':
                case 'seeking_amount':
                case 'monthly_users':
                    if (value && (isNaN(value) || value < 0)) {
                        return 'Debe ser un número positivo';
                    }
                    break;
            }
            return null;
        },

        getFieldValue(field) {
            const element = document.querySelector(`[name="${field}"]`);
            return element ? element.value : '';
        },

        // Progress calculation
        getProgress() {
            return (this.currentStep / this.totalSteps) * 100;
        },

        getStepStatus(stepNumber) {
            if (stepNumber < this.currentStep) {
                return this.isStepValid(stepNumber) ? 'completed' : 'error';
            } else if (stepNumber === this.currentStep) {
                return 'current';
            } else {
                return 'pending';
            }
        },

        // Animation methods
        animateStepTransition() {
            const container = document.querySelector('.step-content');
            if (container) {
                container.style.opacity = '0';
                container.style.transform = 'translateX(20px)';
                
                setTimeout(() => {
                    container.style.transition = 'all 0.3s ease-in-out';
                    container.style.opacity = '1';
                    container.style.transform = 'translateX(0)';
                }, 50);
            }
        },

        // File upload methods
        initFileUploads() {
            this.initDropZone('logo');
            this.initDropZone('cover_image');
        },

        initDropZone(fieldName) {
            const dropZone = document.querySelector(`[data-upload="${fieldName}"]`);
            if (!dropZone) return;

            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                dropZone.addEventListener(eventName, this.preventDefaults, false);
            });

            ['dragenter', 'dragover'].forEach(eventName => {
                dropZone.addEventListener(eventName, () => {
                    dropZone.classList.add('drag-over');
                }, false);
            });

            ['dragleave', 'drop'].forEach(eventName => {
                dropZone.addEventListener(eventName, () => {
                    dropZone.classList.remove('drag-over');
                }, false);
            });

            dropZone.addEventListener('drop', (e) => {
                const files = e.dataTransfer.files;
                this.handleFileUpload(files[0], fieldName);
            }, false);
        },

        preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        },

        handleFileUpload(file, fieldName) {
            if (!file || !file.type.startsWith('image/')) {
                this.showToast('Por favor selecciona una imagen válida', 'error');
                return;
            }

            if (file.size > 2 * 1024 * 1024) { // 2MB limit
                this.showToast('La imagen debe ser menor a 2MB', 'error');
                return;
            }

            // Preview the image
            const reader = new FileReader();
            reader.onload = (e) => {
                const preview = document.querySelector(`[data-preview="${fieldName}"]`);
                if (preview) {
                    preview.src = e.target.result;
                    preview.classList.remove('hidden');
                    preview.style.display = 'block';
                }
            };
            reader.readAsDataURL(file);

            // Set the file to the input
            const input = document.querySelector(`[name="${fieldName}"]`);
            if (input) {
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                input.files = dataTransfer.files;
                
                // Trigger change event for validation
                input.dispatchEvent(new Event('change', { bubbles: true }));
            }

            this.showToast('Imagen cargada exitosamente', 'success');
        },

        // Utility methods
        saveCurrentStep() {
            const currentStepFields = this.steps[this.currentStep - 1].fields;
            currentStepFields.forEach(field => {
                this.formData[field] = this.getFieldValue(field);
            });
            localStorage.setItem('startupWizardData', JSON.stringify(this.formData));
        },

        loadSavedData() {
            const saved = localStorage.getItem('startupWizardData');
            if (saved) {
                this.formData = JSON.parse(saved);
                // Restore form values
                Object.keys(this.formData).forEach(field => {
                    const element = document.querySelector(`[name="${field}"]`);
                    if (element && this.formData[field]) {
                        element.value = this.formData[field];
                    }
                });
            }
        },

        initValidation() {
            // Real-time validation
            document.addEventListener('input', (e) => {
                if (e.target.hasAttribute('name')) {
                    const fieldName = e.target.getAttribute('name');
                    this.validateField(fieldName);
                }
            });
        },

        validateField(fieldName) {
            const value = this.getFieldValue(fieldName);
            const element = document.querySelector(`[name="${fieldName}"]`);
            
            // Clear previous states
            if (element) {
                element.classList.remove('field-error', 'field-success');
            }
            
            // Check if required
            if (this.isFieldRequired(fieldName) && !value) {
                this.errors[fieldName] = 'Este campo es obligatorio';
                if (element) {
                    element.classList.add('field-error');
                }
            } else {
                // Check specific validation
                const specificError = this.validateFieldSpecific(fieldName, value);
                if (specificError) {
                    this.errors[fieldName] = specificError;
                    if (element) {
                        element.classList.add('field-error');
                    }
                } else if (value && this.isFieldRequired(fieldName)) {
                    delete this.errors[fieldName];
                    if (element) {
                        element.classList.add('field-success');
                    }
                } else {
                    delete this.errors[fieldName];
                }

            // Update UI with animation
            this.$nextTick(() => {
                const errorElement = document.querySelector(`[data-error="${fieldName}"]`);
                if (errorElement) {
                    errorElement.textContent = this.errors[fieldName] || '';
                    errorElement.classList.toggle('hidden', !this.errors[fieldName]);
                    
                    // Add animation
                    if (this.errors[fieldName]) {
                        errorElement.style.animation = 'slideInRight 0.3s ease-out';
                    }
                }
            });
        },

        getStepProgress() {
            const steps = {
                1: ['company_name', 'tagline', 'founded_date', 'description'],
                2: ['company_logo', 'company_cover'],
                3: ['industry', 'business_model', 'stage'],
                4: ['employees_count', 'monthly_revenue', 'funding_amount'],
                5: [] // Review step
            };
            
            const currentFields = steps[this.currentStep] || [];
            if (currentFields.length === 0) return 100; // Review step
            
            const completedFields = currentFields.filter(field => {
                const value = this.getFieldValue(field);
                return value && !this.errors[field];
            });
            
            return Math.round((completedFields.length / currentFields.length) * 100);
        },

        getOverallProgress() {
            const allRequiredFields = [
                'company_name', 'tagline', 'description', 'industry', 'business_model'
            ];
            
            const completedFields = allRequiredFields.filter(field => {
                const value = this.getFieldValue(field);
                return value && !this.errors[field];
            });
            
            return Math.round((completedFields.length / allRequiredFields.length) * 100);
        }
    }
}            // Update UI with animation
            this.$nextTick(() => {
                const errorElement = document.querySelector(`[data-error="${fieldName}"]`);
                if (errorElement) {
                    errorElement.textContent = this.errors[fieldName] || '';
                    errorElement.classList.toggle('hidden', !this.errors[fieldName]);
                    
                    // Add animation
                    if (this.errors[fieldName]) {
                        errorElement.style.animation = 'slideInRight 0.3s ease-out';
                    }
                }
            });
        },

        showToast(message, type = 'info') {
            // Create toast notification
            const toast = document.createElement('div');
            toast.className = `fixed top-4 right-4 z-50 px-6 py-4 rounded-lg shadow-lg transition-all duration-300 ${
                type === 'success' ? 'bg-green-500 text-white' :
                type === 'error' ? 'bg-red-500 text-white' :
                'bg-blue-500 text-white'
            }`;
            toast.textContent = message;
            
            document.body.appendChild(toast);
            
            setTimeout(() => {
                toast.style.transform = 'translateX(400px)';
                toast.style.opacity = '0';
                setTimeout(() => document.body.removeChild(toast), 300);
            }, 3000);
        },

        // Form submission
        async submitForm() {
            if (!this.validateCurrentStep()) {
                return;
            }

            this.isLoading = true;
            this.saveCurrentStep();

            try {
                const form = document.querySelector('#startup-form');
                const formData = new FormData(form);
                
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                });

                if (response.ok) {
                    localStorage.removeItem('startupWizardData');
                    this.showToast('¡Startup creada exitosamente!', 'success');
                    setTimeout(() => {
                        window.location.href = response.url;
                    }, 1000);
                } else {
                    throw new Error('Error en el servidor');
                }
            } catch (error) {
                this.showToast('Error al crear la startup. Inténtalo de nuevo.', 'error');
            } finally {
                this.isLoading = false;
            }
        }
    }));
});
