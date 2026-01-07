document.addEventListener('DOMContentLoaded', function() {
    console.log('Startup wizard script loaded');
    
    Alpine.data('startupWizard', () => ({
        currentStep: 1,
        totalSteps: 5,
        isLoading: false,
        errors: {},
        form: {},

        init() {
            console.log('Alpine startupWizard initialized');
            this.setupRealTimeValidation();
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

        nextStep() {
            if (this.validateCurrentStep()) {
                this.saveCurrentStep();
                if (this.currentStep < this.totalSteps) {
                    this.currentStep++;
                    this.showToast(`Paso ${this.currentStep} de ${this.totalSteps}`, 'info');
                }
            }
        },

        prevStep() {
            if (this.currentStep > 1) {
                this.currentStep--;
            }
        },

        goToStep(step) {
            if (step >= 1 && step <= this.totalSteps) {
                this.currentStep = step;
            }
        },

        validateCurrentStep() {
            const requiredFields = this.getRequiredFieldsForStep(this.currentStep);
            let isValid = true;

            requiredFields.forEach(fieldName => {
                this.validateField(fieldName);
                if (this.errors[fieldName]) {
                    isValid = false;
                }
            });

            if (!isValid) {
                this.showToast('Por favor completa todos los campos requeridos', 'error');
            }

            return isValid;
        },

        getRequiredFieldsForStep(step) {
            const stepFields = {
                1: ['company_name', 'tagline', 'description'],
                2: [],
                3: ['industry', 'business_model'],
                4: [],
                5: []
            };
            return stepFields[step] || [];
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

        validateFieldSpecific(fieldName, value) {
            if (!value) return null;

            switch(fieldName) {
                case 'company_name':
                    if (value.length < 2) return 'El nombre debe tener al menos 2 caracteres';
                    if (value.length > 100) return 'El nombre no puede superar los 100 caracteres';
                    if (!/^[a-zA-ZÀ-ÿ\u00f1\u00d1\s\d&.-]+$/.test(value)) return 'El nombre contiene caracteres no válidos';
                    break;
                
                case 'tagline':
                    if (value.length < 10) return 'El eslogan debe tener al menos 10 caracteres';
                    if (value.length > 200) return 'El eslogan no puede superar los 200 caracteres';
                    break;
                
                case 'description':
                    if (value.length < 50) return 'La descripción debe tener al menos 50 caracteres';
                    if (value.length > 1000) return 'La descripción no puede superar los 1000 caracteres';
                    break;
                
                case 'website':
                    if (value && !/^https?:\/\/[^\s$.?#].[^\s]*$/.test(value)) {
                        return 'Por favor ingresa una URL válida (ej: https://ejemplo.com)';
                    }
                    break;
                
                case 'employees_count':
                    const num = parseInt(value);
                    if (isNaN(num) || num < 1) return 'Debe ser un número mayor a 0';
                    if (num > 10000) return 'El número parece demasiado alto';
                    break;
                
                case 'monthly_revenue':
                case 'funding_amount':
                    const amount = parseFloat(value);
                    if (isNaN(amount) || amount < 0) return 'Debe ser un número positivo';
                    break;
            }
            
            return null;
        },

        isFieldRequired(fieldName) {
            const requiredFields = ['company_name', 'tagline', 'description', 'industry', 'business_model'];
            return requiredFields.includes(fieldName);
        },

        getFieldValue(fieldName) {
            const element = document.querySelector(`[name="${fieldName}"]`);
            return element ? element.value : '';
        },

        saveCurrentStep() {
            const formData = new FormData(document.querySelector('#startup-form'));
            const data = {};
            
            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }
            
            this.form = { ...this.form, ...data };
            this.saveToStorage();
        },

        saveToStorage() {
            const data = {
                currentStep: this.currentStep,
                form: this.form,
                errors: this.errors,
                timestamp: Date.now()
            };
            localStorage.setItem('startupWizardData', JSON.stringify(data));
        },

        loadFromStorage() {
            const saved = localStorage.getItem('startupWizardData');
            if (saved) {
                try {
                    const data = JSON.parse(saved);
                    
                    // Check if data is not too old (24 hours)
                    if (Date.now() - data.timestamp < 24 * 60 * 60 * 1000) {
                        this.currentStep = data.currentStep || 1;
                        this.form = data.form || {};
                        this.errors = data.errors || {};
                        
                        // Restore form values
                        this.$nextTick(() => {
                            Object.keys(this.form).forEach(key => {
                                const element = document.querySelector(`[name="${key}"]`);
                                if (element && this.form[key]) {
                                    element.value = this.form[key];
                                }
                            });
                        });
                    }
                } catch (e) {
                    console.error('Error loading from storage:', e);
                }
            }
        },

        // File upload methods
        handleFileUpload(event, fileType) {
            const file = event.target.files[0];
            if (file) {
                this.previewFile(file, fileType);
            }
        },

        handleFileDrop(event, fileType) {
            event.preventDefault();
            const file = event.dataTransfer.files[0];
            if (file) {
                const input = document.querySelector(`[name="${fileType}"]`);
                if (input) {
                    input.files = event.dataTransfer.files;
                    this.previewFile(file, fileType);
                }
            }
        },

        previewFile(file, fileType) {
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const preview = document.querySelector(`#${fileType}-preview`);
                    if (preview) {
                        preview.src = e.target.result;
                        preview.classList.remove('hidden');
                    }
                };
                reader.readAsDataURL(file);
            }
        },

        removeFile(fileType) {
            const input = document.querySelector(`[name="${fileType}"]`);
            const preview = document.querySelector(`#${fileType}-preview`);
            
            if (input) input.value = '';
            if (preview) {
                preview.src = '';
                preview.classList.add('hidden');
            }
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
        },

        showToast(message, type = 'info') {
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
                setTimeout(() => toast.remove(), 300);
            }, 3000);
        },

        async submitForm() {
            if (!this.validateCurrentStep()) return;
            
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
