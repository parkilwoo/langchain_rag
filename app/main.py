import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        **{
            "app": "app.core.app_generator:generate_app",
            "host": "0.0.0.0",
            "port": 8000,
            "workers": 1,
            "reload": True,
            "factory": True,
        }
    )
