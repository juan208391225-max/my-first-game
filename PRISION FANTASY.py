import pygame
import sys
import math
import os
import random

pygame.init()

print("---------- CONFIGURACION ----------")

print("---------- 1. OLEADAS: CUANTOS ENEMIGOS SALEN, CUANTOS A LA VEZ Y QUE TAN RAPIDO ----------")
ZONAS = [
    {"nombre": "Bosque", "casillas": (0, 0, 26, 23), "color": (255, 170, 60), "cerrada": True, "destino": (8, 12), "distancia_aparicion": 800},
    {"nombre": "Ruinas", "casillas": (27, 11, 37, 21), "color": (235, 70, 110), "cerrada": False, "destino": (30, 16), "distancia_aparicion": 450},
]
OLEADA_ENEMIGOS_BASE = 8
OLEADA_ENEMIGOS_MAS = 6
OLEADA_MAX_VIVOS_BASE = 3
OLEADA_MAX_VIVOS_MAS = 2
OLEADA_INTERVALO_BASE = 3.0
OLEADA_INTERVALO_MENOS = 0.6
OLEADA_INTERVALO_MIN = 0.8
OLEADA_ESPERA = 3.0
ENEMIGOS_OLEADA_AGRESIVOS = True
ENEMIGO_TIEMPO_APARICION = 0.6
OLEADA_MARGEN_ENTRADA = 40

print("---------- 2. GOBLIN: VIDA, DANO, VELOCIDAD Y COMPORTAMIENTO ----------")
VIDA_ENEMIGO = 60
RETROCESO_ENEMIGO = 35
TIEMPO_RETROCESO = 0.35

VEL_ENEMIGO_VAGAR = 60
VEL_ENEMIGO_PERSEGUIR = 190
RADIO_DETECCION = 380
RADIO_PERDER = 650
RADIO_VAGAR = 260
DANO_ENEMIGO = 12
ENEMIGO_PREPARAR = 0.40
ENEMIGO_GOLPE = 0.15
ENEMIGO_RECUPERAR = 0.35
ENEMIGO_ENFRIAMIENTO = 0.8
ENEMIGO_UMBRAL_GIRO = 14
ENEMIGO_MIRA_A_LA_DERECHA = False
DANO_POR_CONTACTO = False

print("---------- 3. JUGADOR: VIDA, VELOCIDAD, SALTO Y ATAQUES ----------")
VIDA_JUGADOR = 100
VEL_JUGADOR_CAMINAR = 300
VEL_JUGADOR_CORRER = 520
VEL_JUGADOR_AGACHADO = 130
VEL_JUGADOR_RODAR = 620
FUERZA_SALTO = 820
GRAVEDAD = 2400
GRAVEDAD_GOLPE_ABAJO = 3800
INVULNERABLE_TRAS_GOLPE = 1.2
ENFRIAMIENTO_ATAQUE = 0.2
TIEMPO_COMBO = 0.5
ENFRIAMIENTO_GIRO = 5.0
TIEMPO_ESPADA_EN_MANO = 3.0
DANO_ATAQUE = {
    "atacar": 15,
    "atacar2": 20,
    "atacar_dash": 25,
    "agachado_atacar": 12,
    "atacar_abajo": 30,
    "atacar_giro": 40,
}

print("---------- 4. TAMANOS: ESCALAS Y HITBOXES ----------")
ESCALA_GLOBAL = 1
ESCALA_JUGADOR = 2
ESCALA_ENEMIGOS = 5
ESCALA_OBJETOS = 1
escala_jugador = ESCALA_JUGADOR * ESCALA_GLOBAL
escala_enemigos = ESCALA_ENEMIGOS * ESCALA_GLOBAL
escala_objetos = ESCALA_OBJETOS * ESCALA_GLOBAL


print("---------- HITBOXES ----------")
HITBOX_JUGADOR_PIES = (20, 10)
HITBOX_JUGADOR_CUERPO = (28, 62)
HITBOX_JUGADOR_CUERPO_AGACHADO = (28, 32)
HITBOX_ENEMIGO_PIES = (9, 5)
HITBOX_ENEMIGO_CUERPO = (11, 14)
HITBOX_ENEMIGO_ATAQUE = (9, 6)
HITBOX_ENEMIGO_ATAQUE_POS = (5, 10)
HITBOX_ATAQUES = {
    "atacar": (80, 60),
    "atacar2": (80, 60),
    "atacar_dash": (75, 45),
    "agachado_atacar": (55, 30),
    "atacar_abajo": (65, 55),
    "atacar_giro": (130, 75),
}
HITBOX_ATAQUE_POS = {
    "atacar": (5, 55),
    "atacar2": (5, 60),
    "atacar_dash": (5, 30),
    "agachado_atacar": (5, 30),
    "atacar_abajo": (5, 30),
    "atacar_giro": (5, 30),
}


print("---------- 5. CAMARA Y MIRA ----------")
CAMARA_SUAVIDAD = 0
CAMARA_LIMITADA = True


print("---------- 6. MAPA ----------")
ESCALA_TILES = 4
TAM_TILE = 32 * ESCALA_TILES
MAPA = [
    "TtttttttttttttttttttttttttttttttttttttTt",
    "tTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTtT",
    "Tt......m...Tt........t...RTT.T.......Tt",
    "tT..............~~~~~....t.....T....t.tT",
    "Tt.T..y.T..~~~~~~~~~~~~~..R..m.y.y.M..Tt",
    "tT...M...t.~~~~~~~~~~~~~~..M....T.....tT",
    "Tt....mR...~~~~~~~~~~~~~~~...m..m....TTt",
    "tT.......R..~~~~~~~~~~~~~~~..T.....mT.tT",
    "TtT..y.......~~~~~~~~~~~~~~..yT...t...Tt",
    "tT.T............~~~~~~~~~~~...........tT",
    "Tt...................~~~~~............Tt",
    "tT.t...............t.......##..#######tT",
    "Ttt...::P::::::.....T..R...#F__F#B__C#Tt",
    "tT....::::L::::.m.......y..#____D_b__#tT",
    "Tt............:R..M........#_b__#____#Tt",
    "tTT.t.........:::::::::::::#____#J__F#tT",
    "Tt.T.t.yt.....:::::::::::::D____###D##Tt",
    "tT.m.RT.R.........t.......:#____#rrrr#tT",
    "Tt.....m....M.........T....#__b_#CrbC#Tt",
    "tTttR..yy.......T..........#____#rprr#tT",
    "Tt..m....m...t......T......#BB_J#FrCF#Tt",
    "tTy.....m..y.T.....ty..m...###########tT",
    "TtTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTt",
    "tTtttttttttttttttttttttttttttttttttttttT",
]

MUNDO_ANCHO = len(MAPA[0]) * TAM_TILE
MUNDO_ALTO = len(MAPA) * TAM_TILE

print("---------- FIN DE LA CONFIGURACION ----------")


print("---------- ESTADO INTERNO, COLORES Y FUENTES ----------")
blanco = (255, 255, 255)
negro = (0, 0, 0)
rojo = (255, 0, 0)
azul = (0, 0, 255)
verde = (90, 200, 140)
amarillo = (255, 220, 80)
width = 1549
height = 900
RUN = True
JUGAR = False
AJUSTES = False
MUSICA = False
PAUSA = False
CONTROLES = False
MOSTRAR_HITBOX = False
CURSOR_BLOQUEADO = False
camara = pygame.Vector2(0, 0)
mapa = None
partida = None
captura = None
modo = None
menu_font = pygame.font.Font(None, 45)
titulo_font = pygame.font.Font(None, 110)
fuente_peq = pygame.font.Font(None, 34)
reloj = pygame.time.Clock()

print("---------- MUSICA: LISTA DE REPRODUCCION ----------")
MUSICA_EXT = (".mp3", ".ogg", ".wav")


def buscar_canciones():
    rutas = []
    if os.path.isdir("musica"):
        for n in sorted(os.listdir("musica")):
            if n.lower().endswith(MUSICA_EXT):
                rutas.append(os.path.join("musica", n))
    return rutas


canciones = buscar_canciones()
activas = {c: True for c in canciones}
actual = -1
scroll = 0
FILAS_VISIBLES = 7

ajustes = {"musica": 0.5, "efectos": 0.5, "pantalla_completa": True, "mostrar_fps": False}
sliders = {
    "musica": pygame.Rect(800, 294, 400, 12),
    "efectos": pygame.Rect(800, 374, 400, 12),
}
interruptores = {
    "pantalla_completa": pygame.Rect(800, 438, 120, 48),
    "mostrar_fps": pygame.Rect(800, 518, 120, 48),
}
arrastrando = None

print("---------- VENTANA ----------")

game_surface = pygame.Surface((width, height))
ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("PRISION FANTASY")


print("---------- FONDO PERSONALIZADO ----------")
def cargar_fondo():
    for ruta in ("fondo.png", "fondo.jpg", "fondo.jpeg"):
        if os.path.exists(ruta):
            img = pygame.image.load(ruta).convert()
            return pygame.transform.smoothscale(img, (width, height))
    s = pygame.Surface((width, height))
    for y in range(height):
        t = y / height
        pygame.draw.line(s, (int(20 + 30 * t), int(15 + 10 * t), int(50 + 60 * t)), (0, y), (width, y))
    return s


fondo_menu = cargar_fondo()
velo = pygame.Surface((width, height), pygame.SRCALPHA)
velo.fill((0, 0, 0, 120))

opciones = []
for texto, y, valor in [
    ("jugar", 390, "jugar"),
    ("controles", 465, "controles"),
    ("ajustes", 540, "ajustes"),
    ("salir", 615, "salir"),
]:
    rect = pygame.Rect(0, 0, 340, 62)
    rect.center = (width // 2, y)
    opciones.append({"texto": texto, "rect": rect, "modo": valor})

boton_canciones = pygame.Rect(0, 0, 380, 56)
boton_canciones.center = (width // 2, 620)
boton_anterior = pygame.Rect(0, 0, 260, 56)
boton_anterior.center = (width // 2 - 200, 690)
boton_siguiente = pygame.Rect(0, 0, 260, 56)
boton_siguiente.center = (width // 2 + 200, 690)
boton_volver_musica = pygame.Rect(0, 0, 260, 56)
boton_volver_musica.center = (width // 2, 780)
boton_volver_controles = pygame.Rect(0, 0, 260, 56)
boton_volver_controles.center = (width // 2, 810)

opciones_pausa = []
for texto, y, valor in [
    ("reanudar", 400, "reanudar"),
    ("controles", 470, "controles"),
    ("ajustes", 540, "ajustes"),
    ("menu principal", 610, "menu"),
]:
    rect = pygame.Rect(0, 0, 400, 62)
    rect.center = (width // 2, y)
    opciones_pausa.append({"texto": texto, "rect": rect, "modo": valor})

print("------------CLASES U OBJETOS------------")

print("---------- CLASES DEL MAPA ----------")
class Prop:
    def __init__(self, frames, pie, colision=None, fps=0):
        self.frames = frames
        self.fps = fps
        self.pie = pie
        self.solido = colision is not None
        ancho, alto = colision if colision else (1, 1)
        self.rect = pygame.Rect(0, 0, int(ancho), int(alto))
        self.rect.midbottom = pie

    def dibujar(self, superficie, cam=(0, 0)):
        if self.fps and len(self.frames) > 1:
            imagen = self.frames[int(pygame.time.get_ticks() / 1000 * self.fps) % len(self.frames)]
        else:
            imagen = self.frames[0]
        superficie.blit(imagen, imagen.get_rect(midbottom=(self.pie[0] - cam[0], self.pie[1] - cam[1])))


class Mapa:
    SUELOS = {
        "bosque": ([(14, 1), (15, 2), (15, 3), (15, 4), (14, 2), (14, 3)], [60, 10, 10, 10, 5, 5]),
        "camino": ([(9, 2), (9, 3), (9, 4)], [1, 1, 1]),
        "losa": ([(10, 2), (10, 3), (10, 4)], [1, 1, 1]),
        "losa_roja": ([(12, 2), (12, 3), (12, 4)], [1, 1, 1]),
    }
    TERRENOS = {".": "bosque", ":": "camino", "_": "losa", "r": "losa_roja"}
    MURO_SUPERIOR = (3, 1)
    MURO_FRENTE = ([(3, 2), (3, 3)], [3, 1])
    OBJETOS = {
        "T": ([(25, 4)], 2, (12, 11)),
        "t": ([(26, 3)], 1, (9, 9)),
        "y": ([(26, 1), (26, 2)], 1, (6, 6)),
        "R": ([(19, 1), (19, 2)], 1, (20, 11)),
        "M": ([(21, 2)], 1, (10, 7)),
        "L": ([(18, 7)], 1, (20, 11)),
        "C": ([(18, 1)], 1, (20, 11)),
        "B": ([(18, 5)], 1, (16, 11)),
        "J": ([(18, 3)], 1, (16, 11)),
    }
    DECORADOS = {"m": [(21, 1)], "b": [(22, 1), (22, 2)], "p": [(17, 15)], "D": [(17, 4)]}
    BRASERO = 2

    def __init__(self, plano):
        self.plano = plano
        self.filas = len(plano)
        self.cols = len(plano[0])
        assert all(len(f) == self.cols for f in plano), "todas las filas del plano deben tener el mismo largo"
        for base in (os.getcwd(), os.path.dirname(os.path.abspath(__file__))):
            carpeta = os.path.join(base, "mapa")
            if os.path.isdir(carpeta):
                break
        else:
            print("No encuentro la carpeta 'mapa' junto a este archivo (descomprime mapa.zip).")
            pygame.quit()
            sys.exit()
        self.hoja_tiles = pygame.image.load(os.path.join(carpeta, "tiles.png")).convert_alpha()
        self.hoja_auto = pygame.image.load(os.path.join(carpeta, "autotiles.png")).convert_alpha()
        self.hoja_anim = pygame.image.load(os.path.join(carpeta, "animated-tiles.png")).convert_alpha()
        self._cache = {}
        self.suelo = [[[] for _ in range(self.cols)] for _ in range(self.filas)]
        self.terreno_solido = [[False] * self.cols for _ in range(self.filas)]
        self.bloqueada = [[False] * self.cols for _ in range(self.filas)]
        self.bloquea_vista = [[False] * self.cols for _ in range(self.filas)]
        self.props = []
        self.solidos_en = {}
        self.inicio = (self.cols * TAM_TILE // 2, self.filas * TAM_TILE // 2)
        self._agua = self._autotiles(1)
        self._construir()

    def pieza(self, fila, col, alto=1):
        clave = (fila, col, alto)
        if clave not in self._cache:
            img = self.hoja_tiles.subsurface(((col - 1) * 32, (fila - 1) * 32, 32, 32 * alto)).copy()
            self._cache[clave] = escalar_imagen(img, ESCALA_TILES)
        return self._cache[clave]

    @staticmethod
    def _firma(tile):
        def opaco(x, y):
            return tile.get_at((x, y)).a > 0
        n, e, s, w = opaco(16, 0), opaco(31, 16), opaco(16, 31), opaco(0, 16)
        def esquina(x0, y0, lados):
            if not all(lados):
                return False
            return all(tile.get_at((x, y)).a > 0 for y in range(y0, y0 + 6) for x in range(x0, x0 + 6))
        return (n, e, s, w, esquina(0, 0, (n, w)), esquina(26, 0, (n, e)), esquina(0, 26, (s, w)), esquina(26, 26, (s, e)))

    def _autotiles(self, fila0):
        piezas = {}
        for f in range(4):
            for c in range(12):
                tile = self.hoja_auto.subsurface((c * 32, (fila0 - 1 + f) * 32, 32, 32)).copy()
                if pygame.mask.from_surface(tile).count() == 0:
                    continue
                piezas.setdefault(self._firma(tile), escalar_imagen(tile, ESCALA_TILES))
        return piezas

    def _dentro(self, x, y):
        return 0 <= x < self.cols and 0 <= y < self.filas

    def _terreno_de(self, x, y):
        ch = self.plano[y][x]
        if ch in self.TERRENOS:
            return self.TERRENOS[ch]
        if ch == "D":
            return "losa"
        votos = {}
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if self._dentro(x + dx, y + dy) and self.plano[y + dy][x + dx] in self.TERRENOS:
                    t = self.TERRENOS[self.plano[y + dy][x + dx]]
                    votos[t] = votos.get(t, 0) + 1
        return max(votos, key=votos.get) if votos else "bosque"

    def _frames_brasero(self):
        frames = []
        for c in range(self.hoja_anim.get_width() // 32):
            img = self.hoja_anim.subsurface((c * 32, (self.BRASERO - 1) * 32, 32, 32)).copy()
            if pygame.mask.from_surface(img).count() > 0:
                frames.append(escalar_imagen(img, ESCALA_TILES))
        return frames

    def _construir(self):
        rng = random.Random(7)
        T = TAM_TILE
        def agua(x, y):
            return not self._dentro(x, y) or self.plano[y][x] == "~"
        for y in range(self.filas):
            for x in range(self.cols):
                ch = self.plano[y][x]
                capas = self.suelo[y][x]
                centro = ((x + 0.5) * T, (y + 0.5) * T)
                pie = ((x + 0.5) * T, (y + 1) * T - 2 * ESCALA_TILES)
                if ch == "#":
                    abajo = self.plano[y + 1][x] if self._dentro(x, y + 1) else "."
                    if abajo == "#":
                        capas.append(self.pieza(*self.MURO_SUPERIOR))
                    else:
                        opciones, pesos = self.MURO_FRENTE
                        capas.append(self.pieza(*rng.choices(opciones, pesos)[0]))
                    self.terreno_solido[y][x] = self.bloqueada[y][x] = self.bloquea_vista[y][x] = True
                    continue
                opciones, pesos = self.SUELOS[self._terreno_de(x, y)] if ch != "~" else self.SUELOS["bosque"]
                capas.append(self.pieza(*rng.choices(opciones, pesos)[0]))
                if ch == "~":
                    n, e, s, w = agua(x, y - 1), agua(x + 1, y), agua(x, y + 1), agua(x - 1, y)
                    firma = (n, e, s, w, n and w and agua(x - 1, y - 1), n and e and agua(x + 1, y - 1),
                             s and w and agua(x - 1, y + 1), s and e and agua(x + 1, y + 1))
                    capas.append(self._agua.get(firma) or self._agua[(True,) * 8])
                    self.terreno_solido[y][x] = self.bloqueada[y][x] = True
                elif ch in self.DECORADOS:
                    capas.append(self.pieza(*rng.choice(self.DECORADOS[ch])))
                elif ch in self.OBJETOS:
                    piezas, alto, (cw, chh) = self.OBJETOS[ch]
                    fila, col = rng.choice(piezas)
                    prop = Prop([self.pieza(fila, col, alto)], pie, (cw * ESCALA_TILES, chh * ESCALA_TILES))
                    self.props.append(prop)
                    self.solidos_en.setdefault((y, x), []).append(prop)
                    self.bloqueada[y][x] = True
                elif ch == "F":
                    prop = Prop(self._frames_brasero(), pie, (14 * ESCALA_TILES, 9 * ESCALA_TILES), fps=8)
                    self.props.append(prop)
                    self.solidos_en.setdefault((y, x), []).append(prop)
                    self.bloqueada[y][x] = True
                elif ch == "P":
                    self.inicio = (centro[0], centro[1] + 10)

    def dibujar_suelo(self, superficie, cam):
        T = TAM_TILE
        superficie.fill((14, 18, 18))
        c0, c1 = max(0, cam[0] // T), min(self.cols - 1, (cam[0] + width) // T)
        f0, f1 = max(0, cam[1] // T), min(self.filas - 1, (cam[1] + height) // T)
        for f in range(f0, f1 + 1):
            for c in range(c0, c1 + 1):
                x, y = c * T - cam[0], f * T - cam[1]
                for capa in self.suelo[f][c]:
                    superficie.blit(capa, (x, y))

    def props_visibles(self, cam):
        x0, x1 = cam[0] - TAM_TILE, cam[0] + width + TAM_TILE
        y0, y1 = cam[1], cam[1] + height + 2 * TAM_TILE
        return [p for p in self.props if x0 <= p.pie[0] <= x1 and y0 <= p.pie[1] <= y1]

    def dibujar_colisiones(self, superficie, cam):
        T = TAM_TILE
        for f in range(max(0, cam[1] // T), min(self.filas, (cam[1] + height) // T + 1)):
            for c in range(max(0, cam[0] // T), min(self.cols, (cam[0] + width) // T + 1)):
                if self.terreno_solido[f][c]:
                    pygame.draw.rect(superficie, (255, 40, 40), (c * T - cam[0], f * T - cam[1], T, T), 1)
        for p in self.props_visibles(cam):
            if p.solido:
                pygame.draw.rect(superficie, (255, 160, 0), p.rect.move(-cam[0], -cam[1]), 2)

    def celdas_alcanzables(self, inicio, limite):
        c0, f0, c1, f1 = limite
        vistas = {inicio}
        cola = [inicio]
        for c, f in cola:
            for dc, df in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nc, nf = c + dc, f + df
                if c0 <= nc <= c1 and f0 <= nf <= f1 and (nc, nf) not in vistas and not self.bloqueada[nf][nc]:
                    vistas.add((nc, nf))
                    cola.append((nc, nf))
        return vistas

    def choca(self, rect):
        T = TAM_TILE
        if rect.left < 0 or rect.top < 0 or rect.right > self.cols * T or rect.bottom > self.filas * T:
            return True
        for f in range(rect.top // T, (rect.bottom - 1) // T + 1):
            for c in range(rect.left // T, (rect.right - 1) // T + 1):
                if self.terreno_solido[f][c]:
                    return True
                for p in self.solidos_en.get((f, c), ()):
                    if rect.colliderect(p.rect):
                        return True
        return False

    def hay_vista(self, a, b):
        T = TAM_TILE
        pasos = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) // 32))
        for i in range(1, pasos):
            x = a[0] + (b[0] - a[0]) * i / pasos
            y = a[1] + (b[1] - a[1]) * i / pasos
            c, f = int(x // T), int(y // T)
            if self._dentro(c, f) and self.bloquea_vista[f][c]:
                return False
        return True

    def paso_libre(self, a, b, ancho, alto):
        pasos = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) // 16))
        caja = pygame.Rect(0, 0, int(ancho), int(alto))
        for i in range(pasos + 1):
            caja.center = (a[0] + (b[0] - a[0]) * i / pasos, a[1] + (b[1] - a[1]) * i / pasos)
            if self.choca(caja):
                return False
        return True

    def camino(self, a, b):
        T = TAM_TILE
        ini = (min(self.filas - 1, max(0, int(a[1] // T))), min(self.cols - 1, max(0, int(a[0] // T))))
        fin = (min(self.filas - 1, max(0, int(b[1] // T))), min(self.cols - 1, max(0, int(b[0] // T))))
        if ini == fin:
            return [b]
        previo = {ini: None}
        cola = [ini]
        for f, c in cola:
            if (f, c) == fin:
                break
            for df, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nf, nc = f + df, c + dc
                if self._dentro(nc, nf) and (nf, nc) not in previo and (not self.bloqueada[nf][nc] or (nf, nc) == fin):
                    previo[(nf, nc)] = (f, c)
                    cola.append((nf, nc))
        if fin not in previo:
            return []
        ruta, nodo = [], fin
        while nodo != ini:
            ruta.append(((nodo[1] + 0.5) * T, (nodo[0] + 0.5) * T))
            nodo = previo[nodo]
        ruta.reverse()
        ruta[-1] = tuple(b)
        return ruta


class Oleadas:
    def __init__(self, zonas):
        T = TAM_TILE
        self.zonas = []
        for nivel, z in enumerate(zonas, 1):
            c0, f0, c1, f1 = z["casillas"]
            dc, df = z["destino"]
            libres = mapa.celdas_alcanzables((dc, df), (c0, f0, c1, f1))
            self.zonas.append({
                "nivel": nivel, "nombre": z["nombre"], "color": z["color"], "cerrada": z.get("cerrada", True),
                "rect": pygame.Rect(c0 * T, f0 * T, (c1 - c0 + 1) * T, (f1 - f0 + 1) * T),
                "destino": ((dc + 0.5) * T, (df + 0.5) * T),
                "dist": z.get("distancia_aparicion", 600),
                "total": z.get("enemigos", OLEADA_ENEMIGOS_BASE + OLEADA_ENEMIGOS_MAS * (nivel - 1)),
                "max_vivos": z.get("max_vivos", OLEADA_MAX_VIVOS_BASE + OLEADA_MAX_VIVOS_MAS * (nivel - 1)),
                "intervalo": z.get("intervalo", max(OLEADA_INTERVALO_MIN, OLEADA_INTERVALO_BASE - OLEADA_INTERVALO_MENOS * (nivel - 1))),
                "puntos": [((c + 0.5) * T, (f + 1) * T - 3 * ESCALA_TILES) for c, f in sorted(libres)],
                "estado": "pendiente",
                "generados": 0, "matados": 0, "t_prep": 0.0, "t_spawn": 0.0,
            })
        self.t = 0.0
        self.aviso, self.t_aviso = [], 0.0
        self.t_barrera = 0.0
        self.objetivo_flecha, self.t_ruta = None, -1.0
        self._vinetas = {}

    @property
    def actual(self):
        for z in self.zonas:
            if z["estado"] != "completada":
                return z
        return None

    @property
    def victoria(self):
        return self.actual is None

    def _aviso(self, lineas, segundos=3.0):
        self.aviso, self.t_aviso = lineas, segundos

    def bloquea(self, rect):
        z = self.actual
        if z is None or not z["cerrada"] or z["estado"] not in ("preparando", "activa"):
            return False
        return not z["rect"].contains(rect)

    def actualizar(self, dt, jugador, enemigos):
        self.t += dt
        self.t_aviso -= dt
        self.t_barrera -= dt
        z = self.actual
        if z is None or jugador.muerto:
            return
        for e in enemigos:
            if e.de_oleada and not e.vivo() and not e.contado:
                e.contado = True
                z["matados"] += 1
        dentro = z["rect"].collidepoint(jugador.rect.center)
        if z["estado"] == "pendiente":
            if z["rect"].inflate(-2 * OLEADA_MARGEN_ENTRADA, -2 * OLEADA_MARGEN_ENTRADA).contains(jugador.rect):
                z.update(estado="preparando", generados=0, matados=0, t_prep=OLEADA_ESPERA, t_spawn=0.0)
                self._aviso([f"OLEADA {z['nivel']} - {z['nombre']}"] + (["Zona cerrada: elimina a todos para poder salir"] if z["cerrada"] else []), 3.0)
        elif not dentro:
            self._cancelar(z, enemigos)
        elif z["estado"] == "preparando":
            z["t_prep"] -= dt
            if z["t_prep"] <= 0:
                z["estado"] = "activa"
                self._aviso([f"OLEADA {z['nivel']}!"], 2.0)
        elif z["estado"] == "activa":
            vivos = sum(1 for e in enemigos if e.de_oleada and e.vivo())
            z["t_spawn"] = max(0.0, z["t_spawn"] - dt)
            if z["generados"] < z["total"]:
                if vivos < z["max_vivos"] and z["t_spawn"] <= 0:
                    self._generar(z, jugador, enemigos)
                    z["t_spawn"] = z["intervalo"]
            elif vivos == 0:
                z["estado"] = "completada"
                if self.victoria:
                    self._aviso(["TODAS LAS OLEADAS COMPLETADAS!"], 5.0)
                else:
                    self._aviso([f"OLEADA {z['nivel']} COMPLETADA!"] + (["La zona se ha abierto: puedes salir"] if z["cerrada"] else []), 4.0)
        if self.bloquea(jugador.rect.inflate(16, 16)) and not self.bloquea(jugador.rect):
            self.t_barrera = 1.2

    def _cancelar(self, z, enemigos):
        z.update(estado="pendiente", generados=0, matados=0)
        for e in enemigos:
            if e.de_oleada and e.vivo():
                e.vida = 0
                e.t_muerte = 0.0
                e.contado = True
        self._aviso(["Has salido de la zona: la oleada se detuvo", "Vuelve a entrar para empezarla de nuevo"], 4.0)

    def _generar(self, z, jugador, enemigos):
        jx, jy = jugador.rect.center
        lejos = [p for p in z["puntos"] if math.hypot(p[0] - jx, p[1] - jy) >= z["dist"]]
        punto = random.choice(lejos) if lejos else max(z["puntos"], key=lambda p: math.hypot(p[0] - jx, p[1] - jy))
        e = Enemigo(punto[0], punto[1], agresivo=ENEMIGOS_OLEADA_AGRESIVOS, aparicion=ENEMIGO_TIEMPO_APARICION)
        e.de_oleada = True
        enemigos.agregar(e)
        z["generados"] += 1

    def dibujar_perimetro(self, superficie, cam):
        pantalla = superficie.get_rect()
        G = 44
        for z in self.zonas:
            if z["estado"] == "completada":
                continue
            r = z["rect"].move(-cam[0], -cam[1])
            if not r.colliderect(pantalla):
                continue
            activa = z["estado"] in ("preparando", "activa")
            fuerza = 0.65 + 0.35 * math.sin(self.t * 4) if activa else 0.30
            r0, g0, b0 = z["color"]
            for lado in ("arriba", "abajo", "izq", "der"):
                horizontal = lado in ("arriba", "abajo")
                pos = (r.x, r.y if lado in ("arriba", "izq") else r.bottom - G) if horizontal else \
                      (r.x if lado == "izq" else r.right - G, r.y)
                tam = (r.w, G) if horizontal else (G, r.h)
                vis = pygame.Rect(pos, tam).clip(pantalla)
                if vis.w <= 0 or vis.h <= 0:
                    continue
                banda = pygame.Surface(vis.size, pygame.SRCALPHA)
                for k in range(G):
                    d = k if lado in ("arriba", "izq") else G - 1 - k
                    a = int(150 * fuerza * (1 - d / G) ** 1.6)
                    if horizontal:
                        fila = pos[1] + k - vis.y
                        if 0 <= fila < vis.h:
                            pygame.draw.line(banda, (r0, g0, b0, a), (0, fila), (vis.w, fila))
                    else:
                        col = pos[0] + k - vis.x
                        if 0 <= col < vis.w:
                            pygame.draw.line(banda, (r0, g0, b0, a), (col, 0), (col, vis.h))
                superficie.blit(banda, vis.topleft)
            brillo = 0.45 + 0.55 * fuerza
            pygame.draw.rect(superficie, (int(r0 * brillo), int(g0 * brillo), int(b0 * brillo)), r, 4)

    def _vineta(self, color):
        if color not in self._vinetas:
            pequena = pygame.Surface((48, 27), pygame.SRCALPHA)
            for y in range(27):
                for x in range(48):
                    d = math.hypot((x - 23.5) / 23.5, (y - 13) / 13) / 1.414
                    pequena.set_at((x, y), (*color, int(95 * min(1.0, max(0.0, (d - 0.45) / 0.55)) ** 2)))
            self._vinetas[color] = pygame.transform.smoothscale(pequena, (width, height))
        return self._vinetas[color]

    def dibujar_vineta(self, superficie, jugador):
        z = self.actual
        if z is not None and z["estado"] in ("preparando", "activa") and z["rect"].collidepoint(jugador.rect.center):
            superficie.blit(self._vineta(z["color"]), (0, 0))

    def direccion_flecha(self, jugador):
        z = self.actual
        if z is None or jugador.muerto or z["rect"].collidepoint(jugador.rect.center):
            return None
        origen = pygame.Vector2(jugador.rect.center)
        destino = pygame.Vector2(z["destino"])
        objetivo = destino
        if not mapa.paso_libre(origen, destino, jugador.rect.w, jugador.rect.h):
            if self.t >= self.t_ruta:
                self.t_ruta = self.t + 0.4
                self.objetivo_flecha = None
                for p in mapa.camino(origen, destino):
                    if not mapa.paso_libre(origen, p, jugador.rect.w, jugador.rect.h):
                        break
                    self.objetivo_flecha = pygame.Vector2(p)
            if self.objetivo_flecha is not None:
                objetivo = self.objetivo_flecha
        d = objetivo - origen
        if d.length() < 1:
            d = destino - origen if (destino - origen).length() >= 1 else pygame.Vector2(1, 0)
        return d.normalize(), (destino - origen).length() / TAM_TILE

    def dibujar_flecha(self, superficie, jugador, cam):
        guia = self.direccion_flecha(jugador)
        if guia is None:
            return
        direccion, distancia = guia
        z = self.actual
        centro = pygame.Vector2(jugador.rect.centerx - cam[0], jugador.rect.bottom - 90 - cam[1])
        pivote = centro + direccion * (170 + 6 * math.sin(self.t * 6))
        pivote.x = max(60, min(width - 60, pivote.x))
        pivote.y = max(90, min(height - 90, pivote.y))
        perp = pygame.Vector2(-direccion.y, direccion.x)
        puntos = [pivote + direccion * 34, pivote - direccion * 14 + perp * 24, pivote - direccion * 2, pivote - direccion * 14 - perp * 24]
        pygame.draw.polygon(superficie, (0, 0, 0), puntos, 6)
        pygame.draw.polygon(superficie, z["color"], puntos)
        texto_borde(superficie, f"{z['nombre']} - {int(distancia)} casillas", fuente_peq, z["color"], (pivote.x, pivote.y + 44))

    def dibujar_hud(self, superficie):
        z = self.actual
        if z is None:
            lineas = ["Todas las oleadas completadas"]
        else:
            lineas = [f"OLEADA {z['nivel']}/{len(self.zonas)} - {z['nombre']}"]
            if z["estado"] == "pendiente":
                lineas.append("Entra en la zona (sigue la flecha)")
            elif z["estado"] == "preparando":
                lineas.append(f"Comienza en {max(1, math.ceil(z['t_prep']))}...")
            else:
                lineas.append(f"Enemigos restantes: {z['total'] - z['matados']}" + ("   (zona cerrada)" if z["cerrada"] else ""))
        for i, linea in enumerate(lineas):
            texto_borde(superficie, linea, fuente_peq, blanco, (20, 108 + i * 28), centrado=False)
        if self.t_aviso > 0:
            color = z["color"] if z is not None else amarillo
            for i, linea in enumerate(self.aviso):
                texto_borde(superficie, linea, menu_font if i == 0 else fuente_peq, color if i == 0 else blanco, (width // 2, 190 + i * 50))
        if self.t_barrera > 0:
            texto_borde(superficie, "No puedes salir hasta terminar la oleada", menu_font, (255, 120, 90), (width // 2, height - 150))


print("---------- ANIMACIONES DEL JUGADOR ----------")
CONFIG_ANIM = {
    "quieto": (6, True),
    "quieto_espada": (6, True),
    "caminar": (12, True),
    "correr": (16, True),
    "empujar": (6, True),
    "pared": (6, True),
    "agacharse": (16, False),
    "agachado_quieto": (6, True),
    "agachado_atacar": (18, False),
    "atacar": (20, False),
    "atacar2": (20, False),
    "atacar_dash": (20, False),
    "atacar_giro": (24, False),
    "atacar_abajo": (22, False),
    "saltar": (10, False),
    "caer": (10, False),
    "aterrizar": (16, False),
    "rodar": (24, False),
    "herido": (14, False),
    "morir": (10, False),
    "beber": (8, False),
    "victoria": (8, True),
}


class Jugador:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.rect = pygame.Rect(0, 0, int(HITBOX_JUGADOR_PIES[0] * escala_jugador), int(HITBOX_JUGADOR_PIES[1] * escala_jugador))
        self.rect.center = self.pos

        self.vel_caminar = VEL_JUGADOR_CAMINAR
        self.vel_correr = VEL_JUGADOR_CORRER
        self.vel_agachado = VEL_JUGADOR_AGACHADO
        self.vel_rodar = VEL_JUGADOR_RODAR
        self.vel_aire = VEL_JUGADOR_CAMINAR

        self.anim = "quieto"
        self.indice_frame = 0.0
        self.reversa = False
        self.anim_terminada = False
        self.mirando = 1
        self.imagen = ANIMACIONES["quieto"]["der"][0]
        self.alto_cuerpo = self.imagen.get_bounding_rect().height

        self.accion = None
        self.agachado = False
        self.muerto = False
        self.z = 0.0
        self.vz = 0.0
        self.en_aire = False
        self.dir_accion = pygame.Vector2(1, 0)
        self.empuje = pygame.Vector2(0, 0)
        self.combo = 0
        self.t_combo = 0.0
        self.tiempo_espada = 0.0
        self.cd_giro = 0.0
        self.vida_max = VIDA_JUGADOR
        self.vida = self.vida_max
        self.vida_visible = float(self.vida_max)
        self.invulnerable = 0.0
        self.golpeados = set()
        self.celebrar_pendiente = False
        self.victoria_hecha = False
        self.prev = {}
        self.enfriamiento = 0.3

    def poner_anim(self, nombre, reversa=False, reiniciar=False):
        if reiniciar or nombre != self.anim or reversa != self.reversa:
            self.anim = nombre
            self.reversa = reversa
            self.anim_terminada = False
            n = len(ANIMACIONES[nombre]["der"])
            self.indice_frame = n - 0.001 if reversa else 0.0

    def avanzar_anim(self, dt):
        fps, repite = CONFIG_ANIM[self.anim]
        n = len(ANIMACIONES[self.anim]["der"])
        if self.reversa:
            self.indice_frame -= fps * dt
            if self.indice_frame < 0:
                if repite:
                    self.indice_frame += n
                else:
                    self.indice_frame = 0.0
                    self.anim_terminada = True
        else:
            self.indice_frame += fps * dt
            if self.indice_frame >= n:
                if repite:
                    self.indice_frame %= n
                else:
                    self.indice_frame = n - 0.001
                    self.anim_terminada = True

    def progreso(self):
        n = len(ANIMACIONES[self.anim]["der"])
        p = self.indice_frame / n
        return 1 - p if self.reversa else p

    def elegir_imagen(self):
        frames = ANIMACIONES[self.anim]["der" if self.mirando == 1 else "izq"]
        self.imagen = frames[min(int(self.indice_frame), len(frames) - 1)]

    def empezar(self, nombre, lado=None):
        self.accion = nombre
        if nombre in HITBOX_ATAQUES:
            self.golpeados = set()
        if lado is not None:
            self.mirando = lado
        if nombre == "levantarse":
            self.poner_anim("agacharse", reversa=True, reiniciar=True)
        else:
            self.poner_anim(nombre, reiniciar=True)

    def recibir_dano(self, cantidad=10, origen=None):
        if self.muerto or self.accion == "rodar" or self.invulnerable > 0:
            return False
        self.vida = max(0, self.vida - cantidad)
        self.invulnerable = INVULNERABLE_TRAS_GOLPE
        if self.vida <= 0:
            self.morir()
            return True
        self.agachado = False
        retroceso = pygame.Vector2(-self.mirando, 0)
        if origen is not None:
            alejar = pygame.Vector2(self.rect.center) - pygame.Vector2(origen)
            if alejar.length() > 0:
                retroceso = alejar.normalize()
        self.empuje = retroceso * 320
        self.empezar("herido")
        return True

    def morir(self):
        self.muerto = True
        self.accion = None
        self.agachado = False
        self.z, self.vz, self.en_aire = 0.0, 0.0, False
        self.poner_anim("morir", reiniciar=True)

    def celebrar(self):
        if not self.victoria_hecha and not self.muerto:
            self.victoria_hecha = True
            self.celebrar_pendiente = True

    def cuerpo(self):
        ancho, alto = HITBOX_JUGADOR_CUERPO_AGACHADO if self.agachado else HITBOX_JUGADOR_CUERPO
        zona = pygame.Rect(0, 0, int(ancho * escala_jugador), int(alto * escala_jugador))
        zona.midbottom = (self.rect.centerx, self.rect.bottom - self.z)
        return zona

    def hitbox(self):
        if self.accion not in HITBOX_ATAQUES:
            return None
        n = len(ANIMACIONES[self.anim]["der"])
        if not 1 <= int(self.indice_frame) <= n - 2:
            return None
        ancho, alto = HITBOX_ATAQUES[self.accion]
        zona = pygame.Rect(0, 0, int(ancho * escala_jugador), int(alto * escala_jugador))
        separacion, altura = HITBOX_ATAQUE_POS[self.accion]
        y = self.rect.bottom - altura * escala_jugador - self.z
        if self.accion == "atacar_giro":
            zona.center = (self.rect.centerx, y)
        elif self.mirando == 1:
            zona.midleft = (self.rect.centerx + separacion * escala_jugador, y)
        else:
            zona.midright = (self.rect.centerx - separacion * escala_jugador, y)
        return zona

    def pulsaciones(self, teclas, raton):
        ahora = {
            "saltar": teclas[pygame.K_SPACE],
            "rodar": teclas[pygame.K_r],
            "giro": teclas[pygame.K_e] or raton[2],
            "beber": teclas[pygame.K_q],
        }
        nuevas = {k: bool(v) and not self.prev.get(k, False) for k, v in ahora.items()}
        self.prev = {k: bool(v) for k, v in ahora.items()}
        return nuevas

    def decidir_accion(self, nuevas, ataca, mueve, corre, direccion, lado_raton, quiere_agachar):
        if self.agachado:
            if nuevas["rodar"]:
                self.agachado = False
                self.iniciar_rodar(direccion)
            elif ataca:
                self.empezar("agachado_atacar", lado_raton)
            elif not quiere_agachar:
                self.empezar("levantarse")
            return

        if self.en_aire:
            if ataca:
                self.empezar("atacar_abajo", lado_raton)
            return

        if nuevas["saltar"]:
            self.en_aire = True
            self.vz = FUERZA_SALTO
            self.z = 1.0
            self.vel_aire = self.vel_correr if corre else self.vel_caminar
            self.poner_anim("saltar", reiniciar=True)
        elif nuevas["rodar"]:
            self.iniciar_rodar(direccion)
        elif nuevas["giro"] and self.cd_giro <= 0:
            self.cd_giro = ENFRIAMIENTO_GIRO
            self.empezar("atacar_giro", lado_raton)
        elif nuevas["beber"]:
            self.empezar("beber")
        elif self.celebrar_pendiente and not mueve and not ataca:
            self.celebrar_pendiente = False
            self.empezar("victoria")
        elif ataca:
            if corre:
                centro = pygame.Vector2(self.rect.centerx, self.rect.bottom - 40)
                objetivo = pos_raton_mundo() - centro
                self.dir_accion = objetivo.normalize() if objetivo.length() > 0 else pygame.Vector2(lado_raton, 0)
                self.empezar("atacar_dash", lado_raton)
            else:
                if self.t_combo <= 0:
                    self.combo = 0
                self.empezar(("atacar", "atacar2")[self.combo], lado_raton)
                self.combo = 1 - self.combo
        elif quiere_agachar:
            self.empezar("agacharse")

    def iniciar_rodar(self, direccion):
        self.dir_accion = pygame.Vector2(direccion) if direccion.length() > 0 else pygame.Vector2(self.mirando, 0)
        lado = self.mirando
        if self.dir_accion.x != 0:
            lado = 1 if self.dir_accion.x > 0 else -1
        self.empezar("rodar", lado)

    def _mover_chocando(self, paso):
        atascado = mapa_choca(self.rect)
        for eje in (0, 1):
            d = paso[eje]
            if d == 0:
                continue
            self.pos[eje] += d
            self.rect.center = self.pos
            if not atascado and mapa_choca(self.rect):
                self.pos[eje] -= d
                signo = 1 if d > 0 else -1
                for _ in range(int(abs(d))):
                    self.pos[eje] += signo
                    self.rect.center = self.pos
                    if mapa_choca(self.rect):
                        self.pos[eje] -= signo
                        break
        self.rect.center = self.pos

    def actualizar(self, teclas, dt):
        self.enfriamiento -= dt
        self.cd_giro -= dt
        self.t_combo -= dt
        self.tiempo_espada -= dt
        self.invulnerable -= dt
        if self.vida_visible > self.vida:
            self.vida_visible = max(self.vida, self.vida_visible - 40 * dt)
        else:
            self.vida_visible = self.vida
        raton = pygame.mouse.get_pressed()
        nuevas = self.pulsaciones(teclas, raton)

        if self.muerto:
            self.poner_anim("morir")
            self.avanzar_anim(dt)
            self.elegir_imagen()
            return

        dx = (teclas[pygame.K_d] or teclas[pygame.K_RIGHT]) - (teclas[pygame.K_a] or teclas[pygame.K_LEFT])
        dy = (teclas[pygame.K_s] or teclas[pygame.K_DOWN]) - (teclas[pygame.K_w] or teclas[pygame.K_UP])
        direccion = pygame.Vector2(dx, dy)
        mueve = direccion.length() > 0
        if mueve:
            direccion = direccion.normalize()
        corre = mueve and (teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT])
        quiere_agachar = teclas[pygame.K_c] or teclas[pygame.K_LCTRL]
        lado_raton = -1 if pos_raton_mundo().x < self.rect.centerx else 1
        ataca = raton[0] and self.enfriamiento <= 0

        if self.accion == "victoria" and (mueve or ataca or any(nuevas.values())):
            self.accion = None
        if self.accion is None:
            self.decidir_accion(nuevas, ataca, mueve, corre, direccion, lado_raton, quiere_agachar)

        a = self.accion
        p = self.progreso()
        mov = pygame.Vector2(0, 0)
        if a == "rodar":
            mov = self.dir_accion * self.vel_rodar * (1 - 0.5 * p)
        elif a == "atacar_dash":
            mov = self.dir_accion * 520 * max(0.0, 1 - 1.4 * p)
        elif a == "atacar_giro":
            mov = direccion * self.vel_caminar * 0.5
        elif a == "atacar_abajo":
            mov = direccion * self.vel_aire * 0.5 if self.en_aire else mov
        elif a == "herido":
            mov = self.empuje * (1 - p)
        elif a is None:
            if self.en_aire:
                mov = direccion * self.vel_aire
            elif self.agachado:
                mov = direccion * self.vel_agachado
            else:
                mov = direccion * (self.vel_correr if corre else self.vel_caminar)
        self._mover_chocando(mov * dt)
        area = pygame.Rect(0, self.alto_cuerpo - self.rect.h, MUNDO_ANCHO, MUNDO_ALTO - self.alto_cuerpo + self.rect.h)
        self.rect.clamp_ip(area)
        self.pos.update(self.rect.center)
        toca_izq = self.rect.left <= 0 and direccion.x < 0
        toca_der = self.rect.right >= MUNDO_ANCHO and direccion.x > 0
        contra_pared = toca_izq or toca_der

        if self.en_aire:
            g = GRAVEDAD_GOLPE_ABAJO if self.accion == "atacar_abajo" else GRAVEDAD
            self.vz -= g * dt
            self.z += self.vz * dt
            if self.z <= 0:
                self.z, self.vz, self.en_aire = 0.0, 0.0, False
                if self.accion is None:
                    self.empezar("aterrizar")

        if self.accion is None:
            if self.en_aire:
                if contra_pared:
                    self.mirando = 1 if toca_der else -1
                    self.poner_anim("pared")
                else:
                    self.mirando = lado_raton
                    self.poner_anim("saltar" if self.vz > 0 else "caer")
            elif self.agachado:
                self.mirando = lado_raton
                self.poner_anim("agachado_quieto")
            elif contra_pared:
                self.mirando = 1 if toca_der else -1
                self.poner_anim("empujar")
            elif mueve and corre:
                self.mirando = (1 if direccion.x > 0 else -1) if direccion.x != 0 else lado_raton
                self.poner_anim("correr")
            elif mueve:
                self.mirando = lado_raton
                self.poner_anim("caminar")
            else:
                self.mirando = lado_raton
                self.poner_anim("quieto_espada" if self.tiempo_espada > 0 else "quieto")

        self.avanzar_anim(dt)

        if self.accion is not None and self.anim_terminada:
            terminada = self.accion
            self.accion = None
            if terminada == "agacharse":
                self.agachado = True
            elif terminada == "levantarse":
                self.agachado = False
            elif terminada in HITBOX_ATAQUES:
                self.enfriamiento = ENFRIAMIENTO_ATAQUE
                self.t_combo = TIEMPO_COMBO
                self.tiempo_espada = TIEMPO_ESPADA_EN_MANO

        self.elegir_imagen()

    def dibujar(self, superficie, cam=(0, 0)):
        factor = max(0.4, 1 - self.z / 400)
        sombra = pygame.Surface((max(1, int(30 * escala_jugador * factor)), max(1, int(9 * escala_jugador * factor))), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 90), sombra.get_rect())
        superficie.blit(sombra, sombra.get_rect(center=(self.rect.centerx - cam[0], self.rect.bottom - 2 - cam[1])))
        imagen = self.imagen
        if self.invulnerable > 0 and not self.muerto and self.accion != "rodar":
            if int(self.invulnerable * 16) % 2 == 0:
                imagen = con_transparencia(imagen, 110)
        superficie.blit(imagen, imagen.get_rect(midbottom=(self.rect.centerx - cam[0], self.rect.bottom - self.z - cam[1])))


class Enemigo:
    def __init__(self, x, y, agresivo=False, aparicion=0.0):
        self.rect = pygame.Rect(0, 0, int(HITBOX_ENEMIGO_PIES[0] * escala_enemigos), int(HITBOX_ENEMIGO_PIES[1] * escala_enemigos))
        self.rect.midbottom = (x, y)
        self.pos = pygame.Vector2(self.rect.midbottom)
        self.casa = pygame.Vector2(self.rect.midbottom)
        self.dano = DANO_ENEMIGO
        self.vida_max = VIDA_ENEMIGO
        self.vida = self.vida_max
        if Enemigo._imagenes is None:
            base = escalar_imagen(cargar_sprite_enemigo("goblin"), escala_enemigos)
            alerta = base.copy()
            alerta.fill((150, 0, 0, 0), special_flags=pygame.BLEND_RGB_ADD)
            destello = base.copy()
            destello.fill((170, 170, 170, 0), special_flags=pygame.BLEND_RGB_ADD)
            imagenes = {}
            for nombre, img in (("normal", base), ("alerta", alerta), ("destello", destello)):
                volteada = pygame.transform.flip(img, True, False)
                der, izq = (img, volteada) if ENEMIGO_MIRA_A_LA_DERECHA else (volteada, img)
                imagenes[(nombre, 1)] = der
                imagenes[(nombre, -1)] = izq
            Enemigo._imagenes = (imagenes, base.get_height())
        self.imagenes, self.alto_img = Enemigo._imagenes
        self.estado = "perseguir" if agresivo else "vagar"
        self.mirando = random.choice((-1, 1))
        self.t_vagar = random.uniform(0.2, 1.2)
        self.dir_vagar = pygame.Vector2(0, 0)
        self.ataque = None
        self.t_cd = random.uniform(0.0, 0.5)
        self.ruta = []
        self.t_ruta = 0.0
        self.retroceso = pygame.Vector2(0, 0)
        self.t_retroceso = 0.0
        self.t_muerte = None
        self.eliminado = False
        self.agresivo = agresivo
        self.t_aparicion = aparicion
        self.aparicion_total = aparicion
        self.de_oleada = False
        self.contado = False

    def vivo(self):
        return self.vida > 0

    def cuerpo(self):
        zona = pygame.Rect(0, 0, int(HITBOX_ENEMIGO_CUERPO[0] * escala_enemigos), int(HITBOX_ENEMIGO_CUERPO[1] * escala_enemigos))
        zona.midbottom = self.rect.midbottom
        return zona

    def zona_ataque(self, lado):
        ancho, alto = HITBOX_ENEMIGO_ATAQUE
        separacion, altura = HITBOX_ENEMIGO_ATAQUE_POS
        zona = pygame.Rect(0, 0, int(ancho * escala_enemigos), int(alto * escala_enemigos))
        y = self.rect.bottom - altura * escala_enemigos
        if lado == 1:
            zona.midleft = (self.rect.centerx + separacion * escala_enemigos, y)
        else:
            zona.midright = (self.rect.centerx - separacion * escala_enemigos, y)
        return zona

    def recibir_dano(self, cantidad, origen):
        if not self.vivo() or self.t_retroceso > 0 or self.t_aparicion > 0:
            return False
        self.vida = max(0, self.vida - cantidad)
        alejar = pygame.Vector2(self.rect.center) - pygame.Vector2(origen)
        if alejar.length() == 0:
            alejar = pygame.Vector2(1, 0)
        self.t_retroceso = TIEMPO_RETROCESO
        self.retroceso = alejar.normalize() * (2 * RETROCESO_ENEMIGO / TIEMPO_RETROCESO)
        self.ataque = None
        self.estado = "perseguir"
        if self.vida <= 0:
            self.t_muerte = 0.0
        return True

    def _area(self):
        return pygame.Rect(0, self.alto_img - self.rect.h, MUNDO_ANCHO, MUNDO_ALTO - self.alto_img + self.rect.h)

    def _mover(self, direccion, vel, dt, obstaculos):
        antes = pygame.Vector2(self.pos)
        paso = direccion * vel * dt
        atascado = self.rect.collidelist(obstaculos) != -1 or mapa_choca(self.rect)
        for eje in (0, 1):
            self.pos[eje] += paso[eje]
            self.rect.midbottom = self.pos
            if not atascado and (self.rect.collidelist(obstaculos) != -1 or mapa_choca(self.rect)):
                self.pos[eje] -= paso[eje]
        self.rect.midbottom = self.pos
        antes_rect = self.rect.copy()
        self.rect.clamp_ip(self._area())
        if self.rect != antes_rect:
            self.pos.update(self.rect.midbottom)
        return (self.pos - antes).length() > 0.01

    def _retroceder(self, dt):
        paso = self.retroceso * (self.t_retroceso / TIEMPO_RETROCESO) * dt
        for eje in (0, 1):
            self.pos[eje] += paso[eje]
            self.rect.midbottom = self.pos
            if mapa_choca(self.rect):
                self.pos[eje] -= paso[eje]
        self.rect.midbottom = self.pos
        antes_rect = self.rect.copy()
        self.rect.clamp_ip(self._area())
        if self.rect != antes_rect:
            self.pos.update(self.rect.midbottom)
        self.t_retroceso -= dt

    def _vagar(self, dt, obstaculos):
        self.t_vagar -= dt
        if self.t_vagar <= 0:
            if self.dir_vagar.length() > 0:
                self.dir_vagar = pygame.Vector2(0, 0)
                self.t_vagar = random.uniform(0.6, 1.8)
            else:
                angulo = random.uniform(0, 2 * math.pi)
                lejos = self.casa - pygame.Vector2(self.rect.midbottom)
                if lejos.length() > RADIO_VAGAR:
                    angulo = math.atan2(lejos.y, lejos.x) + random.uniform(-0.8, 0.8)
                self.dir_vagar = pygame.Vector2(math.cos(angulo), math.sin(angulo))
                self.t_vagar = random.uniform(0.6, 1.6)
        if self.dir_vagar.length() > 0:
            if abs(self.dir_vagar.x) > 0.25:
                self.mirando = 1 if self.dir_vagar.x > 0 else -1
            if not self._mover(self.dir_vagar, VEL_ENEMIGO_VAGAR, dt, obstaculos):
                self.t_vagar = 0

    def _perseguir(self, dt, jugador, obstaculos):
        yo = pygame.Vector2(self.rect.center)
        el = pygame.Vector2(jugador.rect.center)
        dx = el.x - yo.x
        if abs(dx) > ENEMIGO_UMBRAL_GIRO:
            self.mirando = 1 if dx > 0 else -1
        if self.t_cd <= 0 and self.zona_ataque(self.mirando).colliderect(jugador.cuerpo()):
            self.ataque = {"fase": "preparar", "t": 0.0, "golpeo": False, "lado": self.mirando}
            return
        destino = el
        if mapa is not None and not mapa.paso_libre(self.rect.center, jugador.rect.center, self.rect.w, self.rect.h):
            self.t_ruta -= dt
            if self.t_ruta <= 0 or not self.ruta:
                self.ruta = mapa.camino(self.rect.center, jugador.rect.center)
                self.t_ruta = 0.4
            while len(self.ruta) > 1 and (pygame.Vector2(self.ruta[0]) - yo).length() < 24:
                self.ruta.pop(0)
            if self.ruta:
                destino = pygame.Vector2(self.ruta[0])
        else:
            self.ruta = []
        if (destino - yo).length() > 1:
            self._mover((destino - yo).normalize(), VEL_ENEMIGO_PERSEGUIR, dt, obstaculos)

    def _atacar(self, dt, jugador):
        a = self.ataque
        a["t"] += dt
        if a["fase"] == "preparar":
            if a["t"] >= ENEMIGO_PREPARAR:
                a["fase"], a["t"] = "golpe", 0.0
        elif a["fase"] == "golpe":
            if not a["golpeo"] and not jugador.muerto and self.zona_ataque(a["lado"]).colliderect(jugador.cuerpo()):
                a["golpeo"] = True
                jugador.recibir_dano(self.dano, self.rect.center)
            if a["t"] >= ENEMIGO_GOLPE:
                a["fase"], a["t"] = "recuperar", 0.0
        elif a["t"] >= ENEMIGO_RECUPERAR:
            self.ataque = None
            self.t_cd = ENEMIGO_ENFRIAMIENTO

    def actualizar(self, dt, jugador, otros):
        self.t_cd -= dt
        if self.t_aparicion > 0:
            self.t_aparicion -= dt
            return
        if self.t_retroceso > 0:
            self._retroceder(dt)
        if self.t_muerte is not None:
            self.t_muerte += dt
            if self.t_muerte >= 0.6:
                self.eliminado = True
            return
        if self.t_retroceso > 0:
            return
        if self.ataque is not None:
            self._atacar(dt, jugador)
            return
        yo = pygame.Vector2(self.rect.center)
        distancia = (pygame.Vector2(jugador.rect.center) - yo).length()
        if self.estado == "vagar":
            if (distancia < RADIO_DETECCION and not jugador.muerto and
                    (distancia < RADIO_DETECCION / 2 or mapa is None or mapa.hay_vista(self.rect.center, jugador.rect.center))):
                self.estado = "perseguir"
        elif (distancia > RADIO_PERDER and not self.agresivo) or jugador.muerto:
            self.estado = "vagar"
            self.t_vagar, self.dir_vagar = 0.0, pygame.Vector2(0, 0)
        obstaculos = [jugador.rect] + [o.rect for o in otros if o is not self and o.vivo()]
        if self.estado == "perseguir":
            self._perseguir(dt, jugador, obstaculos)
        else:
            self._vagar(dt, obstaculos)

    def _desplazamiento(self):
        a = self.ataque
        if a is None:
            return 0
        if a["fase"] == "preparar":
            return -a["lado"] * 3 * escala_enemigos * (a["t"] / ENEMIGO_PREPARAR)
        if a["fase"] == "golpe":
            return a["lado"] * 5 * escala_enemigos
        return a["lado"] * 5 * escala_enemigos * (1 - a["t"] / ENEMIGO_RECUPERAR)

    def dibujar(self, superficie, cam=(0, 0)):
        sombra = pygame.Surface((int(self.rect.w * 1.5), int(self.rect.h * 1.1)), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 90), sombra.get_rect())
        superficie.blit(sombra, sombra.get_rect(center=(self.rect.centerx - cam[0], self.rect.bottom - 2 - cam[1])))
        lado = self.ataque["lado"] if self.ataque else self.mirando
        variante = "normal"
        if self.t_retroceso > TIEMPO_RETROCESO - 0.12:
            variante = "destello"
        elif self.ataque and self.ataque["fase"] == "preparar":
            variante = "alerta" if int(self.ataque["t"] * 16) % 2 == 0 else "normal"
        imagen = self.imagenes[(variante, lado)]
        if self.t_muerte is not None:
            imagen = con_transparencia(imagen, 255 * max(0.0, 1 - self.t_muerte / 0.6))
        elif self.t_aparicion > 0:
            imagen = con_transparencia(imagen, 255 * (1 - self.t_aparicion / max(0.01, self.aparicion_total)))
        pos_img = imagen.get_rect(midbottom=(self.rect.centerx + self._desplazamiento() - cam[0], self.rect.bottom - cam[1]))
        superficie.blit(imagen, pos_img)
        if self.vivo() and self.vida < self.vida_max:
            ancho, alto = imagen.get_width(), max(4, int(1.6 * escala_enemigos))
            barra = pygame.Rect(0, 0, ancho, alto)
            barra.midbottom = (self.rect.centerx - cam[0], pos_img.top - 6)
            pygame.draw.rect(superficie, (35, 10, 14), barra)
            pygame.draw.rect(superficie, (210, 40, 55), (barra.x, barra.y, int(ancho * self.vida / self.vida_max), alto))
            pygame.draw.rect(superficie, blanco, barra, 2)


Enemigo._imagenes = None


class Enemigos:
    def __init__(self):
        self.lista = []

    def __iter__(self):
        return iter(self.lista)

    def __len__(self):
        return len(self.lista)

    def agregar(self, enemigo):
        self.lista.append(enemigo)

    def vivos(self):
        return [e for e in self.lista if e.vivo()]

    def actualizar(self, dt, jugador):
        for e in self.lista:
            e.actualizar(dt, jugador, self.lista)
        self._golpes_del_jugador(jugador)
        self._chocar_con_jugador(jugador)
        self.lista = [e for e in self.lista if not e.eliminado]

    def _golpes_del_jugador(self, jugador):
        zona = jugador.hitbox()
        if zona is None:
            return
        dano = DANO_ATAQUE[jugador.accion]
        for e in self.lista:
            if e.vivo() and e not in jugador.golpeados and zona.colliderect(e.cuerpo()):
                if e.recibir_dano(dano, jugador.rect.center):
                    jugador.golpeados.add(e)

    def _chocar_con_jugador(self, jugador):
        if jugador.muerto:
            return
        cuerpo = jugador.cuerpo()
        for e in self.lista:
            if not e.vivo() or e.t_aparicion > 0:
                continue
            if DANO_POR_CONTACTO and cuerpo.colliderect(e.cuerpo()):
                jugador.recibir_dano(e.dano, e.rect.center)
            if jugador.z < 50 and jugador.rect.colliderect(e.rect):
                salidas = [
                    (e.rect.right - jugador.rect.left, (1, 0)),
                    (jugador.rect.right - e.rect.left, (-1, 0)),
                    (e.rect.bottom - jugador.rect.top, (0, 1)),
                    (jugador.rect.bottom - e.rect.top, (0, -1)),
                ]
                distancia, (sx, sy) = min(salidas)
                jugador.rect.move_ip(sx * distancia, sy * distancia)
                jugador.pos.update(jugador.rect.center)


class Partida:
    def __init__(self):
        self.jugador = Jugador(*mapa.inicio)
        self.enemigos = Enemigos()
        self.oleadas = Oleadas(ZONAS)
        actualizar_camara(self.jugador, 0, True)

    @property
    def terminada(self):
        return self.jugador.muerto or self.oleadas.victoria

    def actualizar(self, dt, teclas):
        self.jugador.actualizar(teclas, dt)
        self.enemigos.actualizar(dt, self.jugador)
        self.oleadas.actualizar(dt, self.jugador, self.enemigos)
        if self.oleadas.victoria:
            self.jugador.celebrar()
        actualizar_camara(self.jugador, dt)

    def dibujar(self, superficie, cursor_oculto):
        cam = camara_pos()
        mapa.dibujar_suelo(superficie, cam)
        self.oleadas.dibujar_perimetro(superficie, cam)
        for ent in sorted(mapa.props_visibles(cam) + self.enemigos.lista + [self.jugador], key=lambda o: o.rect.bottom):
            ent.dibujar(superficie, cam)
        if MOSTRAR_HITBOX:
            self._dibujar_hitboxes(superficie, cam)
        self.oleadas.dibujar_vineta(superficie, self.jugador)
        self.oleadas.dibujar_flecha(superficie, self.jugador, cam)
        dibujar_barra_vida(superficie, self.jugador)
        self.oleadas.dibujar_hud(superficie)
        if self.terminada:
            texto = "Has muerto - pulsa Enter para reiniciar" if self.jugador.muerto else "Victoria! - pulsa Enter para jugar otra vez"
            aviso = menu_font.render(texto, True, amarillo)
            superficie.blit(aviso, aviso.get_rect(center=(width // 2, 130 if self.jugador.muerto else 120)))
        for i, linea in enumerate(ayuda_juego):
            superficie.blit(linea, (20, height - 54 + i * 24))
        if cursor_oculto and MOSTRAR_MIRA:
            dibujar_mira(superficie)

    def _dibujar_hitboxes(self, superficie, cam):
        mapa.dibujar_colisiones(superficie, cam)
        j = self.jugador
        pygame.draw.rect(superficie, (0, 200, 255), j.rect.move(-cam[0], -cam[1]), 2)
        pygame.draw.rect(superficie, (80, 255, 80), j.cuerpo().move(-cam[0], -cam[1]), 2)
        golpe = j.hitbox()
        if golpe is not None:
            pygame.draw.rect(superficie, (255, 255, 0), golpe.move(-cam[0], -cam[1]), 3)
        for e in self.enemigos:
            pygame.draw.rect(superficie, (255, 150, 0), e.rect.move(-cam[0], -cam[1]), 2)
            pygame.draw.rect(superficie, (255, 60, 60), e.cuerpo().move(-cam[0], -cam[1]), 2)
            if e.vivo():
                lado = e.ataque["lado"] if e.ataque else e.mirando
                grosor = 4 if e.ataque and e.ataque["fase"] == "golpe" else 1
                pygame.draw.rect(superficie, (255, 60, 255), e.zona_ataque(lado).move(-cam[0], -cam[1]), grosor)


print("---------- FUNCIONES ----------")
def blit_scaled():
    scaled = pygame.transform.scale(game_surface, ventana.get_size())
    ventana.blit(scaled, (0, 0))


def dibujar_texto(texto, color, y):
    render = menu_font.render(texto, True, color)
    game_surface.blit(render, render.get_rect(center=(width // 2, y)))


def pos_en_juego(pos):
    sx, sy = ventana.get_size()
    return (pos[0] * width / sx, pos[1] * height / sy)


def zona_boton(texto, y):
    return menu_font.render(texto, True, blanco).get_rect(center=(width // 2, y)).inflate(60, 24)


def dibujar_boton(texto, color, color_hover, y):
    zona = zona_boton(texto, y)
    encima = zona.collidepoint(pos_en_juego(pygame.mouse.get_pos()))
    dibujar_texto(texto, color_hover if encima else color, y)
    return zona


def dibujar_boton_caja(texto, rect):
    encima = rect.collidepoint(pos_en_juego(pygame.mouse.get_pos()))
    relleno = (70, 60, 110) if encima else (35, 30, 60)
    borde = amarillo if encima else (150, 150, 190)
    pygame.draw.rect(game_surface, relleno, rect, border_radius=14)
    pygame.draw.rect(game_surface, borde, rect, width=3, border_radius=14)
    render = menu_font.render(texto, True, amarillo if encima else blanco)
    game_surface.blit(render, render.get_rect(center=rect.center))


def dibujar_fondo():
    game_surface.blit(fondo_menu, (0, 0))
    game_surface.blit(velo, (0, 0))


print("---------- FUNCIONES DE MUSICA ----------")
def aplicar_volumen():
    if pygame.mixer.get_init():
        pygame.mixer.music.set_volume(ajustes["musica"])


def nombre_cancion(ruta):
    return os.path.splitext(os.path.basename(ruta))[0]


def hay_activas():
    return any(activas.values())


def reproducir(indice):
    global actual
    try:
        pygame.mixer.music.load(canciones[indice])
        pygame.mixer.music.play(0)
        aplicar_volumen()
        actual = indice
        return True
    except pygame.error:
        activas[canciones[indice]] = False
        return False


def siguiente(paso=1):
    global actual
    if not canciones or not pygame.mixer.get_init():
        return
    n = len(canciones)
    for k in range(1, n + 1):
        idx = (actual + paso * k) % n
        if activas[canciones[idx]] and reproducir(idx):
            return
    pygame.mixer.music.stop()
    actual = -1


def alternar_cancion(indice):
    activas[canciones[indice]] = not activas[canciones[indice]]
    if indice == actual and not activas[canciones[indice]]:
        siguiente()


def revisar_musica():
    if (canciones and pygame.mixer.get_init() and hay_activas()
            and not pygame.mixer.music.get_busy()):
        siguiente()


def aplicar_pantalla():
    global ventana
    if ajustes["pantalla_completa"]:
        ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        ventana = pygame.display.set_mode((1280, 720))


def dibujar_slider(texto, clave):
    barra = sliders[clave]
    valor = ajustes[clave]
    etiqueta = menu_font.render(texto, True, blanco)
    game_surface.blit(etiqueta, etiqueta.get_rect(midleft=(450, barra.centery)))
    pygame.draw.rect(game_surface, (80, 80, 80), barra, border_radius=6)
    relleno = pygame.Rect(barra.left, barra.top, int(barra.width * valor), barra.height)
    pygame.draw.rect(game_surface, amarillo, relleno, border_radius=6)
    pygame.draw.circle(game_surface, blanco, (barra.left + int(barra.width * valor), barra.centery), 14)
    porcentaje = menu_font.render(f"{int(valor * 100)}%", True, blanco)
    game_surface.blit(porcentaje, porcentaje.get_rect(midleft=(barra.right + 40, barra.centery)))


def dibujar_interruptor(texto, clave):
    caja = interruptores[clave]
    activo = ajustes[clave]
    etiqueta = menu_font.render(texto, True, blanco)
    game_surface.blit(etiqueta, etiqueta.get_rect(midleft=(450, caja.centery)))
    pygame.draw.rect(game_surface, (60, 160, 90) if activo else (160, 60, 60), caja, border_radius=10)
    estado = menu_font.render("SI" if activo else "NO", True, blanco)
    game_surface.blit(estado, estado.get_rect(center=caja.center))


def texto_ahora_suena():
    if 0 <= actual < len(canciones):
        return "Ahora suena: " + nombre_cancion(canciones[actual])[:50]
    return "Ahora suena: (nada)"


def show_ajustes():
    dibujar_fondo()
    dibujar_texto("AJUSTES", blanco, 150)
    sonando = fuente_peq.render(texto_ahora_suena(), True, amarillo)
    game_surface.blit(sonando, sonando.get_rect(center=(width // 2, 215)))
    dibujar_slider("Musica", "musica")
    dibujar_slider("Efectos", "efectos")
    dibujar_interruptor("Pantalla completa", "pantalla_completa")
    dibujar_interruptor("Mostrar FPS", "mostrar_fps")
    dibujar_boton_caja("elegir canciones", boton_canciones)
    dibujar_boton("volver", blanco, amarillo, 710)


def filas_visibles():
    fin = min(len(canciones), scroll + FILAS_VISIBLES)
    return [(i, pygame.Rect(350, 230 + v * 62, 850, 52)) for v, i in enumerate(range(scroll, fin))]


def rect_check(fila):
    return pygame.Rect(fila.x + 14, fila.centery - 16, 32, 32)


def rect_sonar(fila):
    return pygame.Rect(fila.right - 170, fila.y + 6, 160, 40)


def show_musica():
    dibujar_fondo()
    dibujar_texto("CANCIONES", blanco, 130)
    sonando = fuente_peq.render(texto_ahora_suena(), True, amarillo)
    game_surface.blit(sonando, sonando.get_rect(center=(width // 2, 185)))
    mouse = pos_en_juego(pygame.mouse.get_pos())

    if not canciones:
        aviso = fuente_peq.render("No hay canciones. Pon archivos .mp3/.ogg/.wav en la carpeta 'musica'.",
                                  True, blanco)
        game_surface.blit(aviso, aviso.get_rect(center=(width // 2, 400)))

    for i, fila in filas_visibles():
        ruta = canciones[i]
        sonando_ahora = (i == actual)
        pygame.draw.rect(game_surface, (70, 60, 110) if sonando_ahora else (35, 30, 60), fila, border_radius=10)
        caja = rect_check(fila)
        pygame.draw.rect(game_surface, blanco, caja, width=3, border_radius=6)
        if activas[ruta]:
            pygame.draw.rect(game_surface, (60, 200, 110), caja.inflate(-12, -12), border_radius=4)
        nombre = fuente_peq.render(nombre_cancion(ruta)[:45], True, amarillo if sonando_ahora else blanco)
        game_surface.blit(nombre, nombre.get_rect(midleft=(fila.x + 70, fila.centery)))
        zona = rect_sonar(fila)
        hover = zona.collidepoint(mouse)
        pygame.draw.rect(game_surface, (90, 80, 140) if hover else (55, 50, 90), zona, border_radius=8)
        txt = fuente_peq.render("sonar ahora", True, amarillo if hover else blanco)
        game_surface.blit(txt, txt.get_rect(center=zona.center))

    if len(canciones) > FILAS_VISIBLES:
        pista = fuente_peq.render("(rueda del raton para ver mas)", True, (200, 200, 200))
        game_surface.blit(pista, pista.get_rect(center=(width // 2, 665)))

    dibujar_boton_caja("anterior", boton_anterior)
    dibujar_boton_caja("siguiente", boton_siguiente)
    dibujar_boton_caja("volver", boton_volver_musica)


def click_musica(click):
    global MUSICA
    for i, fila in filas_visibles():
        if rect_check(fila).inflate(10, 10).collidepoint(click):
            alternar_cancion(i)
            return
        if rect_sonar(fila).collidepoint(click):
            activas[canciones[i]] = True
            reproducir(i)
            return
    if boton_anterior.collidepoint(click):
        siguiente(-1)
    elif boton_siguiente.collidepoint(click):
        siguiente(1)
    elif boton_volver_musica.collidepoint(click):
        MUSICA = False


def mapa_choca(rect):
    return (mapa is not None and mapa.choca(rect)) or (partida is not None and partida.oleadas.bloquea(rect))


def texto_borde(superficie, texto, fuente, color, pos, centrado=True):
    for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (2, 2)):
        sombra = fuente.render(texto, True, (0, 0, 0))
        superficie.blit(sombra, sombra.get_rect(**({"center": (pos[0] + dx, pos[1] + dy)} if centrado else {"topleft": (pos[0] + dx, pos[1] + dy)})))
    render = fuente.render(texto, True, color)
    superficie.blit(render, render.get_rect(**({"center": pos} if centrado else {"topleft": pos})))


def camara_pos():
    return (round(camara.x), round(camara.y))


def pos_raton_mundo():
    cx, cy = camara_pos()
    mx, my = pos_en_juego(pygame.mouse.get_pos())
    return pygame.Vector2(mx + cx, my + cy)


def actualizar_camara(jugador, dt, forzar=False):
    objetivo = pygame.Vector2(jugador.rect.centerx - width / 2, jugador.rect.bottom - 90 - height / 2)
    if CAMARA_LIMITADA:
        for eje, mundo, pantalla in ((0, MUNDO_ANCHO, width), (1, MUNDO_ALTO, height)):
            if mundo <= pantalla:
                objetivo[eje] = (mundo - pantalla) / 2
            else:
                objetivo[eje] = max(0, min(objetivo[eje], mundo - pantalla))
    if forzar or CAMARA_SUAVIDAD <= 0:
        camara.update(objetivo)
    else:
        camara.update(camara + (objetivo - camara) * min(1.0, CAMARA_SUAVIDAD * dt))


def dibujar_mira(superficie):
    x, y = (int(v) for v in pos_en_juego(pygame.mouse.get_pos()))
    for color, grosor in (((0, 0, 0), 4), ((255, 255, 255), 2)):
        pygame.draw.line(superficie, color, (x - 13, y), (x - 5, y), grosor)
        pygame.draw.line(superficie, color, (x + 5, y), (x + 13, y), grosor)
        pygame.draw.line(superficie, color, (x, y - 13), (x, y - 5), grosor)
        pygame.draw.line(superficie, color, (x, y + 5), (x, y + 13), grosor)
    pygame.draw.circle(superficie, (255, 255, 255), (x, y), 2)


def con_transparencia(imagen, alpha):
    copia = imagen.copy()
    copia.fill((255, 255, 255, max(0, min(255, int(alpha)))), special_flags=pygame.BLEND_RGBA_MULT)
    return copia


def escalar_imagen(imagen, escala):
    if escala == 1:
        return imagen
    tam = (max(1, round(imagen.get_width() * escala)), max(1, round(imagen.get_height() * escala)))
    return pygame.transform.scale(imagen, tam)


SPRITES_ENEMIGOS = {}


def cargar_sprite_enemigo(nombre):
    if nombre not in SPRITES_ENEMIGOS:
        for base in (os.getcwd(), os.path.dirname(os.path.abspath(__file__))):
            ruta = os.path.join(base, "enemigos", nombre + ".png")
            if os.path.exists(ruta):
                break
        else:
            print(f"No encuentro enemigos/{nombre}.png junto a este archivo (descomprime enemigos.zip).")
            pygame.quit()
            sys.exit()
        img = pygame.image.load(ruta).convert_alpha()
        SPRITES_ENEMIGOS[nombre] = img.subsurface(img.get_bounding_rect()).copy()
    return SPRITES_ENEMIGOS[nombre]


def dibujar_barra_vida(superficie, jugador):
    x, y, ancho, alto = 20, 70, 320, 26
    frac = jugador.vida / jugador.vida_max
    visible = jugador.vida_visible / jugador.vida_max
    pygame.draw.rect(superficie, (35, 10, 14), (x, y, ancho, alto), border_radius=8)
    if visible > frac:
        pygame.draw.rect(superficie, (240, 215, 215), (x, y, int(ancho * visible), alto), border_radius=8)
    if frac > 0:
        pygame.draw.rect(superficie, (210, 40, 55), (x, y, int(ancho * frac), alto), border_radius=8)
    pygame.draw.rect(superficie, blanco, (x, y, ancho, alto), width=3, border_radius=8)
    texto = fuente_peq.render(f"VIDA {jugador.vida}/{jugador.vida_max}", True, blanco)
    superficie.blit(texto, texto.get_rect(midleft=(x + ancho + 14, y + alto // 2)))


def cargar_animaciones():
    carpeta = None
    for base in (os.getcwd(), os.path.dirname(os.path.abspath(__file__))):
        if os.path.isdir(os.path.join(base, "jugador")):
            carpeta = os.path.join(base, "jugador")
            break
    if carpeta is None:
        print("No encuentro la carpeta 'jugador' junto a este archivo (descomprime jugador_frames.zip).")
        pygame.quit()
        sys.exit()
    animaciones = {}
    for nombre in CONFIG_ANIM:
        frames = []
        n = 1
        while os.path.exists(os.path.join(carpeta, f"{nombre}_{n}.png")):
            img = pygame.image.load(os.path.join(carpeta, f"{nombre}_{n}.png")).convert_alpha()
            frames.append(escalar_imagen(img, escala_jugador))
            n += 1
        if not frames:
            print(f"Faltan los frames de '{nombre}' en {carpeta}")
            pygame.quit()
            sys.exit()
        animaciones[nombre] = {"der": frames, "izq": [pygame.transform.flip(f, True, False) for f in frames]}
    return animaciones


def show_menu():
    dibujar_fondo()
    panel = pygame.Surface((520, 460), pygame.SRCALPHA)
    pygame.draw.rect(panel, (10, 10, 30, 150), panel.get_rect(), border_radius=24)
    game_surface.blit(panel, panel.get_rect(center=(width // 2, 440)))
    y_titulo = 215 + math.sin(pygame.time.get_ticks() / 600) * 6
    sombra = titulo_font.render("PRISION FANTASY", True, negro)
    titulo = titulo_font.render("PRISION FANTASY", True, amarillo)
    game_surface.blit(sombra, sombra.get_rect(center=(width // 2 + 4, y_titulo + 4)))
    game_surface.blit(titulo, titulo.get_rect(center=(width // 2, y_titulo)))
    for op in opciones:
        dibujar_boton_caja(op["texto"], op["rect"])
    ayuda = fuente_peq.render("1 = jugar    2 = ajustes    3 = controles", True, (200, 200, 200))
    game_surface.blit(ayuda, ayuda.get_rect(center=(width // 2, height - 40)))


LISTA_CONTROLES = [
    ("Mover", "W A S D  /  flechas"),
    ("Correr", "Shift (mientras te mueves)"),
    ("Saltar", "Espacio"),
    ("Rodar", "R"),
    ("Agacharse", "C  /  Ctrl (mantener)"),
    ("Atacar (combo)", "clic izquierdo"),
    ("Embestida", "clic izquierdo corriendo"),
    ("Golpe hacia abajo", "clic izquierdo en el aire"),
    ("Giro", "clic derecho  /  E"),
    ("Beber", "Q"),
    ("Pausa", "Esc"),
    ("Ver hitboxes", "F3"),
    ("Bloquear / ocultar cursor", "Tab"),
    ("Reiniciar", "Enter (al morir o ganar)"),
]


def show_controles():
    if PAUSA and captura is not None:
        game_surface.blit(captura, (0, 0))
        game_surface.blit(velo, (0, 0))
    else:
        dibujar_fondo()
    panel = pygame.Surface((960, 670), pygame.SRCALPHA)
    pygame.draw.rect(panel, (10, 10, 30, 170), panel.get_rect(), border_radius=24)
    game_surface.blit(panel, panel.get_rect(center=(width // 2, 440)))
    dibujar_texto("CONTROLES", blanco, 110)
    for i, (accion, tecla) in enumerate(LISTA_CONTROLES):
        y = 190 + i * 42
        a = fuente_peq.render(accion, True, amarillo)
        t = fuente_peq.render(tecla, True, blanco)
        game_surface.blit(a, a.get_rect(midright=(width // 2 - 20, y)))
        game_surface.blit(t, t.get_rect(midleft=(width // 2 + 20, y)))
    dibujar_boton_caja("volver", boton_volver_controles)


def show_pausa():
    if captura is not None:
        game_surface.blit(captura, (0, 0))
    game_surface.blit(velo, (0, 0))
    panel = pygame.Surface((560, 420), pygame.SRCALPHA)
    pygame.draw.rect(panel, (10, 10, 30, 180), panel.get_rect(), border_radius=24)
    game_surface.blit(panel, panel.get_rect(center=(width // 2, 480)))
    titulo = titulo_font.render("PAUSA", True, amarillo)
    game_surface.blit(titulo, titulo.get_rect(center=(width // 2, 300)))
    for op in opciones_pausa:
        dibujar_boton_caja(op["texto"], op["rect"])


print("---------- BUCLE PRINCIPAL: EVENTOS, CURSOR Y PANTALLA ----------")
def manejar_eventos():
    global RUN, JUGAR, AJUSTES, MUSICA, PAUSA, CONTROLES, MOSTRAR_HITBOX, CURSOR_BLOQUEADO
    global captura, modo, scroll, arrastrando, partida
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                MOSTRAR_HITBOX = not MOSTRAR_HITBOX
            if event.key == pygame.K_TAB:
                CURSOR_BLOQUEADO = not CURSOR_BLOQUEADO
            if event.key == pygame.K_RETURN and JUGAR and not PAUSA and partida.terminada:
                partida = Partida()
            if event.key == pygame.K_ESCAPE:
                if CONTROLES:
                    CONTROLES = False
                elif MUSICA:
                    MUSICA = False
                elif AJUSTES:
                    AJUSTES = False
                elif JUGAR and PAUSA:
                    PAUSA = False
                    partida.jugador.enfriamiento = 0.3
                elif JUGAR:
                    captura = game_surface.copy()
                    PAUSA = True
                else:
                    RUN = False
            if not JUGAR and not AJUSTES and not CONTROLES:
                if event.key == pygame.K_1:
                    modo = "jugar"
                    JUGAR = True
                elif event.key == pygame.K_2:
                    modo = "ajustes"
                    AJUSTES = True
                elif event.key == pygame.K_3:
                    CONTROLES = True
        if event.type == pygame.MOUSEWHEEL and AJUSTES and MUSICA:
            maximo = max(0, len(canciones) - FILAS_VISIBLES)
            scroll = max(0, min(maximo, scroll - event.y))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and (not JUGAR or PAUSA):
            click = pos_en_juego(event.pos)
            if CONTROLES:
                if boton_volver_controles.collidepoint(click):
                    CONTROLES = False
            elif not AJUSTES and JUGAR:
                for op in opciones_pausa:
                    if op["rect"].collidepoint(click):
                        if op["modo"] == "reanudar":
                            PAUSA = False
                            partida.jugador.enfriamiento = 0.3
                        elif op["modo"] == "controles":
                            CONTROLES = True
                        elif op["modo"] == "ajustes":
                            AJUSTES = True
                        else:
                            JUGAR = False
                            PAUSA = False
                            partida = Partida()
            elif not AJUSTES:
                for op in opciones:
                    if op["rect"].collidepoint(click):
                        if op["modo"] == "ajustes":
                            modo, AJUSTES = op["modo"], True
                        elif op["modo"] == "controles":
                            CONTROLES = True
                        elif op["modo"] == "salir":
                            RUN = False
                        else:
                            modo, JUGAR = op["modo"], True
            elif MUSICA:
                click_musica(click)
            else:
                for clave, barra in sliders.items():
                    if barra.inflate(40, 40).collidepoint(click):
                        arrastrando = clave
                for clave, caja in interruptores.items():
                    if caja.collidepoint(click):
                        ajustes[clave] = not ajustes[clave]
                        if clave == "pantalla_completa":
                            aplicar_pantalla()
                if boton_canciones.collidepoint(click):
                    MUSICA = True
                if zona_boton("volver", 710).collidepoint(click):
                    AJUSTES = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            arrastrando = None
    if AJUSTES and not MUSICA and arrastrando:
        barra = sliders[arrastrando]
        mx = pos_en_juego(pygame.mouse.get_pos())[0]
        ajustes[arrastrando] = max(0, min(1, (mx - barra.left) / barra.width))
        aplicar_volumen()


def estado_cursor():
    oculto = CURSOR_BLOQUEADO and JUGAR and not PAUSA and not AJUSTES and not CONTROLES
    pygame.mouse.set_visible(not oculto)
    pygame.event.set_grab(oculto)
    return oculto


def actualizar_y_dibujar(dt):
    cursor_oculto = estado_cursor()
    if CONTROLES:
        show_controles()
    elif AJUSTES and MUSICA:
        show_musica()
    elif AJUSTES:
        show_ajustes()
    elif JUGAR and PAUSA:
        show_pausa()
    elif not JUGAR:
        show_menu()
    else:
        partida.actualizar(dt, pygame.key.get_pressed())
        partida.dibujar(game_surface, cursor_oculto)
        if ajustes["mostrar_fps"]:
            fps = menu_font.render(f"FPS: {int(reloj.get_fps())}", True, blanco)
            game_surface.blit(fps, (20, 20))


print("---------- BUCLE PRINCIPAL ----------")
dt = 0
ANIMACIONES = cargar_animaciones()
mapa = Mapa(MAPA)
partida = Partida()
fuente_ayuda = pygame.font.Font(None, 26)
ayuda_juego = [fuente_ayuda.render(t, True, blanco) for t in (
    "WASD mover   Shift correr   Espacio saltar   R rodar   C agacharse   Q beber",
    "Clic izq atacar (combo)   Clic der / E giro   en el aire: atacar = golpe hacia abajo   F3 ver hitboxes",
)]
aplicar_volumen()
siguiente()
while RUN:
    manejar_eventos()
    revisar_musica()
    actualizar_y_dibujar(dt)
    blit_scaled()
    pygame.display.flip()
    dt = reloj.tick(60) / 1000


pygame.quit()
sys.exit()