FROM openkbs/jre-mvn-py3:latest

RUN sudo usermod -u 1001 developer
RUN pip install --no-cache-dir jupyter pyspark==3.0.1

USER developer

CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]