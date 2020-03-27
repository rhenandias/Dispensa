#encoding: utf-8
import imutils
import cv2

# Carrega e exibe a imagem
image = cv2.imread("tetris_blocks.png")
cv2.imshow("Image", image)
cv2.waitKey(0)

# Converte a imagem para tons de cinza
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray", gray)
cv2.waitKey(0)

# Detecção de borda
edged = cv2.Canny(gray, 30, 150)
cv2.imshow("Edged", edged)
cv2.waitKey(0)

# Thresholding
thresh = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)[1]
cv2.imshow("Thresh", thresh)
cv2.waitKey(0)

# Detectando contornos
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
output = image.copy()

for c in cnts:
	cv2.drawContours(output, [c], -1, (255, 0, 159), 3)
	cv2.imshow("Contours", output)
	cv2.waitKey(0)

# Escreve o total de contornos encontrados
text = "{} objetos encontrados".format(len(cnts))
cv2.putText(output, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (240, 0, 159), 2)
cv2.imshow("Contours", output)
cv2.waitKey(0)

# Erosions and Dilations
# É possível aumentar ou diminuir a area obtida após o thresholding na imagem

mask = thresh.copy()
mask = cv2.erode(mask, None, iterations=5)
cv2.imshow("Eroded", mask)
cv2.waitKey(0)

mask = thresh.copy()
mask = cv2.dilate(mask, None, iterations=5)
cv2.imshow("Dilated", mask)
cv2.waitKey(0)

# Masking and bitwise operations
# É possível aplicar "mascaras", selecionando apenas o que é importante na imagem
mask = thresh.copy()
output = cv2.bitwise_and(image, image, mask=mask)
cv2.imshow("Ooutput", output)
cv2.waitKey(0)