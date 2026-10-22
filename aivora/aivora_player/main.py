"""Desktop application entry point."""


def main():
    from .app import Aivora

    app = Aivora()
    app.mainloop()


if __name__ == "__main__":
    main()
