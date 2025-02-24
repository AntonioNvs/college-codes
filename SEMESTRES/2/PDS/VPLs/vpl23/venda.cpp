#include "venda.hpp"

#include <iomanip>
#include <iostream>

using namespace std;

Venda::~Venda() {
  // TODO: Implemente este metodo
  /**
   * Aqui voce deve deletar os ponteiros contidos na lista m_pedidos
   */

  while(!m_pedidos.empty())
    delete m_pedidos.front(), m_pedidos.pop_front();
}

void Venda::adicionaPedido(Pedido* p) {
  m_pedidos.push_back(p);
}

void Venda::imprimeRelatorio() const {
  // TODO: Implemente este metodo
  /**
   * Aqui voce tem que percorrer a lista de todos os pedidos e imprimir o resumo
   * de cada um. Por ultimo, devera ser exibido o total de venda e a quantidade
   * de pedidos processados.
   */

  float total = 0.0;
  int count = 1;
  for(auto it = m_pedidos.begin(); it != m_pedidos.end(); it++) {
    total += (*it)->calculaTotal();
    cout << "Pedido " << count << endl;
    cout << (*it)->resumo() << endl;
    count += 1;
  }

  cout << setprecision(2) << fixed;
  cout << "Relatorio de Vendas" << endl;
  cout << "Total de Vendas: R$ " << total << endl;
  cout << "Total de pedidos: " << m_pedidos.size() << endl;
}