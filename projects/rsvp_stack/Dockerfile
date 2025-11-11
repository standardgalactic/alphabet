FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04
RUN apt update && apt install -y python3 python3-pip git
WORKDIR /app
COPY . /app
RUN pip3 install --upgrade pip
RUN pip3 install -e .
RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu121
RUN pip3 install wandb gradio streamlit
CMD ["rsvp-run"]
