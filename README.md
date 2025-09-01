# Download CEIS – Portal da Transparência

Este projeto realiza o **download automatizado** da base de dados do **Cadastro Nacional de Empresas Inidôneas e Suspensas (CEIS)** diretamente do [Portal da Transparência](https://portaldatransparencia.gov.br/download-de-dados/ceis), utilizando **Python** e **Selenium**.

---

## 🚀 Funcionalidades
- Acessa automaticamente a página de download do CEIS.  
- Rejeita o pop-up de cookies (quando exibido).  
- Verifica a **data da última atualização** disponível no site.  
- Evita downloads duplicados caso não haja novos dados.  
- Realiza o download do arquivo ZIP com a base mais recente.  
- Registra logs de execução em `registros.log`.  

---

## 📋 Pré-requisitos
Antes de executar, é necessário ter instalado em sua máquina:

- [Python 3.8+](https://www.python.org/)  
- [Google Chrome](https://www.google.com/chrome/)  
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) compatível com a versão do seu navegador.  

E instalar as bibliotecas Python necessárias:

```bash
pip install selenium
```

---

## 📂 Estrutura do projeto
- `script.py` → Código principal para automação do download.  
- `registros.log` → Arquivo de log gerado automaticamente.  
- `Downloads/` → Pasta onde os arquivos ZIP baixados serão armazenados.  

---

## ▶️ Como usar
1. Clone este repositório:
   ```bash
   git clone https://github.com/seuusuario/download-ceis.git
   cd download-ceis
   ```

2. Configure a pasta de destino para os downloads (por padrão, `Downloads`).  

3. Execute o script:
   ```bash
   python script.py
   ```

4. O script fará o download automático do arquivo CEIS atualizado (quando disponível).  

---

## 📝 Logs
Os registros de execução são gravados no arquivo `registros.log`, contendo:  
- Data e hora da execução.  
- Sucesso ou falha no download.  
- Mensagens de erro, quando houver.  

---

## ⚖️ Licença
Este projeto é de uso livre para fins de estudo e automação.  
Os dados baixados são públicos e estão disponíveis no **Portal da Transparência**.  
