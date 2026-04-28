import yaml

class MotorInferenciaGenerico:
    def __init__(self, perguntas, regras):
        self.perguntas = perguntas
        self.regras = regras
        self.fatos = set()
        self.diagnosticos = []

    def perguntar_ao_usuario(self):
        for fato, pergunta in self.perguntas.items():
            resposta = input(pergunta + " (s/n): ").strip().lower()
            while resposta not in ['s', 'n']:
                resposta = input("Responda apenas com 's' ou 'n': ").strip().lower()
            if resposta == 's':
                self.fatos.add(fato)

    def inferir(self):
        novos_fatos = True
        while novos_fatos:
            novos_fatos = False
            for regra in self.regras:
                premissas = set(regra['se'])
                consequencia = regra['entao']
                if premissas.issubset(self.fatos) and consequencia not in self.fatos and consequencia not in self.diagnosticos:
                    if (str(consequencia).lower().startswith("diagnóstico") or
                        str(consequencia).lower().startswith("recomendação")):
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
    return MotorInferenciaGenerico(conhecimento['perguntas'], conhecimento['regras'])

if __name__ == "__main__":
    motor = carregar_shell("shell_dengue_chikungunya_zika.yaml")
    motor.executar()
