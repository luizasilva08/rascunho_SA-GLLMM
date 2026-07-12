"""
registro.py — registro central de tabelas do LuxeVoyage.

Mapeia domínio -> tabela -> metadados (módulo, entidade, plural, pk, colunas).
É a fonte única de verdade usada tanto pelo menu de terminal (main.py)
quanto pelo site (app.py / frontend/).
"""

from geografia import estado, municipio
from parceiros import parceiro, cobertura_parceiro, servico_parceiro, avaliacao_parceiro
from catalogo import pacote, temporada, modulo_pacote, preco_sazonal, destaque_sazonal
from clientes import cliente, interesse_cliente, consentimento_lgpd
from crm import usuario_interno, oportunidade_crm, historico_interacao, solicitacao_sla
from comercial import cotacao_personalizada, item_cotacao, proposta_comercial, contrato_digital
from operacional import viagem, pagamento_contrato
from auditoria import log_acesso


REGISTRO = {
    "Geografia": {
        "Estado": dict(mod=estado, entidade="estado", plural="estados",
                        pk="id_estado",
                        cols=["sigla", "nome", "regiao_nome", "timezone"]),
        "Municipio": dict(mod=municipio, entidade="municipio", plural="municipios",
                           pk="id_municipio",
                           cols=["id_estado", "nome", "categoria"]),
    },
    "Parceiros": {
        "Parceiros": dict(mod=parceiro, entidade="parceiro", plural="parceiros",
                           pk="id_parceiro",
                           cols=["razao_social", "tipo_parceiro", "status"]),
        "Cobertura_Parceiros": dict(mod=cobertura_parceiro, entidade="cobertura", plural="coberturas",
                                     pk="id_cobertura",
                                     cols=["id_parceiro", "id_municipio", "status"]),
        "Servicos_Parceiros": dict(mod=servico_parceiro, entidade="servico", plural="servicos",
                                    pk="id_servico_parceiro",
                                    cols=["id_parceiro", "categoria_servico", "nome_servico"]),
        "Avaliacoes_Parceiros": dict(mod=avaliacao_parceiro, entidade="avaliacao", plural="avaliacoes",
                                      pk="id_avaliacao",
                                      cols=["id_parceiro", "id_usuario_interno", "nota", "comentarios"]),
    },
    "Catalogo": {
        "Pacote": dict(mod=pacote, entidade="pacote", plural="pacotes",
                        pk="id_pacote",
                        cols=["nome_pacote", "id_municipio_destino", "status"]),
        "Temporada": dict(mod=temporada, entidade="temporada", plural="temporadas",
                           pk="id_temporada",
                           cols=["nome", "data_inicio", "data_fim"]),
        "Modulos_Pacote": dict(mod=modulo_pacote, entidade="modulo", plural="modulos",
                                pk="id_modulo",
                                cols=["id_pacote", "id_servico_parceiro", "obrigatorio"]),
        "Preco_Sazonal": dict(mod=preco_sazonal, entidade="preco", plural="precos",
                               pk="id_preco",
                               cols=["id_modulo", "id_temporada", "valor_sugerido"]),
        "Destaques_Sazonais": dict(mod=destaque_sazonal, entidade="destaque", plural="destaques",
                                    pk="id_destaque",
                                    cols=["id_municipio", "data_inicio", "data_fim", "classificacao"]),
    },
    "Clientes": {
        "Cliente": dict(mod=cliente, entidade="cliente", plural="clientes",
                         pk="id_cliente",
                         cols=["nome", "cpf_criptografado", "email_criptografado",
                               "telefone_criptografado", "cep", "id_municipio_origem"]),
        "Interesses_Cliente": dict(mod=interesse_cliente, entidade="interesse", plural="interesses",
                                    pk="id_interesse",
                                    cols=["id_cliente", "id_municipio_destino", "status"]),
        "Consentimentos_LGPD": dict(mod=consentimento_lgpd, entidade="consentimento", plural="consentimentos",
                                     pk="id_consentimento",
                                     cols=["id_cliente", "tipo_consentimento", "status"]),
    },
    "CRM": {
        "Usuario_Interno": dict(mod=usuario_interno, entidade="usuario", plural="usuarios",
                                 pk="id_usuario_interno",
                                 cols=["nome", "cargo", "email_corporativo", "nivel_acesso"]),
        "Oportunidade_CRM": dict(mod=oportunidade_crm, entidade="oportunidade", plural="oportunidades",
                                  pk="id_oportunidade",
                                  cols=["id_cliente", "id_usuario_interno", "estagio_funil", "valor_estimado"]),
        "Historico_Interacoes": dict(mod=historico_interacao, entidade="interacao", plural="interacoes",
                                      pk="id_interacao",
                                      cols=["id_oportunidade", "id_cliente", "id_usuario_interno",
                                            "tipo_interacao", "data_interacao"]),
        "Solicitacao_SLA": dict(mod=solicitacao_sla, entidade="solicitacao", plural="solicitacoes",
                                 pk="id_solicitacao",
                                 cols=["id_oportunidade", "id_parceiro", "data_envio", "status"]),
    },
    "Comercial": {
        "Cotacao_Personalizadas": dict(mod=cotacao_personalizada, entidade="cotacao", plural="cotacoes",
                                        pk="id_cotacao",
                                        cols=["id_oportunidade", "id_pacote", "valor_total_calculado", "status"]),
        "Item_Cotacao": dict(mod=item_cotacao, entidade="item", plural="itens",
                              pk="id_item_cotacao",
                              cols=["id_cotacao", "id_modulo", "valor_aplicado"]),
        "Propostas_Comerciais": dict(mod=proposta_comercial, entidade="proposta", plural="propostas",
                                      pk="id_proposta",
                                      cols=["id_cotacao", "versao", "status"]),
        "Contrato_Digital": dict(mod=contrato_digital, entidade="contrato", plural="contratos",
                                  pk="id_contrato",
                                  cols=["id_proposta", "timestamp_aceite", "ip_aceite",
                                        "hash_integridade", "status"]),
    },
    "Operacional": {
        "Viagem": dict(mod=viagem, entidade="viagem", plural="viagens",
                        pk="id_viagem",
                        cols=["id_contrato", "data_embarque", "data_retorno", "status_viagem"]),
        "Pagamento_Contrato": dict(mod=pagamento_contrato, entidade="pagamento", plural="pagamentos",
                                    pk="id_pagamento",
                                    cols=["id_contrato", "metodo_pagamento", "valor_total",
                                          "numero_parcela", "total_parcelas", "status_transacao"]),
    },
    "Auditoria": {
        "Log_Acesso": dict(mod=log_acesso, entidade="log", plural="logs",
                            pk="id_log",
                            cols=["id_usuario_interno", "id_cliente", "tipo_operacao", "data_acesso"]),
    },
}