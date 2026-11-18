#!/usr/bin/env python3
"""Prova do gerador de posts: python3 social/test_render.py"""
import json
import os
import re
import shutil
import tempfile
import unittest
from pathlib import Path

import render

RAIZ = render.AQUI.parent
EXEMPLOS = sorted((render.AQUI / "exemplos").glob("*.json"))
BASE = {"formato": "feed", "layout": "titulo", "tema": "papel", "titulo": "Título"}


def erros(**mudancas):
    return render.validar({**BASE, **mudancas}, render.AQUI / "exemplos")


def gerar(pasta, especificacao, nome="post"):
    arquivo = Path(pasta) / f"{nome}.json"
    arquivo.write_text(json.dumps(especificacao), encoding="utf-8")
    return render.gerar(arquivo)


class Validacao(unittest.TestCase):
    def test_post_minimo_passa(self):
        self.assertEqual(erros(), [])

    def test_acentos_e_cifrao_passam(self):
        self.assertEqual(erros(titulo="R$ 1 de lastro: ação, emissão e *câmbio*"), [])

    def test_recusa_valor_fora_do_conjunto_fechado(self):
        for campo, valor in (("tema", "preto"), ("formato", "banner"), ("layout", "poster"), ("arte", "foguete"),
                             ("cor", "#FF0000"), ("formato", []), ("layout", {}), ("arte", 3), ("semente", None)):
            self.assertTrue(erros(**{campo: valor}), campo)

    def test_recusa_texto_fora_da_voz_e_da_fonte(self):
        for titulo in ("Chegou 🚀", "x" * 111, "Um *destaque aberto", "****", "Bridge no ar!", "So­ft", "Neŉ"):
            self.assertTrue(erros(titulo=titulo), titulo)
        self.assertTrue(erros(selo="Duas\nlinhas"))
        itens = [{"titulo": "Com *destaque*"}, {"titulo": "Sem"}]
        self.assertTrue(erros(layout="lista", itens=itens))

    def test_campo_de_outro_layout_e_recusado(self):
        self.assertTrue(erros(numero="1:1"))
        self.assertTrue(erros(layout="numero", numero="1:1", arte="brs"))

    def test_fundo_de_arcos_so_no_verde_e_no_papel(self):
        for tema in ("verde", "papel"):
            self.assertEqual(erros(tema=tema, fundo="arcos"), [], tema)
        self.assertEqual(erros(fundo="malha"), [])
        self.assertTrue(erros(tema="lima", fundo="arcos"))
        self.assertTrue(erros(fundo="ondas"))
        self.assertTrue(erros(fundo=None))

    def test_pessoa_pede_foto_e_tema_verde(self):
        pessoa = {"formato": "horizontal", "layout": "pessoa", "tema": "verde", "nome": "Nome Sobrenome",
                  "cargo": "Founding Engineer", "foto": "retrato-exemplo.webp"}
        valida = lambda **mudancas: render.validar({**pessoa, **mudancas}, render.AQUI / "exemplos")
        self.assertEqual(valida(), [])
        # Entrada de pessoa: rótulo, nome com destaque em duas linhas, descrição, fecho, foto sem recorte.
        self.assertEqual(valida(selo="Angel Investor", nome="Nome Sobrenome\n*joins Nora.*", texto="Descrição",
                                fecho="More than *capital.*", foto="retrato-exemplo-fundo.webp"), [])
        sem_cargo = {campo: valor for campo, valor in pessoa.items() if campo != "cargo"}
        self.assertEqual(render.validar(sem_cargo, render.AQUI / "exemplos"), [])
        for mudanca in ({"tema": "papel"}, {"foto": "nao-existe.png"}, {"foto": None}, {"foto": "molde-spotlight.json"},
                        {"rodape": "nora.finance"}, {"titulo": "Título"}, {"arte": "brs"}, {"cargo": "x" * 29},
                        {"fundo": "arcos"}, {"fecho": "x" * 41}, {"nome": "Um *destaque aberto"}):
            self.assertTrue(valida(**mudanca), mudanca)
        self.assertTrue(erros(foto="retrato-exemplo.webp"))  # foto só existe no layout pessoa

    def test_titulo_com_arcos_nao_tem_rodape_e_aceita_logo_de_parceiro(self):
        logo = str(RAIZ / "logo" / "nora.svg")
        self.assertEqual(erros(tema="verde", fundo="arcos", parceiro=logo), [])
        self.assertEqual(erros(parceiro=logo), [])
        self.assertTrue(erros(tema="verde", fundo="arcos", rodape="nora.finance"))
        self.assertEqual(erros(rodape="nora.finance"), [])  # com malha o rodapé segue valendo
        self.assertTrue(erros(parceiro="nao-existe.svg"))
        self.assertTrue(erros(parceiro=str(RAIZ / "README.md")))
        self.assertTrue(erros(layout="numero", numero="1:1", parceiro=logo))

    def test_ilustracao_so_entra_no_fundo_aprovado(self):
        self.assertTrue(render.ILUSTRACOES)
        with tempfile.TemporaryDirectory() as pasta:
            for nome, regra in render.ILUSTRACOES.items():
                copia = str(shutil.copy(render.AQUI / "ilustracoes" / f"{nome}.webp", Path(pasta) / "outra.webp"))
                for tema in render.TEMAS:
                    for imagem in (nome, f"../ilustracoes/{nome}.webp", copia):  # pelo nome, pelo caminho e copiada
                        achou = erros(tema=tema, arte="imagem", imagem=imagem)
                        self.assertEqual(achou == [], tema in regra["temas"], f"{nome} em {tema}: {achou}")

    def test_simbolo_da_nora_nao_entra_sobre_os_arcos(self):
        for nome in ("nora-simbolo-brs", "nora-simbolo-3d"):
            self.assertEqual(erros(tema="verde", arte="imagem", imagem=nome), [])
            self.assertIn("não entra no fundo de arcos", "".join(erros(tema="verde", fundo="arcos", arte="imagem", imagem=nome)))
        self.assertEqual(erros(tema="verde", fundo="arcos", arte="imagem", imagem="brs-garantia"), [])

    def test_carrossel_tem_de_duas_a_dez_paginas_do_mesmo_formato(self):
        with self.assertRaises(ValueError):
            render.paginas({"paginas": [BASE]})
        with self.assertRaises(ValueError):
            render.paginas({"paginas": [BASE, {**BASE, "formato": "story"}]})

    def test_transparencia_e_lida_do_cabecalho(self):
        self.assertTrue(render._tem_alfa(render.AQUI / "ilustracoes" / "brs-cofre.webp"))
        self.assertTrue(render._tem_alfa(RAIZ / "logo" / "nora-256.png"))
        with tempfile.TemporaryDirectory() as pasta:
            cortado = Path(pasta) / "cortado.png"
            cortado.write_bytes(b"\x89PNG\r\n\x1a\n")
            self.assertFalse(render._tem_alfa(cortado))


class Render(unittest.TestCase):
    def test_exemplos_saem_no_tamanho_certo(self):
        self.assertTrue(EXEMPLOS)
        with tempfile.TemporaryDirectory() as pasta:
            for exemplo in EXEMPLOS:
                pngs, achou = render.gerar(exemplo, pasta)
                self.assertEqual(achou, [], exemplo.name)  # gerar já confere largura e altura
                self.assertTrue(pngs, exemplo.name)

    def test_retrato_e_aparado_ate_a_pessoa(self):
        # O retrato de exemplo tem sobra transparente em cima e dos lados e encosta na base.
        post = json.loads((render.AQUI / "exemplos" / "molde-spotlight.json").read_text(encoding="utf-8"))
        with render.Navegador() as navegador:
            _, erro = navegador.fotografar(render._interno(post, None, render.AQUI / "exemplos"))
            recorte = navegador._avaliar('document.querySelector(".retrato").style.objectViewBox')
        self.assertIsNone(erro)
        topo, direita, base, esquerda = map(int, re.findall(r"(\d+)px", recorte))
        self.assertTrue(topo and direita and esquerda, recorte)
        self.assertEqual(base, 0, recorte)

    def test_carrossel_com_arcos_mostra_a_numeracao_no_alto(self):
        pagina = {**BASE, "tema": "verde", "fundo": "arcos"}
        with render.Navegador() as navegador:
            _, erro = navegador.fotografar(render._interno(pagina, "01/02", RAIZ))
            numeracao = navegador._avaliar('document.querySelector(".rodape .mono").textContent')
            _, erro_solto = navegador.fotografar(render._interno(pagina, None, RAIZ))
            visivel = navegador._avaliar('getComputedStyle(document.querySelector(".rodape .mono")).visibility')
        self.assertIsNone(erro)
        self.assertIsNone(erro_solto)
        self.assertEqual(numeracao, "01/02")
        self.assertEqual(visivel, "hidden")  # peça solta: sem numeração, nada aparece

    def test_fundos_saem_um_por_tema_e_formato(self):
        with tempfile.TemporaryDirectory() as pasta:
            gravados = render.fundos(pasta)
            self.assertEqual(len(gravados), 2 * len(render.FORMATOS))
            for arquivo in gravados:
                self.assertEqual(arquivo.read_bytes()[:3], b"\xff\xd8\xff", arquivo.name)  # JPEG

    def test_mesma_semente_mesma_malha(self):
        # Compara a malha calculada, não os pixels: com a máquina ocupada o Chromium varia
        # alguns pixels em até 3 níveis, sem efeito visível.
        malhas = []
        for _ in range(2):
            with render.Navegador() as navegador:
                malhas.append([navegador._avaliar(f'malha("{tema}", "campanha")') for tema in render.TEMAS])
                outra = navegador._avaliar('malha("papel", "outra campanha")')
        self.assertEqual(malhas[0], malhas[1])
        self.assertNotEqual(malhas[0][0], outra)

    def test_so_o_campo_obrigatorio_cabe_em_todo_formato(self):
        minimos = (BASE, {**BASE, "arte": "brs"}, {**BASE, "layout": "numero", "numero": "1:1"},
                   {**BASE, "titulo": "Primeira frase. *Segunda em destaque.*"},
                   {"formato": "feed", "layout": "citacao", "tema": "verde", "citacao": "Fala.", "autor": "Nome"},
                   {**BASE, "formato": "paisagem", "layout": "numero", "numero": "R$ 1.000.000"},
                   {**BASE, "fundo": "arcos"}, {**BASE, "tema": "verde", "fundo": "arcos", "arte": "brs"},
                   {"formato": "feed", "layout": "pessoa", "tema": "verde", "nome": "Nome", "cargo": "Cargo",
                    "foto": str(render.AQUI / "exemplos" / "retrato-exemplo.webp")},
                   {"formato": "feed", "layout": "pessoa", "tema": "verde", "nome": "Nome",
                    "foto": str(render.AQUI / "exemplos" / "retrato-exemplo-fundo.webp")},
                   {**BASE, "tema": "verde", "fundo": "arcos", "parceiro": str(RAIZ / "logo" / "nora.svg")})
        with tempfile.TemporaryDirectory() as pasta:
            for i, post in enumerate(minimos):
                for formato in render.FORMATOS:
                    pngs, achou = gerar(pasta, {**post, "formato": formato}, f"{i}-{formato}")
                    self.assertEqual(achou, [], f"{post['layout']} em {formato}")
                    self.assertEqual(len(pngs), 1)

    def test_carrossel_do_guia_renderiza(self):
        guia = (RAIZ / "GUIA-DE-MARCA.md").read_text(encoding="utf-8")
        exemplo = re.search(r"```json\n(\{\n  \"comum\".*?)\n```", guia, re.S).group(1)
        with tempfile.TemporaryDirectory() as pasta:
            pngs, achou = gerar(pasta, json.loads(exemplo), "guia")
            self.assertEqual(achou, [])
            self.assertEqual([p.name for p in pngs], ["guia-01.png", "guia-02.png", "guia-03.png"])

    def test_texto_que_nao_cabe_e_recusado_sem_gerar_png(self):
        estouros = (
            {**BASE, "formato": "quadrado", "arte": "brs", "titulo": "Palavra " * 13, "texto": "Frase longa. " * 16},
            {**BASE, "layout": "numero", "numero": "W" * 12},
            {**BASE, "titulo": "W" * 60},  # palavra sem quebra, mais larga que a área útil
            {"comum": {**BASE, "rodape": "x" * 40}, "paginas": [{}, {}]},  # rodapé + numeração encosta no logo
            {**BASE, "chamada": "W" * 28},  # botão mais largo que a área útil
        )
        with tempfile.TemporaryDirectory() as pasta:
            for i, post in enumerate(estouros):
                pngs, achou = gerar(pasta, post, f"estoura-{i}")
                self.assertEqual(pngs, [], post)
                self.assertIn("não cabe", achou[0])
            self.assertEqual(list(Path(pasta).glob("*.png")), [])

    def test_carrossel_com_pagina_recusada_nao_deixa_png(self):
        with tempfile.TemporaryDirectory() as pasta:
            ruim = {**BASE, "formato": "quadrado", "arte": "brs", "titulo": "Palavra " * 13, "texto": "Frase longa. " * 16}
            pngs, achou = gerar(pasta, {"paginas": [{**BASE, "formato": "quadrado"}, ruim]})
            self.assertEqual(pngs, [])
            self.assertIn("página 02", achou[0])
            self.assertEqual(list(Path(pasta).glob("*.png")), [])

    def test_png_nunca_sai_por_cima_da_imagem_de_entrada(self):
        with tempfile.TemporaryDirectory() as pasta:
            imagem = Path(shutil.copy(RAIZ / "logo" / "nora-256.png", Path(pasta) / "post.png"))
            antes = imagem.read_bytes()
            pngs, achou = gerar(pasta, {**BASE, "arte": "imagem", "imagem": "post.png"})
            self.assertEqual(pngs, [])
            self.assertIn("por cima", achou[0])
            self.assertEqual(imagem.read_bytes(), antes)

    def test_link_no_destino_e_trocado_e_nao_seguido(self):
        with tempfile.TemporaryDirectory() as pasta:
            alvo = Path(pasta) / "nao-toque.txt"
            alvo.write_text("intacto", encoding="utf-8")
            (Path(pasta) / "post.png").symlink_to(alvo)
            pngs, achou = gerar(pasta, BASE)
            self.assertEqual(achou, [])
            self.assertEqual(alvo.read_text(encoding="utf-8"), "intacto")
            self.assertFalse(pngs[0].is_symlink())
            self.assertEqual(list(Path(pasta).glob(".*.parcial")), [])

    def test_link_no_nome_provisorio_nao_e_seguido(self):
        with tempfile.TemporaryDirectory() as pasta:
            alvo = Path(pasta) / "nao-toque.txt"
            alvo.write_text("intacto", encoding="utf-8")
            (Path(pasta) / f".post.png.{os.getpid()}.parcial").symlink_to(alvo)
            pngs, achou = gerar(pasta, BASE)
            self.assertEqual(pngs, [])
            self.assertTrue(achou)
            self.assertEqual(alvo.read_text(encoding="utf-8"), "intacto")

    def test_saida_invalida_vira_erro_e_nao_excecao(self):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "post.json"
            arquivo.write_text(json.dumps(BASE), encoding="utf-8")
            pngs, achou = render.gerar(arquivo, arquivo)  # -o apontando para um arquivo
            self.assertEqual(pngs, [])
            self.assertTrue(achou)

    @unittest.skipIf(os.geteuid() == 0, "root lê qualquer arquivo")
    def test_imagem_sem_permissao_vira_erro_e_nao_excecao(self):
        with tempfile.TemporaryDirectory() as pasta:
            imagem = Path(shutil.copy(RAIZ / "logo" / "nora-256.png", Path(pasta) / "trancada.png"))
            imagem.chmod(0)
            pngs, achou = gerar(pasta, {**BASE, "arte": "imagem", "imagem": "trancada.png"})
            self.assertEqual(pngs, [])
            self.assertTrue(achou)

    def test_navegador_que_nao_responde_nao_deixa_processo_nem_descritor(self):
        abertos = lambda: len(os.listdir("/proc/self/fd")) if os.path.isdir("/proc/self/fd") else 0
        antes, real = abertos(), os.environ.get("CHROME")
        os.environ["CHROME"] = shutil.which("true")  # "navegador" que sai sem responder
        try:
            with tempfile.TemporaryDirectory() as pasta:
                pngs, achou = gerar(pasta, BASE)
        finally:
            os.environ.pop("CHROME") if real is None else os.environ.update(CHROME=real)
        self.assertEqual(pngs, [])
        self.assertTrue(achou)
        self.assertEqual(abertos(), antes)


if __name__ == "__main__":
    unittest.main()
