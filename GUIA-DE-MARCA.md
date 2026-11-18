# Guia de marca da Nora

Vale para tudo que leva a marca da Nora ou do BRS: post, anúncio, apresentação,
documento, página. A referência viva é o site [nora.finance](https://www.nora.finance);
este guia registra o que ele usa e como aplicar fora dele.

Quem cria peça para rede social não desenha: descreve o post num JSON e o
gerador deste repositório monta a arte. A seção [Posts](#posts) explica.

## A marca em uma frase

A Nora opera a rede por trás do BRS, a stablecoin do real brasileiro, feita
para as plataformas que levam o real para a blockchain.

- **Nora** é a empresa e a rede. **BRS** é a stablecoin. São duas marcas: a
  Nora assina, o BRS é o produto.
- Escreva `BRS` em maiúsculas, `Nora` com inicial maiúscula, `onchain` junto,
  `Pix` assim.

Fatos que o site afirma e que uma peça pode repetir sem outra fonte:

- 1 BRS = 1 BRL, com lastro integral, 1:1.
- As reservas ficam em títulos soberanos e de mercado monetário.
- O resgate é 1:1 em reais, por Pix.
- O BRS está no ar em Solana, Ethereum, Base e Polygon, com bridge para a Solana.
- Qualquer carteira Solana ou EVM guarda, envia e recebe BRS.
- A liquidação leva segundos, a qualquer hora de qualquer dia.

## Voz

Direta, calma e precisa. Quem lê é gente de produto, tesouraria e engenharia
de fintechs e exchanges.

- Frase curta, verbo ativo, uma ideia por peça.
- Título em até duas frases. O destaque de cor marca o fecho: a segunda frase
  ("O BRS chegou à Solana. **Bridge no ar.**") ou o trecho final
  ("O real brasileiro, **onchain.**").
- Número e fato fora da lista acima só com fonte pública (site, documentação,
  dado onchain) ou vindos de quem pediu a peça. Sem fonte, a peça sai sem o número.
- Descreva o que o BRS é e faz. Rendimento, retorno, yield, ganho, taxa e
  percentual ficam fora da peça. Se o assunto pedir (a economia da rede para
  parceiros, por exemplo), pergunte a quem pediu como dizer.
- Sem emoji, sem ponto de exclamação, sem urgência ("últimas vagas", "não
  perca"), sem superlativo ("o maior", "revolucionário").
- Português do Brasil por padrão; inglês quando o público da peça é de fora.

O gerador barra emoji e ponto de exclamação. O resto da voz depende de quem
escreve: ele não sabe se uma frase promete demais.

## Cores

Fonte única: [`colors/tokens.json`](colors/tokens.json) (também em
[CSS](colors/palette.css), [SCSS](colors/palette.scss) e
[Tailwind](colors/tailwind.colors.js)).

| Cor | Hex | Papel |
|---|---|---|
| Papel | `#F4F1EA` | fundo claro padrão |
| Verde | `#003C2F` | fundo escuro, destaque de título no claro, disco do BRS |
| Lima | `#C6F24E` | botão e chamada, fundo de destaque |
| Lima do BRS | `#E3FF63` | marca do BRS, destaque de título sobre o verde |
| Tinta | `#0A0A0A` | texto sobre papel e sobre lima |
| Pedra | `#4A4740` | texto de apoio sobre papel |
| Sálvia | `#C9D7D0` | texto de apoio sobre verde |

- Três fundos: papel, verde e lima. Uma peça usa um só.
- Par de texto por fundo: tinta sobre papel e lima; papel sobre verde. O
  destaque é verde no claro e lima do BRS no escuro.
- As duas limas não se misturam na mesma função: `#C6F24E` é da Nora (botão,
  fundo), `#E3FF63` é do BRS (marca e destaque sobre verde).
- O fundo ganha uma malha de gradientes suaves nas cores da própria paleta
  (as da tabela e os tons de apoio de `tokens.json`), como o brilho lima do
  topo do site. Nunca uma cor de fora.
- Preto `#000000` e os cinzas continuam na paleta para produto e documento
  (terminal de código, interface). Peça de comunicação usa os três fundos acima.
- Apresentações de 2026 usam vizinhos quase idênticos (`#003C30`, `#E2FB56`,
  `#F7F6F1`). Seguem válidas; material novo usa os valores desta tabela.

## Tipografia

**Geist** para tudo; **Geist Mono** para rótulo, rodapé e numeração. As duas
são abertas (SIL Open Font License) e estão em [`fonts/`](fonts/), na versão
1.7.2 do projeto [vercel/geist-font](https://github.com/vercel/geist-font).

- Título: Geist Medium (500), entrelinha 1,02 e letras apertadas (-0,045em).
- Texto: Geist Regular (400), entrelinha 1,32.
- Rótulo: Geist Mono Medium, maiúsculas, espaçamento de 0,12em.
- O logo já vem em curvas: nunca redigite "nora" numa fonte.
- Apresentações de 2026 em Instrument Sans seguem válidas; material novo usa Geist.

## Logo da Nora

Arquivos em [`logo/`](logo/). O símbolo tem 17 raios.

- Sobre papel e lima: variante `on-light` (preta). Sobre verde: `on-dark` (papel).
- Área livre de 12,5% da maior dimensão em volta. Use `padded` quando a peça
  não garante essa folga e `tight` quando o layout já garante.
- Use o arquivo como está: sem esticar, girar, recolorir, contornar, aplicar
  brilho ou redesenhar os raios.
- O logo que assina uma peça é sempre o arquivo oficial; nenhuma IA o desenha.
  As versões 3D do símbolo em `social/ilustracoes/` são ilustração: entram
  como arte e não substituem o logo.
- Em post, o logo fica no rodapé, à esquerda. O gerador põe sozinho. No layout
  `pessoa` ele sobe para o topo, porque o retrato ocupa a base.

## Marca do BRS

Disco chapado verde `#003C2F` com a sigla BRS e duas curvas em lima `#E3FF63`.
Arquivos oficiais em [Nora-Finance/brs-assets](https://github.com/Nora-Finance/brs-assets);
as duas variantes usadas em post estão em [`social/brs/`](social/brs/).

- Marca chapada sobre papel e lima: disco verde. Sobre verde: disco lima. O
  gerador escolhe sozinho em `"arte": "brs"`.
- O disco é chapado: sem aro, anel, friso, filete ou borda metálica, e sem
  brilho de moeda.
- Em ilustração 3D o disco é sempre o verde, com espessura e a lateral no
  mesmo verde fosco, inclusive sobre fundo verde.

## Posts

Todo post sai do gerador, a partir de um JSON. O gerador só aceita o que está
nas listas abaixo e recusa texto que não cabe: é isso que mantém os posts
iguais entre si.

```sh
python3 social/render.py meu-post.json             # grava meu-post.png ao lado do JSON
python3 social/render.py meu-post.json -o saida/   # grava em outra pasta
python3 social/test_render.py                      # prova do gerador
```

O comando roda de qualquer pasta. Carrossel grava um PNG por página:
`meu-post-01.png`, `meu-post-02.png`. Com erro de validação ou de desenho,
nenhum PNG é gravado.
Precisa de Python 3.10 ou mais novo e de Chromium ou Chrome, em Linux ou macOS.

### Campos de todo post

| Campo | Valores |
|---|---|
| `formato` (obrigatório) | `feed` 1080×1350 (padrão do Instagram e do LinkedIn), `quadrado` 1080×1080, `story` 1080×1920, `paisagem` 1200×675 (X e prévia de link), `horizontal` 1440×1080 (imagem 4:3 no X e no LinkedIn) |
| `tema` (obrigatório) | `papel`, `verde`, `lima` |
| `layout` (obrigatório) | `titulo`, `numero`, `lista`, `citacao`, `pessoa` |
| `selo` | etiqueta no topo, até 28 caracteres ("Novidade", "Lastro") |
| `rodape` | texto à direita do logo, até 40 caracteres; padrão `nora.finance` |
| `semente` | palavra que define a malha do fundo, até 60 caracteres; padrão é o título |

### Campos por layout

Em negrito, o que é obrigatório; entre parênteses, o máximo de caracteres.

| Layout | Para quê | Campos |
|---|---|---|
| `titulo` | anúncio, afirmação, capa e fecho de carrossel | **`titulo`** (110), `texto` (220), `chamada` (botão, 28), `arte`, `imagem` |
| `numero` | um dado | **`numero`** (12: "1:1", "R$ 1"), **`titulo`** (60), `texto` (160) |
| `lista` | de 2 a 4 pontos | **`titulo`** (70), **`itens`**: cada um com **`titulo`** (48) e `texto` (110) |
| `citacao` | fala de alguém | **`citacao`** (220), **`autor`** (40), `cargo` (60) |
| `pessoa` | apresentar alguém, na série [Spotlight do time](#spotlight-do-time) | **`nome`** (40), **`cargo`** (28), **`foto`** |

- **Destaque:** nos campos `titulo` e `citacao`, em qualquer layout, o trecho
  entre asteriscos ganha a cor de destaque: `"O BRS chegou à Solana. *Bridge no ar.*"`.
- **Quebra de linha:** o título quebra sozinho, em linhas equilibradas. Para
  escolher a quebra, use `\n` em `titulo`, `citacao`, `texto` ou `nome`; o uso mais
  comum é pôr o destaque numa linha própria: `"Construa com o BRS.\n*Fale com a Nora.*"`.
- **Arte** (só no layout `titulo`): `"arte"` vale `nenhuma` (padrão), `brs`
  (a marca do BRS) ou `imagem`. Com `imagem`, o campo `"imagem"` leva o nome de
  uma [ilustração pronta](#ilustrações-prontas) (`"brs-celular"`) ou o caminho de
  um arquivo PNG, JPG ou WebP, relativo ao JSON ou absoluto. Imagem com fundo
  transparente entra solta; sem transparência, entra num cartão de cantos
  arredondados.
- **Tamanho do texto:** o título se ajusta sozinho ao espaço. Se o gerador
  responder que o texto não cabe, encurte o campo mais longo: os corpos não mudam.
- **Story:** o gerador reserva 250 px livres no topo e na base, onde o
  aplicativo põe a interface dele.

### Carrossel

```json
{
  "comum": { "formato": "feed", "semente": "brs-quatro-redes" },
  "paginas": [
    { "layout": "titulo", "tema": "verde", "titulo": "O real brasileiro, *onchain.*", "arte": "brs" },
    { "layout": "numero", "tema": "papel", "numero": "R$ 1", "titulo": "em reserva para cada BRS emitido." },
    { "layout": "titulo", "tema": "verde", "titulo": "Construa com o BRS. *Fale com a Nora.*", "chamada": "nora.finance" }
  ]
}
```

De 2 a 10 páginas, todas no mesmo formato; cada uma herda `comum` e recebe a
numeração no rodapé.

### Coerência entre posts

- Uma campanha, uma `semente`: o fundo fica igual em todas as peças dela.
- No perfil, alterne papel e verde. Sem saber qual foi o post anterior: verde
  para anúncio e peça institucional, papel para explicação, lista e dado.
- Lima é exceção, para dado ou anúncio forte: no máximo um em cada quatro posts.
- Carrossel abre e fecha no mesmo tema; o miolo pode ir no outro.
- Uma mensagem por peça. Se precisa de dois títulos, são dois posts ou um carrossel.
- Explicação em etapas vira `lista` ou carrossel. Diagrama de caixas ligadas
  por setas não é linguagem da marca.

Exemplos prontos, com o JSON de cada um, em [`social/exemplos/`](social/exemplos/):

![Exemplos de posts gerados pelo kit](social/exemplos/galeria.webp)

### Séries

Série é um tipo de post que se repete: mesma arte, mesmo padrão de texto. Só
muda o assunto de cada edição.

#### Spotlight do time

Apresenta uma pessoa do time da Nora: quem é, o que construiu antes e o que
faz aqui. Uma pessoa por post. Referências no ar:
[João Bilesimo](https://x.com/norafinancexyz/status/2120198582796009505) e
[André Rocco](https://x.com/norafinancexyz/status/2123034716182094108).

A série tem layout próprio, `pessoa`. A arte é sempre a mesma: fundo verde
escuro com dois arcos em lima, o retrato recortado à direita com brilho nos
ombros, logo no topo, a linha "Nora team Spotlight", o nome e o cargo numa
pílula. Só mudam o nome, o cargo e a foto:

```json
{
  "formato": "horizontal",
  "layout": "pessoa",
  "tema": "verde",
  "nome": "Nome Sobrenome",
  "cargo": "Founding Engineer",
  "foto": "foto-recortada.png"
}
```

- **Formato:** `horizontal` no X e no LinkedIn (é o formato das edições no
  ar), `feed` no Instagram, `story` nos stories. Nos formatos em pé o texto
  fica em cima e o retrato embaixo, dentro do arco.
- **Tema:** só `verde`. O layout não tem rodapé; `rodape` é recusado.
- **Linha de abertura:** "Nora team Spotlight" por padrão. O campo `selo`
  troca o texto, e a última palavra sai em destaque.
- **Foto:** retrato real da pessoa, cedido por ela, do peito para cima e com o
  tronco indo até a base da foto. Entra já recortado, em PNG ou WebP com fundo
  transparente; o gerador apara a sobra em volta. Para recortar:
  `uvx --from "rembg[cpu,cli]" rembg i -m isnet-general-use foto.jpg foto.png`.
  Confira o contorno do cabelo e se não sobrou resíduo solto. Remover o fundo
  pode; nenhuma IA gera nem retoca rosto.
- **Nome e cargo:** o nome cabe numa linha e diminui sozinho; para duas
  linhas, use `\n`. Com nome ou cargo longo no `horizontal`, confira no PNG se
  o texto não encosta no rosto.
- **Texto do post**, em inglês no X, em três partes:

  ```text
  Introducing @perfil

  At [onde trabalhou], [Nome] [o que construiu, com um fato que se confere].

  Now, as [cargo] at Nora, [he/she] [o que faz na Nora].
  ```

  Uma linha final pode ligar a pessoa ao produto ("$BRS is built to scale.").
- **Fatos:** nome, cargo, perfil e trajetória vêm da própria pessoa. Número da
  trajetória (usuários, volume) só com fonte pública ou confirmação dela.
- A pessoa aprova a arte e o texto antes de o post ir ao ar.

## Imagem gerada por IA

A arte determinística (fundo, tipografia, logo, marca do BRS) vem sempre do
gerador. A IA de imagem entra só para a ilustração, que vai no campo `imagem`.

- Linguagem: objeto 3D fosco, uma metáfora por imagem, bastante espaço vazio,
  luz suave. Paleta: verde `#003C2F`, lima `#E3FF63`, papel `#F4F1EA` e grafite.
- A imagem sai sem texto, sem logo e sem interface. Texto e logo entram pelo gerador.
- O BRS só aparece desenhado quando o modelo recebe o ícone oficial como
  referência. Confira o resultado contra o oficial: disco chapado, sigla BRS,
  duas curvas, nenhum aro.
- A emoção da cena acompanha a mensagem: segurança pede objeto firme e fechado,
  novidade pede movimento. Cena alegre em notícia séria é erro.
- Fora da linguagem: neon azul ou roxo, ouro, moeda genérica, estética de
  cassino, foguete, lua, gráfico disparando, brilho exagerado, cara de
  brinquedo, pessoa realista. Gente do time aparece só em foto real, pela
  série [Spotlight do time](#spotlight-do-time).

### Ilustrações prontas

Oito ilustrações aprovadas em [`social/ilustracoes/`](social/ilustracoes/), com
fundo transparente. Cada uma só entra nos temas em que foi aprovada; o gerador
confere por [`index.json`](social/ilustracoes/index.json), mesmo que o arquivo
seja copiado ou renomeado.

| Ilustração | Serve para | Temas |
|---|---|---|
| `brs-cofre` | lastro guardado, segurança | papel, lima |
| `brs-celular` | BRS no app, pagamento, carteira | papel, verde, lima |
| `brs-lastro` | reservas, lastro 1:1 | papel, lima |
| `brs-pilhas` | crescimento, volume, emissão | papel, lima |
| `brs-garantia` | garantia, equilíbrio, paridade | verde |
| `brs-cartao` | cartão, gasto do dia a dia | verde |
| `nora-simbolo-brs` | Nora e BRS juntos, rede | papel, verde |
| `nora-simbolo-3d` | institucional Nora | verde |

Uso no JSON: `"arte": "imagem", "imagem": "brs-celular"`. Antes de gerar imagem
nova, veja se uma destas já resolve.

### Imagem nova

Roteiro de pedido para a IA de imagem:

```text
Ilustração 3D fosca, estilo objeto de estúdio, de [OBJETO OU CENA], com a moeda
BRS da referência anexada: disco chapado verde-escuro #003C2F, sigla BRS e duas
curvas em lima #E3FF63, sem aro, anel, friso ou borda metálica; a lateral do
disco é do mesmo verde fosco. Paleta restrita a verde #003C2F, lima #E3FF63,
creme #F4F1EA e grafite. Luz suave de estúdio, sombra curta. Fundo liso
[#F4F1EA para tema claro | #5E7F74 para recortar depois]. Sem texto, sem outros
logos, sem pessoas. Enquadramento com folga em volta do objeto.
```
