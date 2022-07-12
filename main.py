from PIL import Image, ImageDraw
import random
import math
input_img = Image.open("circles.png")
input_img = input_img.convert("L")  # 흑백으로 전환
rows = input_img.size[0]
cols = input_img.size[1]

output_img = Image.new("L", (rows, cols), color=255)
drawer = ImageDraw.Draw(output_img)  # 호 그려주는 거
angle = 3  # 중심각
distance = 3  # 호간 거리
stresses = [25, 145, 325]  # 살짝 밝아지는 각도들
stress_range = 15  # 밝아지는 범위
for radius in range(0, 750, distance):
    # 반지름 길이가 길어질수록 중심각이 커지도록 함 -> 중간에는 정밀한데 가장자리는 안그럼
    if radius > 300:
        angle = 6
    if radius > 400:
        angle = 9

    # 360를 360/angle 개의 중심각이 angle인 호로 나눔
    segments = []
    i = random.randint(0, angle)
    while i < 360 + angle:
        segments.append(i)
        i += angle

    # 그리는 부분
    for segment in segments:
        # 원 그림에서 해당 호의 중심 위치에 있는 색을 탐지 -> 그 색으로 호를 색칠
        color = input_img.getpixel((rows//2 + round(radius * math.cos(math.radians(segment+angle/2))),
                                    cols//2 + round(radius * math.sin(math.radians(segment+angle/2)))))

        # 가장 가까운 stress로부터의 위치 파악 -> stress_range보다 작다면 가까운 정도에 따라 밝기를 높임
        stress_distance = 180
        for stress in stresses:
            stress_distance = min(stress_distance, abs(stress-segment), 360-abs(stress-segment))
        if stress_distance < stress_range:
            color = round(min(max(0, color+(255-color)*(stress_range-stress_distance)*(0.15/stress_range)), 255))

        # 호 그리기
        drawer.arc(((rows//2 - radius, cols//2 - radius), (rows//2 + radius, cols//2 + radius)),
                   start=segment, end=segment + angle , fill=color, width=(255-color)//80+1)

# 이 위치에서
# output_img.show("Before Filling Whites")
# 를 실행해보자.
# 이상한 줄무늬 탄생
# 이유: 비트맵이기 때문에 호와 호 사이의 공간에 특정한 형태의 빈칸이 만들어짐 -> 이어지면서 무늬 형성
# -> 고치기 위해 고생함!!

# 흰색 칸들을 상하좌우의 칸의 색의 평균으로 채워넣기
pixel_map = output_img.load()
for row in range(1, rows-1):
    for col in range(1, cols-1):
        if pixel_map[row, col] == 255:
            up = pixel_map[row-1, col]
            down = pixel_map[row+1, col]
            left = pixel_map[row, col-1]
            right = pixel_map[row, col+1]
            pixel_map[row, col] = (up + down + left + right) // 4

output_img.show()
output_img.save("circles in circles.png")
