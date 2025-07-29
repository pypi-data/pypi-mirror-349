FROM continuumio/miniconda3

WORKDIR /src/ecmwf-jupyter-components

COPY environment.yml /src/ecmwf-jupyter-components/

RUN conda install -c conda-forge gcc python=3.11 \
    && conda env update -n base -f environment.yml

COPY . /src/ecmwf-jupyter-components

RUN pip install --no-deps -e .
