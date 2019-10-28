from src.app import App


def main():
    try:
        app = App()
        app.mainloop()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
