# Uses a multi-architecture Linux Arch image, instead of official x86_64 only.
FROM ljmf00/archlinux:base-20241115004222
WORKDIR /knowledge_verificator
COPY . .

# Install pre-requisites.
RUN yes | pacman -Syu npm python3 python-poetry

# Install the backend's dependencies.
RUN poetry install --no-root --no-dev

# Install the frontend with its JavaScript modules.
RUN npm install --prefix frontend

# Expose the frontend port.
EXPOSE 3000

# Download the required models.
RUN poetry run python -m knowledge_verificator.download_models

# Run the backend and the frontend.
CMD ["poetry", "run", "python", "-m", "knowledge_verificator.main"]
