# Levantamento de licenças — Ideal Oficina

**Projeto:** Ideal Oficina  
**Responsável pelo projeto:** Juan Pedro  
**Data do levantamento:** 04/11/2026

## 1. Dependências identificadas

A tabela abaixo foi elaborada com base nas dependências diretas e versões registradas no arquivo `requirements.txt` do projeto.

| Dependência | Versão utilizada | Licença | Permite uso comercial? | Obriga abrir o código de um projeto derivado? |
|---|---:|---|---|---|
| FastAPI | 0.141.1 | MIT | Sim | Não. A licença exige preservar o aviso de copyright e o texto da licença nas cópias ou partes substanciais. |
| mysql-connector-python | 26.7.0 | GPLv2 + Universal FOSS Exception 1.0 | Sim, respeitando os termos da licença e da exceção | Pode haver obrigação de disponibilizar o código-fonte de versões modificadas ou de obras derivadas distribuídas, conforme a aplicação da GPL e da exceção. Avaliar o caso de distribuição. |
| Pydantic | 2.13.4 | MIT | Sim | Não. A licença exige preservar o aviso de copyright e o texto da licença nas cópias ou partes substanciais. |
| python-dotenv | 1.2.3 | BSD-3-Clause | Sim | Não. É necessário preservar os avisos de copyright, as condições e a isenção de responsabilidade. |
| Uvicorn | 0.52.4 | BSD-3-Clause | Sim | Não. É necessário preservar os avisos de copyright, as condições e a isenção de responsabilidade. |

## 2. Interpretação dos resultados

- **MIT:** permite usar, copiar, modificar, distribuir e comercializar o software. Não exige publicar o código-fonte do projeto derivado, mas exige manter o aviso de copyright e o texto da licença nas cópias ou partes substanciais.
- **BSD-3-Clause:** permite uso comercial, modificação e distribuição. Não exige abrir o código do projeto derivado, mas exige manter os avisos e cumprir as condições da licença.
- **GPLv2 com Universal FOSS Exception:** permite uso, modificação e distribuição sob seus termos. A GPL pode exigir disponibilização do código-fonte correspondente quando cópias ou obras derivadas são distribuídas. A exceção adicional pode alterar a análise em determinadas situações de ligação com software separado. Por isso, o uso e a forma de distribuição do MySQL Connector/Python devem ser avaliados conforme os textos integrais das licenças.

## 3. Conclusão

As dependências FastAPI, Pydantic, python-dotenv e Uvicorn utilizam licenças permissivas (MIT ou BSD-3-Clause), que permitem uso comercial e não obrigam, por si só, a publicação do código-fonte do projeto que as utiliza, desde que os avisos e condições exigidos sejam preservados.

O MySQL Connector/Python possui uma licença com obrigações específicas (GPLv2 e Universal FOSS Exception). Portanto, merece atenção especial caso o Ideal Oficina seja distribuído a terceiros, principalmente se houver modificações no próprio conector ou uma forma de integração que possa ser considerada obra derivada.

A licença MIT incluída na raiz do Ideal Oficina se aplica ao código original do projeto, **não substitui nem altera as licenças das dependências de terceiros**.

## 4. Fontes consultadas

- `requirements.txt` do Ideal Oficina: https://github.com/Ju4nD33v/Ideal-Oficina/blob/main/requirements.txt
- FastAPI — repositório e licença: https://github.com/fastapi/fastapi
- Pydantic — repositório e licença: https://github.com/pydantic/pydantic
- python-dotenv — repositório e licença: https://github.com/theskumar/python-dotenv
- Uvicorn — repositório e licença: https://github.com/encode/uvicorn
- MySQL Connector/Python — texto oficial da licença: https://dev.mysql.com/doc/dev/connector-python/latest/license.html
- Universal FOSS Exception 1.0: https://oss.oracle.com/licenses/universal-foss-exception/

---

*Observação: este documento é um levantamento informativo das licenças declaradas pelas dependências. Não constitui parecer jurídico. Antes de distribuir comercialmente o software, confira os arquivos de licença das versões efetivamente instaladas e a forma concreta de distribuição.*
