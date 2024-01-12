# Requisitos

## Locais

* Locais podem ser cadastrados independentemente (eles antecedem os eventos e permanecem com o fim do evento, podendo sediar vários deles)
* Podem ou não ter endereço (caso seja online, não há endereço, e o local será chamado "Online")
* Caso hajam vários endereços com o mesmo tipo de local (uma franquia, supermercado...), haverá um elemento (com chave primária) diferente para cada "instância" com endereço diferente

## Endereços

* Podem ser cadastrados independentemente, pois antecedem os locais, inclusive podem trocar o estabelecimento (representado pelo "local")
* Ao mudar de "local", o local_id deve ser atualizado
* Para criar um endereço, a existência dele deve ser antes verificada (implementar?)

## Eventos

* Para criar um evento, deve ser especificado um local
* Relação entre eventos e locais administrada em Sediar
* Detalhes são opcionais

## Det_eventos

* Para criar uma instância, deve haver um evento com que se relacione
* Deve haver um ev_status (situação do evento, como "marcado", "encerrado" ou "cancelado")
* O campo "avaliação" seria atualizado constantemente e automaticamente conforme inputs de usuários (média)

## Sediar

* Cada linha deve referenciar um evento e um local, e deve possuir um pacote, mesmo que a entrada seja grátis

## Pacotes

* Devem ter data e preço
* Se não possuir um nome, será chamado de "Padrão"