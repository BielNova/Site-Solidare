from django.db import models
from django.utils import timezone

# Choices para o status da inscrição
STATUS_INSCRICAO_CHOICES = (
    ('PENDENTE', 'Pendente'),
    ('APROVADO', 'Aprovado'),
    ('REPROVADO', 'Reprovado'),
    ('CANCELADO', 'Cancelado'),
)

class Curso(models.Model):
    """
    Representa um curso oferecido pelo Instituto.
    """
    nome = models.CharField(max_length=200, unique=True, verbose_name="Nome do Curso")
    descricao = models.TextField(verbose_name="Descrição Detalhada do Curso")
    idade_minima = models.IntegerField(blank=True, null=True, verbose_name="Idade Mínima Recomendada")
    idade_maxima = models.IntegerField(blank=True, null=True, verbose_name="Idade Máxima Recomendada")
    vagas_total = models.IntegerField(default=0, verbose_name="Número de Vagas")
    ativo = models.BooleanField(default=True, verbose_name="Curso Ativo?")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['nome']

    def __str__(self):
        return self.nome

class ProcessoSeletivo(models.Model):
    """
    Define um período específico para inscrições em cursos.
    Ex: "Processo Seletivo Verão 2025"
    """
    nome = models.CharField(max_length=200, unique=True, verbose_name="Nome do Processo Seletivo")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição do Processo Seletivo")
    data_inicio_inscricoes = models.DateField(verbose_name="Início das Inscrições")
    data_fim_inscricoes = models.DateField(verbose_name="Fim das Inscrições")
    data_resultado = models.DateField(blank=True, null=True, verbose_name="Data do Resultado (Opcional)")
    cursos_oferecidos = models.ManyToManyField(Curso, related_name='processos_seletivos', verbose_name="Cursos Disponíveis Neste Processo")
    ativo = models.BooleanField(default=True, verbose_name="Processo Ativo?")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    class Meta:
        verbose_name = "Processo Seletivo"
        verbose_name_plural = "Processos Seletivos"
        ordering = ['-data_inicio_inscricoes']

    def __str__(self):
        return self.nome

    def esta_aberto_para_inscricoes(self):
        """Verifica se o processo seletivo está aberto para inscrições."""
        today = timezone.localdate()
        return self.ativo and (self.data_inicio_inscricoes <= today <= self.data_fim_inscricoes)

class Inscricao(models.Model):
    """
    Representa a inscrição de uma criança em um curso através de um processo seletivo.
    """
    processo_seletivo = models.ForeignKey(ProcessoSeletivo, on_delete=models.CASCADE, related_name='inscricoes', verbose_name="Processo Seletivo")
    curso_escolhido = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='inscricoes', verbose_name="Curso Escolhido")

    # Dados da Criança
    nome_completo_crianca = models.CharField(max_length=255, verbose_name="Nome Completo da Criança")
    data_nascimento_crianca = models.DateField(verbose_name="Data de Nascimento da Criança")
    cpf_crianca = models.CharField(max_length=14, blank=True, null=True, verbose_name="CPF da Criança (Opcional)") # Ex: '000.000.000-00'

    # Dados do Responsável (assumindo que o responsável fará a inscrição)
    nome_responsavel = models.CharField(max_length=255, verbose_name="Nome Completo do Responsável")
    cpf_responsavel = models.CharField(max_length=14, unique=True, verbose_name="CPF do Responsável")
    email_responsavel = models.EmailField(verbose_name="E-mail do Responsável")
    telefone_responsavel = models.CharField(max_length=20, verbose_name="Telefone do Responsável")

    # Informações da Inscrição
    data_inscricao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Inscrição")
    status = models.CharField(
        max_length=10,
        choices=STATUS_INSCRICAO_CHOICES,
        default='PENDENTE',
        verbose_name="Status da Inscrição"
    )
    observacoes_admin = models.TextField(blank=True, null=True, verbose_name="Observações do Administrador")

    class Meta:
        verbose_name = "Inscrição"
        verbose_name_plural = "Inscrições"
        # Garante que um CPF de responsável só possa se inscrever uma vez por processo seletivo e curso
        unique_together = ('processo_seletivo', 'curso_escolhido', 'cpf_responsavel')
        ordering = ['-data_inscricao']

    def __str__(self):
        return f"Inscrição de {self.nome_completo_crianca} no curso {self.curso_escolhido.nome} ({self.processo_seletivo.nome})"

    def idade_da_crianca(self):
        """Calcula a idade da criança na data atual."""
        today = timezone.localdate()
        born = self.data_nascimento_crianca
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))