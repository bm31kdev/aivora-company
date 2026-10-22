"""Desktop application entry point."""


def main():
    from .app import AivoraStudio

    app = AivoraStudio()
    app.mainloop()


if __name__ == "__main__":
    main()
