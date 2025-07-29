FROM test-base-image:tmp AS base_image

USER app

ENTRYPOINT ["python3"]
CMD ["-m", "unittest", "discover"]

COPY . /usr/src/app/src

#checkov:skip=CKV_DOCKER_2: A health check is not needed
