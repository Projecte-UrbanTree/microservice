from fastapi import FastAPI


app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "dev"}


def main():
    pass

if __name__ == "__main__":
    main()