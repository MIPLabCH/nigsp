# syntax=docker/dockerfile:1
# escape=\
# NiGSP Docker Container Image
#
# Copyright 2022, Stefano Moia.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Use official python 3.8.13 (Debian Buster)
FROM python:3.8.13-slim-buster

WORKDIR /app

# Prepare environment
COPY . .
RUN pip3 install .[all]

ENV DEBIAN_FRONTEND="noninteractive" \
    LANG="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8"

CMD nigsp

ARG BUILD_DATE
ARG VCS_REF
ARG VERSION
LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="NiGSP" \
      org.label-schema.description="NiGSP: python library for Graph Signal Processing on Neuroimaging data" \
      org.label-schema.url="https://github.com/miplabch/nigsp" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/miplabch/nigsp" \
      org.label-schema.version=$VERSION \
      org.label-schema.schema-version="1.0"
