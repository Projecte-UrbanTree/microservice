from fastapi import FastAPI

from .api.v1.endpoints import sensors

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "dev"}

app.include_router(sensors.router)

def main():
    pass

if __name__ == "__main__":
    main()