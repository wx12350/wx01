# utils/captcha.py 示例代码
from io import BytesIO
from random import choices
from string import ascii_letters, digits
from PIL import Image, ImageDraw, ImageFont


def generate_captcha():
    # 生成随机字符（4位）
    chars = choices(ascii_letters + digits, k=4)
    text = ''.join(chars)

    # 创建图片
    image = Image.new('RGB', (120, 40), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 使用默认字体或指定字体路径
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()

    # 绘制文本
    draw.text((10, 5), text, font=font, fill=(0, 0, 0))

    return text, image