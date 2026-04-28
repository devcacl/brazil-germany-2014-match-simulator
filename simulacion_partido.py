"""
╔══════════════════════════════════════════════════════════════════╗
║  SIMULADOR BRASIL vs ALEMANIA - Copa Mundial 2014               ║
║  Interfaz Gráfica PyQt6 con Cancha Interactiva                  ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import math
import random
import numpy as np
from scipy import stats
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSlider, QTabWidget, QTableWidget,
    QTableWidgetItem, QGroupBox, QSplitter, QProgressBar,
    QSpinBox, QFrame, QScrollArea, QGridLayout, QComboBox,
    QTextEdit, QSizePolicy
)
from PyQt6.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QPointF, QRectF, QEasingCurve,
    QPropertyAnimation, QObject, pyqtProperty
)
from PyQt6.QtGui import (
    QPainter, QPen, QBrush, QColor, QFont, QPainterPath,
    QLinearGradient, QRadialGradient, QFontMetrics, QPixmap,
    QPalette, QConicalGradient
)

# ─────────────────────────────────────────────────────────────────
#  PALETA DE COLORES  (modo oscuro moderno)
# ─────────────────────────────────────────────────────────────────
C = {
    "bg":        "#0D1117",
    "panel":     "#161B22",
    "card":      "#1C2128",
    "border":    "#30363D",
    "accent":    "#238636",
    "accent2":   "#1F6FEB",
    "brasil":    "#009C3B",
    "brasil_l":  "#00C44A",
    "ale":       "#FFFFFF",
    "ale_l":     "#DDDDDD",
    "gold":      "#F7CC65",
    "red":       "#DA3633",
    "text":      "#E6EDF3",
    "text2":     "#8B949E",
    "grass1":    "#1A5C2A",
    "grass2":    "#1D6830",
    "line":      "rgba(255,255,255,180)",
    "gol_flash": "#FFD700",
}

STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {C['bg']};
    color: {C['text']};
    font-family: 'Segoe UI', 'SF Pro Display', Arial, sans-serif;
}}
QGroupBox {{
    background-color: {C['panel']};
    border: 1px solid {C['border']};
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 8px;
    font-weight: bold;
    font-size: 11px;
    color: {C['text2']};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: {C['text']};
}}
QPushButton {{
    background-color: {C['accent']};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 18px;
    font-weight: bold;
    font-size: 12px;
    min-height: 34px;
}}
QPushButton:hover {{
    background-color: #2EA043;
}}
QPushButton:pressed {{
    background-color: #1A7A2A;
}}
QPushButton:disabled {{
    background-color: {C['border']};
    color: {C['text2']};
}}
QPushButton#btnSecondary {{
    background-color: {C['accent2']};
}}
QPushButton#btnSecondary:hover {{
    background-color: #388BFD;
}}
QPushButton#btnDanger {{
    background-color: {C['red']};
}}
QPushButton#btnDanger:hover {{
    background-color: #F85149;
}}
QSlider::groove:horizontal {{
    height: 4px;
    background: {C['border']};
    border-radius: 2px;
}}
QSlider::handle:horizontal {{
    width: 16px;
    height: 16px;
    margin: -6px 0;
    background: {C['accent']};
    border-radius: 8px;
}}
QSlider::sub-page:horizontal {{
    background: {C['accent']};
    border-radius: 2px;
}}
QTabWidget::pane {{
    border: 1px solid {C['border']};
    background-color: {C['panel']};
    border-radius: 0 8px 8px 8px;
}}
QTabBar::tab {{
    background-color: {C['card']};
    color: {C['text2']};
    border: 1px solid {C['border']};
    padding: 8px 16px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}}
QTabBar::tab:selected {{
    background-color: {C['panel']};
    color: {C['text']};
    border-bottom-color: {C['panel']};
}}
QTableWidget {{
    background-color: {C['card']};
    border: 1px solid {C['border']};
    border-radius: 6px;
    gridline-color: {C['border']};
    selection-background-color: {C['accent2']};
    font-size: 11px;
}}
QTableWidget::item {{
    padding: 6px 10px;
    border-bottom: 1px solid {C['border']};
}}
QHeaderView::section {{
    background-color: {C['panel']};
    color: {C['text2']};
    font-weight: bold;
    font-size: 11px;
    padding: 8px;
    border: none;
    border-bottom: 1px solid {C['border']};
}}
QProgressBar {{
    background-color: {C['border']};
    border-radius: 4px;
    height: 8px;
    text-align: center;
}}
QProgressBar::chunk {{
    background-color: {C['accent']};
    border-radius: 4px;
}}
QSpinBox, QComboBox {{
    background-color: {C['card']};
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 5px;
    padding: 5px 8px;
    font-size: 12px;
    min-height: 28px;
}}
QSpinBox::up-button, QSpinBox::down-button {{
    background-color: {C['border']};
    border-radius: 3px;
    width: 20px;
}}
QScrollArea {{
    border: none;
    background-color: transparent;
}}
QTextEdit {{
    background-color: {C['card']};
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 6px;
    font-family: 'Cascadia Code', 'Consolas', monospace;
    font-size: 11px;
    padding: 8px;
}}
QLabel#titleLabel {{
    font-size: 22px;
    font-weight: bold;
    color: {C['gold']};
}}
QLabel#subtitleLabel {{
    font-size: 12px;
    color: {C['text2']};
}}
QLabel#scoreLabel {{
    font-size: 48px;
    font-weight: bold;
    color: {C['text']};
}}
QLabel#teamLabel {{
    font-size: 16px;
    font-weight: bold;
}}
QLabel#minuteLabel {{
    font-size: 28px;
    font-weight: bold;
    color: {C['gold']};
}}
QFrame#divider {{
    background-color: {C['border']};
    max-height: 1px;
    min-height: 1px;
}}
"""

# ─────────────────────────────────────────────────────────────────
#  MOTOR DE SIMULACIÓN (basado en el notebook)
# ─────────────────────────────────────────────────────────────────
EVENTOS_DATA = {
    'GOL':   {'Brasil': 0,  'Alemania': 5},
    'TIR':   {'Brasil': 0,  'Alemania': 7},
    'PER':   {'Brasil': 4,  'Alemania': 5},
    'REC':   {'Brasil': 34, 'Alemania': 33},
    'FAL':   {'Brasil': 3,  'Alemania': 2},
    'SAB':   {'Brasil': 10, 'Alemania': 14},
    'COR':   {'Brasil': 2,  'Alemania': 2},
    'SAP':   {'Brasil': 2,  'Alemania': 3},
    'FDJ':   {'Brasil': 2,  'Alemania': 0},
}

EVENTOS_REALES = [
    (0,  'INI', 'Ambos'),   (1,  'COR', 'Alemania'), (2,  'TIR', 'Alemania'),
    (3,  'PER', 'Alemania'),(4,  'REC', 'Brasil'),    (5,  'PER', 'Brasil'),
    (6,  'REC', 'Alemania'),(7,  'TIR', 'Alemania'),  (9,  'FAL', 'Brasil'),
    (11, 'COR', 'Alemania'),(11, 'GOL', 'Alemania'),  (12, 'INI', 'Brasil'),
    (14, 'PER', 'Brasil'),  (15, 'REC', 'Alemania'),  (16, 'TIR', 'Alemania'),
    (18, 'COR', 'Alemania'),(20, 'PER', 'Brasil'),    (21, 'REC', 'Alemania'),
    (23, 'GOL', 'Alemania'),(24, 'GOL', 'Alemania'),  (25, 'GOL', 'Alemania'),
    (26, 'INI', 'Brasil'),  (29, 'GOL', 'Alemania'),  (30, 'INI', 'Brasil'),
    (36, 'TIR', 'Alemania'),(38, 'SAB', 'Brasil'),    (40, 'TIR', 'Alemania'),
    (43, 'SAP', 'Brasil'),  (45, 'INI', 'Ambos'),
]
GOLES_REALES = [11, 23, 24, 25, 29]

EMOJIS = {'GOL': '⚽', 'TIR': '🎯', 'PER': '❌', 'REC': '🔄',
          'FAL': '🟨', 'SAB': '🟡', 'COR': '🚩', 'SAP': '🔄', 'FDJ': '⚠️', 'INI': '▶️'}
NOMBRES = {'GOL': 'GOL', 'TIR': 'Disparo', 'PER': 'Pérdida', 'REC': 'Recuperación',
           'FAL': 'Falta', 'SAB': 'Saque banda', 'COR': 'Córner',
           'SAP': 'Saque portería', 'FDJ': 'Fuera de juego', 'INI': 'Inicio'}

COLORES_EQ = {'Brasil': C['brasil'], 'Alemania': '#4A90D9', 'Ambos': C['gold']}

WEIBULL_PARAMS = (1.2, 0.0, 1.05)  # shape, loc, scale (ajustados del notebook)


class SimulationEngine:
    def __init__(self):
        self._prepare_probs()

    def _prepare_probs(self):
        datos = {e: v['Brasil'] + v['Alemania'] for e, v in EVENTOS_DATA.items()}
        total = sum(datos.values())
        self.prob_evento = {e: v / total for e, v in datos.items()}
        self.eventos_list = list(self.prob_evento.keys())
        self.prob_weights = [self.prob_evento[e] for e in self.eventos_list]
        self.prob_equipo = {}
        for ev, vals in EVENTOS_DATA.items():
            t = vals['Brasil'] + vals['Alemania']
            if t == 0:
                self.prob_equipo[ev] = {'Brasil': 0.5, 'Alemania': 0.5}
            else:
                self.prob_equipo[ev] = {'Brasil': vals['Brasil'] / t, 'Alemania': vals['Alemania'] / t}

    def _sample_time(self, rng):
        for _ in range(200):
            try:
                v = stats.weibull_min.rvs(*WEIBULL_PARAMS, random_state=rng)
                if np.isfinite(v) and 0.05 < v < 20:
                    return float(v)
            except Exception:
                pass
        return 0.5

    def simulate(self, seed=None, duracion=45):
        rng = np.random.default_rng(seed)
        minuto = 0.0
        marcador = {'Brasil': 0, 'Alemania': 0}
        eventos = []
        while True:
            dt = self._sample_time(rng)
            minuto += dt
            if minuto > duracion:
                break
            ev = rng.choice(self.eventos_list, p=self.prob_weights)
            p_local = self.prob_equipo[ev]['Brasil']
            equipo = 'Brasil' if rng.random() < p_local else 'Alemania'
            eventos.append({'minuto': round(minuto, 2), 'evento': ev, 'equipo': equipo})
            if ev == 'GOL':
                marcador[equipo] += 1
        return eventos, marcador

    def run_montecarlo(self, n=5000, progress_cb=None):
        resultados = []
        exactas = 0
        mejor = None
        mejor_err = float('inf')
        target = {'Brasil': 0, 'Alemania': 5}
        for seed in range(n):
            evs, marc = self.simulate(seed=seed)
            if marc == target:
                exactas += 1
            err = (abs(marc['Brasil'] - target['Brasil']) +
                   abs(marc['Alemania'] - target['Alemania']))
            resultados.append({'seed': seed, 'marcador': marc, 'eventos': evs, 'error': err})
            if err < mejor_err:
                mejor_err = err
                mejor = resultados[-1]
            if progress_cb and seed % 200 == 0:
                progress_cb(int(seed * 100 / n))
        return resultados, mejor, exactas


# ─────────────────────────────────────────────────────────────────
#  WIDGET: CANCHA DE FÚTBOL
# ─────────────────────────────────────────────────────────────────
class CanchaWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 380)
        self.eventos_activos = []   # lista de dicts con pos, color, texto, alpha
        self.pelota = None          # (x_norm, y_norm) 0..1
        self.pelota_alpha = 0
        self._anim_timer = QTimer(self)
        self._anim_timer.timeout.connect(self._update_anim)
        self._anim_timer.start(40)
        self._flash_gol = 0         # 0..255 para flash dorado

    def add_evento(self, ev_type, equipo, minuto):
        # posición en el campo según equipo y evento
        x, y = self._pos_for_event(ev_type, equipo)
        color = QColor(COLORES_EQ.get(equipo, '#FFFFFF'))
        if ev_type == 'GOL':
            self._flash_gol = 255
        self.eventos_activos.append({
            'x': x, 'y': y, 'color': color,
            'texto': f"{EMOJIS.get(ev_type, '•')} {NOMBRES.get(ev_type, ev_type)}",
            'alpha': 255, 'radio': 20, 'ev': ev_type, 'min': minuto
        })
        self.pelota = (x, y)
        self.pelota_alpha = 255
        if len(self.eventos_activos) > 12:
            self.eventos_activos.pop(0)
        self.update()

    def clear(self):
        self.eventos_activos.clear()
        self.pelota = None
        self._flash_gol = 0
        self.update()

    def _pos_for_event(self, ev, equipo):
        """Devuelve posición normalizada (0-1) en la cancha."""
        rnd = random.Random(hash((ev, equipo, random.random())))
        if equipo == 'Alemania':
            base_x = 0.6 + rnd.uniform(0, 0.35)
        elif equipo == 'Brasil':
            base_x = 0.05 + rnd.uniform(0, 0.35)
        else:
            base_x = 0.45 + rnd.uniform(-0.05, 0.1)

        if ev == 'GOL':
            base_x = 0.93 if equipo == 'Alemania' else 0.07
            base_y = 0.5 + rnd.uniform(-0.05, 0.05)
        elif ev == 'COR':
            base_y = rnd.choice([0.02, 0.98])
            base_x = 0.97 if equipo == 'Alemania' else 0.03
        else:
            base_y = 0.1 + rnd.uniform(0, 0.8)

        return (min(max(base_x, 0.02), 0.98), min(max(base_y, 0.05), 0.95))

    def _update_anim(self):
        changed = False
        for ev in self.eventos_activos:
            if ev['alpha'] > 0:
                ev['alpha'] = max(0, ev['alpha'] - 4)
                changed = True
        if self._flash_gol > 0:
            self._flash_gol = max(0, self._flash_gol - 8)
            changed = True
        if self.pelota_alpha > 0:
            self.pelota_alpha = max(0, self.pelota_alpha - 2)
            changed = True
        if changed:
            self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        W, H = self.width(), self.height()
        PAD = 30

        # ── Fondo degradado verde cancha ──
        grad = QLinearGradient(0, 0, 0, H)
        grad.setColorAt(0.0, QColor(C['grass1']))
        grad.setColorAt(1.0, QColor(C['grass2']))
        p.fillRect(0, 0, W, H, grad)

        # ── Franjas de cancha (efecto césped) ──
        p.setOpacity(0.07)
        franja_w = (W - 2*PAD) / 10
        for i in range(10):
            if i % 2 == 0:
                p.fillRect(int(PAD + i*franja_w), PAD, int(franja_w), H - 2*PAD,
                           QBrush(QColor('white')))
        p.setOpacity(1.0)

        # ── Flash de gol ──
        if self._flash_gol > 0:
            c = QColor(C['gol_flash'])
            c.setAlpha(min(80, self._flash_gol))
            p.fillRect(0, 0, W, H, c)

        # ── Líneas de la cancha ──
        pen = QPen(QColor(255, 255, 255, 160), 1.8)
        p.setPen(pen)
        p.setBrush(Qt.BrushStyle.NoBrush)

        # Borde
        p.drawRect(PAD, PAD, W - 2*PAD, H - 2*PAD)
        # Línea central
        p.drawLine(W//2, PAD, W//2, H - PAD)
        # Círculo central
        r_circ = int(min(W, H) * 0.11)
        p.drawEllipse(W//2 - r_circ, H//2 - r_circ, 2*r_circ, 2*r_circ)
        p.drawPoint(W//2, H//2)

        # Áreas grandes
        aw = int((W - 2*PAD) * 0.14)
        ah = int((H - 2*PAD) * 0.55)
        ay = PAD + (H - 2*PAD - ah)//2
        p.drawRect(PAD, ay, aw, ah)                       # izq
        p.drawRect(W - PAD - aw, ay, aw, ah)             # der

        # Áreas chicas
        sw = int((W - 2*PAD) * 0.06)
        sh = int((H - 2*PAD) * 0.28)
        sy = PAD + (H - 2*PAD - sh)//2
        p.drawRect(PAD, sy, sw, sh)
        p.drawRect(W - PAD - sw, sy, sw, sh)

        # Portería izq
        gw = 8
        gh = int((H - 2*PAD) * 0.16)
        gy = H//2 - gh//2
        p.setPen(QPen(QColor(255, 255, 255, 220), 3))
        p.drawRect(PAD - gw, gy, gw, gh)
        p.setPen(pen)
        # Portería der
        p.drawRect(W - PAD, gy, gw, gh)
        p.setPen(pen)

        # ── Semírculos de área ──
        p.drawArc(int(PAD + aw - r_circ//2), H//2 - r_circ//2, r_circ, r_circ,
                  -90*16, 180*16)
        p.drawArc(int(W - PAD - aw - r_circ//2), H//2 - r_circ//2, r_circ, r_circ,
                  90*16, 180*16)

        # ── Etiquetas de equipos ──
        p.setOpacity(0.7)
        font_eq = QFont('Arial', 10, QFont.Weight.Bold)
        p.setFont(font_eq)
        p.setPen(QColor(C['brasil']))
        p.drawText(PAD + 6, PAD - 8, "🇧🇷 BRASIL")
        p.setPen(QColor('#4A90D9'))
        metrics = QFontMetrics(font_eq)
        txt = "ALEMANIA 🇩🇪"
        p.drawText(W - PAD - metrics.horizontalAdvance(txt) - 6, PAD - 8, txt)
        p.setOpacity(1.0)

        # ── Bola (última posición) ──
        if self.pelota and self.pelota_alpha > 0:
            px = int(PAD + self.pelota[0] * (W - 2*PAD))
            py = int(PAD + self.pelota[1] * (H - 2*PAD))
            ball_r = 10
            p.setOpacity(self.pelota_alpha / 255)
            # Sombra
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QBrush(QColor(0, 0, 0, 80)))
            p.drawEllipse(px - ball_r + 3, py - ball_r + 4, ball_r*2, ball_r*2)
            # Balón
            ball_grad = QRadialGradient(px - 3, py - 3, ball_r*2)
            ball_grad.setColorAt(0, QColor('#FFFFFF'))
            ball_grad.setColorAt(0.6, QColor('#CCCCCC'))
            ball_grad.setColorAt(1, QColor('#888888'))
            p.setBrush(QBrush(ball_grad))
            p.setPen(QPen(QColor(80, 80, 80), 1))
            p.drawEllipse(px - ball_r, py - ball_r, ball_r*2, ball_r*2)
            p.setOpacity(1.0)

        # ── Eventos activos (puntos animados) ──
        for ev in reversed(self.eventos_activos):
            if ev['alpha'] <= 0:
                continue
            alpha = ev['alpha']
            px = int(PAD + ev['x'] * (W - 2*PAD))
            py = int(PAD + ev['y'] * (H - 2*PAD))
            r = int(ev['radio'] * (1 + (255 - alpha) / 255 * 0.6))

            # Halo
            halo = QColor(ev['color'])
            halo.setAlpha(int(alpha * 0.35))
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QBrush(halo))
            p.drawEllipse(px - r, py - r, 2*r, 2*r)

            # Círculo principal
            dot = QColor(ev['color'])
            dot.setAlpha(alpha)
            p.setBrush(QBrush(dot))
            p.setPen(QPen(QColor(255, 255, 255, min(alpha, 150)), 1.5))
            r2 = max(6, r - 6)
            p.drawEllipse(px - r2, py - r2, 2*r2, 2*r2)

            # Etiqueta
            if alpha > 120:
                p.setOpacity(alpha / 255)
                font_ev = QFont('Arial', 9)
                p.setFont(font_ev)
                p.setPen(QColor(255, 255, 255, alpha))
                bg = QColor(0, 0, 0, int(alpha * 0.7))
                label = ev['texto']
                fm = QFontMetrics(font_ev)
                tw = fm.horizontalAdvance(label) + 8
                p.setBrush(QBrush(bg))
                p.setPen(Qt.PenStyle.NoPen)
                p.drawRoundedRect(px - tw//2, py - r2 - 20, tw, 16, 4, 4)
                p.setPen(QColor(255, 255, 255, alpha))
                p.drawText(px - tw//2 + 4, py - r2 - 7, label)
                p.setOpacity(1.0)

        p.end()


# ─────────────────────────────────────────────────────────────────
#  WIDGET: GRÁFICA DE GOLES
# ─────────────────────────────────────────────────────────────────
class GraficaGolesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(200)
        self.goles_reales = GOLES_REALES
        self.goles_sim = []
        self.minuto_actual = 0

    def set_goles_sim(self, goles):
        self.goles_sim = sorted(goles)
        self.update()

    def set_minuto(self, m):
        self.minuto_actual = m
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        W, H = self.width(), self.height()
        PAD_L, PAD_R, PAD_T, PAD_B = 50, 20, 20, 35

        p.fillRect(0, 0, W, H, QColor(C['card']))

        cw = W - PAD_L - PAD_R
        ch = H - PAD_T - PAD_B
        max_goles = max(6, len(self.goles_reales) + 1, len(self.goles_sim) + 1)

        def tx(minuto):
            return int(PAD_L + minuto / 45 * cw)

        def ty(goles):
            return int(PAD_T + ch - goles / max_goles * ch)

        # Grid
        p.setPen(QPen(QColor(C['border']), 1, Qt.PenStyle.DashLine))
        for i in range(0, 7):
            yy = ty(i)
            if PAD_T <= yy <= PAD_T + ch:
                p.drawLine(PAD_L, yy, PAD_L + cw, yy)
        for m in [0, 9, 18, 27, 36, 45]:
            xx = tx(m)
            p.drawLine(xx, PAD_T, xx, PAD_T + ch)

        # Ejes
        p.setPen(QPen(QColor(C['text2']), 1.5))
        p.drawLine(PAD_L, PAD_T, PAD_L, PAD_T + ch)
        p.drawLine(PAD_L, PAD_T + ch, PAD_L + cw, PAD_T + ch)

        # Etiquetas
        font_s = QFont('Arial', 8)
        p.setFont(font_s)
        p.setPen(QColor(C['text2']))
        for m in [0, 9, 18, 27, 36, 45]:
            p.drawText(tx(m) - 8, PAD_T + ch + 15, f"{m}'")
        for i in range(0, max_goles):
            if i <= 6:
                p.drawText(PAD_L - 22, ty(i) + 4, str(i))

        def draw_step_line(tiempos, color_hex, dash=False):
            color = QColor(color_hex)
            pen = QPen(color, 2.5)
            if dash:
                pen.setStyle(Qt.PenStyle.DashLine)
            p.setPen(pen)
            puntos = [(0, 0)] + [(t, i+1) for i, t in enumerate(sorted(tiempos))] + [(45, len(tiempos))]
            for i in range(len(puntos) - 1):
                x1, y1 = tx(puntos[i][0]), ty(puntos[i][1])
                x2, y2 = tx(puntos[i+1][0]), ty(puntos[i][1])
                x3, y3 = tx(puntos[i+1][0]), ty(puntos[i+1][1])
                p.drawLine(x1, y1, x2, y1)
                p.drawLine(x2, y1, x3, y3)

            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QBrush(color))
            for i, t in enumerate(sorted(tiempos)):
                cx_, cy_ = tx(t), ty(i+1)
                p.drawEllipse(cx_ - 5, cy_ - 5, 10, 10)

        draw_step_line(self.goles_reales, C['gold'])
        if self.goles_sim:
            draw_step_line(self.goles_sim, '#4A90D9', dash=True)

        # Línea de minuto actual
        if 0 < self.minuto_actual <= 45:
            p.setPen(QPen(QColor(C['red']), 1.5, Qt.PenStyle.DotLine))
            xx = tx(self.minuto_actual)
            p.drawLine(xx, PAD_T, xx, PAD_T + ch)

        # Leyenda
        ley_x = PAD_L + 4
        ley_y = PAD_T + 6
        p.setFont(QFont('Arial', 8))
        p.setPen(QPen(QColor(C['gold']), 2))
        p.drawLine(ley_x, ley_y + 4, ley_x + 18, ley_y + 4)
        p.setPen(QColor(C['gold']))
        p.drawText(ley_x + 22, ley_y + 8, "Real")
        p.setPen(QPen(QColor('#4A90D9'), 2, Qt.PenStyle.DashLine))
        p.drawLine(ley_x + 60, ley_y + 4, ley_x + 78, ley_y + 4)
        p.setPen(QColor('#4A90D9'))
        p.drawText(ley_x + 82, ley_y + 8, "Simulada")
        p.end()


# ─────────────────────────────────────────────────────────────────
#  THREAD DE SIMULACIÓN (no bloquea la UI)
# ─────────────────────────────────────────────────────────────────
class MontecarloThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(list, dict, int)

    def __init__(self, engine, n):
        super().__init__()
        self.engine = engine
        self.n = n

    def run(self):
        resultados, mejor, exactas = self.engine.run_montecarlo(
            self.n, progress_cb=lambda v: self.progress.emit(v)
        )
        self.finished.emit(resultados, mejor, exactas)


# ─────────────────────────────────────────────────────────────────
#  VENTANA PRINCIPAL
# ─────────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.engine = SimulationEngine()
        self.sim_timer = QTimer(self)
        self.sim_timer.timeout.connect(self._step_simulation)
        self.sim_eventos = []
        self.sim_step = 0
        self.sim_velocidad = 600
        self.marcador_sim = {'Brasil': 0, 'Alemania': 0}
        self.mc_resultados = []
        self.mc_mejor = None
        self.mc_exactas = 0
        self._build_ui()
        self.setWindowTitle("⚽  Simulador Brasil vs Alemania — Copa Mundial 2014")
        self.resize(1300, 820)
        self._load_real_game()

    def _build_ui(self):
        self.setStyleSheet(STYLESHEET)
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(0)
        root.setContentsMargins(0, 0, 0, 0)

        # ── Header ──
        header = self._make_header()
        root.addWidget(header)

        # ── Splitter principal ──
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        # Panel izquierdo: controles + cancha
        left = self._make_left_panel()
        splitter.addWidget(left)

        # Panel derecho: tabs
        right = self._make_right_panel()
        splitter.addWidget(right)

        splitter.setSizes([760, 540])
        root.addWidget(splitter)

        # ── Status bar ──
        self.statusBar().setStyleSheet(
            f"background:{C['panel']};color:{C['text2']};border-top:1px solid {C['border']};")
        self.statusBar().showMessage("  Listo — Selecciona un modo de simulación para comenzar")

    def _make_header(self):
        w = QWidget()
        w.setFixedHeight(80)
        w.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #0D2A1A, stop:0.5 {C['panel']}, stop:1 #0A1F35);
            border-bottom: 1px solid {C['border']};
        """)
        lay = QHBoxLayout(w)
        lay.setContentsMargins(20, 0, 20, 0)

        # Título
        title_box = QVBoxLayout()
        lbl_t = QLabel("⚽  SIMULADOR DE PARTIDO")
        lbl_t.setObjectName("titleLabel")
        lbl_s = QLabel("Brasil vs Alemania · Copa Mundial 2014 · Primer Tiempo")
        lbl_s.setObjectName("subtitleLabel")
        title_box.addWidget(lbl_t)
        title_box.addWidget(lbl_s)
        lay.addLayout(title_box)
        lay.addStretch()

        # Marcador
        score_box = QHBoxLayout()
        score_box.setSpacing(10)

        self.lbl_team_bra = QLabel("🇧🇷 Brasil")
        self.lbl_team_bra.setObjectName("teamLabel")
        self.lbl_team_bra.setStyleSheet(f"color:{C['brasil']};")

        self.lbl_score = QLabel("0 — 0")
        self.lbl_score.setObjectName("scoreLabel")
        self.lbl_score.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_team_ale = QLabel("Alemania 🇩🇪")
        self.lbl_team_ale.setObjectName("teamLabel")
        self.lbl_team_ale.setStyleSheet("color:#4A90D9;")

        score_box.addWidget(self.lbl_team_bra)
        score_box.addWidget(self.lbl_score)
        score_box.addWidget(self.lbl_team_ale)
        lay.addLayout(score_box)
        lay.addStretch()

        # Minuto
        min_box = QVBoxLayout()
        min_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_min_title = QLabel("MINUTO")
        lbl_min_title.setStyleSheet(f"color:{C['text2']};font-size:10px;font-weight:bold;")
        lbl_min_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_minute = QLabel("0'")
        self.lbl_minute.setObjectName("minuteLabel")
        self.lbl_minute.setAlignment(Qt.AlignmentFlag.AlignCenter)
        min_box.addWidget(lbl_min_title)
        min_box.addWidget(self.lbl_minute)
        lay.addLayout(min_box)
        return w

    def _make_left_panel(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(12, 12, 6, 12)
        lay.setSpacing(10)

        # ── Cancha ──
        cancha_box = QGroupBox("⚽  Cancha — Vista en Vivo")
        cancha_lay = QVBoxLayout(cancha_box)
        self.cancha = CanchaWidget()
        cancha_lay.addWidget(self.cancha)
        lay.addWidget(cancha_box, stretch=3)

        # ── Gráfica goles ──
        graf_box = QGroupBox("📈  Evolución de Goles")
        graf_lay = QVBoxLayout(graf_box)
        self.grafica_goles = GraficaGolesWidget()
        graf_lay.addWidget(self.grafica_goles)
        lay.addWidget(graf_box, stretch=2)

        # ── Controles ──
        ctrl_box = QGroupBox("🎮  Controles de Simulación")
        ctrl_lay = QVBoxLayout(ctrl_box)
        ctrl_lay.setSpacing(8)

        # Fila 1: botones principales
        row1 = QHBoxLayout()
        self.btn_play_real = QPushButton("▶  Reproducir Partido Real")
        self.btn_play_real.setObjectName("btnSecondary")
        self.btn_play_real.clicked.connect(self._play_real_game)

        self.btn_sim_one = QPushButton("🎲  Simular Partido")
        self.btn_sim_one.clicked.connect(self._simulate_one)

        self.btn_stop = QPushButton("⏹  Detener")
        self.btn_stop.setObjectName("btnDanger")
        self.btn_stop.clicked.connect(self._stop_sim)
        self.btn_stop.setEnabled(False)

        row1.addWidget(self.btn_play_real)
        row1.addWidget(self.btn_sim_one)
        row1.addWidget(self.btn_stop)
        ctrl_lay.addLayout(row1)

        # Fila 2: velocidad y seed
        row2 = QHBoxLayout()
        lbl_vel = QLabel("Velocidad:")
        lbl_vel.setStyleSheet(f"color:{C['text2']};font-size:11px;")
        self.slider_vel = QSlider(Qt.Orientation.Horizontal)
        self.slider_vel.setRange(1, 10)
        self.slider_vel.setValue(5)
        self.slider_vel.valueChanged.connect(self._update_velocity)
        self.lbl_vel_val = QLabel("Normal")
        self.lbl_vel_val.setStyleSheet(f"color:{C['gold']};font-size:11px;min-width:60px;")

        row2.addWidget(lbl_vel)
        row2.addWidget(self.slider_vel)
        row2.addWidget(self.lbl_vel_val)

        lbl_seed = QLabel("  Seed:")
        lbl_seed.setStyleSheet(f"color:{C['text2']};font-size:11px;")
        self.spin_seed = QSpinBox()
        self.spin_seed.setRange(-1, 99999)
        self.spin_seed.setValue(-1)
        self.spin_seed.setSpecialValueText("Aleatorio")
        self.spin_seed.setFixedWidth(110)
        row2.addWidget(lbl_seed)
        row2.addWidget(self.spin_seed)
        ctrl_lay.addLayout(row2)

        lay.addWidget(ctrl_box)
        return w

    def _make_right_panel(self):
        tabs = QTabWidget()
        tabs.addTab(self._tab_eventos(), "📋  Eventos")
        tabs.addTab(self._tab_montecarlo(), "🎲  Monte Carlo")
        tabs.addTab(self._tab_stats(), "📊  Estadísticas")
        tabs.addTab(self._tab_info(), "ℹ️  Acerca del Modelo")
        return tabs

    def _tab_eventos(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(10, 10, 10, 10)

        # Última acción
        last_box = QGroupBox("Último Evento")
        last_lay = QHBoxLayout(last_box)
        self.lbl_last_ev = QLabel("—")
        self.lbl_last_ev.setStyleSheet(f"font-size:15px;font-weight:bold;color:{C['gold']};")
        last_lay.addWidget(self.lbl_last_ev)
        lay.addWidget(last_box)

        # Tabla eventos
        self.tabla_eventos = QTableWidget(0, 4)
        self.tabla_eventos.setHorizontalHeaderLabels(["Min'", "Tipo", "Evento", "Equipo"])
        self.tabla_eventos.horizontalHeader().setStretchLastSection(True)
        self.tabla_eventos.setColumnWidth(0, 50)
        self.tabla_eventos.setColumnWidth(1, 44)
        self.tabla_eventos.setColumnWidth(2, 130)
        self.tabla_eventos.verticalHeader().setVisible(False)
        self.tabla_eventos.setAlternatingRowColors(True)
        self.tabla_eventos.setStyleSheet(self.tabla_eventos.styleSheet() +
            f"alternate-background-color:{C['panel']};")
        lay.addWidget(self.tabla_eventos)
        return w

    def _tab_montecarlo(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(10, 10, 10, 10)
        lay.setSpacing(10)

        # Controles MC
        mc_ctrl = QGroupBox("Configuración Monte Carlo")
        mc_ctrl_lay = QGridLayout(mc_ctrl)

        mc_ctrl_lay.addWidget(QLabel("N° de simulaciones:"), 0, 0)
        self.spin_mc_n = QSpinBox()
        self.spin_mc_n.setRange(100, 50000)
        self.spin_mc_n.setValue(5000)
        self.spin_mc_n.setSingleStep(500)
        mc_ctrl_lay.addWidget(self.spin_mc_n, 0, 1)

        self.btn_run_mc = QPushButton("🚀  Ejecutar Monte Carlo")
        self.btn_run_mc.clicked.connect(self._run_montecarlo)
        mc_ctrl_lay.addWidget(self.btn_run_mc, 0, 2)

        self.bar_mc = QProgressBar()
        self.bar_mc.setVisible(False)
        mc_ctrl_lay.addWidget(self.bar_mc, 1, 0, 1, 3)
        lay.addWidget(mc_ctrl)

        # Resultados MC
        res_box = QGroupBox("Resultados Monte Carlo")
        res_lay = QGridLayout(res_box)

        def stat_card(title, value_id):
            box = QVBoxLayout()
            lbl_t = QLabel(title)
            lbl_t.setStyleSheet(f"color:{C['text2']};font-size:10px;")
            lbl_v = QLabel("—")
            lbl_v.setStyleSheet(f"color:{C['gold']};font-size:18px;font-weight:bold;")
            setattr(self, value_id, lbl_v)
            box.addWidget(lbl_t)
            box.addWidget(lbl_v)
            return box

        res_lay.addLayout(stat_card("Prob. marcador exacto 0-5", "lbl_mc_prob"), 0, 0)
        res_lay.addLayout(stat_card("Simulaciones exactas", "lbl_mc_exact"), 0, 1)
        res_lay.addLayout(stat_card("Mejor seed", "lbl_mc_seed"), 1, 0)
        res_lay.addLayout(stat_card("Error tiempos (min)", "lbl_mc_err"), 1, 1)
        lay.addWidget(res_box)

        # Distribución resultados (histograma simple)
        hist_box = QGroupBox("Distribución de Goles Alemania")
        hist_lay = QVBoxLayout(hist_box)
        self.mc_hist_widget = MCHistWidget()
        hist_lay.addWidget(self.mc_hist_widget)
        lay.addWidget(hist_box, stretch=1)

        # Botón: reproducir mejor sim
        self.btn_play_best = QPushButton("▶  Reproducir Mejor Simulación")
        self.btn_play_best.setObjectName("btnSecondary")
        self.btn_play_best.clicked.connect(self._play_best_sim)
        self.btn_play_best.setEnabled(False)
        lay.addWidget(self.btn_play_best)
        return w

    def _tab_stats(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(10, 10, 10, 10)
        lay.setSpacing(10)

        # Tabla frecuencias
        freq_box = QGroupBox("Frecuencia de Eventos (Datos Reales)")
        freq_lay = QVBoxLayout(freq_box)
        self.tabla_freq = QTableWidget(len(EVENTOS_DATA), 5)
        self.tabla_freq.setHorizontalHeaderLabels(["Evento", "Brasil", "Alemania", "Total", "% Brasil"])
        self.tabla_freq.verticalHeader().setVisible(False)
        self._fill_freq_table()
        freq_lay.addWidget(self.tabla_freq)
        lay.addWidget(freq_box)

        # Distribución Weibull info
        dist_box = QGroupBox("Distribución Seleccionada: Weibull")
        dist_lay = QGridLayout(dist_box)
        infos = [
            ("Forma (shape):", "1.20"), ("Escala (scale):", "1.05"),
            ("Media tiempos:", "~1.1 min"), ("Desv. est.:", "~0.93 min"),
            ("Test KS:", "Mejor AIC"), ("P-valor:", "0.089"),
        ]
        for i, (k, v) in enumerate(infos):
            r, c = i // 2, (i % 2) * 2
            lk = QLabel(k)
            lk.setStyleSheet(f"color:{C['text2']};font-size:11px;")
            lv = QLabel(v)
            lv.setStyleSheet(f"color:{C['gold']};font-size:12px;font-weight:bold;")
            dist_lay.addWidget(lk, r, c)
            dist_lay.addWidget(lv, r, c+1)
        lay.addWidget(dist_box)
        return w

    def _tab_info(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(10, 10, 10, 10)
        txt = QTextEdit()
        txt.setReadOnly(True)
        txt.setHtml("""
        <style>
            body { color: #E6EDF3; font-family: 'Segoe UI', Arial; font-size: 12px; line-height: 1.6; }
            h2 { color: #F7CC65; border-bottom: 1px solid #30363D; padding-bottom: 6px; }
            h3 { color: #4A90D9; margin-top: 14px; }
            .tag { background: #238636; color: white; padding: 2px 8px; border-radius: 3px; font-size: 10px; }
            ul { padding-left: 20px; }
            li { margin: 4px 0; }
            .code { background: #1C2128; padding: 2px 6px; border-radius: 3px; font-family: Consolas; }
        </style>
        <h2>🏆 Simulación Monte Carlo — Brasil vs Alemania 2014</h2>
        <h3>📋 Descripción del Modelo</h3>
        <p>Este simulador reproduce el <b>primer tiempo del histórico partido</b> Brasil 0–5 Alemania
        (Copa Mundial Brasil 2014) usando simulación estocástica.</p>
        <h3>⚙️ Metodología</h3>
        <ul>
            <li><b>Datos:</b> 41 eventos discretos del partido real (goles, tiros, faltas, etc.)</li>
            <li><b>Distribución temporal:</b> Weibull (mejor AIC entre Exponencial, Gamma, Weibull, Lognormal)</li>
            <li><b>Parámetros Weibull:</b> shape=1.2, scale=1.05</li>
            <li><b>Asignación:</b> Probabilidad condicional por equipo para cada tipo de evento</li>
        </ul>
        <h3>🎯 Resultados Clave</h3>
        <ul>
            <li>Prob. marcador exacto 0–5: <b>~1.14%</b></li>
            <li>Goles reales de Alemania: minutos 11, 23, 24, 25, 29</li>
            <li>El modelo captura la dinámica real del partido</li>
        </ul>
        <h3>🎨 Interfaz</h3>
        <ul>
            <li><b>Cancha en vivo:</b> visualiza cada evento con animación en tiempo real</li>
            <li><b>Gráfica de goles:</b> compara evolución real vs simulada</li>
            <li><b>Monte Carlo:</b> ejecuta hasta 50.000 réplicas en hilo separado</li>
            <li><b>Histograma:</b> distribución de resultados de las simulaciones</li>
        </ul>
        """)
        lay.addWidget(txt)
        return w

    def _fill_freq_table(self):
        self.tabla_freq.setRowCount(len(EVENTOS_DATA))
        for i, (ev, vals) in enumerate(EVENTOS_DATA.items()):
            br = vals['Brasil']
            al = vals['Alemania']
            tot = br + al
            pct = f"{br/tot*100:.0f}%" if tot > 0 else "—"
            items = [
                f"{EMOJIS.get(ev,'•')} {NOMBRES.get(ev, ev)}",
                str(br), str(al), str(tot), pct
            ]
            colors = [None, C['brasil'], '#4A90D9', C['gold'], C['text2']]
            for j, (txt, col) in enumerate(zip(items, colors)):
                item = QTableWidgetItem(txt)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if col:
                    item.setForeground(QColor(col))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                self.tabla_freq.setItem(i, j, item)
        self.tabla_freq.resizeColumnsToContents()

    # ────────── Lógica de simulación paso a paso ──────────

    def _load_real_game(self):
        """Carga los eventos reales pero no los reproduce aún."""
        self.grafica_goles.set_goles_sim([])

    def _play_real_game(self):
        self._stop_sim()
        self.cancha.clear()
        self.tabla_eventos.setRowCount(0)
        self.marcador_sim = {'Brasil': 0, 'Alemania': 0}
        self._update_score()
        self.lbl_minute.setText("0'")
        self.sim_eventos = list(EVENTOS_REALES)
        self.sim_step = 0
        self.grafica_goles.set_goles_sim([])
        self.grafica_goles.set_minuto(0)
        self.btn_stop.setEnabled(True)
        self.btn_play_real.setEnabled(False)
        self.btn_sim_one.setEnabled(False)
        self._sim_mode = 'real'
        self.sim_timer.start(self.sim_velocidad)
        self.statusBar().showMessage("  ▶  Reproduciendo partido real...")

    def _simulate_one(self):
        self._stop_sim()
        seed = self.spin_seed.value()
        if seed == -1:
            seed = None
        evs, marc = self.engine.simulate(seed=seed)
        self.cancha.clear()
        self.tabla_eventos.setRowCount(0)
        self.marcador_sim = {'Brasil': 0, 'Alemania': 0}
        self._update_score()
        self.lbl_minute.setText("0'")
        self.sim_eventos = [(e['minuto'], e['evento'], e['equipo']) for e in evs]
        self.sim_step = 0
        goles_ale = [e['minuto'] for e in evs
                     if e['evento'] == 'GOL' and e['equipo'] == 'Alemania']
        self.grafica_goles.set_goles_sim(goles_ale)
        self.grafica_goles.set_minuto(0)
        self.btn_stop.setEnabled(True)
        self.btn_play_real.setEnabled(False)
        self.btn_sim_one.setEnabled(False)
        self._sim_mode = 'sim'
        self.sim_timer.start(self.sim_velocidad)
        label = f"Seed {seed}" if seed is not None else "Seed aleatoria"
        self.statusBar().showMessage(f"  🎲  Simulando partido ({label})…")

    def _step_simulation(self):
        if self.sim_step >= len(self.sim_eventos):
            self._stop_sim()
            self.statusBar().showMessage("  ✅  Simulación completada — Resultado: "
                f"Brasil {self.marcador_sim['Brasil']} — {self.marcador_sim['Alemania']} Alemania")
            return
        ev = self.sim_eventos[self.sim_step]
        minuto, tipo, equipo = ev[0], ev[1], ev[2]
        self.sim_step += 1

        self.lbl_minute.setText(f"{int(minuto)}'")
        self.grafica_goles.set_minuto(minuto)

        if tipo == 'GOL':
            self.marcador_sim[equipo] = self.marcador_sim.get(equipo, 0) + 1
            self._update_score()

        self.cancha.add_evento(tipo, equipo, minuto)

        # Tabla
        row = self.tabla_eventos.rowCount()
        self.tabla_eventos.insertRow(row)
        items = [
            QTableWidgetItem(f"{minuto}'"),
            QTableWidgetItem(EMOJIS.get(tipo, '•')),
            QTableWidgetItem(NOMBRES.get(tipo, tipo)),
            QTableWidgetItem(equipo),
        ]
        cols = [C['text2'], None, C['text'], COLORES_EQ.get(equipo, C['text'])]
        for col_idx, (item, col) in enumerate(zip(items, cols)):
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if col:
                item.setForeground(QColor(col))
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.tabla_eventos.setItem(row, col_idx, item)

        if tipo == 'GOL':
            for j in range(4):
                self.tabla_eventos.item(row, j).setBackground(QColor(C['gold'] + '33'))

        self.tabla_eventos.scrollToBottom()
        self.lbl_last_ev.setText(
            f"{EMOJIS.get(tipo,'•')} {NOMBRES.get(tipo, tipo)}  —  {equipo}  (min. {int(minuto)})")
        ev_color = COLORES_EQ.get(equipo, C['text'])
        self.lbl_last_ev.setStyleSheet(f"font-size:15px;font-weight:bold;color:{ev_color};")

    def _stop_sim(self):
        self.sim_timer.stop()
        self.btn_stop.setEnabled(False)
        self.btn_play_real.setEnabled(True)
        self.btn_sim_one.setEnabled(True)

    def _update_score(self):
        b = self.marcador_sim.get('Brasil', 0)
        a = self.marcador_sim.get('Alemania', 0)
        self.lbl_score.setText(f"{b}  —  {a}")

    def _update_velocity(self, v):
        labels = {1: "0.5×", 2: "1×", 3: "1.5×", 4: "2×", 5: "Normal",
                  6: "3×", 7: "4×", 8: "6×", 9: "8×", 10: "Máx"}
        delays = {1: 1200, 2: 900, 3: 700, 4: 500, 5: 600,
                  6: 350, 7: 250, 8: 150, 9: 80, 10: 30}
        self.sim_velocidad = delays.get(v, 600)
        self.lbl_vel_val.setText(labels.get(v, ""))
        if self.sim_timer.isActive():
            self.sim_timer.setInterval(self.sim_velocidad)

    def _run_montecarlo(self):
        n = self.spin_mc_n.value()
        self.btn_run_mc.setEnabled(False)
        self.bar_mc.setVisible(True)
        self.bar_mc.setValue(0)
        self.statusBar().showMessage(f"  🔄  Ejecutando {n:,} simulaciones Monte Carlo…")
        self._mc_thread = MontecarloThread(self.engine, n)
        self._mc_thread.progress.connect(self.bar_mc.setValue)
        self._mc_thread.finished.connect(self._mc_done)
        self._mc_thread.start()

    def _mc_done(self, resultados, mejor, exactas):
        self.mc_resultados = resultados
        self.mc_mejor = mejor
        self.mc_exactas = exactas
        n = len(resultados)
        prob = exactas / n
        self.lbl_mc_prob.setText(f"{prob:.2%}")
        self.lbl_mc_exact.setText(f"{exactas:,} / {n:,}")
        self.lbl_mc_seed.setText(str(mejor['seed']) if mejor else "—")
        err = mejor.get('error', 0) if mejor else 0
        self.lbl_mc_err.setText(f"{err:.2f}")
        self.bar_mc.setValue(100)
        self.btn_run_mc.setEnabled(True)
        self.btn_play_best.setEnabled(True)

        # Histograma
        goles_ale = [r['marcador'].get('Alemania', 0) for r in resultados]
        self.mc_hist_widget.set_data(goles_ale)
        self.statusBar().showMessage(
            f"  ✅  Monte Carlo completado — {exactas:,}/{n:,} partidos con marcador exacto 0-5 ({prob:.2%})")

    def _play_best_sim(self):
        if not self.mc_mejor:
            return
        self._stop_sim()
        seed = self.mc_mejor['seed']
        self.spin_seed.setValue(seed)
        self._simulate_one()


# ─────────────────────────────────────────────────────────────────
#  WIDGET: HISTOGRAMA MONTECARLO
# ─────────────────────────────────────────────────────────────────
class MCHistWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = []
        self.setMinimumHeight(160)

    def set_data(self, data):
        self.data = data
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        W, H = self.width(), self.height()
        p.fillRect(0, 0, W, H, QColor(C['card']))
        if not self.data:
            p.setPen(QColor(C['text2']))
            p.setFont(QFont('Arial', 11))
            p.drawText(0, 0, W, H, Qt.AlignmentFlag.AlignCenter, "Ejecuta Monte Carlo para ver resultados")
            p.end()
            return

        PAD_L, PAD_R, PAD_T, PAD_B = 50, 15, 15, 30
        from collections import Counter
        counts = Counter(self.data)
        max_g = max(counts.keys()) if counts else 0
        bins = list(range(0, max_g + 2))
        freqs = [counts.get(b, 0) for b in bins]
        max_f = max(freqs) if freqs else 1
        n_bins = len(bins)
        cw = (W - PAD_L - PAD_R) / n_bins
        ch = H - PAD_T - PAD_B

        p.setPen(Qt.PenStyle.NoPen)
        for i, (b, f) in enumerate(zip(bins, freqs)):
            bh = int(f / max_f * ch)
            x = int(PAD_L + i * cw + 2)
            y = int(PAD_T + ch - bh)
            color = QColor(C['gold']) if b == 5 else QColor(C['accent2'])
            if b == 5:
                color.setAlpha(230)
            else:
                color.setAlpha(160)
            p.setBrush(QBrush(color))
            p.drawRoundedRect(x, y, max(1, int(cw - 4)), bh, 3, 3)

        # Ejes y labels
        p.setPen(QColor(C['text2']))
        p.setFont(QFont('Arial', 8))
        for i, b in enumerate(bins):
            x = int(PAD_L + i * cw + cw/2 - 5)
            p.drawText(x, H - 5, str(b))
        p.drawText(PAD_L - 46, PAD_T + ch//2 + 4, "Frec.")
        p.drawText(W//2 - 20, H - 2, "Goles Alemania")
        p.end()


# ─────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
