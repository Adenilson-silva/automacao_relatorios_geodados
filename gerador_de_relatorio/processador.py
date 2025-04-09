import json
import os
import geopandas as gpd
import pandas as pd
import folium
from google.cloud import bigquery
from google.oauth2 import service_account
from google.api_core.exceptions import GoogleAPIError


def conectar_ao_bigquery(caminho_chave, project_id): 
    """
    Estabelece uma conexão com o Google BigQuery usando uma conta de serviço.

    Parâmetros:
    ----------
    caminho_chave : str
        Caminho para o arquivo JSON com as credenciais da conta de serviço.
    project_id : str
        ID do projeto do Google Cloud ao qual se deseja conectar.

    Retorna:
    -------
    google.cloud.bigquery.client.Client ou None
        Um objeto cliente do BigQuery se a conexão for bem-sucedida, 
        ou None se ocorrer algum erro.
    """
    try:
        credenciais = service_account.Credentials.from_service_account_file(caminho_chave)
        cliente = bigquery.Client(credentials=credenciais, project=project_id)
        print("Conectado com sucesso!")
        return cliente
    except Exception as e:
        print(f"Erro ao se conectar: {e}")
        return None


def consultar_shapefiles_big_query(projeto_id: str, dataset: str, tabela: str, caminho_chave: str) -> pd.DataFrame:
    """
    Consulta a tabela de shapefiles no BigQuery e retorna os dados em um DataFrame.

    Args:
        projeto_id (str): ID do projeto no Google Cloud.
        dataset (str): Nome do dataset no BigQuery.
        tabela (str): Nome da tabela com os shapefiles.
        caminho_chave (str): Caminho para a chave do serviço.

    Returns:
        pd.DataFrame: Dados retornados pela consulta, ou DataFrame vazio em caso de erro.
    """
    try:
        cliente = conectar_ao_bigquery(caminho_chave, projeto_id)
        query = f"""
            SELECT 
                nivel_1, 
                nivel_2, 
                nivel_3,
                nivel_4,
                nivel_5,
                nivel_6,
                nivel_7,
                nivel_8,
                shapefile_nome, 
                geometria_e_atributos
            FROM `{projeto_id}.{dataset}.{tabela}`
        """
        dados = cliente.query(query).to_dataframe()
        return dados
    except GoogleAPIError as erro:
        print(f"Erro ao consultar BigQuery: {erro}")
        return pd.DataFrame() 
    except Exception as erro:
        print(f"Erro inesperado: {erro}")
        return pd.DataFrame()


def gerar_mapa(caminho_shp, caminho_relatorio):
        try:
            gdf = gpd.read_file(caminho_shp)
            # Para calcular o centroide corretamente, reprojeta temporariamente para UTM (por exemplo, zona 23S - EPSG:31983)
            gdf_proj = gdf.to_crs(epsg=31983) 
            # Calcula o centroide projetado e converte de volta para WGS84
            centroid_utm = gdf_proj.geometry.centroid
            centroid_gdf = gpd.GeoSeries(centroid_utm, crs='EPSG:31983').to_crs(epsg=4326)
            # Cria o mapa centralizado no centroide corrigido
            mapa = folium.Map(location=[centroid_gdf.y.mean(), centroid_gdf.x.mean()], zoom_start=11)
            folium.GeoJson(gdf).add_to(mapa)
            caminho_mapa = os.path.join(caminho_relatorio, "mapa_temp.html")
            mapa.save(caminho_mapa)
            return caminho_mapa
        except Exception as e:
           print(f"<p style='color:red;'>Erro ao gerar o mapa: {e}</p>")


def gerar_relatorio(caminho_shp, pasta_saida, caminho_chave, projeto_id, dataset_id, tabela_id):
    gdf1 = gpd.read_file(caminho_shp)
    caminho_relatorio = os.path.join(pasta_saida, 'relatorio')
    os.makedirs(caminho_relatorio, exist_ok=True)
    caminho_html = os.path.join(caminho_relatorio,'Relatorio.html')
    with open(caminho_html, 'w', encoding='utf-8') as f:
        f.write(f"<html><head><title>Relatório de Localização</title>")
        f.write("""
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; }
                th { background-color: #f2f2f2; text-align: left; }
                tr:nth-child(even) { background-color: #f9f9f9; }

                .tab-button {
                    padding: 10px 20px;
                    margin-right: 5px;
                    border: none;
                    background-color: #eee;
                    cursor: pointer;
                    font-weight: bold;
                }

                .tab-button.active {
                    background-color: #ccc;
                }

                .tab-content {
                    display: none;
                    margin-top: 20px;
                }

                .tab-content.active {
                    display: block;
                }
            </style>
            <script>
                function showTab(tabId) {
                    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
                    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
                    document.getElementById(tabId).classList.add('active');
                    document.getElementById(tabId + '-btn').classList.add('active');
                }
            </script>
            <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.4/css/jquery.dataTables.css">
            <script type="text/javascript" charset="utf8" src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
            <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.js"></script>
        """)
        f.write("</head><body>")
        f.write(f"<h2>Relatório de Localização</h2>")
        # Botões de abas
        f.write("""
            <div>
                <button class="tab-button active" id="completo-btn" onclick="showTab('completo')">Relatório Completo</button>
                <button class="tab-button" id="com_sobreposicao-btn" onclick="showTab('com_sobreposicao')">Relatório Simplificado</button>
                <button class="tab-button" id="mapa-btn" onclick="showTab('com_mapa')">Mapa</button>
            </div>
        """)
        # Conteúdo das abas
        f.write('<div id="completo" class="tab-content active">')
        bloco_sobreposicao = '<div id="com_sobreposicao" class="tab-content">'
        bloco_mapa = '<div id="com_mapa" class="tab-content">'
        dados_gis = consultar_shapefiles_big_query(projeto_id, dataset_id, tabela_id, caminho_chave)
        for i, row in enumerate(dados_gis.itertuples()):
            niveis = [str(valor) for n in range(1, 9) if not pd.isna(valor := getattr(row, f"nivel_{n}", None))]
            try:
                dados = json.loads(row.geometria_e_atributos)
                gdf_big_query = gpd.GeoDataFrame.from_features(dados["features"])

                if gdf1.crs != 4326:
                    gdf1 = gdf1.to_crs(epsg=4326)
                if gdf_big_query.crs is None or gdf_big_query.crs != 4326:
                    gdf_big_query = gdf_big_query.set_crs("EPSG:4326")

                sobreposicoes = gdf1.geometry.apply(lambda geom: gdf_big_query.intersects(geom).any())
                #intersecoes = gpd.overlay(gdf1, gdf_big_query, how='intersection', keep_geom_type=False)
                intersecoes = gdf_big_query[gdf_big_query.geometry.apply(lambda geom: gdf1.intersects(geom).any())]
                alguma_sobreposicao = sobreposicoes.any()
                intersecoes_sem_geom = intersecoes.drop(columns='geometry', errors='ignore').drop_duplicates()
                # Bloco do relatório completo
                f.write(f"<h3>{'/'.join(niveis)}</h3>")
                f.write(f"<p><strong>Há interferência?</strong> {'Sim' if alguma_sobreposicao else 'Não'}</p>")
                f.write(f"<p><strong>Interferências:</strong></p>")
                if not intersecoes_sem_geom.empty:
                    f.write(intersecoes_sem_geom.to_html(index=False, escape=False))
                    f.write("<br>")
                else:
                    f.write("<p>Nenhuma interferência foi encontrada.</p>")
                    f.write("<br>")
                # Bloco somente com Relatório Simplificado
                if alguma_sobreposicao:
                    bloco_sobreposicao += f"<h3>{'/'.join(niveis)}</h3>"
                    bloco_sobreposicao += f"<p><strong>Interferências:</strong></p>"
                    if not intersecoes_sem_geom.empty:
                        bloco_sobreposicao += intersecoes_sem_geom.to_html(index=False, escape=False)
                        bloco_sobreposicao += "<br>"
                    else:
                        bloco_sobreposicao += "<p>Nenhuma interferência foi encontrada.</p>"
                        bloco_sobreposicao += "<br>"
            except Exception as e:
                msg_erro = f"<h3>Resultado - {'/'.join(niveis)}</h3><p style='color:red;'>Erro ao processar: {str(e)}</p>"
                f.write(msg_erro)
                bloco_sobreposicao += msg_erro
        # Bloco somente com o Mapa
        mapa = gerar_mapa(caminho_shp, caminho_relatorio)
        bloco_mapa += f"<h3>Mapa de Localização</h3>"
        bloco_mapa += f'<iframe src="{os.path.basename(mapa)}" width="100%" height="600px" style="border:none;"></iframe>'
        # Finalizar ambas as divs
        f.write('</div>')
        bloco_sobreposicao += '</div>'
        f.write(bloco_sobreposicao)
        bloco_mapa += '</div>'
        f.write(bloco_mapa)
        # Fechar o HTML
        f.write("""
            <script>
                document.addEventListener("DOMContentLoaded", function() {
                    document.querySelectorAll("table").forEach(table => {
                        table.classList.add("display");
                        $(table).DataTable({
                            "paging": false,           // desativa paginação
                            "lengthChange": false,     // remove o "Show N entries"
                            "info": false, 
                            "infoEmpty": "",
                            "infoFiltered": "",
                        language: {
                            search: "Pesquisar:",
                            zeroRecords: "Nenhum registro encontrado",
                            infoEmpty: "Sem registros disponíveis",
                            emptyTable: "Nenhum dado disponível na tabela"
                        }
                        });
                    });
                });
            </script>
        </body></html>
        """)
    print(f"Relatório HTML salvo em: {caminho_html}")





