from kba.app import Application
import uvicorn

def main():
    app = Application()

    webcfg = uvicorn.Config(app.app, host="127.0.0.1", port=8080, log_level="info")
    server = uvicorn.Server(webcfg)
    server.run()




if __name__ == "__main__":
    main()
