from PIL import Image, ImageDraw, ImageFont
import textwrap



def draw_instagram_news(text_description, generated_image_path, lab):
    background_image = Image.new('RGB', (1080, 1080), color=(255, 255, 255))
    generated_image = Image.open(f'output/bg_{lab}.png')
    lab_image = Image.open(f'assets/{lab}.png')

    background_image.paste(generated_image, (0, 0))
    background_image.paste(lab_image, (0, 0), lab_image)

    d = ImageDraw.Draw(background_image)
    font = ImageFont.truetype('fonts/OpenSans-Regular.ttf', 45)

    # Prepare the text for automatic line wrapping
    wrapped_text = textwrap.wrap(str(text_description), width=45)  # Maximum line width

    # Display each line of text with a different y-coordinate
    y_position = 420
    for line in wrapped_text:
        d.text((45, y_position), line, font=font, fill=(255, 255, 255))
        y_position += 50  # Add vertical space between lines

    background_image.save(f'output/post_{lab}.png')
    return f'output/post_{lab}.png'


def justify(line, font, width):
    words = line.split()
    spaces_to_fill = width - sum(font.getsize(word)[0] for word in words)
    if len(words) == 1:
        return line
    spaces_to_add = spaces_to_fill // (len(words) - 1)
    justified_line = ''
    for word in words[:-1]:
        justified_line += word + '  ' * (font.getsize(' ')[0] + spaces_to_add)
    justified_line += words[-1]
    return justified_line

