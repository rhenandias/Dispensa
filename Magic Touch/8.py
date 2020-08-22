import imutils
import cv2
import matplotlib.pyplot as plt
import time
import numpy as np
import pyautogui
import math

# Configurações e Flags

font = cv2.FONT_HERSHEY_SIMPLEX		# Fonte para exibição de texto de debug
# Offset para posicionamento do recorte de tela após identificar o header do jogo
offset = [0, -28]
window_size = [375, 660]			# Tamanho do recorte da tela do jogo
debug_image = False					# Ativa ou desativa exibição da imagem de saída do processamento
middle_speed = 400					# Velocidade média de movimento do swipe
# A última imagem tirada da tela deve ser salva? Para salvar novos padrões
save_last_screen = False

pattern1 = cv2.imread("pattern1.png")
pattern2 = cv2.imread("pattern2.png")
pattern3 = cv2.imread("pattern3.png")
pattern4 = cv2.imread("pattern4.png")
pattern5 = cv2.imread("pattern5.png")
# pattern6 = cv2.imread("pattern6.png")

# Cria lista com patterns
patterns = [pattern1, pattern2, pattern3, pattern4, pattern5]

# Lista de cores para os patterns
pattern_colors = []

# Função para calcular distância entre dois pontos


def euclidian_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Função para encontrar a cor dominante de uma imagem


def dominant_color(img):
    data = np.reshape(img, (-1, 3))
    data = np.float32(data)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness, labels, centers = cv2.kmeans(
        data, 1, None, criteria, 10, flags)

    return(centers[0].astype(np.int32))


# Identifica as cores dominantes de cada padrão
for pattern in patterns:
    color = dominant_color(pattern)
    pattern_colors.append(tuple(color))

# Identifica posição do header do jogo na tela do computador
header_position = pyautogui.locateOnScreen("header.png", confidence=0.5)
coord = (header_position[0] - offset[0], header_position[1] - offset[1])

# Padrões de movimentos para cada balão
pattern_profiles = {
    '0': [(152, 533), (193, 462), (234, 533)],
    '1': [(152, 462), (193, 533), (234, 462)],
    '2': [(152, 497), (234, 497)],
    '3': [(193, 533), (193, 462)],
    '4': [(179, 451), (216, 499), (193, 522), (170, 499), (207, 451)]
}

# Executa padrão


def run_pattern_profile(profile_id):
    # Adquire o padrão que vai ser executado
    cur_pattern = pattern_profiles[profile_id]

    # Clica com o mouse no primeiro ponto do padrão
    pyautogui.moveTo(x=coord[0] + cur_pattern[0][0],
                     y=coord[1] + cur_pattern[0][1])
    pyautogui.mouseDown(button='left')

    # Atualiza última posição, para calculo do tempo médio de movimento
    last_coord = [cur_pattern[0][0], cur_pattern[0][1]]

    # Percorre os pontos seguintes com o mouse pressionado
    for i in range(1, len(cur_pattern)):
        # Calcula distancia e duração para o próximo ponto da sequência
        next_coord = [cur_pattern[i][0], cur_pattern[i][1]]
        distance = euclidian_distance(
            last_coord[0], last_coord[1], next_coord[0], next_coord[1])
        swipe_duration = distance / middle_speed

        # Executa movimento
        pyautogui.moveTo(x=coord[0] + cur_pattern[i][0],
                         y=coord[1] + cur_pattern[i][1], duration=swipe_duration)

        # Salva última coordenada para o próximo calculo de velocidade
        last_coord = [cur_pattern[i][0], cur_pattern[i][1]]

    # Após o último ponto do padrão, solta o botão do mouse
    pyautogui.mouseUp(button='left')


# Game Loop
while True:
    game_screen = pyautogui.screenshot(
        region=(coord[0], coord[1], window_size[0], window_size[1]))
    game_screen = np.array(game_screen)[:, :, ::-1].copy()

    if save_last_screen:
        cv2.imwrite('last_screen.png', game_screen)

    active_profiles = []

    for idx, template in enumerate(patterns):
        (h, w, d) = template.shape
        res = cv2.matchTemplate(game_screen, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.65
        loc = np.where(res >= threshold)
        points = list(zip(*loc[::-1]))

        margin = 5
        for current_point in points:
            for target_point in points:
                distance = euclidian_distance(
                    current_point[0], current_point[1], target_point[0], target_point[1])
                if distance <= margin:
                    points.remove(target_point)

        if len(points):
            active_profiles.append(idx)

        if debug_image:
            for pt in points:
                color = (int(pattern_colors[idx][0]), int(
                    pattern_colors[idx][1]), int(pattern_colors[idx][2]))
                cv2.rectangle(game_screen, pt,
                              (pt[0] + w, pt[1] + h), color, 2)

    for profile in active_profiles:
        run_pattern_profile(str(profile))
        active_profiles = [i for i in active_profiles if i != profile]

    if debug_image:
        cv2.imshow("game", game_screen)
        cv2.waitKey(1)
