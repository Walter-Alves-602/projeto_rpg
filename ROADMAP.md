# Roadmap de Evolução do Projeto RPG

## 1. Refino da Experiência do Usuário
- Melhorar feedback visual (notificações, toasts, loading)
- Adicionar validação de formulários no frontend
- Implementar página de perfil do usuário (alterar senha, dados, etc)

## 2. Ficha de Personagem
- Permitir edição de atributos e habilidades diretamente pela interface
- Adicionar histórico de evolução do personagem (nível, XP, eventos)
- Implementar upload de avatar/foto do personagem
- Exibir descrições detalhadas das habilidades (tooltip/modal)

## 3. Mesa e Sessão
- Sistema de chat integrado para cada mesa
- Gerenciamento de sessões (agendar, registrar eventos, anotações compartilhadas)
- Permitir mestre enviar convites para jogadores
- Implementar sistema de rolagem de dados compartilhado (com histórico para todos da mesa)

## 4. Inventário e Magias
- Permitir adicionar/remover itens e magias com descrições
- Implementar sistema de busca/filtro para itens e magias
- Adicionar suporte a magias preparadas/conjuradas

## 5. Segurança e Autenticação
- Implementar recuperação de senha por e-mail
- Adicionar autenticação por OAuth (Google, Discord, etc)
- Permitir logout em todos dispositivos

## 6. Backend e Arquitetura
- Refatorar para separar melhor os domínios (mesa, personagem, usuário)
- Adicionar testes automatizados (unitários e de integração)
- Implementar logs e monitoramento de erros
- Adicionar API REST para integração com apps externos

## 7. Qualidade de Código e DevOps
- Documentar endpoints e modelos (Swagger/OpenAPI)
- Adicionar CI/CD para deploy automático
- Gerar documentação técnica do projeto

## 8. Recursos Avançados
- Sistema de iniciativa automática para combate
- Gerador de personagens e NPCs aleatórios
- Exportar ficha em PDF
- Dashboard para mestres (estatísticas, controle de campanhas)
