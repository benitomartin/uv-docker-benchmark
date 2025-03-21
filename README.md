# Docker + uv Benchmark

![Image](https://github.com/user-attachments/assets/e7ef5d59-d122-44c3-97e4-432a770c6ac8)

This project demonstrates different approaches to building Python applications using `uv` package manager with Docker, featuring three distinct Dockerfile strategies:

- `singlestage.Dockerfile`: Single-stage build that keeps `uv` in the final image
- `standalone.Dockerfile`: Multi-stage build using system Python, removes `uv` in the final stage
- `multistage.Dockerfile`: Multi-stage build using uv-managed Python, removes `uv` in the final stage

The following [blog](https://medium.com/@benitomartin/deep-dive-into-uv-dockerfiles-by-astral-image-size-performance-best-practices-5790974b9579) describes the differences between these strategies.

## Project Structure

```
.
├── singlestage.Dockerfile
├── multistage.Dockerfile
├── standalone.Dockerfile
├── src/
│   └── uv_docker_example/
│       └── __init__.py
├── pyproject.toml
├── uv.lock
├── .dockerignore
└── benchmark_docker_images.py
```
## Benchmarking

The project includes a comprehensive benchmarking tool (`benchmark_docker_images.py`) that measures:

- Image sizes
- Build times 

To run the benchmark:

```bash
uv venv
source .venv/bin/activate
uv sync
uv run benchmark_docker_images.py
```

The script will:
1. Build each Dockerfile
2. Compare results between different strategies
3. Clean up images after testing

### Sample Benchmark Output

Size (including all dependencies):

- Multi-Stage   → 4'126.72 MB
- Standalone   → 4'157.44 MB
- Single-Stage  → 4'188.16 MB

Build time:

- Multi-Stage   → 2m 9.5s
- Standalone   → 2m 16.6s
- Single-Stage  → 3m 0.5s

## Dependencies

Main dependencies:
- FastAPI
- scikit-learn
- MLflow
- TensorFlow
- LightGBM
- NumPy
- Pandas
- PyArrow
- SciPy
- Pydantic

Development dependencies:
- Ruff (≥0.6.2)
- FastAPI CLI (≥0.0.5)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
