from PIL import Image, ImageDraw
import cv2
img = Image.open('image/plotter.jpeg').convert('RGB')
width, height = img.size
# print(width,height)
# draw = ImageDraw.Draw(img)
# # 0.344907, 0.639175, 0.558961, 0.828483
# x1=0.344907*640
# y1= 0.639175*480
# x2= 0.558961*640
# y2=0.828483*480

cv2_image = cv2.imread('image/plotter.jpeg', cv2.IMREAD_COLOR)
cv2_image =cv2.flip(cv2_image, 1)
cv2.imwrite('image/plotter_flip.jpeg',cv2_image)

# draw.rectangle((x1,y2,x2,y1), outline=(0,255,0), width = 3)

# img.show()
