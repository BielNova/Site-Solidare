document.addEventListener('DOMContentLoaded', function() {
    const formSteps = document.querySelectorAll('.form-step');
    const progressBarSteps = document.querySelectorAll('.progress-steps .step');
    const totalSteps = formSteps.length;
    let currentStep = 0;

    function showStep(stepIndex) {
        formSteps.forEach((step, index) => {
            if (index === stepIndex) {
                step.style.display = 'block';
                step.classList.add('active');
            } else {
                step.style.display = 'none';
                step.classList.remove('active');
            }
        });

        progressBarSteps.forEach((pbStep, index) => {
            if (index === stepIndex) {
                pbStep.classList.add('active');
            } else {
                pbStep.classList.remove('active');
            }
            // Marcar passos anteriores como completos
            if (index < stepIndex) {
                pbStep.classList.add('completed');
            } else {
                pbStep.classList.remove('completed');
            }
        });
    }

    // Navegação para o próximo passo
    document.querySelectorAll('.btn-next').forEach(button => {
        button.addEventListener('click', function() {
            // **IMPORTANTE: Validação no Frontend**
            // Aqui você deveria adicionar a lógica de validação para os campos da etapa atual.
            // Por exemplo:
            // const currentInputs = formSteps[currentStep].querySelectorAll('input, select, textarea');
            // let isValid = true;
            // currentInputs.forEach(input => {
            //     if (input.required && !input.value) { // Exemplo simples
            //         isValid = false;
            //         input.classList.add('is-invalid'); // Adicionar classe para indicar erro
            //     } else {
            //         input.classList.remove('is-invalid');
            //     }
            // });

            // if (!isValid) {
            //     alert('Por favor, preencha todos os campos obrigatórios.');
            //     return;
            // }

            if (currentStep < totalSteps - 1) {
                currentStep++;
                showStep(currentStep);
            }
        });
    });

    // Navegação para o passo anterior
    document.querySelectorAll('.btn-prev').forEach(button => {
        button.addEventListener('click', function() {
            if (currentStep > 0) {
                currentStep--;
                showStep(currentStep);
            }
        });
    });

    // Inicializa o formulário mostrando a primeira etapa
    showStep(currentStep);
});