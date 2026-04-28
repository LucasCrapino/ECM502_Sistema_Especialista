# ECM502 — Sistema Especialista: Diagnóstico de Dengue, Chikungunya e Zika

> Trabalho desenvolvido para a disciplina de **Inteligência Artificial (ECM502)** do curso de Engenharia de Computação.

---

## 📌 Descrição do Projeto

Este projeto implementa um **Mini Sistema Especialista** capaz de auxiliar no diagnóstico diferencial entre três doenças transmitidas pelo mosquito *Aedes aegypti*: **Dengue**, **Chikungunya** e **Zika**. O sistema coleta sintomas relatados pelo usuário e, por meio de encadeamento progressivo, infere conclusões diagnósticas baseadas em regras clínicas extraídas de literatura especializada da **Fiocruz**.

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

---

## ⚙️ Como Funciona

### 1. Coleta de Fatos
O sistema faz perguntas objetivas (sim/não) ao usuário sobre os sintomas do paciente. Cada resposta positiva é adicionada à base de dados como um fato verdadeiro, que poderá ser usado pelo motor de inferência.

### 2. Encadeamento Progressivo
Com os fatos coletados, o motor executa o ciclo de inferência:

```
Fatos iniciais (sintomas)
        ↓
  Padrões primários         ex: febre_alta → padrao_febre_dengue_ou_chik
        ↓
  Sinais compostos          ex: padrao_febre + artralgia_grave → sinal_chikungunya_forte
        ↓
  Diagnóstico final         ex: sinal_chikungunya_forte + conjuntivite → CHIKUNGUNYA confirmado
```

O processo repete até que nenhuma nova regra possa ser disparada.

### 3. Diagnósticos Possíveis
O sistema é capaz de emitir **9 diagnósticos** em três níveis de certeza:

| Doença | Confirmado | Provável | Suspeita |
|---|:---:|:---:|:---:|
| Chikungunya | ✅ | ✅ | ✅ |
| Dengue | ✅ | ✅ | ✅ |
| Zika | ✅ | ✅ | ✅ |

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

> Por padrão, o motor carrega `shell_dengue_chikungunya_zika.yaml`. Para usar outro arquivo de regras, edite a última linha do `motor_generico.py`.

### Exemplo de sessão
```
🔍 Sistema Especialista (Motor Genérico)
Responda com 's' (sim) ou 'n' (não) às perguntas abaixo:

O paciente apresenta febre alta (acima de 39°C) de início súbito? (s/n): s
O paciente apresenta febre baixa (abaixo de 38°C) ou ausência de febre? (s/n): n
O paciente apresenta dores INTENSAS nas articulações? (s/n): s
...

⏳ Iniciando encadeamento progressivo...

🧠 Inferido: padrao_febre_dengue_ou_chik
🧠 Inferido: artralgia_grave
🧠 Inferido: sinal_chikungunya_forte
✔ Diagnóstico: CHIKUNGUNYA (suspeita) — ...

✅ Conclusões Finais:
👉 Diagnóstico: CHIKUNGUNYA — Febre alta, artralgia intensa com edema...
```

---

## 🔧 Extensibilidade

A separação entre motor e base de conhecimento permite que qualquer novo domínio seja incorporado criando apenas um novo arquivo `.yaml` com duas seções:

```yaml
perguntas:  # fatos a coletar do usuário
regras:     # regras SE/ENTÃO para inferência
```

---

## 📚 Referências

- FIOCRUZ. *Zika, chikungunya e dengue: entenda as diferenças*. Disponível em: https://agencia.fiocruz.br/zika-chikungunya-e-dengue-entenda-diferencas

---

## 👥 Integrantes

| Nome | RA |
|---|---|
| Felipe Kenzo Ohara Sakae | 22.00815-2 |
| Lucas Gozze Crapino | 22.00667-2 |
| Murillo Penha Strina | 22.00730-0 |