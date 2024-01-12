# E-vent

Esta aplicação tem como objetivo funcionar como um gerenciador e buscador de eventos, no qual empresas (ou outros usuários) criam e registram seus eventos, particulares ou públicos, inserindo as informações relevantes a respeito, enquanto que os usuários podem acessar, acompanhar o andamento dos eventos, declarar interesse ou confirmar presença, ver se conhecidos também pretendem ir, além de avaliar a experiência que teve no evento, para que outros usuários possam verificar sua qualidade.

## Arquiterura do projeto
Ao se pensar na arquitetura que seria usada no projeto, foram escolhidos dois estilos arquiteturais para serem usados de base, o estilo arquitetural RESTful APIs baseado em HTTP e o estilo arquitetural em Camadas (Layering), escolhemos esses dois estilos pois pensamos que eles funcionam de forma harmonica juntos, além de serem mais facilmente implementados com as tecnologias que estão sendo usadas no projeto atualmente. Assim, construimos os seguintes diagramas que tem como objetivo permitir a fácil visualização e compreensão do funcionamento do projeto.  

[diagrama c4 nível de contexto](./C4_diagrama_contexto.png)  

[diagrama c4 nível 3 do projeto](./C4_Diagrama_de_componentes.png)

## Descrição dos componentes
Cada componente tem sua funcionalidade específica e não deve realizar funções que pertencem a outros componentes. Por isso segue abaixo uma descrição dos principais componentes presentes no nosso diagrama: 
 *  Web Page controle  
Responsável por redirecionar o usuário a página desejada para poder interagir com aplicação usando a interface visual  
* Main Page  
Responsável por apresentar o usuário à aplicação e então mostrar a ele as opções que ele tem de interação com a mesma  
* Event Search page  
Responsável por permitir com que o usuário envie solicitações de busca usando uma interface gráfica  
* Event Creation page  
Responsável por permitir com que o usuário envie solicitações de criação de eventos por meio de uma interface gráfica  
* Event Edit Page  
Responsável por permitir com que o usuário envie solicitações de edição de eventos por meio de uma interface gráfica  
* API REST  
Responsável por fazer a comunicação entre a interface gráfica vista pelo usuário com o servidor por meio de metodos HTTP  
* Search Engine  
Responsável por preparar as buscas que serão executadas no banco de dados  
* Event Controller  
Responsável por garantir que as operações realizadas são válidas e realizar as alterações necessárias para que as mesma possam ser feitas  
* Security Component  
Responsável por garantir a segurança do servidor e do banco de dados  
* Database Access Component  
Responsável pela conexão do servidor ao banco de dados  
* Database  
Responsável por armazenar as informações de Eventos e de Usuários 

### Desenvolvedores
Vinícius Farias
v195030@dac.unicamp.br

Luiz Felipe Cezar
l183146@dac.unicamp.br

otavioanovazzi
otavio2204@gmail.com

