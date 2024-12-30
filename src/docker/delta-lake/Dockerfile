# Core Idea adapted from https://raw.githubusercontent.com/delta-io/delta-docs/refs/heads/main/static/quickstart_docker/Dockerfile_delta_quickstart

## Reference https://pypi.org/project/deltalake/
## https://pypi.org/project/jupyterlab/
ARG BASE_CONTAINER=spark:3.5.0-scala2.12-java11-python3-ubuntu
FROM $BASE_CONTAINER AS spark
FROM spark AS delta
USER root
ARG DELTA_SPARK_VERSION="3.2.0"
ARG DELTALAKE_VERSION="0.21.0"
ARG JUPYTERLAB_VERSION="4.3.4"

ARG PANDAS_VERSION="2.0.3"
ARG ROAPI_VERSION="0.12.0"
RUN pip install --quiet --no-cache-dir delta-spark==${DELTA_SPARK_VERSION} \
deltalake==${DELTALAKE_VERSION} jupyterlab==${JUPYTERLAB_VERSION} pandas==${PANDAS_VERSION} roapi==${ROAPI_VERSION} \
kafka-python



# Environment variables
FROM delta AS startup
ARG NBuser=NBuser
ARG GROUP=NBuser
ARG WORKDIR=/opt/spark/work-dir
ENV DELTA_PACKAGE_VERSION=delta-spark_2.12:${DELTA_SPARK_VERSION}

# OS Installations Configurations
RUN groupadd -r ${GROUP} && useradd -r -m -g ${GROUP} ${NBuser}
RUN apt -qq update
RUN apt -qq -y install vim curl

# Configure ownership
COPY --chown=${NBuser} startup.sh "${WORKDIR}"
COPY --chown=${NBuser} jupyter/* "${WORKDIR}"
RUN chown -R ${NBuser}:${GROUP} /home/${NBuser}/ \
&& chown -R ${NBuser}:${GROUP} ${WORKDIR}

# Rust install
USER ${NBuser}


# Establish entrypoint
ENTRYPOINT ["bash", "startup.sh"]
