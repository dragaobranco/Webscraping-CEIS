from datetime import datetime
import logging
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Configurações do logger
logging.basicConfig(style = '{',
                    filename = 'registros.log',
                    level = logging.INFO,
                    format = '{asctime} - {levelname}: {message}',
                    datefmt = '%d/%m/%y %H:%M'
                    )
logger = logging.getLogger(__name__)

def download_ceis(pasta_download, data_extracao_anterior = None, logger = logger):
    '''Realiza o download do arquivo ZIP do CEIS a partir do Portal da Transparência.

    Args:
        pasta_download (str): Caminho da pasta onde o arquivo será salvo.
        data_extracao_anterior (str): Data da última extração para comparação.
        logger (logging.Logger): Objeto de log para registrar eventos.

    Returns:
        tuple: Caminho do arquivo ZIP baixado e a data da extração atual, ou (None, None) se não houver novos dados ou em caso de erro.
    '''
    # Inicializar navegador como None para evitar UnboundLocalError
    navegador = None

    # Abertura do navegador
    chrome_options = Options()
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': pasta_download,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True
    })
    
    try:
        # Abertura do navegador
        navegador = webdriver.Chrome(options=chrome_options)

        # Download da base CEIS - Cadastro Nacional de Empresas Inidôneas e Suspensas
        # Abertura da página
        url = 'https://portaldatransparencia.gov.br/download-de-dados/ceis'
        print(f'Abrindo URL: {url}')
        navegador.get(url)

        # Aguarda o popup de cookies aparecer e clica em "Rejeitar cookies"
        try:
            print('Procurando botão de cookies...')
            rejeitar_cookies = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.ID, 'accept-minimal-btn')))
            print('Clicando no botão de rejeitar cookies...')
            rejeitar_cookies.click()
            print('Cookies rejeitados com sucesso')
        except TimeoutException:
            print('Popup de cookies não apareceu ou já foi tratado')
        except Exception as e:
            print(f'Erro ao lidar com popup de cookies: {str(e)}')
        
        # Identificação do botão de download
        print('Procurando botão de download...')
        try:
            download = WebDriverWait(navegador, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="link-unico"]/li/a')))
            print(f"Botão de download encontrado: {download.text}")
        except Exception as e:
            print(f"Falha ao encontrar botão de download: {str(e)}")
            # Screenshot para debug
            navegador.save_screenshot(os.path.join(pasta_download, 'erro_webscraping.png'))
            return None, None
        
        # Extração da data e verificação
        data_extracao_atual = datetime.strptime(download.text, '%d/%m/%Y').date()
        print(f'Data de extração atual: {data_extracao_atual}')

        # Verifica se a data última extração é igual à dos dados disponíveis no site
        if data_extracao_anterior == data_extracao_atual:
            logger.info(f'Não há novos dados para serem baixados. Última atualização realizada em {download.text}.')
            return None, None
    
        # Construção do nome do arquivo
        ano = str(data_extracao_atual)[0:4]
        mes = str(data_extracao_atual)[5:7]
        dia = str(data_extracao_atual)[8:10]
        nome_arquivo = f'{ano}{mes}{dia}_CEIS.zip'

        arquivo_zip = os.path.join(pasta_download, nome_arquivo)

        # Execução do download
        download.click()
        
        # Confirmação do download
        for tentativa in range(10):
            if os.path.exists(arquivo_zip):                    
                logging.info('Download concluído com sucesso!')
                return arquivo_zip, data_extracao_atual                
            sleep(1)

        logger.error('Falha no download!')                
        return None, None

    except Exception as e:
        logger.error(f'Erro: {e}')
        return None, None
    
    finally:
        navegador.quit()
        logging.shutdown()

if __name__ == "__main__":
    pasta_download = 'Downloads'
    data_extracao_anterior = None
    download_ceis(pasta_download, data_extracao_anterior, logger)