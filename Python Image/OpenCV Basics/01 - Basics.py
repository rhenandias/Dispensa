# encoding: utf-8
import imutils
import cv2

#=======================================================================================
# Carregando e exibindo uma imagem
#=======================================================================================

# Carrega uma imagem e mostra suas dimensões
# Uma imagem é carregada como uma numpy array multidimensional
# comprimento x altura x profundidade
# Importante notar que a altura vem antes do comprimento
# Profundidade é a quantidade de canais, no caso, Reg Green Blue
image = cv2.imread("jp.png")
(h, w, d) = image.shape
print("Comprimento: {}, Altura: {}, Profundidade: {}" .format(w, h, d))

# Exibe a imagem na tela
cv2.imshow("Image", image)
cv2.waitKey(0)

#=======================================================================================
# Informações sobre um Pixel
#=======================================================================================

# Adquire informações sobre um pixel da imagem
# No OpenCV, a ordem de cores do pixels é BGR, e não RGB
# As informações deum pixel são um 3-tuple
(B, G, R) = image[100, 50]
print("R: {}, G: {}, B: {}" .format(R, G, B))

#=======================================================================================
# Recortando uma parte da imagem
#=======================================================================================

# Recorta um pedaço da imagem
# Importante notar novamente que a ordem é (altura, comprimento)
# image[startY : endY, startX : endX]
girl = image[20:220, 85:270]
cv2.imshow("Girl", girl)
cv2.waitKey(0)


#=======================================================================================
# Redimensionando Imagens
#==================================================================================================================================================================

# Redimensiona a imagem sem considerar o aspect ratio
resized = cv2.resize(image, (200, 200))
cv2.imshow("Fixed Resizing", resized)
cv2.waitKey(0)

# Redimensiona a imagem considerando seu aspect ratio
r = 300.0 / w
dim = (300, int(h * r))
resized = cv2.resize(image, dim)
cv2.imshow("Aspect Ratio Resize", resized)
cv2.waitKey(0)

# Redimensionando com a biblitoeca imutils
resized = imutils.resize(image, width=300)
cv2.imshow("Imutils Resize", resized)
cv2.waitKey(0)

#=======================================================================================
# Rotacionando uma imagem
#=======================================================================================

# Rotaciona a imagem em 45°
# Para isso primeiro é necessário calcular o centro da imagem
# E então, aplicar a rotação pela biblioteca da OpenCV
center = (w // 2, h // 2)
M = cv.getRotationMatrix2D(center, -45, 1.0)
rotated = cv.warpAffine(image, M, (w, h))
cv.imshow("OpenCV Rotation", rotated)
cv.waitKey(0)

# Rotacionando a imagem com a biblioteca imutils
rotated = imutils.rotate(image, -45)
cv.imshow("Imtuils Rotated", rotated)
cv.waitKey(0)

# Rotacionando a imagem e exibindo sem clipping
rotated = imutils.rotate_bound(image, 45)
cv.imshow("Imutils Bound Rotation", rotated)
cv.waitKey(0)

#=======================================================================================
# Adicionando Blur a uma imagem
#=======================================================================================

# Adicionar blur a uma imagem é útil para reduzir ruídos de alta frequência na imagem
# Esses ruídos podem atrapalhar e confundir algoritmos de visão
# Adicionar blur é um jeito facil de remover este ruído
blurred = cv.GaussianBlur(image, (11, 11), 0)
cv.imshow("Blurred", blurred)
cv.waitKey(0)

#=======================================================================================
# Desenhando em uma imagem
#=======================================================================================

# Primeiro é necessário criar uma cópia da imagem, toda alteração muda a array da imagem
output = image.copy()

# Desenhando um Retangulo
# Para criar um retângulo, passa-se duas coordenadas
# Pt1: ponto de inicio do retangulo (x, y) - canto superior esquerdo
# Pt2: ponto final do retangulo (x, y) - canto inferior direito
# Cor: (B, G, R)
# Grossura do traço
cv.rectangle(output, (170, 92), (270, 213), (255, 0, 255), 2)

# Desenhando um círculo
# image, center, radius, color, thickness
cv.circle(output, (565, 146), 20, (255, 255, 0), -1)

# Desenhando uma linha
cv.line(output, (541, 139), (450, 215), (255, 0, 255), 5)

# Escrevendo um texto sob a imagem
cv.putText(output, "Aprendendo OpenCV", (201, 272), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

cv.imshow("Drawing", output)
cv.waitKey(0)