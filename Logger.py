def colored(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text} \033[38;2;255;255;255m"


INFO = ["[INFO]: ", [74, 144, 226]]
SUCCESS = ["[SUCCESS]: ", [130, 221, 85]]
ERROR = ["[ERROR]: ", [226, 54, 54]]
WARNING = ["[WARNING]: ", [237, 185, 94]]


def LOG(ll, message):
    print(colored(ll[1][0], ll[1][1], ll[1][2], ll[0] + message))
