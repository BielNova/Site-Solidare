// static/js/inscricao_form.js

document.addEventListener('DOMContentLoaded', function() {
    const formSteps = document.querySelectorAll('.form-step');
    const prevBtns = document.querySelectorAll('.btn-prev');
    const nextBtns = document.querySelectorAll('.btn-next');
    const progressBarSteps = document.querySelectorAll('.progress-steps .step');

    let currentStep = 0;

    // Função para atualizar a exibição das etapas
    function updateFormSteps() {
        formSteps.forEach((step, index) => {
            step.style.display = (index === currentStep) ? 'block' : 'none';
        });
        updateProgressBar();
    }

    // Função para atualizar a barra de progresso
    function updateProgressBar() {
        progressBarSteps.forEach((step, index) => {
            if (index === currentStep) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
            // Ativar conectores se a etapa anterior estiver ativa
            const connector = step.nextElementSibling;
            if (connector && index < currentStep) {
                connector.classList.add('active');
            } else if (connector) {
                connector.classList.remove('active');
            }
        });
    }

    // Adicionar listeners para os botões "Próximo"
    nextBtns.forEach(button => {
        button.addEventListener('click', () => {
            // Opcional: Adicionar validação aqui antes de avançar
            // if (!validateCurrentStep()) {
            //     return; // Não avança se a validação falhar
            // }

            if (currentStep < formSteps.length - 1) {
                currentStep++;
                updateFormSteps();
            }
        });
    });

    // Adicionar listeners para os botões "Anterior"
    prevBtns.forEach(button => {
        button.addEventListener('click', () => {
            if (currentStep > 0) {
                currentStep--;
                updateFormSteps();
            }
        });
    });

    // Inicializar o formulário na primeira etapa
    updateFormSteps();


    // === LÓGICA PARA MOSTRAR/ESCONDER CAMPOS ADICIONAIS ===

    // SAÚDE: Plano de Saúde
    const planoSim = document.getElementById('plano_sim');
    const planoNao = document.getElementById('plano_nao');
    const qualPlanoSaude = document.getElementById('qual_plano_saude');
    if (planoSim && planoNao && qualPlanoSaude) {
        const togglePlanoSaude = () => qualPlanoSaude.style.display = planoSim.checked ? 'block' : 'none';
        planoSim.addEventListener('change', togglePlanoSaude);
        planoNao.addEventListener('change', togglePlanoSaude);
        togglePlanoSaude(); // Inicializar estado
    }

    // SAÚDE: Acompanhamento Médico
    const medicoSim = document.getElementById('medico_sim');
    const medicoNao = document.getElementById('medico_nao');
    const qualProblemaSaude = document.getElementById('qual_problema_saude');
    if (medicoSim && medicoNao && qualProblemaSaude) {
        const toggleProblemaSaude = () => qualProblemaSaude.style.display = medicoSim.checked ? 'block' : 'none';
        medicoSim.addEventListener('change', toggleProblemaSaude);
        medicoNao.addEventListener('change', toggleProblemaSaude);
        toggleProblemaSaude(); // Inicializar estado
    }

    // SAÚDE: Cirurgia
    const cirurgiaSim = document.getElementById('cirurgia_sim');
    const cirurgiaNao = document.getElementById('cirurgia_nao');
    const qualCirurgia = document.getElementById('qual_cirurgia');
    if (cirurgiaSim && cirurgiaNao && qualCirurgia) {
        const toggleCirurgia = () => qualCirurgia.style.display = cirurgiaSim.checked ? 'block' : 'none';
        cirurgiaSim.addEventListener('change', toggleCirurgia);
        cirurgiaNao.addEventListener('change', toggleCirurgia);
        toggleCirurgia(); // Inicializar estado
    }

    // SAÚDE: Deficiência Física
    const defFisicaSim = document.getElementById('def_fisica_sim');
    const defFisicaNao = document.getElementById('def_fisica_nao');
    const qualDeficienciaFisica = document.getElementById('qual_deficiencia_fisica');
    if (defFisicaSim && defFisicaNao && qualDeficienciaFisica) {
        const toggleDefFisica = () => qualDeficienciaFisica.style.display = defFisicaSim.checked ? 'block' : 'none';
        defFisicaSim.addEventListener('change', toggleDefFisica);
        defFisicaNao.addEventListener('change', toggleDefFisica);
        toggleDefFisica(); // Inicializar estado
    }

    // SAÚDE: Condição de Desenvolvimento Mental
    const defMentalSim = document.getElementById('def_mental_sim');
    const defMentalNao = document.getElementById('def_mental_nao');
    const doencaTranstornoSelect = document.getElementById('doenca_transtorno');
    if (defMentalSim && defMentalNao && doencaTranstornoSelect) {
        const toggleDoencaTranstorno = () => doencaTranstornoSelect.style.display = defMentalSim.checked ? 'block' : 'none';
        defMentalSim.addEventListener('change', toggleDoencaTranstorno);
        defMentalNao.addEventListener('change', toggleDoencaTranstorno);
        toggleDoencaTranstorno(); // Inicializar estado
    }

    // GRUPOS COMUNITÁRIOS: Campo "Qual"
    const gruposSim = document.getElementById('grupos_sim');
    const gruposNao = document.getElementById('grupos_nao');
    const qualGrupoComunitario = document.getElementById('qual_grupo_comunitario');
    if (gruposSim && gruposNao && qualGrupoComunitario) {
        const toggleGrupoComunitario = () => qualGrupoComunitario.style.display = gruposSim.checked ? 'block' : 'none';
        gruposSim.addEventListener('change', toggleGrupoComunitario);
        gruposNao.addEventListener('change', toggleGrupoComunitario);
        toggleGrupoComunitario(); // Inicializar estado
    }

    // ETAPA 4: Conhece algum conselho de direito?
    const conselhoSim = document.getElementById('conselho_sim');
    const conselhoJaOuvi = document.getElementById('conselho_ja_ouvi');
    const conselhoNao = document.getElementById('conselho_nao');
    const conselhoQual = document.getElementById('conselho_qual');
    if (conselhoSim && conselhoJaOuvi && conselhoNao && conselhoQual) {
        const toggleConselhoQual = () => {
            conselhoQual.style.display = (conselhoSim.checked || conselhoJaOuvi.checked) ? 'block' : 'none';
        };
        conselhoSim.addEventListener('change', toggleConselhoQual);
        conselhoJaOuvi.addEventListener('change', toggleConselhoQual);
        conselhoNao.addEventListener('change', toggleConselhoQual);
        toggleConselhoQual(); // Inicializar estado
    }


    // NOVOS JS PARA ETAPA 8: MORADIA E SANEAMENTO
    // Números de Cômodos - Mostrar input "Quantos?" se "Outro" for selecionado
    const numComodosSelect = document.getElementById('num_comodos');
    const outrosComodosInput = document.getElementById('outros_comodos');
    if (numComodosSelect && outrosComodosInput) {
        const toggleOutrosComodos = () => outrosComodosInput.style.display = numComodosSelect.value === 'outro' ? 'block' : 'none';
        numComodosSelect.addEventListener('change', toggleOutrosComodos);
        toggleOutrosComodos(); // Inicializar estado
    }

    // Tem Banheiro - Mostrar select "Se sim, dentro da casa?" se "Sim" for marcado
    const temBanheiroSim8 = document.getElementById('tem_banheiro_sim_8');
    const temBanheiroNao8 = document.getElementById('tem_banheiro_nao_8');
    const banheiroDentroCasaSelect = document.getElementById('banheiro_dentro_casa');
    if (temBanheiroSim8 && temBanheiroNao8 && banheiroDentroCasaSelect) {
        const toggleBanheiroDentroCasa = () => banheiroDentroCasaSelect.style.display = temBanheiroSim8.checked ? 'inline-block' : 'none';
        temBanheiroSim8.addEventListener('change', toggleBanheiroDentroCasa);
        temBanheiroNao8.addEventListener('change', toggleBanheiroDentroCasa);
        toggleBanheiroDentroCasa(); // Inicializar estado
    }
});