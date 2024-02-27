from PIL import Image, ImageDraw, ImageFont
from math import pi, sqrt
import os

circle_path = "assets/circle_image.png"
table_path = "assets/table_image.png"

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
    # Lт = d/2 – (корень (Sсеч / nr * (nr +1 - Т) / Pi) + корень (Sсеч / nr * (nr - Т) / Pi))/2
    for n in range(n_points):
        T = n + 1
        # L = radius - sqrt(((Square / n_points) * (n_points+1-T) + (Square / n_points) * (n_points-T)) / (2 * pi))
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