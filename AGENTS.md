# Nora: instruções para IAs

Este repositório é a fonte da marca da Nora e do BRS. As regras estão em
[`GUIA-DE-MARCA.md`](GUIA-DE-MARCA.md): leia inteiro antes de criar qualquer
peça, texto ou imagem da Nora. Se o que você lembra divergir do guia, vale o guia.

## Criar um post de rede social

1. Escolha `formato`, `layout` e `tema` nas tabelas da seção Posts do guia e
   escreva o texto conforme a seção Voz. Parta do exemplo mais parecido em
   `social/exemplos/`. Post de série (apresentar alguém do time, por exemplo)
   segue a receita da seção Séries do guia.
2. Salve a especificação num `.json` fora deste repositório, na pasta do
   trabalho.
3. Rode `python3 social/render.py caminho/do/post.json`. O erro diz o campo e
   o motivo; "o texto não cabe" pede encurtar o campo mais longo. Corrija o
   JSON e rode de novo. Feito quando o comando imprime o caminho do PNG.
4. Abra o PNG e confira com os olhos: título legível numa leitura só, destaque
   no trecho certo, nada cortado. Feito quando você viu a imagem, não quando o
   comando passou.
5. Entregue o PNG e o JSON juntos, para a peça poder ser refeita.

Sem terminal ou sem navegador para rodar o gerador: entregue só o JSON,
validado contra as tabelas do guia, e diga que falta renderizar.

## Limites

- O gerador é o único caminho para post. Layout, cor, tamanho de letra e
  posição do logo já estão decididos nele: o que varia é o JSON.
- Logo da Nora e marca do BRS entram pelos arquivos oficiais (`logo/`,
  `social/brs/`). Para ilustrar, use primeiro uma das prontas (`"imagem": "brs-cofre"`);
  IA de imagem produz só ilustração nova, pelo roteiro da seção "Imagem gerada
  por IA" do guia.
- Número, parceiro, data e afirmação sobre o BRS vêm de quem pediu a peça, da
  lista de fatos do guia ou de fonte pública. O que faltar vira pergunta, não
  suposição.
- Pedido que o guia não permite (cor de fora, emoji, promessa de ganho): diga
  o que ficou de fora e por quê, e entregue a versão que o guia permite.
- Peça nova não é publicação: quem pediu aprova antes de ir ao ar.

## Mudar o kit

Mudou `social/post.html` ou `social/render.py`: rode `python3 social/test_render.py`
e refaça a galeria com o comando da seção Manutenção do `README.md`. Mudou
arquivo listado em `SHA256SUMS`: atualize a linha dele e o `manifest.json`.
