import imgkit
from PIL import Image
import re

def create(head, body, footer, width, height):
    head = '<div style="height: ' + str(height - 16) + 'px; width: ' + str(width - 15) + 'px; position: relative;">' + head + '<div style="border-left: ' + str(width - 15) + 'px solid grey; height: 2px;"></div>'
    footer = '<div style="border-left: ' + str(width - 15) + 'px solid grey; height: 2px;"></div>' + footer
    footer = '<div style="visibility: hidden;">' + footer + '</div></div><div style="position: absolute; bottom: 0;">' + footer + '</div>'
    lines = get_lines(body)
    images = generate_image(head, lines, footer, width, height)

def get_lines(html):
    lines = []
    line_count = len(re.findall(r'<\/p>', html))
    for i in range(0, line_count):
        match = re.search(r'<\/p>', html)
        lines.append(html[:match.end()])
        html = html[match.end():]
    return lines

def generate_image(head, lines, footer, width, height):
    max_height = height
    max_width = width
    skips = 0
    img_count = 0
    # Generate as many images as necessary
    while True:
        n = 0
        html = head
        for line in range(0, len(lines) - skips):
            html += lines[line]
            n += 1
        html += footer
        options = {'width': max_width}
        imgkit.from_string(html, 'out' + str(img_count) + '.png', options=options)
        im = Image.open('out' + str(img_count) + '.png')
        width, height = im.size
        # Check height
        if height > max_height:
            skips += 1
        else:
            # Generate right size img
            options = {'width': max_width, 'height': max_height}
            imgkit.from_string(html, 'out' + str(img_count) + '.png', options=options)
            # Check if all lines are included
            if skips == 0:
                break
            else:
                # Reset counters and remove already used text
                skips = 0
                img_count += 1
                for line in range(0, n):
                    del lines[0]
                n = 0
    print(img_count + 1)
