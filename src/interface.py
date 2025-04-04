from i_app import Page, BaseApp

class MainInterface(BaseApp):
    def start(self, page: Page):
        # print("start")
        self._running = True


    def update(self, page: Page, delta_time: float, events: list[dict[int, int]]):
        for event in events:
            # print(event)
            if event['type'] == 1 and event['press'] == 1:
                if event['key'] == ord('q'):
                    self._running = False                

        page.text[5][5] = 'c'
        page.text[5][6] = '🤯'
        page.foreground[5][5] = [255, 80, 80]


    def terminate(self, page: Page, status_code: int = 0):
        print(f"terminate status code {status_code}")

    def is_running(self):
        return self._running
        # return super().is_running()