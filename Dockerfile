FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 USE_TORCH=1 USE_TF=0 \
    PIP_DEFAULT_TIMEOUT=600 PIP_RETRIES=10
RUN apt-get update && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app

# Each big download is its own RUN step, so it is cached as soon as it succeeds.

# 1) torch + torchvision: CPU builds, versions pinned to what fer's dependency (facenet-pytorch) allows
#    (torch 2.2.x, torchvision 0.17.x). Installing them first stops pip from pulling the ~2.5 GB CUDA build.
RUN pip install filelock typing-extensions sympy==1.12 networkx jinja2 fsspec setuptools numpy==1.26.4
RUN pip install --no-deps torch==2.2.2+cpu torchvision==0.17.2+cpu --index-url https://download.pytorch.org/whl/cpu
RUN python -c "import torch; print('torch', torch.__version__)"

# 2) TensorFlow (used by FER)
RUN pip install tensorflow==2.15.1 numpy==1.26.4

# 3) Web app + HuggingFace (transformers 4.x works with torch 2.2)
RUN pip install flask gunicorn boto3 prometheus-client transformers==4.44.2

# 4) FER (needs moviepy 1.x: moviepy 2.x removed moviepy.editor)
RUN pip install moviepy==1.0.3 fer==22.5.1
RUN python -c "import torch, fer, transformers, flask; print('deps ok, torch', torch.__version__)"

COPY . .
# Bake the HuggingFace model + FER weights into the image so the first request is fast
RUN python -c "import text.predict, face.predict"
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "1", "--threads", "4", "--timeout", "180", "--access-logfile", "-", "app:app"]
