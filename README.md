# ECM502 — Sistema Especialista: Diagnóstico de Dengue, Chikungunya e Zika

> Trabalho desenvolvido para a disciplina de **Inteligência Artificial (ECM502)** do curso de Engenharia de Computação.

---

## 📌 Descrição do Projeto

Este projeto implementa um **Mini Sistema Especialista** capaz de auxiliar no diagnóstico diferencial entre três doenças transmitidas pelo mosquito *Aedes aegypti*: **Dengue**, **Chikungunya** e **Zika**. O sistema coleta sintomas relatados pelo usuário e, por meio de encadeamento progressivo (*forward chaining*), infere conclusões diagnósticas baseadas em regras clínicas extraídas de literatura especializada da **Fiocruz**.

---

## 🧠 Fundamentação Teórica

Um **Sistema Especialista** é um sistema baseado em regras que incorpora o conhecimento de especialistas humanos para tirar conclusões ou fazer diagnósticos a partir de dados fornecidos. Sua arquitetura é composta por três elementos principais:

- **Base de Conhecimento** — conjunto de regras no formato `SE <condição> ENTÃO <conclusão>`, representando o conhecimento do domínio
- **Base de Dados (Memória de Trabalho)** — conjunto de fatos conhecidos sobre o caso atual, inicialmente populado pelas respostas do usuário
- **Motor de Inferência** — mecanismo que aplica as regras aos fatos para derivar novas conclusões

O tipo de raciocínio empregado é o **encadeamento progressivo** (*forward chaining*): partindo dos fatos observados (sintomas relatados), o motor dispara regras sucessivamente, adicionando novos fatos intermediários até alcançar um diagnóstico ou esgotar as regras aplicáveis. Essa abordagem é classificada como *dirigida por dados* e é especialmente adequada para sistemas de análise e diagnóstico clínico.

---

## 🏗️ Arquitetura

O projeto segue a separação clássica entre conhecimento e processamento, o que permite que o mesmo motor genérico seja aplicado a diferentes domínios apenas trocando o arquivo de regras.

```
ECM502_Sistema_Especialista/
│
├── motor_generico.py                  # Motor de inferência (shell genérico)
├── shell_dengue_chikungunya_zika.yaml # Base de conhecimento do projeto
```

### Componentes

| Arquivo | Papel no Sistema Especialista |
|---|---|
| `motor_generico.py` | Motor de Inferência + Interface com o Usuário |
| `shell_*.yaml` (seção `perguntas`) | Base de Dados — coleta de fatos via input |
| `shell_*.yaml` (seção `regras`) | Base de Conhecimento — regras SE/ENTÃO |
| `shell_*.yaml` (seção `dependencias`) | Lógica condicional entre perguntas |

---

## ⚙️ Como Funciona

### 1. Coleta de Fatos com Perguntas Condicionais
O sistema faz perguntas objetivas (sim/não) sobre os sintomas do paciente. Perguntas logicamente dependentes de respostas anteriores são automaticamente puladas, evitando questionamentos redundantes ou sem sentido. As dependências são declaradas no próprio arquivo `.yaml`, sem necessidade de alterar o motor:

| Pergunta | Condição para ser feita |
|---|---|
| Febre baixa | Somente se **não** há febre alta |
| Dor articular leve | Somente se **não** há dor intensa |
| Edema/rigidez | Somente se **há** dor intensa |
| Timing e coceira das manchas | Somente se **há** manchas na pele |
| Coceira leve | Somente se **não** há coceira intensa |
| Sintomas brandos | Somente se **não** há febre alta |

### 2. Encadeamento Progressivo
Com os fatos coletados, o motor executa o ciclo de inferência em três camadas:

```
Fatos iniciais (sintomas)
        ↓
  Padrões primários       ex: febre_alta → padrao_febre_alta
        ↓
  Sinais compostos        ex: padrao_febre_alta + artralgia_grave → chik_base
                          ex: chik_base + rash_apos_48h           → chik_com_rash
                          ex: chik_com_rash + conjuntivite         → chik_confirmado
        ↓
  Diagnóstico final       ex: chik_confirmado → "CHIKUNGUNYA (confirmado)"
```

O processo repete até que nenhuma nova regra possa ser disparada.

### 3. Um Diagnóstico por Doença
O motor garante **no máximo um diagnóstico por doença**: o mais específico (listado primeiro no YAML) é registrado e bloqueia automaticamente os de menor certeza para a mesma condição, evitando resultados redundantes.

### 4. Diagnósticos Possíveis
O sistema é capaz de emitir **6 diagnósticos** em dois níveis de certeza:

| Doença | Confirmado | Suspeita |
|---|:---:|:---:|
| Chikungunya | ✅ | ✅ |
| Dengue | ✅ | ✅ |
| Zika | ✅ | ✅ |

---

## 🔬 Base de Conhecimento: Diferenciadores Clínicos

As regras foram construídas com base nas orientações clínicas da **Fiocruz**, capturando os principais marcadores que distinguem as três doenças:

| Sintoma | Dengue | Chikungunya | Zika |
|---|---|---|---|
| **Febre** | Alta, início súbito | Alta, início súbito | Baixa ou ausente |
| **Dor articular** | Leve a moderada | **Intensa**, com edema | Leve |
| **Rash cutâneo** | Pode estar presente | Após 48h dos sintomas | **Primeiras 24h**, com coceira intensa |
| **Prurido (coceira)** | Leve | Leve | **Intenso** |
| **Olhos** | Dor nos olhos | Olhos vermelhos | Olhos vermelhos |

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.x instalado
- Biblioteca `pyyaml`

### Instalação da dependência
```bash
python -m pip install pyyaml
```

### Execução
```bash
python motor_generico.py
```

### Exemplo de sessão
```
🔍 Sistema Especialista (Motor Genérico)
Responda com 's' (sim) ou 'n' (não) às perguntas abaixo:

O paciente apresenta febre alta (acima de 39°C) de início súbito? (s/n): s
O paciente apresenta dores INTENSAS nas articulações? (s/n): s
Há inchaço (edema) ou rigidez nas articulações? (s/n): s
O paciente apresenta manchas vermelhas na pele? (s/n): s
As manchas na pele surgiram nas primeiras 24 horas dos sintomas? (s/n): n
As manchas na pele surgiram após 48 horas do início dos sintomas? (s/n): s
O paciente sente coceira intensa nas manchas? (s/n): s
O paciente apresenta olhos vermelhos? (s/n): s
...

⏳ Iniciando encadeamento progressivo...

🧠 Inferido: padrao_febre_alta (a partir de: febre_alta)
🧠 Inferido: artralgia_grave (a partir de: dor_articulacao_intensa, edema_articulacoes)
🧠 Inferido: chik_base (a partir de: padrao_febre_alta, artralgia_grave)
🧠 Inferido: chik_com_rash (a partir de: chik_base, rash_apos_48h)
🧠 Inferido: chik_confirmado (a partir de: chik_com_rash, conjuntivite_presente)

✔ Diagnóstico: CHIKUNGUNYA (confirmado) — Febre alta, artralgia intensa com edema...

✅ Conclusões Finais:
👉 Diagnóstico: CHIKUNGUNYA (confirmado) — Febre alta, artralgia intensa com edema...
```

---

## 🔧 Extensibilidade

A separação entre motor e base de conhecimento permite que qualquer novo domínio seja incorporado criando apenas um novo arquivo `.yaml`. O campo `dependencias` é opcional — os arquivos de exemplo fornecidos com o protótipo original (`shell_medicina.yaml`, `shell_seguranca.yaml`, `shell_culinaria.yaml`) continuam funcionando normalmente sem ele.

```yaml
perguntas:    # fatos a coletar do usuário
dependencias: # (opcional) lógica condicional entre perguntas
regras:       # regras SE/ENTÃO para inferência
```

---

## 📚 Referência

- FIOCRUZ. *Zika, chikungunya e dengue: entenda as diferenças*. Disponível em: https://agencia.fiocruz.br/zika-chikungunya-e-dengue-entenda-diferencas

---

## 👥 Integrantes

| Nome | RA |
|---|---|
| Felipe Kenzo Ohara Sakae | 22.00815-2 |
| Lucas Gozze Crapino | 22.00667-2 |
| Murillo Penha Strina | 22.00730-0 |