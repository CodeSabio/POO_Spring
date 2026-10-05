"""Jogo da Cobrinha (Snake) no terminal, usando apenas a biblioteca padrão.

Controles: setas ou WASD para mover, P para pausar, Q para sair.
Execute com: python3 jogo_cobrinha.py
"""
import curses
import random

DIRECOES = {
    curses.KEY_UP: (-1, 0), ord("w"): (-1, 0),
    curses.KEY_DOWN: (1, 0), ord("s"): (1, 0),
    curses.KEY_LEFT: (0, -1), ord("a"): (0, -1),
    curses.KEY_RIGHT: (0, 1), ord("d"): (0, 1),
}


def nova_comida(altura, largura, cobra):
    livres = [(y, x) for y in range(1, altura - 1) for x in range(1, largura - 1)
              if (y, x) not in cobra]
    return random.choice(livres)


def jogar(tela):
    curses.curs_set(0)
    tela.keypad(True)
    altura, largura = tela.getmaxyx()
    altura, largura = min(altura, 24), min(largura, 60)
    janela = curses.newwin(altura, largura, 0, 0)
    janela.keypad(True)

    while True:
        cobra = [(altura // 2, largura // 4 + i) for i in range(3, 0, -1)]
        direcao = (0, 1)
        comida = nova_comida(altura, largura, cobra)
        pontos = 0
        pausado = False

        while True:
            janela.timeout(max(40, 130 - pontos * 3))
            tecla = janela.getch()
            if tecla in (ord("q"), ord("Q")):
                return
            if tecla in (ord("p"), ord("P")):
                pausado = not pausado
            if pausado:
                continue
            if tecla in DIRECOES:
                nova = DIRECOES[tecla]
                if (nova[0] + direcao[0], nova[1] + direcao[1]) != (0, 0):
                    direcao = nova

            cabeca = (cobra[0][0] + direcao[0], cobra[0][1] + direcao[1])
            if (cabeca in cobra or cabeca[0] in (0, altura - 1)
                    or cabeca[1] in (0, largura - 1)):
                break
            cobra.insert(0, cabeca)
            if cabeca == comida:
                pontos += 1
                comida = nova_comida(altura, largura, cobra)
            else:
                cobra.pop()

            janela.erase()
            janela.border()
            janela.addstr(0, 2, f" Pontos: {pontos} ")
            janela.addch(comida[0], comida[1], "*")
            for i, (y, x) in enumerate(cobra):
                janela.addch(y, x, "O" if i == 0 else "o")
            janela.refresh()

        janela.timeout(-1)
        janela.addstr(altura // 2 - 1, largura // 2 - 6, " FIM DE JOGO ")
        janela.addstr(altura // 2, largura // 2 - 10, f" Pontos: {pontos} ".center(20))
        janela.addstr(altura // 2 + 1, largura // 2 - 14, " R: jogar de novo | Q: sair ")
        janela.refresh()
        while True:
            tecla = janela.getch()
            if tecla in (ord("q"), ord("Q")):
                return
            if tecla in (ord("r"), ord("R")):
                break


if __name__ == "__main__":
    curses.wrapper(jogar)
