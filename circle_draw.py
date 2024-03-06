from PIL import Image, ImageDraw, ImageFont
from math import pi, sqrt
import math

circle_path = "assets/circle_image.png"
rect_path = "assets/rect_image.png"
table_path = "assets/table_image.png"


def rect_pic(min_side, max_side, nA, nB):
    print("rect_pic ", min_side, max_side, nA, nB)
    bold_point_radius = 3
    koef = max_side / min_side
    if koef > 3:
        koef = 3
    width = 360
    height = int(360 / koef) + 20
    background_color = (255, 255, 255)  # White color
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)
    
    rect_width = int(width * 0.8)
    rect_height = int(rect_width / koef)
    
    rect_x = (width - rect_width) // 2
    rect_y = (height - rect_height) // 2
    print(width, height, rect_width, rect_height)
    print(rect_x, rect_y, rect_x + rect_width, rect_y + rect_height)
    draw.rectangle([rect_x, rect_y, rect_x + rect_width, rect_y + rect_height], outline="black")

    data = []
    nT = nA * nB
    for el in range(nT):
        T = el + 1
        osB = math.ceil(T/nA)
        osA = T - (osB -1)* nA
        La = (2 * osA - 1) / (2 * nA)
        Lb = (2 * osB - 1) / (2 * nB)
        point = (La * rect_width, Lb * rect_height)
        # print(point)
        data.append(point)

    for n_line in range(nA):
        x = rect_x + data[n_line][0]
        for y in range(rect_y, rect_y + rect_height, 3):
            draw.point((x, y), fill=(0, 0, 0))

    for n_line in range(nB):
        y = rect_y + data[n_line*nA][1]
        for x in range(rect_x, rect_x + rect_width, 3):
            draw.point((x, y), fill=(0, 0, 0)) 

    font_size = 10
    font = ImageFont.truetype("assets/Arial.ttf", font_size)

    for point in range(nT):
        draw.ellipse([(data[point][0] + rect_x - bold_point_radius, data[point][1] + rect_y - bold_point_radius),
                    (data[point][0] + rect_x + bold_point_radius, data[point][1] + rect_y + bold_point_radius)],
                    fill=(0, 255, 0))  # Green
        draw.text((data[point][0] + rect_x - 12, data[point][1] + rect_y - 15), str(point + 1), fill="black", font=font)

    image.save(rect_path)


def table_rec_pic(min_side, max_side, nA, nB):
    n_points = nA * nB
    row_height = 40
    image_width = table_width = 360
    table_height = image_height = 30 + n_points * row_height
    print("image_width", image_width, image_height)
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    header =  ["Точка №", "Расстояние A,мм", "Расстояние B,мм"]

    data = []
    nT = nA * nB
    for el in range(nT):
        T = el + 1
        osB = math.ceil(T/nA)
        osA = T - (osB -1)* nA
        La = max_side * (2 * osA - 1) / (2 * nA)
        Lb = min_side * (2 * osB - 1) / (2 * nB)
        point = (int(La * 1000), int(Lb * 1000))
        data.append(point)

    font_size = 16
    font = ImageFont.truetype("assets/Arial.ttf", font_size)
    text_width = 30

    draw.text((15, 5), header[0], fill="black", font=font)
    draw.text((87, 5), header[1], fill="black", font=font)
    draw.text((220, 5), header[2], fill="black", font=font)
    draw.line((85, 0, 85, table_height), fill="black", width=1)
    draw.line((218, 0, 218, table_height), fill="black", width=1)
    draw.line((0, 30, table_width, 30), fill="black", width=1)

    for el in range(n_points): #point numbers
        x = 45
        y = el * row_height + 40
        draw.text((x, y), str(el + 1), fill="black", font=font)
        draw.text((x + 95, y), str(data[el][0]), fill="black", font=font)
        draw.text((x + 230, y), str(data[el][1]), fill="black", font=font)

        for x in range(0, image_width, 3):
            draw.point((x, y + text_width), fill=(0, 0, 0))

    image.save(table_path)
    return table_height / table_width

def circle_pic(n_points):
    print("draw ", n_points, " points")   
    width = 360
    height = 360
    background_color = (255, 255, 255)  # White color
    image = Image.new("RGB", (width, height), background_color)

    # Get a drawing context for the image
    draw = ImageDraw.Draw(image)

    # Calculate the center coordinates
    center_x = width // 2
    center_y = height // 2

    
    radius = 170 # Define the radius of the circle

    top_left = (center_x - radius, center_y - radius) # Calculate the coordinates for the bounding box of the circle
    bottom_right = (center_x + radius, center_y + radius)

    vertical_axis_x = center_x  # Draw vertical axis (dotted line)
    vertical_axis_start_y = 0
    vertical_axis_end_y = height
    vertical_axis_step = 5

    for y in range(vertical_axis_start_y, vertical_axis_end_y, vertical_axis_step):
        draw.point((vertical_axis_x, y), fill=(0, 0, 0))  # Draw a dot for each step

    horizontal_axis_y = center_y  # Draw horizontal axis (dotted line)
    horizontal_axis_start_x = 0
    horizontal_axis_end_x = width
    horizontal_axis_step = 5

    for x in range(horizontal_axis_start_x, horizontal_axis_end_x, horizontal_axis_step):
        draw.point((x, horizontal_axis_y), fill=(0, 0, 0))  # Draw a dot for each step

    circle_color = (0, 0, 0)  # Black color     # Draw an unfilled circle in the center of the image
    draw.ellipse([top_left, bottom_right], outline=circle_color)
    bold_point_radius = 3

    Square = pi * radius * radius
    distances = []
    for n in range(n_points):
        T = n + 1
        L = sqrt(((Square / n_points) * (n_points+1-T) + (Square / n_points) * (n_points-T)) / (2 * pi))
        distances.append(L)
        print(L)

    if n_points > 5:
        font_size = 8
        print("font_size = 8")
    else:
        font_size = 12
        print("font_size = 12")
    font = ImageFont.truetype("assets/Arial.ttf", font_size)

    for i, distance in enumerate(distances,start=0):
        point1 = (center_x, center_y - distance)  # Above the circle
        point2 = (center_x, center_y + distance)  # Below the circle
        point3 = (center_x - distance, center_y)  # Left of the circle
        point4 = (center_x + distance, center_y)  # Right of the circle
    
        # Draw bold points on the image
        draw.ellipse([(point1[0] - bold_point_radius, point1[1] - bold_point_radius),
                    (point1[0] + bold_point_radius, point1[1] + bold_point_radius)],
                    fill=(0, 255, 0))  # Green
        draw.ellipse([(point2[0] - bold_point_radius, point2[1] - bold_point_radius),
                    (point2[0] + bold_point_radius, point2[1] + bold_point_radius)],
                    fill=(0, 255, 0))  # Green
        draw.ellipse([(point3[0] - bold_point_radius, point3[1] - bold_point_radius),
                    (point3[0] + bold_point_radius, point3[1] + bold_point_radius)],
                    fill=(0, 0, 255))  # Blue
        draw.ellipse([(point4[0] - bold_point_radius, point4[1] - bold_point_radius),
                    (point4[0] + bold_point_radius, point4[1] + bold_point_radius)],
                    fill=(0, 0, 255))  # Blue

        draw.text((point3[0]-3, point3[1]-17), str(i+1), fill=(0, 0, 0), font=font) 
        draw.text((point4[0]-5, point4[1]-17), str(2*n_points - i), fill=(0, 0, 0), font=font) 
                   
        draw.text((point1[0] + 5, point1[1] - 5), str(2*n_points+i+1), fill=(0, 0, 0), font=font)  
        draw.text((point2[0] + 5, point2[1] - 5), str(4*n_points - i), fill=(0, 0, 0), font=font)  
    
    draw.text((width - 40, center_y + 7), "ось 1", fill="black", font=font)
    draw.text((center_x - 40, 17), "ось 2", fill="black", font=font)

    image.save(circle_path)


def circle_pic2():
    print("draw only 2 points")  
    width = 360
    height = 360
    background_color = (255, 255, 255)  # White color
    image = Image.new("RGB", (width, height), background_color)

    draw = ImageDraw.Draw(image)
    center_x = width // 2
    center_y = height // 2

    radius = 170 # Define the radius of the circle

    top_left = (center_x - radius, center_y - radius) # Calculate the coordinates for the bounding box of the circle
    bottom_right = (center_x + radius, center_y + radius)

    vertical_axis_x = center_x  # Draw vertical axis (dotted line)
    vertical_axis_start_y = 0
    vertical_axis_end_y = height
    vertical_axis_step = 5

    for y in range(vertical_axis_start_y, vertical_axis_end_y, vertical_axis_step):
        draw.point((vertical_axis_x, y), fill=(0, 0, 0))  # Draw a dot for each step

    horizontal_axis_y = center_y  # Draw horizontal axis (dotted line)
    horizontal_axis_start_x = 0
    horizontal_axis_end_x = width
    horizontal_axis_step = 5

    for x in range(horizontal_axis_start_x, horizontal_axis_end_x, horizontal_axis_step):
        draw.point((x, horizontal_axis_y), fill=(0, 0, 0))  # Draw a dot for each step

    circle_color = (0, 0, 0)  # Black color     # Draw an unfilled circle in the center of the image
    draw.ellipse([top_left, bottom_right], outline=circle_color)
    bold_point_radius = 3

    Square = pi * radius * radius
    distances = []
    T = 1
    n_points = 1
    L = sqrt(((Square / n_points) * (n_points+1-T) + (Square / n_points) * (n_points-T)) / (2 * pi))
    distances.append(L)
    # print(L)

    for i, distance in enumerate(distances,start=0):
        point3 = (center_x - distance, center_y)  # Left of the circle
        point4 = (center_x + distance, center_y)  # Right of the circle
        draw.ellipse([(point3[0] - bold_point_radius, point3[1] - bold_point_radius),
                    (point3[0] + bold_point_radius, point3[1] + bold_point_radius)],
                    fill=(0, 0, 255))  # Blue
        draw.ellipse([(point4[0] - bold_point_radius, point4[1] - bold_point_radius),
                    (point4[0] + bold_point_radius, point4[1] + bold_point_radius)],
                    fill=(255, 255, 0))  # Yellow
        draw.text((point3[0] - 10, point3[1] - 10), "1", fill=(0, 0, 0))  # Blue
        draw.text((point4[0] + 10, point4[1] - 10), "2", fill=(0, 0, 0))  # Yellow

    font_size = 12
    font = ImageFont.truetype("assets/Arial.ttf", font_size)
    draw.text((width - 40, center_y + 7), "ось 1", fill="black", font=font)
    draw.text((center_x - 40, 17), "ось 2", fill="black", font=font)

    image.save(circle_path)
    #image.show()

def table_pic(n_points, radius):
    row_height = 40
    image_width = table_width = 360
    table_height = image_height = 33 + n_points * row_height * 4
    column_width = table_width // 3
    print("image_width", image_width, image_height)
    radius = int(radius * 1000)
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    header =  ["Точка №", "Ось", "Расстояние, мм"]

    Square = pi * radius * radius
    distances = []
    for n in range(n_points):
        T = n + 1
        L = radius - sqrt(((Square / n_points) * (n_points+1-T) + (Square / n_points) * (n_points-T)) / (2 * pi))
        L = int(L)
        distances.append(L)
        # print(L)

    data = []
    for el in range(n_points):
        point = [str(el+1), "1", str(distances[el])]
        data.append(point)
    for el in range(n_points):
        point = [str(n_points + el+1), "1", str(2*radius - distances[n_points- el-1])]
        data.append(point)
    for el in range(n_points):
        point = [str(n_points* 2 + el+1), "2", str(distances[el])]
        data.append(point)
    for el in range(n_points):
        point = [str(n_points * 3 + el+1), "2", str(2*radius - distances[n_points- el-1])]
        data.append(point)
    
    for el in data:
        print(el)
    font_size = 20
    font = ImageFont.truetype("assets/Arial.ttf", font_size)
    text_width = 10

    draw.text((10, 0), header[0], fill="black", font=font)
    draw.text((120, 0), header[1], fill="black", font=font)
    draw.text((200, 0), header[2], fill="black", font=font)

    draw.line((110, 0, 110, table_height), fill="black", width=1)
    draw.line((190, 0, 190, table_height), fill="black", width=1)
    draw.line((0, 30, table_width, 30), fill="black", width=1)

    # Draw the data rows
    for row_index, row_data in enumerate(data):
        for col_index, cell_data in enumerate(row_data):
            
            x = col_index * column_width + (column_width/2 - text_width) // 2
            y = (row_index + 1) * row_height
            draw.text((x, y), cell_data, fill="black", font=font)

        for x in range(0, table_width, 2):
            draw.point((x, (row_index + 2) * row_height - 7), fill=(0, 0, 0))    

    image.save(table_path)

def table_pic2(radius):
    n_points = 1
    row_height = 40
    image_width = table_width = 360
    table_height = image_height = 33 + n_points * row_height * 2
    column_width = table_width // 3
    
    radius = int(radius * 1000)
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    header =  ["Точка №", "Ось", "Расстояние, мм"]

    Square = pi * radius * radius
    distances = []
    for n in range(n_points):
        T = n + 1
        L = radius - sqrt(((Square / n_points) * (n_points+1-T) + (Square / n_points) * (n_points-T)) / (2 * pi))
        L = int(L)
        distances.append(L)
        print(L)

    data = []
    for el in range(n_points):
        point = [str(el+1), "1", str(distances[el])]
        data.append(point)
    for el in range(n_points):
        point = [str(n_points + el+1), "1", str(2*radius - distances[n_points- el-1])]
        data.append(point)
    # for el in range(n_points):
    #     point = [str(n_points* 2 + el+1), "2", str(distances[el])]
    #     data.append(point)
    # for el in range(n_points):
    #     point = [str(n_points * 3 + el+1), "2", str(2*radius - distances[n_points- el-1])]
    #     data.append(point)
    
    for el in data:
        print(el)
    font_size = 20
    font = ImageFont.truetype("assets/Arial.ttf", font_size)
    text_width = 10

    draw.text((10, 0), header[0], fill="black", font=font)
    draw.text((120, 0), header[1], fill="black", font=font)
    draw.text((200, 0), header[2], fill="black", font=font)

    draw.line((110, 0, 110, table_height), fill="black", width=1)
    draw.line((190, 0, 190, table_height), fill="black", width=1)
    draw.line((0, 30, table_width, 30), fill="black", width=1)

    # Draw the data rows
    for row_index, row_data in enumerate(data):
        for col_index, cell_data in enumerate(row_data):
            
            x = col_index * column_width + (column_width/2 - text_width) // 2
            y = (row_index + 1) * row_height
            draw.text((x, y), cell_data, fill="black", font=font)

        for x in range(0, table_width, 2):
            draw.point((x, (row_index + 2) * row_height - 7), fill=(0, 0, 0))    

    image.save(table_path)