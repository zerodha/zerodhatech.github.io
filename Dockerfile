FROM python:3.11 as builder

ENV HUGO_VERSION 0.68.3
ENV HUGO_BINARY hugo_extended_${HUGO_VERSION}_Linux-64bit.tar.gz

# Install Hugo and other deps
RUN set -e && \
  apt install wget ca-certificates git && \
  wget https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/${HUGO_BINARY} && \
  tar xzf ${HUGO_BINARY} && \
  rm -r ${HUGO_BINARY} && \
  mv hugo /usr/bin

FROM builder as build
COPY ./ /public
WORKDIR /public
RUN /usr/bin/hugo --gc --minify --enableGitInfo
