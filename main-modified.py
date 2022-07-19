from PIL import Image, ImageDraw
import random
import math
import os

dir_img = ""
while True:   #파일 위치 받기 (빈 입력 = circles.png)
    input_dir = input("file's address>>> ")
    if not input_dir:
        input_dir = "circles.png"
    if os.path.isfile(input_dir):
        dir_img = os.path.abspath(input_dir)
        break
    else: print("try again \n")

input_img = Image.open(dir_img)
input_img = input_img.convert("L")  # 흑백으로 전환
rows = input_img.size[0]
cols = input_img.size[1]
standard_angle = 3  # 기준 중심각
distance = 3  # 호간 거리
rad = math.ceil(math.sqrt(rows ** 2 + cols ** 2) / 2 )  #사진 정중앙에서 꼭짓점 거리

output_img = Image.new("L", (2 * rad, 2 * rad), color=255) #output_img 크기 rad만큼 늘리기
box = tuple((n - o) // 2 for n, o in zip(output_img.size, input_img.size))
output_img.paste(input_img, box)
drawer = ImageDraw.Draw(output_img)  # 호 그려주는 거

stresses = [25, 145, 325]  # 살짝 밝아지는 각도들
stress_range = 15  # 밝아지는 범위

for radius in range(0, math.ceil(rad), distance):
    # 반지름 길이가 길어질수록 중심각이 커지도록 함 -> 중간에는 정밀한데 가장자리는 안그럼
    angle = standard_angle
    if radius > rad / 5 * 2:
        angle = 2 * angle
    if radius > rad / 15 * 8:
        angle = 3 * angle

    # 360를 360/angle 개의 중심각이 angle인 호로 나눔
    segments = []
    i = random.randint(0, angle)
    while i < 360 + angle:
        segments.append(i)
        i += angle

    # 그리는 부분
    for segment in segments:
        # 원 그림에서 해당 호의 중심 위치에 있는 색을 탐지 -> 그 색으로 호를 색칠
        color = output_img.getpixel((rad + round(radius * math.cos(math.radians(segment+angle/2))),
                                    rad + round(radius * math.sin(math.radians(segment+angle/2)))))

        # 가장 가까운 stress로부터의 위치 파악 -> stress_range보다 작다면 가까운 정도에 따라 밝기를 높임
        stress_distance = 180
        for stress in stresses:
            stress_distance = min(stress_distance, abs(stress-segment), 360-abs(stress-segment))
        if stress_distance < stress_range:
            color = round(min(max(0, color+(255-color)*(stress_range-stress_distance)*(0.15/stress_range)), 255))

        # 호 그리기
        drawer.arc(((rad - radius, rad - radius), (rad + radius, rad + radius)),
                   start=segment, end=segment + angle , fill=color, width=(255-color)//120+distance+1)

output_img.show()
output_img.save("circles in circles.png")
