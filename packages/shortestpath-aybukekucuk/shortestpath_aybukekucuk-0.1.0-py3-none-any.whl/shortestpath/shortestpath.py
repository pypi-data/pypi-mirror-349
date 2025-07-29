import heapq

def shortest_path(graph, start, end):
    """
    Bu fonksiyon, bana verilen bir graf yapısında
    başlangıç ve bitiş düğümleri arasındaki en kısa yolu bulur.

    graph: {'A': {'B': 3, 'C': 5}, ...}
    start: başlangıç düğümü
    end: bitiş düğümü

    NEGATİF ağırlık varsa KeyError fırlatır.
    Ulaşılamıyorsa (inf, []), başarıyla çalışır.
    """

    # 1) NEGATİF AĞIRLIK KONTROLÜ
    for node, komsular in graph.items():
        for agirlik in komsular.values():
            if agirlik < 0:
                # Ben negatif ağırlık kabul etmiyorum
                raise KeyError("Graf negatif ağırlık içeremez")

    # 2) Kuyruk ve ziyaret kayıtlarını hazırlıyorum
    queue = []
    heapq.heappush(queue, (0, start, [start]))
    visited = {start: 0}

    # 3) Kuyruk boşalana kadar en kısa yolu aramaya devam ediyorum
    while queue:
        cost, node, path = heapq.heappop(queue)

        # Hedefe ulaştıysam gider
        if node == end:
            return cost, path

        # Değilse komşuları gez
        for neighbor, weight in graph.get(node, {}).items():
            new_cost = cost + weight
            if neighbor not in visited or new_cost < visited[neighbor]:
                visited[neighbor] = new_cost
                heapq.heappush(queue, (new_cost, neighbor, path + [neighbor]))

    # 4) Hedefe hiç ulaşılamadıysa
    return float('inf'), []

if __name__ == "__main__":
    # Test amaçlı basit bir graf
    graph = {
        'A': {'B': 2, 'C': 4},
        'B': {'C': 1, 'D': 7},
        'C': {'D': 3},
        'D': {}
    }
    distance, path = shortest_path(graph, 'A', 'D')
    print("En kısa mesafe:", distance)
    print("İzlenen yol:", path)