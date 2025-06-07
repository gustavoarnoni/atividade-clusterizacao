import math
from collections import defaultdict


def distancia_euclidiana(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))


class Registro:
    def __init__(self, dados, is_centroid=False):
        self.dados = dados
        self.is_centroid = is_centroid

    def __repr__(self):
        return f"Registro({self.dados}, centroid={self.is_centroid})"


class Cluster:
    def __init__(self, registro_inicial):
        self.registros = [registro_inicial]
        registro_inicial.is_centroid = True

    def adicionar_registro(self, registro):
        self.registros.append(registro)

    def remover_registro(self, registro):
        self.registros.remove(registro)

    def alterar_registro(self, indice, novo_dado):
        self.registros[indice].dados = novo_dado

    def get_centroide(self):
        for r in self.registros:
            if r.is_centroid:
                return r.dados
        return None

    def __repr__(self):
        return f"Cluster({self.registros})"


class Clusterizacao:
    def __init__(self, limiar=5.0):
        self.clusters = []
        self.limiar = limiar

    def iniciar_com_dois(self, registro1, registro2):
        self.clusters.append(Cluster(registro1))
        self.clusters.append(Cluster(registro2))

    def exibir_clusters(self):
        for i, cluster in enumerate(self.clusters):
            print(f"Cluster {i}: {cluster}")

    def atribuir_registro(self, novo_registro):
        distancias = []

        for cluster in self.clusters:
            centroide = cluster.get_centroide()
            if centroide is None:
                continue
            dist = distancia_euclidiana(novo_registro.dados, centroide)
            distancias.append((dist, cluster))

        _, cluster_mais_proximo = min(distancias, key=lambda x: x[0])
        cluster_mais_proximo.adicionar_registro(novo_registro)

        self.recalcular_centroide(cluster_mais_proximo)

    def recalcular_centroide(self, cluster):
        if len(cluster.registros) == 0:
            return

        cluster.registros = [r for r in cluster.registros if not r.is_centroid]

        dimensao = len(cluster.registros[0].dados)
        soma = [0.0] * dimensao
        for reg in cluster.registros:
            for i in range(dimensao):
                soma[i] += reg.dados[i]

        media = [x / len(cluster.registros) for x in soma]
        cluster.registros.append(Registro(media, is_centroid=True))

    def analisar_dispersao_e_reorganizar(self):
        novos_clusters = []
        for cluster in self.clusters:
            centroide = cluster.get_centroide()
            registros_distantes = []

            for reg in cluster.registros:
                if not reg.is_centroid:
                    dist = distancia_euclidiana(reg.dados, centroide)
                    if dist > self.limiar:
                        registros_distantes.append(reg)

            for reg in registros_distantes:
                cluster.remover_registro(reg)
                novo_cluster = Cluster(reg)
                novos_clusters.append(novo_cluster)

            self.recalcular_centroide(cluster)

        self.clusters.extend(novos_clusters)

    def converter_categorico_para_numerico(self, registros):
        """Etapa 5 — converte strings para inteiros, sem alterar os dados originais."""
        transformado = []
        mapeamento = defaultdict(dict)

        for reg in registros:
            convertido = []
            for i, val in enumerate(reg.dados):
                if isinstance(val, str):
                    if val not in mapeamento[i]:
                        mapeamento[i][val] = len(mapeamento[i])
                    convertido.append(mapeamento[i][val])
                else:
                    convertido.append(val)
            transformado.append(convertido)

        return transformado


# Execução
r1 = Registro([1.0, 2.0])
r2 = Registro([8.0, 9.0])

c = Clusterizacao(limiar=4.0)
c.iniciar_com_dois(r1, r2)

print("Estado inicial:")
c.exibir_clusters()

c.atribuir_registro(Registro([2.0, 3.0]))
c.atribuir_registro(Registro([15.0, 15.0]))

print("\nApós atribuições:")
c.exibir_clusters()

c.analisar_dispersao_e_reorganizar()

print("\nApós análise de dispersão e reorganização:")
c.exibir_clusters()

print("\nConversão de dados categóricos:")
categoricos = [Registro(['azul', 'grande']), Registro(['vermelho', 'pequeno']), Registro(['azul', 'pequeno'])]
convertidos = c.converter_categorico_para_numerico(categoricos)
for original, convertido in zip(categoricos, convertidos):
    print(f"{original.dados} -> {convertido}")

