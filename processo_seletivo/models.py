# processo_seletivo/models.py
# (este é o código completo que você deve ter neste arquivo)

from django.db import models

class Inscricao(models.Model):
    # 1. Dados Pessoais
    nome_completo = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    SEXO_CHOICES = [
        ('feminino', 'Feminino'),
        ('masculino', 'Masculino'),
        ('nao_informado', 'Não Informar'),
    ]
    sexo = models.CharField(max_length=20, choices=SEXO_CHOICES, default='nao_informado')
    COR_CHOICES = [
        ('pardo', 'Pardo'),
        ('branco', 'Branco'),
        ('preto', 'Preto'),
        ('amarelo', 'Amarelo'),
        ('indigena', 'Indígena'),
    ]
    cor = models.CharField(max_length=20, choices=COR_CHOICES, default='pardo')
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=15)
    apadrinhado = models.BooleanField(default=False)

    # 2. Escolaridade
    ESCOLARIDADE_CHOICES = [
        ('fundamental_completo', 'Fundamental Completo'),
        ('fundamental_incompleto', 'Fundamental Incompleto'),
        ('medio_completo', 'Médio Completo'),
        ('medio_incompleto', 'Ensino médio - Não finalizado'),
        ('superior_completo', 'Superior Completo'),
        ('superior_incompleto', 'Superior Incompleto'),
    ]
    nivel_escolaridade = models.CharField(max_length=50, choices=ESCOLARIDADE_CHOICES, blank=True, null=True)
    REDE_ENSINO_CHOICES = [
        ('publica', 'Rede pública (municipais/estadual/federal)'),
        ('privada', 'Rede privada'),
    ]
    rede_ensino = models.CharField(max_length=20, choices=REDE_ENSINO_CHOICES, blank=True, null=True)
    ano_periodo = models.CharField(max_length=50, blank=True, null=True)
    bolsista = models.BooleanField(default=False)

    # 3. Profissão
    TRABALHA_CHOICES = [
        ('sim', 'Sim'),
        ('nao', 'Não'),
        ('autonomo', 'Autônomo'),
        ('estagiario', 'Estagiário'),
        ('desempregado', 'Desempregado'),
    ]
    trabalha = models.CharField(max_length=20, choices=TRABALHA_CHOICES, blank=True, null=True)
    bairro_residencia = models.CharField(max_length=100, blank=True, null=True)
    familia_participa = models.BooleanField(default=False)
    media_salarial = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # 4. Noções Complementares
    CONHECE_ECA_CHOICES = [
        ('sim', 'Sim'),
        ('ja_ouvi', 'Já ouvi falar'),
        ('nao', 'Não conheço'),
    ]
    conhece_eca = models.CharField(max_length=20, choices=CONHECE_ECA_CHOICES, blank=True, null=True)

    CONSELHO_DIREITO_CHOICES = [
        ('sim', 'Sim'),
        ('ja_ouvi', 'Já ouvi falar'),
        ('nao', 'Não conheço'),
    ]
    conselho_direito = models.CharField(max_length=20, choices=CONSELHO_DIREITO_CHOICES, blank=True, null=True)
    conselho_qual = models.CharField(max_length=255, blank=True, null=True)

    FORUM_SOCIAL_CHOICES = [
        ('sim', 'Sim'),
        ('ja_ouvi', 'Já ouvi falar'),
        ('nao', 'Não conheço'),
    ]
    forum_social = models.CharField(max_length=20, choices=FORUM_SOCIAL_CHOICES, blank=True, null=True)

    NOCAO_DIREITOS_CHOICES = [
        ('sim_possuo', 'Sim, possuo.'),
        ('nao_sei', 'Não, não sei o que são.'),
    ]
    nocao_direitos = models.CharField(max_length=20, choices=NOCAO_DIREITOS_CHOICES, blank=True, null=True)

    REFERENCIA_FAMILIAR_CHOICES = [
        ('positiva', 'Positiva.'),
        ('negativa', 'Negativa.'),
    ]
    referencia_familiar = models.CharField(max_length=20, choices=REFERENCIA_FAMILIAR_CHOICES, blank=True, null=True)


    # 5. Saúde
    plano_saude = models.BooleanField(default=False)
    qual_plano_saude = models.CharField(max_length=100, blank=True, null=True)
    acompanhamento_medico = models.BooleanField(default=False)
    qual_problema_saude = models.CharField(max_length=255, blank=True, null=True)
    cirurgia = models.BooleanField(default=False)
    qual_cirurgia = models.CharField(max_length=255, blank=True, null=True)
    deficiencia_fisica = models.BooleanField(default=False)
    qual_deficiencia_fisica = models.CharField(max_length=255, blank=True, null=True)
    deficiencia_mental = models.BooleanField(default=False)
    DOENCA_TRANSTORNO_CHOICES = [
        ('autismo', 'Autismo'),
        ('tdah', 'TDAH'),
        ('depressao', 'Depressão'),
        ('transtorno_bipolar', 'Transtorno Bipolar'),
        ('outro', 'Outro'),
    ]
    doenca_transtorno = models.CharField(max_length=50, choices=DOENCA_TRANSTORNO_CHOICES, blank=True, null=True)


    # 6. Hábitos Alimentares
    REFEICOES_DIA_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5_mais', '5 ou mais'),
    ]
    refeicoes_dia = models.CharField(max_length=10, choices=REFEICOES_DIA_CHOICES, blank=True, null=True)
    costuma_comer = models.CharField(max_length=255, blank=True, null=True)


    # 7. Grupos Comunitários
    participa_grupos = models.BooleanField(default=False)
    qual_grupo_comunitario = models.CharField(max_length=255, blank=True, null=True)


    # 8. Moradia e Saneamento
    TIPO_MORADIA_CHOICES = [
        ('propria', 'Própria'),
        ('alugada', 'Alugada'),
        ('cedida', 'Cedida'),
        ('outro', 'Outro'),
    ]
    tipo_moradia = models.CharField(max_length=20, choices=TIPO_MORADIA_CHOICES, blank=True, null=True)

    MATERIAL_CONSTRUCAO_CHOICES = [
        ('alvenaria', 'Alvenaria - Tijolos'),
        ('madeira', 'Madeira'),
        ('taipa', 'Taipa'),
        ('outro', 'Outro'),
    ]
    material_construcao = models.CharField(max_length=20, choices=MATERIAL_CONSTRUCAO_CHOICES, blank=True, null=True)

    vulnerabilidade_territorial = models.CharField(max_length=255, blank=True, null=True)

    NUM_COMODOS_CHOICES = [
        ('1_5', '1-5'),
        ('4_6', '4-6'),
        ('outro', 'Outro'),
    ]
    num_comodos = models.CharField(max_length=10, choices=NUM_COMODOS_CHOICES, blank=True, null=True)
    outros_comodos = models.IntegerField(blank=True, null=True)

    tem_banheiro = models.BooleanField(default=False)
    BANHEIRO_DENTRO_CASA_CHOICES = [
        ('sim', 'Sim'),
        ('nao', 'Não'),
    ]
    banheiro_dentro_casa = models.CharField(max_length=10, choices=BANHEIRO_DENTRO_CASA_CHOICES, blank=True, null=True)

    energia_eletrica = models.BooleanField(default=False)


    # 9. Bens
    bens_possuidos = models.CharField(max_length=255, blank=True, null=True)
    aquisicao_bens = models.CharField(max_length=255, blank=True, null=True)
    condicao_bens = models.CharField(max_length=255, blank=True, null=True)


    # 10. Assistência
    cadastro_unico = models.BooleanField(default=False)
    bolsa_familia = models.BooleanField(default=False)
    beneficio_bpc = models.BooleanField(default=False)


    # 11. Renda
    RENDA_FAMILIAR_TOTAL_CHOICES = [
        ('ate_meio_sm', 'Até 1/2 Salário mínimo'),
        ('1_2sm', '1 a 2 Salários mínimos'),
        ('3_4sm', '3 a 4 Salários mínimos'),
        ('acima_4sm', 'Acima de 4 Salários mínimos'),
    ]
    renda_familiar_total = models.CharField(max_length=20, choices=RENDA_FAMILIAR_TOTAL_CHOICES, blank=True, null=True)
    renda_per_capita = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    def __str__(self):
        return self.nome_completo + " - " + str(self.data_nascimento)