"""Entry point for running ai_shopping as a module."""

import uvicorn


def main():
    uvicorn.run("ai_shopping.web.app:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
