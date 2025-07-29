from controller import Controller, InputType


if __name__ == "__main__":
    ctrlr = Controller(DEBUG=True)
    ctrlr.listen(0)
    while True:
        events = list(ctrlr.read())
        if len(events) != 0:
            print(events)
