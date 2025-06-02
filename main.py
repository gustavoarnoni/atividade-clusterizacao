import math


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
    def __init__(self):
        self.clusters = []

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

        for reg in cluster.registros:
            reg.is_centroid = False

        dimensao = len(cluster.registros[0].dados)
        soma = [0.0] * dimensao
        for reg in cluster.registros:
            for i in range(dimensao):
                soma[i] += reg.dados[i]

        media = [x / len(cluster.registros) for x in soma]

        cluster.registros.append(Registro(media, is_centroid=True))


if __name__ == "__main__":
    r1 = Registro([1.0, 2.0])
    r2 = Registro([8.0, 9.0])

    c = Clusterizacao()
    c.iniciar_com_dois(r1, r2)

    print("Estado inicial:")
    c.exibir_clusters()

    r3 = Registro([2.0, 3.0])
    c.atribuir_registro(r3)

    print("\nApós adicionar novo registro:")
    c.exibir_clusters()
