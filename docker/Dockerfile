FROM aibolit:dataset as STORAGE

FROM jupyter/datascience-notebook
RUN pip install torch==1.5.0 catboost==0.22 pandas==1.0.0 mypy==0.770
RUN pip install networkx==2.4 lightgbm==2.3.1 scikit-learn==0.22.1 sphinx==2.3.1
RUN git config --global user.email "docker@example.com"
RUN git config --global user.name "Docker Dockerovich"
RUN git config --global core.editor "vim"

USER root
RUN apt-get -y update && apt-get -y install vim
RUN apt-get -y install default-jdk maven
USER jovyan

RUN mkdir _tmp
RUN mkdir java_files
COPY --chown=jovyan:users --from=STORAGE /dataset.zip .
COPY --chown=jovyan:users --from=STORAGE /halstead.jar ./_tmp
COPY --chown=jovyan:users --from=STORAGE /pmd-bin.zip ./_tmp
COPY git_clone_and_pull_pr.sh .
RUN unzip -q dataset.zip -d ./java_files
ENV JAVA_FILES_PATH /home/jovyan/java_files
ENTRYPOINT []