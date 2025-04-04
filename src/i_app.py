from abc import ABC, abstractmethod

class Page:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background: list[list[tuple[int, int, int]]] = [[(32, 32, 32) for _ in range(width)] for _ in range(height)]
        self.foreground: list[list[tuple[int, int, int]]] = [[(255, 255, 255) for _ in range(width)] for _ in range(height)]
        self.text: list[list[str]] = [[" " for _ in range(width)] for _ in range(height)]
    
    def draw(self, x: int, y: int):
        # out = f"\033[{y};{x}H" # move cursor to position
        out = ""
        for dy in range(self.height):
            out += f"\033[{y + dy};{x}H"
            out += "".join([
                f"\33[48;2;{self.background[dy][i][0]};{self.background[dy][i][1]};{self.background[dy][i][2]}m"
                f"\33[38;2;{self.foreground[dy][i][0]};{self.foreground[dy][i][1]};{self.foreground[dy][i][2]}m"
                f"{char}"
                for i, char in enumerate(self.text[dy])
            ])

        print(out, end='')



class BaseApp(ABC):
    @abstractmethod
    def start(self, page: Page):
        ...

    @abstractmethod
    def update(self, page: Page, delta_time: float, events: list[dict[int, int]]):
        ...

    @abstractmethod
    def terminate(self, page: Page, status_code: int = 0):
        ...

    def is_running(self) -> bool:
        return True