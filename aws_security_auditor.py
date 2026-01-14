#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AWS Security Auditor - Ferramenta de Auditoria de Segurança AWS
Projeto DIO: Segurança na AWS - A Importância e Melhores Práticas
Autor: Hbini
Versão: 1.0

Funcionalidades:
- Validação de configurações de segurança IAM
- Verificação de conformidade com melhores práticas
- Geração de relatórios de segurança
- Análise de riscos em camadas
"""

import json
import sys
from datetime import datetime
from enum import Enum
from typing import Dict, List, Tuple


class SecurityLevel(Enum):
    """Níveis de severidade de segurança"""
    CRITICAL = "CRÍTICO"
    HIGH = "ALTO"
    MEDIUM = "MÉDIO"
    LOW = "BAIXO"
    INFO = "INFORMAÇÃO"


class SecurityCheck:
    """Classe para representar uma verificação de segurança"""
    
    def __init__(self, name: str, level: SecurityLevel, description: str, recommendation: str):
        self.name = name
        self.level = level
        self.description = description
        self.recommendation = recommendation
        self.status = False  # False = Falhou, True = Passou
        
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            'nome': self.name,
            'severidade': self.level.value,
            'descricao': self.description,
            'recomendacao': self.recommendation,
            'status': 'PASSOU' if self.status else 'FALHOU'
        }


class AWSSecurityAuditor:
    """Auditor principal de segurança AWS"""
    
    def __init__(self):
        self.checks: List[SecurityCheck] = []
        self.results: List[Dict] = []
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._initialize_checks()
    
    def _initialize_checks(self):
        """Inicializa as verificações de segurança padrão"""
        # Verificações IAM
        self.checks.append(SecurityCheck(
            name="MFA Habilitado para Contas Root",
            level=SecurityLevel.CRITICAL,
            description="A Autenticação Multi-Fator (MFA) deve estar habilitada na conta root",
            recommendation="Habilitar MFA na console da AWS para a conta root usando um dispositivo autenticador"
        ))
        
        self.checks.append(SecurityCheck(
            name="Uso de Grupos IAM",
            level=SecurityLevel.HIGH,
            description="Sempre usar grupos IAM ao invés de atribuir permissões diretamente a usuários",
            recommendation="Organize usuários IAM em grupos com políticas apropriadas de permissão"
        ))
        
        # Verificações de Rede
        self.checks.append(SecurityCheck(
            name="VPC Isolada",
            level=SecurityLevel.HIGH,
            description="Recursos críticos devem estar em uma VPC isolada e privada",
            recommendation="Utilizar VPC com subnets privadas e NAT Gateways para acesso à internet"
        ))
        
        self.checks.append(SecurityCheck(
            name="Security Groups Restritivos",
            level=SecurityLevel.HIGH,
            description="Security Groups devem seguir o princípio do menor privilégio",
            recommendation="Limitar tráfego apenas aos protocolos e portas necessários"
        ))
        
        # Verificações de Dados
        self.checks.append(SecurityCheck(
            name="Criptografia em Repouso",
            level=SecurityLevel.CRITICAL,
            description="Todos os dados em repouso devem ser criptografados",
            recommendation="Ativar criptografia KMS para S3, RDS, EBS e outros serviços de armazenamento"
        ))
        
        self.checks.append(SecurityCheck(
            name="Criptografia em Trânsito",
            level=SecurityLevel.HIGH,
            description="Dados em trânsito devem usar TLS/SSL",
            recommendation="Implementar HTTPS/TLS 1.2+ para todas as comunicações"
        ))
        
        # Verificações de Monitoramento
        self.checks.append(SecurityCheck(
            name="CloudTrail Habilitado",
            level=SecurityLevel.HIGH,
            description="CloudTrail deve registrar todas as chamadas de API",
            recommendation="Ativar CloudTrail e armazenar logs em bucket S3 criptografado"
        ))
        
        self.checks.append(SecurityCheck(
            name="CloudWatch Alertas",
            level=SecurityLevel.MEDIUM,
            description="Alertas CloudWatch devem ser configurados para eventos críticos",
            recommendation="Criar alarmes para atividades suspeitas e enviar notificações"
        ))
        
        # Verificações de Conformidade
        self.checks.append(SecurityCheck(
            name="AWS Config Habilitado",
            level=SecurityLevel.MEDIUM,
            description="AWS Config deve rastrear mudanças de configuração",
            recommendation="Ativar AWS Config para conformidade contínua"
        ))
        
        self.checks.append(SecurityCheck(
            name="Backup e Recuperação",
            level=SecurityLevel.HIGH,
            description="Estratégia de backup e recuperação de desastres",
            recommendation="Implementar backups automáticos com replicação geográfica"
        ))
    
    def run_audit(self, pass_rate: float = 0.5) -> Dict:
        """Executa a auditoria com uma taxa de sucesso simulada"""
        passed = 0
        failed = 0
        
        for i, check in enumerate(self.checks):
            # Simula resultado baseado na taxa de sucesso
            check.status = (i / len(self.checks)) < pass_rate
            if check.status:
                passed += 1
            else:
                failed += 1
            self.results.append(check.to_dict())
        
        return {
            'timestamp': self.timestamp,
            'total_checks': len(self.checks),
            'passed': passed,
            'failed': failed,
            'pass_percentage': round((passed / len(self.checks)) * 100, 2),
            'results': self.results
        }
    
    def generate_report(self, audit_result: Dict) -> str:
        """Gera relatório em formato texto"""
        report = []
        report.append("="*80)
        report.append("RELATÓRIO DE AUDITORIA DE SEGURANÇA AWS")
        report.append("="*80)
        report.append(f"\nData e Hora: {audit_result['timestamp']}")
        report.append(f"\nRESULTADOS GERAIS:")
        report.append(f"  Total de Verificações: {audit_result['total_checks']}")
        report.append(f"  Passou: {audit_result['passed']} ✓")
        report.append(f"  Falhou: {audit_result['failed']} ✗")
        report.append(f"  Taxa de Aprovação: {audit_result['pass_percentage']}%")
        report.append(f"\n" + "-"*80)
        report.append("DETALHES DAS VERIFICAÇÕES:")
        report.append("-"*80)
        
        for i, result in enumerate(audit_result['results'], 1):
            status_icon = "✓" if result['status'] == 'PASSOU' else "✗"
            report.append(f"\n{i}. [{status_icon}] {result['nome']}")
            report.append(f"   Severidade: {result['severidade']}")
            report.append(f"   Descrição: {result['descricao']}")
            report.append(f"   Recomendação: {result['recomendacao']}")
        
        report.append(f"\n" + "="*80)
        report.append("RECOMENDAÇÕES PRIORITÁRIAS:")
        report.append("="*80)
        
        # Ordena por severidade
        critical_failed = [r for r in audit_result['results'] 
                          if r['severidade'] == 'CRÍTICO' and r['status'] == 'FALHOU']
        high_failed = [r for r in audit_result['results'] 
                      if r['severidade'] == 'ALTO' and r['status'] == 'FALHOU']
        
        if critical_failed:
            report.append("\nCRÍTICO (IMPLEMENTAR IMEDIATAMENTE):")
            for result in critical_failed:
                report.append(f"  • {result['nome']}: {result['recomendacao']}")
        
        if high_failed:
            report.append("\nALTO (IMPLEMENTAR MUITO EM BREVE):")
            for result in high_failed:
                report.append(f"  • {result['nome']}: {result['recomendacao']}")
        
        report.append(f"\n" + "="*80)
        
        return "\n".join(report)
    
    def export_json(self, audit_result: Dict, filename: str = "audit_report.json"):
        """Exporta resultado para JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(audit_result, f, indent=2, ensure_ascii=False)
        return filename


def main():
    """Função principal"""
    print("\n" + "="*80)
    print("AWS SECURITY AUDITOR v1.0 - Ferramenta de Auditoria de Segurança")
    print("="*80)
    print("\nIniciando auditoria de segurança...\n")
    
    # Cria auditor
    auditor = AWSSecurityAuditor()
    
    # Executa auditoria com taxa de sucesso de 60%
    print("Executando 10 verificações de segurança...")
    result = auditor.run_audit(pass_rate=0.6)
    
    # Gera relatório
    report = auditor.generate_report(result)
    print(report)
    
    # Opcionalmente, exporta para JSON
    json_file = auditor.export_json(result, "audit_report.json")
    print(f"\n✓ Relatório JSON exportado: {json_file}")
    print("\nAuditoria concluída com sucesso!\n")
    
    # Retorna código de saída apropriado
    if result['passed'] == result['total_checks']:
        return 0  # Sucesso total
    elif result['failed'] >= 5:
        return 1  # Falhas críticas
    else:
        return 0  # Sucesso parcial aceitável


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nAuditoria cancelada pelo usuário.")
        sys.exit(2)
    except Exception as e:
        print(f"\nErro durante a auditoria: {e}")
        sys.exit(3)
