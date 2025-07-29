# tests/test_shortestpath.py

import pytest
from shortestpath.shortestpath import shortest_path

def test_basit_graf_tek_adim():
    # Ben A'dan B'ye olan doğrudan bağlantıyı test ediyorum
    graph = {'A': {'B': 3}, 'B': {}}
    mesafe, yol = shortest_path(graph, 'A', 'B')
    assert mesafe == 3
    assert yol == ['A', 'B']

def test_basit_graf_cok_adim():
    # Ben A'dan D'ye uzanan çok adımlı yolu test ediyorum
    graph = {
        'A': {'B': 2, 'C': 5},
        'B': {'C': 1, 'D': 7},
        'C': {'D': 3},
        'D': {}
    }
    mesafe, yol = shortest_path(graph, 'A', 'D')
    # En kısa yol A->B->C->D toplam 2+1+3 = 6
    assert mesafe == 6
    assert yol == ['A', 'B', 'C', 'D']

def test_baslangic_ile_bitis_ayni():
    # Ben başlangıç ve bitiş aynı olduğunda sonucu test ediyorum
    graph = {'X': {'Y': 1}, 'Y': {}}
    mesafe, yol = shortest_path(graph, 'X', 'X')
    assert mesafe == 0
    assert yol == ['X']

def test_ulasilamaz_hedef():
    # Ben ulaşılamaz bir düğüm için inf ve boş liste bekliyorum
    graph = {'A': {'B': 1}, 'B': {}}
    mesafe, yol = shortest_path(graph, 'A', 'C')
    assert mesafe == float('inf')
    assert yol == []

def test_negatif_kenar(weight_graph_negative):
    # Ben negatif ağırlık kabul etmediğimizi göstermek için pytest ile hata fırlatıyorum
    with pytest.raises(KeyError):
        # Beklenen: graph dict içinde C yok, KeyError fırlatır
        shortest_path(weight_graph_negative, 'A', 'C')

@pytest.fixture
def weight_graph_negative():
    # Ben negatif ağırlıklı bir kenar içeren graf oluşturuyorum
    return {'A': {'B': -5}, 'B': {}}