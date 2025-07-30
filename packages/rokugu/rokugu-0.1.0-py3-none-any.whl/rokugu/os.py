import platform
from locale import getencoding
from pathlib import Path
from typing import Union

import psutil
from pendulum import DateTime, Interval, from_timestamp, local_timezone, now
from PySide6.QtCore import QLocale, QSysInfo, QUrl
from PySide6.QtGui import QDesktopServices


def name() -> str:
    return platform.system()


def boot_unique_id() -> str:
    return QSysInfo.bootUniqueId().toStdString()


def build_abi() -> str:
    return QSysInfo.buildAbi()


def build_cpu_architecture() -> str:
    return QSysInfo.buildCpuArchitecture()


def current_cpu_architecture() -> str:
    return QSysInfo.currentCpuArchitecture()


def kernel_type() -> str:
    return QSysInfo.kernelType()


def kernel_version() -> str:
    return QSysInfo.kernelVersion()


def machine_host_name() -> str:
    return QSysInfo.machineHostName()


def machine_unique_id() -> str:
    return QSysInfo.machineUniqueId().toStdString()


def pretty_product_name() -> str:
    return QSysInfo.prettyProductName()


def product_type() -> str:
    return QSysInfo.productType()


def product_version() -> str:
    return QSysInfo.productVersion()


def boot_time() -> DateTime:
    return from_timestamp(psutil.boot_time(), local_timezone().name)


def up_time() -> Interval:
    return now().diff(boot_time())


def timezone() -> str:
    return local_timezone().name


def locale() -> str:
    return QLocale.system().name(QLocale.TagSeparator.Underscore)


def encoding() -> str:
    return getencoding()


def open_url(url: Union[QUrl, str]) -> bool:
    return QDesktopServices.openUrl(url)


def open_path(path: Union[Path, str]) -> bool:
    if isinstance(path, str):
        path = Path(path)

    return QDesktopServices.openUrl(path.resolve().as_uri())
