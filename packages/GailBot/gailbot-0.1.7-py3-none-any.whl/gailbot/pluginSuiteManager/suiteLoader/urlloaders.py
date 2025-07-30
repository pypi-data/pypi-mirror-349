# -*- coding: utf-8 -*-
# @Author: Jason Y. Wu
# @Date:   2023-07-17 19:21:51
# @Last Modified by:   Jason Y. Wu
# @Last Modified time: 2023-08-01 05:34:44
import os
import re
import boto3
import requests
from botocore.exceptions import ParamValidationError
from cryptography.fernet import Fernet
from typing import List, IO, TextIO
from abc import ABC
from .directoryloader import PluginDirectorySuiteLoader
from gailbot.shared.utils.logger import makelogger
from gailbot.shared.utils.general import read_toml, delete
from gailbot.configs import PLUGIN_CONFIG
from gailbot.shared.utils.download import download_from_urls
from gailbot.pluginSuiteManager.S3BucketManager import S3BucketManager

from ..suite.pluginData import ConfModel
from ..suite.suite import PluginSuite

logger = makelogger("url_loader")


class UrlLoader(ABC):
    """base class for loading plugin from url"""

    def __init__(self, download_dir, suites_dir) -> None:
        self.download_dir = download_dir
        self.suites_dir = suites_dir
        self.dir_loader = PluginDirectorySuiteLoader(suites_dir)
        super().__init__()

    @staticmethod
    def is_supported_url(url: str) -> bool:
        """
        check if the url is supported
        """
        raise NotImplementedError

    def load(self, url: str, f: IO) -> List[PluginSuite]:
        """load the source from the url"""
        raise NotImplementedError


class ZipUrlLoader(UrlLoader):
    """load plugin from an url source"""

    def __init__(self, download_dir, suites_dir) -> None:
        """initialize the plugin loader

        Args:
            download_dir (str): path to where the plugin suite will be downloaded
            suites_dir (str): path to where the plugin will be stored after
                              download
        """
        super().__init__(download_dir, suites_dir)

    @staticmethod
    def is_supported_url(url: str) -> bool:
        try:
            response = requests.head(url)
            content_type = response.headers.get('content-type', '')
            # Check if the content type indicates a zip file
            return content_type.lower() == 'application/zip' or url.lower().endswith('.zip')
        except requests.RequestException as e:
            return False

    def load(self, url: str, f: TextIO) -> [PluginSuite]:
        if not self.is_supported_url(url):
            return []

        download_path = download_from_urls(
            urls=[url], download_dir=self.download_dir, unzip=True
        )[0]

        suite_name = None

        # get the suite name from the toml file
        for root, dirs, files in os.walk(download_path):
            if PLUGIN_CONFIG.CONFIG in files:
                config = os.path.join(root, PLUGIN_CONFIG.CONFIG)
                suite_name = ConfModel(**read_toml(config)).suite.name
                suite_path = download_path[:(download_path.rfind("/"))] + "/" + suite_name
                os.rename(download_path, suite_path)
                logger.info(f"download path: {download_path} suite path: {suite_path}")
                break

        if not suite_name:
            f.write(f"{url} does not store a valid {PLUGIN_CONFIG.CONFIG} configuration file\n")
            return []
        if not suite_path:
            f.write(f"{suite_path} does not exist\n")
            return []

        suites = self.dir_loader.load(suite_path, f)
        delete(suite_path)
        return suites


class S3BucketLoader(UrlLoader):
    """load plugin from an url source"""

    def __init__(self, download_dir, suites_dir) -> None:
        """initialize the plugin loader

        Args:
            download_dir (str): path to where the plugin suite will be downloaded
            suites_dir (str): path to where the plugin will be stored after
                              download
        """
        super().__init__(download_dir, suites_dir)
        self.download_dir = download_dir
        self.suites_dir = suites_dir

    @staticmethod
    def is_supported_url(bucket: str) -> bool:
        try:
            s3BucketManager = S3BucketManager.get_instance()
            r3 = s3BucketManager.get_r3()
            r3.meta.client.head_bucket(Bucket=bucket)
            return True
        except ParamValidationError:
            return False
        except Exception as e:
            return False

    def load(self, bucket: str, f: TextIO) -> List[PluginSuite]:
        if not self.is_supported_url(bucket):
            return []
        

        s3BucketManager = S3BucketManager.get_instance()
        s3 = s3BucketManager.get_s3()

        plugin_suites = []
        # get all object from teh bucket

        objects = s3.list_objects_v2(Bucket=bucket)["Contents"]
        for obj in objects:
            key = obj["Key"]
            if "zip" in key:
                # Generate a pre-signed URL for the object
                url = s3.generate_presigned_url(
                    "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=3600
                )
                url = url[0: url.index("?")]
                logger.info(f"loading plugin from url {url}")
                ZipLoader = ZipUrlLoader(self.download_dir, self.suites_dir)
                plugin_suites.extend(ZipLoader.load(url, f))
        return plugin_suites
