def color_block_print(r, g, b):
    print(f"\033[48;2;{r};{g};{b}m   \033[0m RGB({r},{g},{b})")

def color_print(text, r, g, b):
    print(f"\033[38;2;{r};{g};{b}m{text}\033[0m")
