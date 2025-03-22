from PIL import Image, ImageDraw, ImageFont
import datetime


def create_obs_image(show_name, image_size=(2400, 400)):

    font_path = "./GaretHeavy.ttf"
    img = Image.new('RGBA', image_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    font_size = image_size[1] // 5
    font = ImageFont.truetype(font_path, size=font_size)

    left, top, right, bottom = draw.textbbox((0, 0), show_name, font=font)
    text_width = right - left
    text_height = bottom - top

    max_text_width = image_size[0] * 0.8

    while text_width > max_text_width:
        font_size -= 2
        font = ImageFont.truetype(font_path, size=font_size)
        left, top, right, bottom = draw.textbbox((0, 0), show_name, font=font)
        text_width = right - left
        text_height = bottom - top

    padding = font_size // 3
    rectangle_height = text_height + 2 * padding

    x1 = 0
    y1 = (image_size[1] - rectangle_height) // 2
    y2 = y1 + rectangle_height

    fill_colour = (149, 239, 185)
    outline_colour = fill_colour

    final_text_width = draw.textbbox((0, 0), show_name, font=font)[
        2] - draw.textbbox((0, 0), show_name, font=font)[0]
    final_image_width = x1 + final_text_width + 2 * padding

    img = Image.new('RGBA', (final_image_width, image_size[1]), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([x1, y1, final_image_width, y2], radius=rectangle_height // 4,
                           fill=fill_colour, outline=outline_colour)

    text_x = x1 + (final_image_width - final_text_width) // 2
    text_y = y1 + (rectangle_height - text_height) // 2
    draw.text((text_x, text_y - padding), show_name,
              font=font, fill=(32, 46, 78))

    img.save("./dcufm-12hr-show-name.png")

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Current Show Updated ({current_time}): {show_name}")
