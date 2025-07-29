def color_block_print(r, g, b):
    print(f"\033[48;2;{r};{g};{b}m   \033[0m RGB({r},{g},{b})")

def color_print(text, r, g, b):
    print(f"\033[38;2;{r};{g};{b}m{text}\033[0m")


def fading_print(text, start_rgb, end_rgb):
    """
    Print text with fading colors from start_rgb to end_rgb.

    Parameters:
    - text (str): The text to print
    - start_rgb (tuple): (r, g, b) start color
    - end_rgb (tuple): (r, g, b) end color
    """
    length = max(len(text) - 1, 1) 

    for i, char in enumerate(text):
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * i / length)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * i / length)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * i / length)
        print(f"\033[38;2;{r};{g};{b}m{char}\033[0m", end='')

    print()  

