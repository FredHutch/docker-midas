FROM python:3.9-slim
LABEL AUTHOR="sminot@fredhutch.org"

# Add files
RUN mkdir /usr/midas
WORKDIR /usr/midas

# ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
	apt-get install -y g++ && \
	apt-get install -y build-essential wget zlib1g-dev libbz2-dev liblzma-dev \
	libncurses5-dev libncursesw5-dev libz-dev libgsl-dev gcc procps && \
	echo "INSTALLING MIDAS" && \
	wget https://github.com/czbiohub-sf/MIDAS/archive/refs/tags/v3.tar.gz && \
	tar xzf v3.tar.gz && \
	pip3 install setuptools "numpy>=1.7.0" "biopython>=1.6.2" "pysam>=0.8.1" "pandas>=0.17.1"
ENV PYTHONPATH="/usr/midas/MIDAS-3"
RUN cd MIDAS-3 && \
	python3 setup.py install

# Add to the PATH
ENV PYTHONPATH="/usr/midas/MIDAS-3:${PYTHONPATH}"
ENV PATH="/usr/midas/MIDAS-3/scripts:${PATH}"

# Add the hs-blastn, bowtie2, and samtools binaries to the PATH
COPY --from=quay.io/biocontainers/hs-blastn:0.0.5--h9948957_6 /usr/local/bin/hs-blastn /usr/midas/MIDAS-3/bin/Linux/hs-blastn
COPY --from=quay.io/biocontainers/bowtie2:2.3.2--py36pl5.22.0_1 /usr/local/bin/bowtie2 /usr/midas/MIDAS-3/bin/Linux/bowtie2
COPY --from=quay.io/biocontainers/samtools:1.4--0 /usr/local/bin/samtools /usr/midas/MIDAS-3/bin/Linux/samtools
