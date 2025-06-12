# Stage 1: Build stage
FROM python:3.11.5 AS builder
WORKDIR /home/graphiant-playbooks
## Copy files
COPY configs /home/graphiant-playbooks/configs
COPY libs /home/graphiant-playbooks/libs
COPY scripts /home/graphiant-playbooks/scripts
COPY templates /home/graphiant-playbooks/templates
COPY test /home/graphiant-playbooks/test
COPY README.md /home/graphiant-playbooks/README.md
COPY LICENSE /home/graphiant-playbooks/LICENSE
## Install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt /home/graphiant-playbooks/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final stage
FROM python:3.11.5-slim
ARG COMMIT_SHA=dev
WORKDIR /home/graphiant-playbooks
COPY --from=builder /home/graphiant-playbooks /home/graphiant-playbooks
COPY --from=builder /opt/venv /opt/venv
RUN apt-get update && apt-get install -y --no-install-recommends \
    vim \
    git \
    sshpass \
    && rm -rf /var/lib/apt/lists/*
ENV PATH="/opt/venv/bin:$PATH"
ENV GRAPHIANT_PLAYBOOKS_VERSION=$COMMIT_SHA
CMD ["/bin/bash"]
