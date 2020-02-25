FROM ubuntu:16.04
MAINTAINER sminot@fredhutch.org

# Add files
RUN mkdir /usr/midas
ADD requirements.txt /usr/midas


# Install prerequisites
# Install MIDAS, and remove the samtools and bowtie2 binaries
# Install Samtools
# Install Bowtie2
# Install SRA toolkit
RUN apt update && \
	apt-get install -y build-essential wget unzip python2.7 python-dev git python-pip \
	bats awscli curl zlib1g-dev libbz2-dev liblzma-dev libcurl4-openssl-dev libssl1.0.0 \
	libssl-dev libtbb-dev g++ hmmer && \
	pip install -r /usr/midas/requirements.txt && \
	cd /usr/midas && \
	echo "" && \
	echo "INSTALLING MIDAS" && \
	wget https://github.com/snayfach/MIDAS/archive/v1.3.2.tar.gz && \
	tar xzf v1.3.2.tar.gz && \
	python MIDAS-1.3.2/setup.py install && \
	rm /usr/midas/MIDAS-1.3.2/bin/Linux/samtools && \
	rm /usr/midas/MIDAS-1.3.2/bin/Linux/bowtie2* && \
	echo "" && \
	echo "INSTALLING SAMTOOLS" && \
	cd /usr/midas && \
	wget https://github.com/samtools/samtools/releases/download/1.4/samtools-1.4.tar.bz2 && \
	tar xf samtools-1.4.tar.bz2 && \
	cd samtools-1.4 && \
	./configure --without-curses && \
	make && \
	make install && \
	rm /usr/local/bin/samtools && \
	ln -s /usr/midas/samtools-1.4/samtools /usr/midas/MIDAS-1.3.2/bin/Linux/ && \
	ln -s /usr/midas/samtools-1.4/samtools /usr/local/bin/ && \
	rm /usr/midas/samtools-1.4.tar.bz2 && \
	echo "" && \
	echo "INSTALLING BOWTIE2" && \
	cd /usr/midas && \
	wget https://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.3.2/bowtie2-2.3.2-linux-x86_64.zip && \
	unzip bowtie2-2.3.2-linux-x86_64.zip && \
	rm bowtie2-2.3.2-linux-x86_64.zip && \
	cd bowtie2-2.3.2 && \
	ln -s /usr/midas/bowtie2-2.3.2/bowtie2* /usr/midas/MIDAS-1.3.2/bin/Linux/ && \
	ln -s /usr/midas/bowtie2-2.3.2/bowtie2* /usr/local/bin/ && \
	echo "" && \
	echo "INSTALLING SRA TOOLKIT" && \
	cd /usr/local/bin && \
	wget https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.8.2/sratoolkit.2.8.2-ubuntu64.tar.gz && \
	tar xzf sratoolkit.2.8.2-ubuntu64.tar.gz && \
	ln -s /usr/local/bin/sratoolkit.2.8.2-ubuntu64/bin/* /usr/local/bin/ && \
	rm sratoolkit.2.8.2-ubuntu64.tar.gz

# Use /share as the working directory
RUN mkdir /share
WORKDIR /share

# Add to the PATH
ENV PYTHONPATH="/usr/midas/MIDAS-1.3.2:${PYTHONPATH}"
ENV PATH="/usr/midas/MIDAS-1.3.2/scripts:${PATH}"

# Add the run script to the PATH
ADD run.py /usr/midas
ADD lib /usr/midas/lib
RUN cd /usr/midas && \
	chmod +x run.py && \
	ln -s /usr/midas/run.py /usr/bin/

# Run tests and then remove the folder
ADD tests /usr/midas/tests
RUN bats /usr/midas/tests/ && rm -r /usr/midas/tests/
