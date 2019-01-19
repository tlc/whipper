FROM debian:buster

RUN apt-get update \
  && apt-get install -y cdrdao python-gobject-2 python-musicbrainzngs python-mutagen python-setuptools \
  python-cddb python-requests libsndfile1-dev flac sox \
  libiso9660-dev python-pip swig make pkgconf \
  eject locales \
  autoconf libtool curl \
  && pip install pycdio==2.0.0

# Xiph cdparanoia with patches
RUN curl -Lo - 'http://downloads.xiph.org/releases/cdparanoia/cdparanoia-III-10.2.src.tgz' | tar zxf - \
  && cd cdparanoia-III-10.2 \
  && curl -Lo 01-overread.patch 'http://lists.xiph.org/pipermail/paranoia-dev/attachments/20130730/e4d81f91/attachment.obj' \
  && curl -Lo 02-overread_data.patch 'http://lists.xiph.org/pipermail/paranoia-dev/attachments/20130730/e4d81f91/attachment-0001.obj' \
  && curl -Lo cdparanoia-longest-match.patch 'https://savannah.gnu.org/bugs/download.php?file_id=39207' \
  && patch < 01-overread.patch \
  && patch < 02-overread_data.patch \
  && patch -p1 < cdparanoia-longest-match.patch \
  && ./configure \
  && make all \
  && make install \
  && cd .. \
  && rm -rf cdparanoia-III-10.2 \
  && ln -s /usr/local/bin/cdparanoia /usr/local/bin/cd-paranoia

RUN ldconfig

# add user
RUN useradd -m worker -G cdrom \
  && mkdir -p /output /home/worker/.config/whipper \
  && chown worker: /output /home/worker/.config/whipper
VOLUME ["/home/worker/.config/whipper", "/output"]

# setup locales + cleanup
RUN echo "LC_ALL=en_US.UTF-8" >> /etc/environment \
  && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
  && echo "LANG=en_US.UTF-8" > /etc/locale.conf \
  && locale-gen en_US.UTF-8 \
  && apt-get clean && apt-get autoremove -y

# install whipper
RUN mkdir /whipper
COPY . /whipper/
RUN cd /whipper/src && make && make install \
  && cd /whipper && python2 setup.py install \
  && rm -rf /whipper \
  && whipper -v

ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US
ENV LANGUAGE=en_US.UTF-8
ENV PYTHONIOENCODING=utf-8

USER worker
WORKDIR /output
ENTRYPOINT ["whipper"]
