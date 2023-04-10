from fastapi import FastAPI


app = FastAPI()


@app.get('/ping')
async def ping():
    return {'message': 'pong'}


def main():
    pass


if __name__ == "__main__":
    main()
