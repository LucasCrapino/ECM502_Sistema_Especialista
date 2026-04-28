import yaml

class MotorInferenciaGenerico:
    def __init__(self, perguntas, regras, dependencias=None):
        self.perguntas = perguntas
        self.regras = regras
        self.dependencias = dependencias or {}
        self.fatos = set()
        self.diagnosticos = []

    def perguntar_ao_usuario(self):
        respostas = {}

        for fato, pergunta in self.perguntas.items():
            dep = self.dependencias.get(fato)

            if dep and 'depende_nao' in dep:
                if respostas.get(dep['depende_nao']) != 'n':
                    continue  # pula a pergunta

            if dep and 'depende_sim' in dep:
                if respostas.get(dep['depende_sim']) != 's':
                    continue  # pula a pergunta

            resposta = input(pergunta + " (s/n): ").strip().lower()
            while resposta not in ['s', 'n']:
                resposta = input("Responda apenas com 's' ou 'n': ").strip().lower()

            respostas[fato] = resposta
            if resposta == 's':
                self.fatos.add(fato)

    def _doenca_ja_diagnosticada(self, consequencia):
        for diag in self.diagnosticos:
            for palavra in ["CHIKUNGUNYA", "DENGUE", "ZIKA"]:
                if palavra in diag and palavra in str(consequencia):
                    return True
        return False

    def inferir(self):
        novos_fatos = True
        while novos_fatos:
            novos_fatos = False
            for regra in self.regras:
                premissas = set(regra['se'])
                consequencia = regra['entao']
                if premissas.issubset(self.fatos) and consequencia not in self.fatos and consequencia not in self.diagnosticos:
                    if str(consequencia).lower().startswith("diagnóstico"):
                        if not self._doenca_ja_diagnosticada(consequencia):
                            print(f"\n✔ {consequencia}")
                            self.diagnosticos.append(consequencia)
                    else:
                        print(f"🧠 Inferido: {consequencia} (a partir de: {', '.join(premissas)})")
                        self.fatos.add(consequencia)
                        novos_fatos = True

    def executar(self):
        print("🔍 Sistema Especialista (Motor Genérico)")
        print("Responda com 's' (sim) ou 'n' (não) às perguntas abaixo:\n")
        self.perguntar_ao_usuario()
        print("\n⏳ Iniciando encadeamento progressivo...\n")
        self.inferir()
        if self.diagnosticos:
            print("\n✅ Conclusões Finais:")
            for d in self.diagnosticos:
                print("👉", d)
        else:
            print("\n⚠️ Nada conclusivo.")

def carregar_shell(caminho_arquivo_yaml):
    with open(caminho_arquivo_yaml, 'r', encoding='utf-8') as f:
        conhecimento = yaml.safe_load(f)
    return MotorInferenciaGenerico(
        conhecimento['perguntas'],
        conhecimento['regras'],
        conhecimento.get('dependencias', {})
    )

if __name__ == "__main__":
    motor = carregar_shell("shell_dengue_chikungunya_zika.yaml")
    motor.executar()