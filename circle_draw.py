from PIL import Image, ImageDraw

def circle_pic(distances):
    # Create a new image with a white background
    width = 400
    height = 400
    background_color = (255, 255, 255)  # White color
    image = Image.new("RGB", (width, height), background_color)

    # Get a drawing context for the image
    draw = ImageDraw.Draw(image)

    # Calculate the center coordinates
    center_x = width // 2
    center_y = height // 2

    # Define the radius of the circle
    radius = 190

    # Calculate the coordinates for the bounding box of the circle
    top_left = (center_x - radius, center_y - radius)
    bottom_right = (center_x + radius, center_y + radius)

    # Draw vertical axis (dotted line)
    vertical_axis_x = center_x
    vertical_axis_start_y = 0
    vertical_axis_end_y = height
    vertical_axis_step = 5

    for y in range(vertical_axis_start_y, vertical_axis_end_y, vertical_axis_step):
        draw.point((vertical_axis_x, y), fill=(0, 0, 0))  # Draw a dot for each step

    # Draw horizontal axis (dotted line)
    horizontal_axis_y = center_y
    horizontal_axis_start_x = 0
    horizontal_axis_end_x = width
    horizontal_axis_step = 5

    for x in range(horizontal_axis_start_x, horizontal_axis_end_x, horizontal_axis_step):
        draw.point((x, horizontal_axis_y), fill=(0, 0, 0))  # Draw a dot for each step

    # Draw an unfilled circle in the center of the image
    circle_color = (0, 0, 0)  # Black color
    draw.ellipse([top_left, bottom_right], outline=circle_color)

    # Put four bold points on the axes with different distances from the circle
    # These distances are defined arbitrarily for demonstration purposes
    #distances = [100]
    bold_point_radius = 3

    # for i, distance in enumerate(distances, start=1):
        # Calculate coordinates of points on the axes
    point1 = (center_x, center_y - distances[0])  # Above the circle
    point2 = (center_x, center_y + distances[1])  # Below the circle
    point3 = (center_x - distances[2], center_y)  # Left of the circle
    point4 = (center_x + distances[3], center_y)  # Right of the circle
    
    # Draw bold points on the image
    draw.ellipse([(point1[0] - bold_point_radius, point1[1] - bold_point_radius),
                (point1[0] + bold_point_radius, point1[1] + bold_point_radius)],
                fill=(255, 0, 0))  # Red
    draw.ellipse([(point2[0] - bold_point_radius, point2[1] - bold_point_radius),
                (point2[0] + bold_point_radius, point2[1] + bold_point_radius)],
                fill=(0, 255, 0))  # Green
    draw.ellipse([(point3[0] - bold_point_radius, point3[1] - bold_point_radius),
                (point3[0] + bold_point_radius, point3[1] + bold_point_radius)],
                fill=(0, 0, 255))  # Blue
    draw.ellipse([(point4[0] - bold_point_radius, point4[1] - bold_point_radius),
                (point4[0] + bold_point_radius, point4[1] + bold_point_radius)],
                fill=(255, 255, 0))  # Yellow
    
    # Draw text near each point
    draw.text((point1[0] + 5, point1[1] - 10), str(3), fill=(0, 0, 0))  # Red
    draw.text((point2[0] + 5, point2[1] + 5), str(4), fill=(0, 0, 0))  # Green
    draw.text((point3[0] - 20, point3[1] - 10), str(1), fill=(0, 0, 0))  # Blue
    draw.text((point4[0] + 5, point4[1] - 10), str(2), fill=(0, 0, 0))  # Yellow

    # Save the image to a file
    image.save("assets/circle_image.png")

    # Display the image (optional)
    #image.show()
