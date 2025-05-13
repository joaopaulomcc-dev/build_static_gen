uv run python src/main.py "/build_static_gen/"
cd docs && uv run python -m http.server 8888