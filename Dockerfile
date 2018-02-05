FROM ubuntu:16.04
MAINTAINER sminot@fredhutch.org

# Install prerequisites
RUN apt update && \
	apt-get install -y build-essential wget unzip python2.7 python-dev git python-pip \
	bats awscli curl zlib1g-dev libbz2-dev liblzma-dev libcurl4-openssl-dev libssl1.0.0 libssl-dev


# Use /share as the working directory
RUN mkdir /share
WORKDIR /share

# Add files
RUN mkdir /usr/midas
ADD requirements.txt /usr/midas

# Install python requirements
RUN pip install -r /usr/midas/requirements.txt && rm /usr/midas/requirements.txt


# Install MIDAS
RUN cd /usr/midas && \
	wget https://github.com/snayfach/MIDAS/archive/v1.3.2.tar.gz && \
	tar xzvf v1.3.2.tar.gz
# Add to the PATH
ENV PYTHONPATH="/usr/midas/MIDAS-1.3.2:${PYTHONPATH}"
ENV PATH="/usr/midas/MIDAS-1.3.2/bin/Linux:${PATH}"
ENV PATH="/usr/midas/MIDAS-1.3.2/scripts:${PATH}"

# Install SAMTOOLS
RUN cd /usr/midas && \
	wget https://github.com/samtools/samtools/releases/download/1.4/samtools-1.4.tar.bz2 && \
	tar xf samtools-1.4.tar.bz2 && \
	cd samtools-1.4 && \
	./configure --without-curses && \
	make && \
	make install && \
	rm /usr/local/bin/samtools && \
	rm /usr/midas/MIDAS-1.3.2/bin/Linux/samtools && \
	ln -s /usr/midas/samtools-1.4/samtools /usr/local/bin/ && \
	rm /usr/midas/samtools-1.4.tar.bz2 && \
	ln -s /usr/midas/samtools-1.4/samtools /usr/midas/MIDAS-1.3.2/bin/Linux/

# Install the SRA toolkit
RUN cd /usr/local/bin && \
	wget https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.8.2/sratoolkit.2.8.2-ubuntu64.tar.gz && \
	tar xzf sratoolkit.2.8.2-ubuntu64.tar.gz && \
	ln -s /usr/local/bin/sratoolkit.2.8.2-ubuntu64/bin/* /usr/local/bin/ && \
	rm sratoolkit.2.8.2-ubuntu64.tar.gz

# Add the run script to the PATH
ADD run.py /usr/midas
ADD helpers /usr/midas/helpers
RUN cd /usr/midas && \
	chmod +x run.py && \
	ln -s /usr/midas/run.py /usr/bin/


# Run tests and then remove the folder
ADD tests /usr/midas/tests
RUN bats /usr/midas/tests/ && rm -r /usr/midas/tests/
