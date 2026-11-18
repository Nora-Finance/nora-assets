# Instalar a marca da Nora numa IA

Cole o texto abaixo numa conversa nova com a IA (Claude, ChatGPT, Codex ou
outra). Ela lê o guia, grava as regras na memória permanente e prova que
funcionou. Depois disso, basta pedir "faz um post da Nora sobre X".

```text
Você vai instalar a marca da Nora na sua memória permanente, para que toda
arte, post ou texto da Nora que você fizer daqui em diante siga o mesmo padrão.

1. Leia inteiros, nesta ordem:
   https://raw.githubusercontent.com/Nora-Finance/nora-assets/main/AGENTS.md
   https://raw.githubusercontent.com/Nora-Finance/nora-assets/main/GUIA-DE-MARCA.md
   Se você roda num computador com git, clone
   https://github.com/Nora-Finance/nora-assets numa pasta estável e leia de lá.

2. Grave o CARTÃO abaixo, palavra por palavra, onde você guarda o que vale
   entre conversas: arquivo de memória, instruções do projeto ou memória do
   assistente. Se clonou o repositório, acrescente ao cartão o caminho da pasta.
   Se você não guarda nada entre conversas, diga isso e me peça para colar o
   cartão nas instruções do projeto.

3. Prove a instalação. Com terminal: rode
   python3 social/render.py social/exemplos/titulo-papel.json -o <pasta temporária>
   e me mostre o PNG. Sem terminal: escreva o JSON de um post de teste no
   formato do guia.

4. Responda em três linhas: onde gravou o cartão, onde está o repositório
   (ou "sem clone") e o resultado do passo 3.

CARTÃO
Marca Nora e BRS. Fonte: github.com/Nora-Finance/nora-assets, ramo main.
- Antes de criar arte, post ou texto da Nora, releia GUIA-DE-MARCA.md e
  AGENTS.md desse repositório. Se este cartão e o guia divergirem, vale o guia.
- Post de rede social sai do gerador do repositório: escrevo um JSON e rodo
  python3 social/render.py. O layout já está decidido lá; eu escolho o tipo
  da peça, formato, tema e texto.
- Peça de anúncio (parceiro, lançamento, evento, pessoa): fundo verde-noite
  #001D17 com os arcos em lima, logo no topo à esquerda, rótulo em maiúsculas
  espaçadas, título pesado com o fecho em lima, imagem à direita ou embaixo.
  Peça de explicação (dado, lista, citação, carrossel): logo no rodapé.
- Cores: verde-noite #001D17, papel #F4F1EA, verde #003C2F, lima #C6F24E,
  lima do BRS #E3FF63, tinta #0A0A0A.
- Letra: Geist; Geist Mono em assinatura e numeração.
- Logo da Nora e marca do BRS: só os arquivos oficiais do repositório. O BRS é
  um disco chapado verde com a sigla e duas curvas em lima, sem aro.
- Voz: direta, calma, precisa. Título em até duas frases, a segunda em
  destaque. Sem emoji e sem exclamação. Rendimento, retorno e ganho ficam
  fora da peça. Número só com fonte pública.
- IA de imagem faz só a ilustração, sem texto e sem logo, pelo roteiro do guia.
  Gente só em foto real, cedida pela pessoa; nenhuma IA gera nem retoca rosto.
- Peça nova espera a aprovação de quem pediu antes de ser publicada.
```

Para atualizar depois de uma mudança no guia: "releia o guia da Nora e
atualize o cartão".
