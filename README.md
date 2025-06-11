# SIEG Dívida Ativa Automation

Este repositório contém um script em Python para baixar automaticamente as dívidas ativas da empresa **Green Ambiental** utilizando o portal **SIEG IriS**.

## Requisitos
- Python 3.8+
- [Playwright](https://playwright.dev/python/)
- `pyautogui` (ou biblioteca similar) para manipulação da janela "Salvar como" do Windows

Instale as dependências principais com:

```bash
pip install playwright pyautogui
playwright install
```

## Uso
Execute o script `baixar_dividas.py`:

```bash
python baixar_dividas.py
```

Caso o portal redirecione para `/home` depois do login, o script acessa novamente a página de Dívida Ativa antes de continuar.

O script realiza login, seleciona a empresa pelo CNPJ e baixa todos os PDFs de dívidas, salvando-os em:

```
G:\EMPRESAS\GREEN AMBIENTAL LTDA\Contabilidade\Conferências\Débitos Federais\PGFN
```

Os arquivos são nomeados de acordo com o número da inscrição de cada dívida.

Durante a execução são gerados logs informando cada etapa do processo. Caso ocorra algum erro, o script captura uma captura de tela para auxiliar na análise.
