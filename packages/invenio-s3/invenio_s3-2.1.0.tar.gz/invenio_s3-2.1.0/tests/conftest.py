# -*- coding: utf-8 -*-
#
# Copyright (C) 2018, 2019 Esteban J. G. Gabancho.
# Copyright (C) 2024 KTH Royal Institute of Technology.
#
# Invenio-S3 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Pytest configuration."""
import hashlib

import boto3
import pytest
from flask import current_app
from invenio_app.factory import create_api
from moto import mock_aws

from invenio_s3 import S3FSFileStorage


@pytest.fixture(scope="module")
def app_config(app_config):
    """Customize application configuration."""
    app_config["FILES_REST_STORAGE_FACTORY"] = "invenio_s3.s3fs_storage_factory"
    app_config["S3_ENDPOINT_URL"] = None
    app_config["S3_ACCESS_KEY_ID"] = "test"
    app_config["S3_SECRECT_ACCESS_KEY"] = "test"
    app_config["THEME_FRONTPAGE"] = False
    return app_config


@pytest.fixture(scope="module")
def create_app():
    """Application factory fixture."""
    return create_api


@pytest.fixture(scope="function")
def s3_bucket(appctx):
    """S3 bucket fixture."""
    with mock_aws():
        session = boto3.Session(
            aws_access_key_id=current_app.config.get("S3_ACCESS_KEY_ID"),
            aws_secret_access_key=current_app.config.get("S3_SECRECT_ACCESS_KEY"),
        )
        s3 = session.resource("s3")
        bucket = s3.create_bucket(Bucket="test_invenio_s3")

        yield bucket

        for obj in bucket.objects.all():
            obj.delete()
        bucket.delete()


@pytest.fixture(scope="function")
def s3fs_testpath(s3_bucket):
    """S3 test path."""
    return "s3://{}/path/to/data".format(s3_bucket.name)


@pytest.fixture(scope="function")
def s3fs(s3_bucket, s3fs_testpath):
    """Instance of S3FSFileStorage."""
    s3_storage = S3FSFileStorage(s3fs_testpath)
    return s3_storage


@pytest.fixture
def file_instance_mock(s3fs_testpath):
    """Mock of a file instance."""

    class FileInstance(object):
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    return FileInstance(
        id="deadbeef-65bd-4d9b-93e2-ec88cc59aec5",
        uri=s3fs_testpath,
        size=4,
        updated=None,
    )


@pytest.fixture()
def get_md5():
    """Get MD5 of data."""

    def inner(data, prefix=True):
        m = hashlib.md5()
        m.update(data)
        return "md5:{0}".format(m.hexdigest()) if prefix else m.hexdigest()

    return inner
