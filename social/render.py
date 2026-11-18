#!/usr/bin/env python3
"""Gera posts da Nora em PNG a partir de uma especificação JSON.

    python3 social/render.py meu-post.json            # PNG ao lado do JSON
    python3 social/render.py meu-post.json -o saida/  # PNG em outra pasta

Só biblioteca padrão, em Linux ou macOS; precisa de um Chromium ou Chrome
instalado (a variável CHROME aponta outro executável). Campos e regras:
GUIA-DE-MARCA.md, seção Posts.
"""
import argparse
import base64
import json
import os
import select
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FORMATOS = {
    "feed": (1080, 1350), "quadrado": (1080, 1080), "story": (1080, 1920), "paisagem": (1200, 675),
    "horizontal": (1440, 1080),
}
TEMAS = ("papel", "verde", "lima")
ARTES = ("nenhuma", "brs", "imagem")
FUNDOS = ("malha", "arcos")
# Por layout: campo -> (obrigatório, máximo de caracteres).
LAYOUTS = {
    "titulo": {"titulo": (True, 110), "texto": (False, 220), "chamada": (False, 28)},
    "numero": {"numero": (True, 12), "titulo": (True, 60), "texto": (False, 160)},
    "lista": {"titulo": (True, 70)},
    "citacao": {"citacao": (True, 220), "autor": (True, 40), "cargo": (False, 60)},
    "pessoa": {"nome": (True, 40), "cargo": (True, 28)},
}
COMUNS = {"selo": (False, 28), "rodape": (False, 40), "semente": (False, 60)}
ITEM = {"titulo": (True, 48), "texto": (False, 110)}
COM_DESTAQUE = ("titulo", "citacao")  # campos em que *asteriscos* marcam o destaque
COM_QUEBRA = ("titulo", "citacao", "texto", "nome")  # campos em que \n escolhe a quebra de linha
# O que a Geist e a Geist Mono desenham: latim com acentos e a pontuação usual. Emoji e
# símbolo de fora sairiam em outra fonte, por isso são recusados.
NA_FONTE = (
    set(map(chr, range(0x20, 0x7F)))
    | set(map(chr, range(0xA0, 0x180)))
    | set(map(chr, (0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2026, 0x2190, 0x2192)))
) - set(map(chr, (0xAD, 0xB5, 0x114, 0x115, 0x12C, 0x12D, 0x132, 0x133, 0x138, 0x13F, 0x140, 0x149, 0x14E, 0x14F, 0x17F)))
ILUSTRACOES = json.loads((AQUI / "ilustracoes" / "index.json").read_text(encoding="utf-8"))
NAVEGADORES = (
    "chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
)


def _textos(campos, regras, onde, erros, destaque=()):
    for nome, (obrigatorio, maximo) in regras.items():
        if nome not in campos:
            if obrigatorio:
                erros.append(f"{onde}: falta o campo '{nome}'")
            continue
        valor = campos[nome]
        if not isinstance(valor, str) or not valor.replace("*", "").strip():
            erros.append(f"{onde}: '{nome}' precisa ser um texto não vazio")
            continue
        if len(valor) > maximo:
            erros.append(f"{onde}: '{nome}' tem {len(valor)} caracteres; o máximo é {maximo}")
        fora = sorted(set(valor) - NA_FONTE - ({"\n"} if nome in COM_QUEBRA else set()))
        if fora:
            erros.append(f"{onde}: '{nome}' usa caractere fora da fonte da marca (emoji não entra): {' '.join(map(repr, fora))}")
        if "!" in valor:
            erros.append(f"{onde}: '{nome}' tem ponto de exclamação; a voz da marca não usa")
        if nome in destaque:
            if valor.count("*") % 2:
                erros.append(f"{onde}: '{nome}' tem asterisco de destaque sem par")
        elif "*" in valor:
            erros.append(f"{onde}: '{nome}' não aceita asterisco de destaque")


def _imagem(post, base):
    """Arquivo da imagem do post: nome de ilustração do kit, ou caminho relativo ao JSON (ou absoluto)."""
    nome = post["imagem"]
    return AQUI / "ilustracoes" / f"{nome}.webp" if nome in ILUSTRACOES else base / nome


def _ilustracao(arquivo):
    """Nome e regra da ilustração do kit com este conteúdo, mesmo que copiada ou renomeada."""
    conteudo = arquivo.read_bytes()
    for nome, regra in ILUSTRACOES.items():
        if (AQUI / "ilustracoes" / f"{nome}.webp").read_bytes() == conteudo:
            return nome, regra
    return None


def validar(post, base, onde="post"):
    """Confere um post contra os conjuntos fechados da marca. Devolve a lista de erros."""
    erros = []
    if not isinstance(post, dict):
        return [f"{onde}: precisa ser um objeto JSON"]
    for campo, opcoes in (("formato", FORMATOS), ("layout", LAYOUTS), ("tema", TEMAS)):
        if not isinstance(post.get(campo), str) or post[campo] not in opcoes:
            erros.append(f"{onde}: '{campo}' deve ser um de: {', '.join(opcoes)}")
    layout = LAYOUTS.get(post["layout"]) if isinstance(post.get("layout"), str) else None
    if not layout:
        return erros
    permitidos = {"formato", "layout", "tema", "fundo", *COMUNS, *layout}
    if post["layout"] == "lista":
        permitidos.add("itens")
    if post["layout"] == "titulo":
        permitidos |= {"arte", "imagem"}
    if post["layout"] == "pessoa":  # o logo sobe para o topo e a foto ocupa a base: não há rodapé
        permitidos = permitidos - {"rodape", "fundo"} | {"foto"}
    for campo in sorted(set(post) - permitidos):
        erros.append(f"{onde}: campo '{campo}' não existe no layout '{post['layout']}'")
    _textos(post, {**COMUNS, **layout}, onde, erros, COM_DESTAQUE)

    if post["layout"] == "lista":
        itens = post.get("itens")
        if not isinstance(itens, list) or not 2 <= len(itens) <= 4:
            erros.append(f"{onde}: 'itens' precisa ter de 2 a 4 itens")
        else:
            for i, item in enumerate(itens, 1):
                if not isinstance(item, dict) or set(item) - set(ITEM):
                    erros.append(f"{onde}: item {i} aceita só 'titulo' e 'texto'")
                else:
                    _textos(item, ITEM, f"{onde}, item {i}", erros)

    if post["layout"] == "pessoa":
        foto = post.get("foto")
        if post.get("tema") != "verde":
            erros.append(f"{onde}: o layout 'pessoa' só existe no tema verde")
        if not isinstance(foto, str) or len(foto) > 500 or not (base / foto).is_file():
            erros.append(f"{onde}: 'foto' precisa ser um arquivo existente")
        elif (base / foto).suffix.lower() not in (".png", ".webp") or not _tem_alfa(base / foto):
            erros.append(f"{onde}: 'foto' precisa ser um retrato recortado, com fundo transparente, em PNG ou WebP")

    fundo = post.get("fundo", "malha")
    if not isinstance(fundo, str) or fundo not in FUNDOS:
        erros.append(f"{onde}: 'fundo' deve ser um de: {', '.join(FUNDOS)}")
    elif fundo == "arcos" and post.get("tema") == "lima":
        erros.append(f"{onde}: o fundo de arcos só existe nos temas verde e papel")

    arte = post.get("arte", "nenhuma")
    if not isinstance(arte, str) or arte not in ARTES:
        erros.append(f"{onde}: 'arte' deve ser um de: {', '.join(ARTES)}")
    elif arte == "imagem":
        caminho = post.get("imagem")
        if not isinstance(caminho, str) or len(caminho) > 500 or not _imagem(post, base).is_file():
            erros.append(f"{onde}: 'imagem' precisa ser o nome de uma ilustração do kit ou um arquivo existente")
        elif _imagem(post, base).suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
            erros.append(f"{onde}: 'imagem' precisa ser PNG, JPG ou WebP")
        else:
            # Ilustração do kit só entra nos fundos em que foi aprovada (ilustracoes/index.json).
            achada = _ilustracao(_imagem(post, base))
            if achada and post.get("tema") in TEMAS and post["tema"] not in achada[1]["temas"]:
                erros.append(f"{onde}: a ilustração '{achada[0]}' só vale nos temas: {', '.join(achada[1]['temas'])}")
    elif "imagem" in post:
        erros.append(f"{onde}: 'imagem' só vale com \"arte\": \"imagem\"")
    return erros


def paginas(especificacao):
    """Um post solto vira uma página; um carrossel ({comum, paginas}) vira várias, numeradas."""
    if isinstance(especificacao, dict) and "paginas" in especificacao:
        comum, lista = especificacao.get("comum", {}), especificacao["paginas"]
        if set(especificacao) - {"comum", "paginas"} or not isinstance(comum, dict):
            raise ValueError("carrossel aceita só 'comum' (objeto) e 'paginas' (lista)")
        if not isinstance(lista, list) or not 2 <= len(lista) <= 10:
            raise ValueError("carrossel precisa ter de 2 a 10 páginas")
        if not all(isinstance(p, dict) for p in lista):
            raise ValueError("cada página do carrossel precisa ser um objeto JSON")
        lote = [({**comum, **p}, f"{i:02d}/{len(lista):02d}") for i, p in enumerate(lista, 1)]
        if any(post.get("formato") != lote[0][0].get("formato") for post, _ in lote):
            raise ValueError("todas as páginas do carrossel precisam do mesmo formato")
        return lote
    return [(especificacao, None)]


def _tem_alfa(arquivo):
    """Transparência pelo cabeçalho: PNG com canal alfa ou tRNS, WebP com alfa (VP8X ou VP8L)."""
    dados = arquivo.read_bytes()
    if dados[:8] == b"\x89PNG\r\n\x1a\n" and len(dados) > 25:
        return dados[25] in (4, 6) or b"tRNS" in dados[: max(dados.find(b"IDAT"), 0)]
    if dados[8:16] == b"WEBPVP8X" and len(dados) > 20:
        return bool(dados[20] & 0x10)
    return dados[8:16] == b"WEBPVP8L" and len(dados) > 24 and bool(dados[24] & 0x10)


def _navegador():
    for candidato in (os.environ.get("CHROME"), *NAVEGADORES):
        if candidato and shutil.which(candidato):
            return shutil.which(candidato)
    raise RuntimeError("Chromium ou Chrome não encontrado; instale um ou defina CHROME=/caminho/do/navegador")


class Navegador:
    """Chromium sem janela com post.html aberto, comandado pelo protocolo de depuração num pipe.

    O pipe (e não a captura de tela da linha de comando) deixa esperar o desenho terminar de
    verdade antes da foto: sem isso, um em cada cem posts saía incompleto com a máquina ocupada.
    """

    def __enter__(self):
        executavel = _navegador()
        self._processo = None
        self._perfil = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        entrada, self._envia = os.pipe()
        self._recebe, saida = os.pipe()
        self._id, self._sessao, self._resto, self._fila = 0, None, b"", []
        try:  # qualquer falha daqui em diante desfaz processo, descritores e perfil
            try:
                self._processo = subprocess.Popen(
                    [
                        executavel, "--headless=new", "--remote-debugging-pipe", f"--user-data-dir={self._perfil.name}",
                        "--no-sandbox",  # agentes costumam rodar como root ou em contêiner; a página é local e do próprio kit
                        "--hide-scrollbars", "--force-device-scale-factor=1", "--font-render-hinting=none",
                    ],
                    # O Chromium lê os comandos no descritor 3 e responde no 4.
                    pass_fds=(3, 4), preexec_fn=lambda: (os.dup2(entrada, 3), os.dup2(saida, 4)),
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            finally:
                os.close(entrada)
                os.close(saida)
            alvo = self._chamar("Target.createTarget", url="about:blank")["targetId"]
            self._sessao = self._chamar("Target.attachToTarget", targetId=alvo, flatten=True)["sessionId"]
            self._chamar("Page.enable")
            self._chamar("Page.navigate", url=(AQUI / "post.html").as_uri())
            while not self._carregou():
                self._ate(lambda m: m.get("method") == "Page.loadEventFired", "carregar post.html")
        except BaseException:
            self.__exit__()
            raise
        return self

    def __exit__(self, *_):
        if self._processo:
            try:  # fecha com educação para o perfil temporário poder ser apagado
                self._sessao = None
                self._chamar("Browser.close")
                self._processo.wait(timeout=10)
            except (RuntimeError, OSError, subprocess.TimeoutExpired):
                self._processo.kill()
                self._processo.wait()
        os.close(self._envia)
        os.close(self._recebe)
        self._perfil.cleanup()

    def _carregou(self):
        try:
            return self._avaliar("typeof desenhar") == "function"
        except RuntimeError:
            return False  # contexto trocado no meio da navegação

    def _ate(self, serve, etapa):
        """Devolve a próxima mensagem que serve, guardando as outras para quem vier depois."""
        for i, mensagem in enumerate(self._fila):
            if serve(mensagem):
                return self._fila.pop(i)
        while True:
            while b"\0" not in self._resto:
                if not select.select([self._recebe], [], [], 60)[0]:
                    raise RuntimeError(f"o navegador não respondeu em 60 s ({etapa})")
                pedaco = os.read(self._recebe, 1 << 20)
                if not pedaco:
                    raise RuntimeError("o navegador fechou antes de terminar")
                self._resto += pedaco
            bruto, self._resto = self._resto.split(b"\0", 1)
            mensagem = json.loads(bruto)
            if serve(mensagem):
                return mensagem
            self._fila.append(mensagem)

    def _chamar(self, metodo, **parametros):
        self._id += 1
        pedido = {"id": self._id, "method": metodo, "params": parametros}
        if self._sessao:
            pedido["sessionId"] = self._sessao
        os.write(self._envia, json.dumps(pedido).encode() + b"\0")
        resposta = self._ate(lambda m: m.get("id") == self._id, metodo)
        if "error" in resposta:
            raise RuntimeError(f"{metodo}: {resposta['error'].get('message')}")
        return resposta["result"]

    def _avaliar(self, expressao):
        """Roda JavaScript na página, esperando a promessa. Devolve o valor; falha vira RuntimeError."""
        saida = self._chamar("Runtime.evaluate", expression=expressao, awaitPromise=True, returnByValue=True)
        if "exceptionDetails" in saida:
            detalhe = saida["exceptionDetails"].get("exception", {})
            raise RuntimeError(detalhe.get("value") or detalhe.get("description") or "falha ao desenhar")
        return saida["result"].get("value")

    def fotografar(self, post):
        """Desenha o post. Devolve (bytes do PNG, None) ou (None, motivo da recusa)."""
        largura, altura = FORMATOS[post["formato"]]
        try:
            self._chamar("Emulation.setDeviceMetricsOverride", width=largura, height=altura, deviceScaleFactor=1, mobile=False)
            # Sem o "ok" da página não há foto: a tela ainda mostraria o post anterior.
            if self._avaliar(f"desenhar({json.dumps(post)})") != "ok":
                return None, "o navegador não confirmou o desenho"
            png = base64.b64decode(self._chamar("Page.captureScreenshot", format="png")["data"])
        except RuntimeError as erro:
            return None, str(erro)
        if struct.unpack(">II", png[16:24]) != (largura, altura):
            return None, f"o PNG não saiu em {largura}x{altura}"
        return png, None


def _interno(post, pagina, base):
    """Acrescenta ao post o que só o gerador sabe: a página do carrossel e a imagem resolvida."""
    interno = {**post, "_pagina": pagina}
    if post.get("arte") == "imagem":
        imagem = _imagem(post, base).resolve()
        interno["_imagem"] = imagem.as_uri()
        interno["_cartao"] = not _tem_alfa(imagem)  # imagem sem transparência entra num cartão arredondado
    if post["layout"] == "pessoa":
        foto = base / post["foto"]
        # Embutida (data:) em vez de file:, para a página poder ler os pixels e aparar a sobra transparente.
        tipo = "png" if foto.suffix.lower() == ".png" else "webp"
        interno["_foto"] = f"data:image/{tipo};base64,{base64.b64encode(foto.read_bytes()).decode()}"
    return interno


def gerar(arquivo, saida=None):
    """Valida e renderiza o JSON. Devolve (pngs gravados, erros).

    Com erro de validação ou de desenho, nenhum PNG é gravado. Só uma falha do sistema de
    arquivos no meio da troca final pode deixar um carrossel pela metade, e ela vira erro.
    """
    arquivo = Path(arquivo)
    try:
        lote = paginas(json.loads(arquivo.read_text(encoding="utf-8")))
    except (OSError, ValueError, RecursionError) as erro:
        return [], [f"{arquivo.name}: {erro}"]
    nomes = [f"página {n[:2]}" if n else "post" for _, n in lote]
    pasta = Path(saida) if saida else arquivo.parent
    provisorios = []
    try:
        erros = [e for (post, _), onde in zip(lote, nomes) for e in validar(post, arquivo.parent, onde)]
        if erros:
            return [], erros
        # Sem resolve() no nome final: um link plantado no destino é trocado pelo PNG, nunca seguido.
        destinos = [pasta.resolve() / f"{arquivo.stem}{'-' + n[:2] if n else ''}.png" for _, n in lote]
        entradas = {_imagem(post, arquivo.parent).resolve() for post, _ in lote if post.get("arte") == "imagem"}
        entradas |= {(arquivo.parent / post["foto"]).resolve() for post, _ in lote if post["layout"] == "pessoa"}
        if entradas & {d.resolve() for d in destinos} or any(d.is_dir() for d in destinos):
            return [], ["o PNG sairia por cima da imagem de entrada ou de uma pasta; use -o ou dê outro nome ao JSON"]
        prontos = []
        with Navegador() as navegador:
            for (post, pagina), onde in zip(lote, nomes):
                png, erro = navegador.fotografar(_interno(post, pagina, arquivo.parent))
                if erro:
                    return [], [f"{onde}: {erro}"]
                prontos.append(png)
        pasta.mkdir(parents=True, exist_ok=True)
        # Grava tudo em arquivos provisórios e só então troca: ou saem todos os PNGs, ou nenhum.
        for destino, png in zip(destinos, prontos):
            provisorio = destino.with_name(f".{destino.name}.{os.getpid()}.parcial")
            # O_EXCL: se já existe algo com esse nome (arquivo ou link), falha em vez de escrever por cima.
            with os.fdopen(os.open(provisorio, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o666), "wb") as gravacao:
                provisorios.append(provisorio)
                gravacao.write(png)
        for provisorio, destino in zip(provisorios, destinos):
            os.replace(provisorio, destino)
    except (RuntimeError, OSError) as erro:
        return [], [str(erro)]
    finally:
        for provisorio in provisorios:  # só o que esta execução criou
            try:
                provisorio.unlink(missing_ok=True)
            except OSError:
                pass
    return destinos, []


def main():
    argumentos = argparse.ArgumentParser(description="Gera posts da Nora em PNG a partir de um JSON.")
    argumentos.add_argument("json", nargs="+", help="arquivo(s) de especificação")
    argumentos.add_argument("-o", "--saida", help="pasta dos PNGs (padrão: a pasta do JSON)")
    opcoes = argumentos.parse_args()
    falhou = False
    for arquivo in opcoes.json:
        pngs, erros = gerar(arquivo, opcoes.saida)
        for png in pngs:
            print(png)
        for erro in erros:
            print(f"erro: {erro}", file=sys.stderr)
        falhou = falhou or bool(erros)
    sys.exit(1 if falhou else 0)


if __name__ == "__main__":
    main()
