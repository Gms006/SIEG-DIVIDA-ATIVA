# agents.md – Automação SIEG IRIS: Dívida Ativa

---

## acessar_sieg

### Objetivo
Realizar login no portal SIEG IRIS e navegar até a seção de Dívida Ativa.

### Etapas
1. Acesse: `https://iris.sieg.com/DividaAtiva`
2. Preencha:
   - E-mail: `contabil2@netocontabilidade.com.br` (campo `#txtEmail`)
   - Senha: `Brasil*123` (campo `#txtPassword`)
3. Clique no botão "Entrar" (`#btnSubmit`)
4. Aguarde o redirecionamento para a tela de Dívida Ativa

---

## selecionar_empresa

### Objetivo
Selecionar a empresa Green Ambiental usando o CNPJ.

### Etapas
1. Localize o campo `input.multiselect__input`
2. Digite: `10608734000101`
3. Simule `Enter`
4. Aguarde o carregamento e verifique a presença de:
   ```html
   <span class="hidden xl:inline-block">(10608734000101)</span>
abrir_detalhes_dividas
Objetivo
Exibir as dívidas ativas da empresa selecionada.

Etapas
Clique no elemento:

html
Copiar
Editar
<span class="pill-alert pill cursor-pointer" onclick="SeeDetails(...)">
baixar_detalhe_divida
Objetivo
Para cada dívida ativa exibida, abrir e iniciar o processo de download do PDF.

Etapas
Clique no botão "Baixar":

html
Copiar
Editar
<a id="btnDownload-..." class="btn btn-sm ...">
Clique no botão:

html
Copiar
Editar
<div role="button">Imprimir</div>
salvar_pdf_modal_windows
Objetivo
Automatizar a janela "Salvar como" do Windows para salvar o PDF corretamente.

Etapas
Aguarde a janela nativa abrir

Use pywinauto ou pyautogui para:

Navegar até:

makefile
Copiar
Editar
G:\EMPRESAS\GREEN AMBIENTAL LTDA\Contabilidade\Conferências\Débitos Federais\PGFN
Renomear o arquivo com base no HTML:

html
Copiar
Editar
<h5>N° inscrição: <span>11 2 25 004790-06</span></h5>
Nome sugerido: divida_10608734000101_1122500479006.pdf

Pressionar o botão:

html
Copiar
Editar
<button><span>Salvar</span></button>
paginacao_dividas
Objetivo
Navegar entre as páginas da tabela de dívidas ativas para garantir que todas sejam processadas.

Etapas
Detecte o controle de paginação:

html
Copiar
Editar
<ul class="pagination">
  ...
  <a data-dt-idx="next">&gt;</a>
  ...
</ul>
Enquanto o botão "next" estiver habilitado:

Clique

Aguarde a nova página

Repita o processo de baixar_detalhe_divida

observacoes_gerais
Use wait_for_selector e wait_for_load_state para garantir estabilidade

Capture logs com CNPJ, número da inscrição e nome do arquivo salvo

Crie tratamento de exceções para falhas na abertura da janela "Salvar como"

O nome do PDF deve ser único e baseado na inscrição da dívida
