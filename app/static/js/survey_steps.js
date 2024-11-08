// Para verificar que el script se está cargando
console.log('Script survey_steps.js cargado');

const SurveyForm = {
    currentStep: 1,
    totalSteps: 5,

    init() {
        console.log('Inicializando SurveyForm...');
        
        const nextBtn = document.getElementById('nextBtn');
        const prevBtn = document.getElementById('prevBtn');

        if (nextBtn) {
            console.log('Botón siguiente encontrado');
            nextBtn.onclick = () => {
                console.log('Botón siguiente clickeado');
                this.nextStep();
            };
        } else {
            console.log('Error: No se encontró el botón siguiente');
        }

        if (prevBtn) {
            console.log('Botón anterior encontrado');
            prevBtn.onclick = () => {
                console.log('Botón anterior clickeado');
                this.prevStep();
            };
        }

        // Mostrar primer paso
        this.showStep(1);
    },

    showStep(stepNumber) {
        console.log(`Mostrando paso ${stepNumber}`);
        
        // Ocultar todos los pasos
        const steps = document.querySelectorAll('.step-content');
        steps.forEach(step => {
            step.style.display = 'none';
        });

        // Mostrar el paso actual
        const currentStep = document.getElementById(`step${stepNumber}`);
        if (currentStep) {
            currentStep.style.display = 'block';
            console.log(`Paso ${stepNumber} mostrado`);
        } else {
            console.log(`Error: No se encontró el paso ${stepNumber}`);
        }

        this.updateButtons();
        this.updateProgressBar();
    },

    nextStep() {
        console.log('Ejecutando nextStep()');
        console.log('Paso actual:', this.currentStep);
        
        if (this.validateStep(this.currentStep)) {
            if (this.currentStep < this.totalSteps) {
                this.currentStep++;
                console.log('Avanzando al paso:', this.currentStep);
                this.showStep(this.currentStep);
            } else {
                console.log('Último paso - enviando formulario');
                document.getElementById('surveyForm').submit();
            }
        }
    },

    prevStep() {
        console.log('Ejecutando prevStep()');
        if (this.currentStep > 1) {
            this.currentStep--;
            this.showStep(this.currentStep);
        }
    },

    validateStep(step) {
        console.log('Validando paso:', step);
        let isValid = true;
        const currentStep = document.getElementById(`step${step}`);
        
        if (currentStep) {
            const requiredFields = currentStep.querySelectorAll('input[required], select[required]');
            console.log('Campos requeridos encontrados:', requiredFields.length);
            
            requiredFields.forEach(field => {
                if (!field.value) {
                    isValid = false;
                    field.classList.add('is-invalid');
                    console.log('Campo inválido:', field.name);
                } else {
                    field.classList.remove('is-invalid');
                }
            });
        } else {
            console.log(`Error: No se encontró el contenedor del paso ${step}`);
        }

        return isValid;
    },

    updateButtons() {
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');

        if (prevBtn && nextBtn) {
            prevBtn.style.display = this.currentStep === 1 ? 'none' : 'block';
            nextBtn.innerHTML = this.currentStep === this.totalSteps ? 
                'Finalizar <i class="bi bi-check-lg"></i>' : 
                'Siguiente <i class="bi bi-arrow-right"></i>';
        }
    },

    updateProgressBar() {
        const progress = ((this.currentStep - 1) / (this.totalSteps - 1)) * 100;
        const progressBar = document.querySelector('.progress-bar');
        if (progressBar) {
            progressBar.style.width = `${progress}%`;
            progressBar.setAttribute('aria-valuenow', progress);
        }

        const stepText = document.querySelector('small.text-muted');
        if (stepText) {
            stepText.textContent = `Paso ${this.currentStep} de ${this.totalSteps}`;
        }
    }
};

// Inicializar cuando el documento esté listo
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM cargado - Inicializando formulario');
    SurveyForm.init();
});