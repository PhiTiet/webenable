from kba.app import Application
from kba.data import DataRefresher
import uvicorn

def main():
    app = Application()

    webcfg = uvicorn.Config(app.app, host="127.0.0.1", port=8080, log_level="info")
    server = uvicorn.Server(webcfg)
    server.run()

    # data = DataRefresher()
    # data.run()

    # print(data.get_data().model_dump_json())




if __name__ == "__main__":
    main()
