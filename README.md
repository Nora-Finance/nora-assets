# Nora · assets oficiais

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="logo/svg/nora_logo-horizontal-short_fullcolor_on-dark_padded-outlined.svg">
  <img src="logo/nora.svg" width="320" alt="Nora">
</picture>

Identidade institucional da [Nora Finance](https://www.nora.finance): logos,
símbolos, favicons, vetores para impressão e paleta digital.

## Arquivos principais

| Uso | Arquivo / pasta |
|---|---|
| Logo Nora | [logo/nora.svg](logo/nora.svg) |
| Logo Nora Finance | [logo/nora-finance.svg](logo/nora-finance.svg) |
| Símbolo | [logo/nora-symbol.svg](logo/nora-symbol.svg) |
| Símbolo PNG de 256 px | [logo/nora-256.png](logo/nora-256.png) |
| Todas as variantes SVG | [logo/svg/](logo/svg/) |
| PNG e WebP de 256 a 4096 px de largura | [logo/png/](logo/png/), [logo/webp/](logo/webp/) |
| Impressão | [logo/pdf/](logo/pdf/), [logo/eps/](logo/eps/) |
| Ícones de site e aplicativo | [logo/favicon/](logo/favicon/) |
| Cores para design e desenvolvimento | [colors/tokens.json](colors/tokens.json), [CSS](colors/palette.css), [SCSS](colors/palette.scss), [Tailwind](colors/tailwind.colors.js), [ASE](colors/nora.ase) |

URLs diretas:

```text
https://raw.githubusercontent.com/Nora-Finance/nora-assets/main/logo/nora.svg
https://raw.githubusercontent.com/Nora-Finance/nora-assets/main/logo/nora-finance.svg
https://raw.githubusercontent.com/Nora-Finance/nora-assets/main/logo/nora-symbol.svg
https://raw.githubusercontent.com/Nora-Finance/nora-assets/main/logo/nora-256.png
```

## Escolher a variante

- `on-light`: uso sobre fundo claro. `on-dark`: uso sobre fundo escuro.
- `fullcolor`: cores da marca. `mono-black` e `mono-white`: monocromáticas.
- `horizontal-short`: wordmark Nora. `horizontal`: wordmark Nora Finance.
- `padded`: inclui área livre de 12,5%. `tight`: enquadramento justo.
- Os SVG de distribuição têm letras em contornos, sem depender de fonte instalada.

Use o tamanho final adequado, preserve as proporções e evite esticar, redesenhar
ou mudar as cores. A cor principal institucional é **#C6F24E**;
[tokens.json](colors/tokens.json) documenta a paleta completa e suas funções.

## Origem e integridade

Os arquivos são cópias exatas da biblioteca institucional **2.2.0**, usando
a identidade aprovada **2.1**: símbolo simétrico de 17 raios com correção óptica
de +20% na largura. O [master](logo/master/nora-symbol.svg) tem SHA-256:

```text
b1a2c26f57b29166f32da7ed117608747523ba2fa556000fd93c375c2f4571c4
```

[manifest.json](manifest.json) registra a origem e o SHA-256 de cada asset.
Confira os arquivos com `sha256sum -c SHA256SUMS`.

## Uso da marca

Marca e logo são propriedade da Nora Finance. Estes arquivos servem à
identificação da Nora em integrações e materiais institucionais. Não altere a
identidade nem sugira parceria ou endosso inexistente.

Os assets e contratos do token BRS estão em
[Nora-Finance/brs-assets](https://github.com/Nora-Finance/brs-assets).
