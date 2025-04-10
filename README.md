# ETL, Processamento Geoespacial, _Cloud Computing_ e Automação de Relatórios
## Automatização de Relatórios com Dados GIS Vetoriais armazenados no Google BigQuery


<div align="center">
  <img src="https://drive.google.com/uc?export=view&id=1LSYRNi3MSSxwlsb9BZhnr7OEyWVMzeut" width="500">
</div>

## Sobre este Projeto 
Os conjuntos de arquivos _shafiles_ aqui utilizados foram obtidos em: <a href='https://www.ide.df.gov.br/geoportal/' target="_blank">GeoPortal-DF</a>

## Contextualização
Este projeto é constituído de duas etapas:

##### - ETL dos _Shapefiles_ para o Google BigQuery
Nesta etapa do projeto, foi realizada a leitura de uma pasta contendo diversos conjuntos de arquivos <a href='https://desktop.arcgis.com/en/arcmap/latest/manage-data/shapefiles/what-is-a-shapefile.htm' target="_blank">_shapefile_</a>. A pasta apresentava uma organização hierárquica, que foi preservada no processo de ingestão dos dados no <a href='https://cloud.google.com/bigquery/docs/introduction?hl=pt-br' target="_blank">_Google BigQuery_</a>, a fim manter a categorização temática dos _shapefiles_. A seguir, apresenta-se uma breve descrição de cada etapa do processo de ETL:

- _Extract_: Leitura dos arquivos _shapefile_.
- _Transform_: Organização dos dados, adequando-os para o carregamento.
- _Load_: Inserção dos dados no _Google BigQuery_, com a criação de uma única tabela para armazenamento dos dados.

Segue a tabela criada no _Google BigQuery_ após o processo de ETL:
<div align="center">
  <img src="https://drive.google.com/uc?export=view&id=13SNtO5hh8YAuIGXHwtXkaGe5e1ZHFKxl" width="800">
</div>



##### - Gerador de Relatório Automático 
Na segundo etapa do projeto, foi elaborado um sistema para geração de relatório automáticos. De modo geral, o sistema consiste em sobrepor os dados armazenados no Google BigQuery com os dados obtidos de um no shapefile fornecido pelo usuario.

Carregar um novo shapefile e convertê-lo em um formato adequado.

Consultar o BigQuery usando SQL espacial (por exemplo, ST_INTERSECTS).

Gerar um relatório (CSV, Excel ou visualização gráfica).

<div align="center">
  <img src="https://drive.google.com/uc?export=view&id=17oddV7w475KfTUOxVoVim8P8EgkYgVAM" width="800">
</div>

<div align="center">
  <img src="https://drive.google.com/uc?export=view&id=1pKBA5MpmplMhUyBNqPHlH7jZqGtzmfag" width="800">
</div>

<a href='https://drive.google.com/file/d/1l3lMte5s016fkJo4zcp8y2kRwXvYszbe/view?usp=sharing' target="_blank">Aqui</a>

## Tecnologias utilizadas
- Python
- VSCode
- Google BigQuery


## Quem é o Autor?
Leia meu resumo e me envie uma mensagem: https://www.linkedin.com/in/adenilson-silva/

Vamos conversar...
