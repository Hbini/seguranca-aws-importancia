# AWS Security Auditor - Guia de Uso

## Visão Geral

O **AWS Security Auditor** é um programa ejecutável em Python que realiza auditoria automática de segurança em ambientes AWS. Ele valida 10 verificações críticas de segurança e gera relatórios detalhados.

## Requisitos

- Python 3.6 ou superior
- Sem dependências externas (usa apenas a biblioteca padrão do Python)

## Instalação

### Opção 1: Clone o repositório

```bash
git clone https://github.com/Hbini/seguranca-aws-importancia.git
cd seguranca-aws-importancia
```

### Opção 2: Baixe apenas o arquivo

```bash
wget https://raw.githubusercontent.com/Hbini/seguranca-aws-importancia/main/aws_security_auditor.py
```

## Execução

### No Linux/Mac:

```bash
python3 aws_security_auditor.py
```

Ou, se o arquivo tiver permissão de execução:

```bash
./aws_security_auditor.py
```

### No Windows:

```bash
python aws_security_auditor.py
```

## Saída do Programa

O programa gera duas saídas:

### 1. Relatório em Texto (Console)

```
================================================================================
RELATÓRIO DE AUDITORIA DE SEGURANÇA AWS
================================================================================

Data e Hora: 2024-01-14 15:30:45

RESULTADOS GERAIS:
  Total de Verificações: 10
  Passou: 6 ✓
  Falhou: 4 ✗
  Taxa de Aprovação: 60.0%

DETALHES DAS VERIFICAÇÕES:
1. [✓] MFA Habilitado para Contas Root
   Severidade: CRÍTICO
   Descrição: A Autenticação Multi-Fator (MFA) deve estar habilitada na conta root
   Recomendação: Habilitar MFA na console da AWS...
...
```

### 2. Arquivo JSON

O programa exporta automaticamente um arquivo `audit_report.json` contendo os resultados estruturados em JSON para integração com outros sistemas.

## Verificações de Segurança

O auditor realiza 10 verificações distribuidas em 5 pilares:

### Pilar 1: Identidade e Acesso (IAM)
1. **MFA Habilitado para Contas Root** [CRÍTICO]
2. **Uso de Grupos IAM** [ALTO]

### Pilar 2: Segurança de Rede
3. **VPC Isolada** [ALTO]
4. **Security Groups Restritivos** [ALTO]

### Pilar 3: Proteção de Dados
5. **Criptografia em Repouso** [CRÍTICO]
6. **Criptografia em Trânsito** [ALTO]

### Pilar 4: Monitoramento
7. **CloudTrail Habilitado** [ALTO]
8. **CloudWatch Alertas** [MÉDIO]

### Pilar 5: Conformidade
9. **AWS Config Habilitado** [MÉDIO]
10. **Backup e Recuperação** [ALTO]

## Níveis de Severidade

- **CRÍTICO**: Implementar imediatamente. Falha de segurança crítica.
- **ALTO**: Implementar muito em breve. Risco significativo.
- **MÉDIO**: Implementar em curto prazo. Vulnerabilidade moderada.
- **BAIXO**: Implementar quando possível. Risco menor.
- **INFORMAÇÃO**: Apenas informativo, sem risco.

## Códigos de Saída

O programa retorna os seguintes códigos de saída:

- **0**: Execução bem-sucedida (resultado total ou aceitável)
- **1**: Falhas críticas detectadas (5 ou mais verificações falharam)
- **2**: Cancelado pelo usuário (Ctrl+C)
- **3**: Erro durante a execução

## Personalizando o Programa

### Adicionar Novas Verificações

Para adicionar uma nova verificação de segurança, edite o método `_initialize_checks()`:

```python
self.checks.append(SecurityCheck(
    name="Nome da Verificação",
    level=SecurityLevel.HIGH,
    description="Descrição da verificação",
    recommendation="Recomendação de ação"
))
```

### Modificar Taxa de Sucesso da Simulação

Na função `main()`, altere o parâmetro `pass_rate`:

```python
# 70% de sucesso
result = auditor.run_audit(pass_rate=0.7)
```

## Exemplos de Uso

### Auditoria Básica

```bash
python3 aws_security_auditor.py
```

### Auditoria com Redirecionamento para Arquivo

```bash
python3 aws_security_auditor.py > relatorio_seguranca.txt
```

### Integração com Script de Automação

```bash
#!/bin/bash
python3 aws_security_auditor.py
if [ $? -eq 0 ]; then
    echo "Auditoria concluída com sucesso"
    # Enviar relatório por email
    mail -s "Relatório de Auditoria AWS" admin@example.com < relatorio_seguranca.txt
else
    echo "Problemas de segurança detectados!"
    exit 1
fi
```

## Arquivo de Relatório JSON

O arquivo `audit_report.json` gerado possui a seguinte estrutura:

```json
{
  "timestamp": "2024-01-14 15:30:45",
  "total_checks": 10,
  "passed": 6,
  "failed": 4,
  "pass_percentage": 60.0,
  "results": [
    {
      "nome": "MFA Habilitado para Contas Root",
      "severidade": "CRÍTICO",
      "descricao": "A Autenticação Multi-Fator...",
      "recomendacao": "Habilitar MFA na console da AWS...",
      "status": "PASSOU"
    },
    ...
  ]
}
```

## Solução de Problemas

### "Python não encontrado"

```bash
# Verificar versão instalada
python3 --version

# Se não estiver instalado
# Ubuntu/Debian
sudo apt install python3

# macOS
brew install python3

# Windows - baixar de https://www.python.org
```

### "Erro de Permissão"

```bash
# Dar permissão de execução
chmod +x aws_security_auditor.py
```

### "Arquivo JSON não foi criado"

```bash
# Verificar permissão de escrita no diretório
ls -la

# Executar com sudo se necessário
sudo python3 aws_security_auditor.py
```

## Licença

MIT - Livre para uso em projetos pessoais e comerciais

## Suporte

Para dúvidas, abra uma issue no repositório GitHub.
