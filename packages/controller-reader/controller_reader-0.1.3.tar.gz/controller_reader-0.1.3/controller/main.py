from controller import Controller, InputType


if __name__ == "__main__":
    ctrlr = Controller(DEBUG=True)
    ctrlr.listen(0)
    while True:
        events = ctrlr.consume_events()
        value = ctrlr.consume_values()
        if len(events) != 0:
            print(events, value)
