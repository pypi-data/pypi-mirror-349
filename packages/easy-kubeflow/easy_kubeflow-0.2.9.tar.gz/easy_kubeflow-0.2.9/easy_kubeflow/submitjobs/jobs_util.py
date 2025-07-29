import json
import os
import re
import time

from simplejson import JSONDecodeError

import requests
from typing import Optional, Union
from uuid import uuid4

from easy_kubeflow.utils import MyLogger

NODE_HOST = 'w-ucd-bj-k8s.stonewise.cn'
NAMESPACE = "default"

_logger = MyLogger()


def _verify_name(name=None):
    """
    verify right name for k8s
    :param name:
    :return:
    """
    if name:
        if re.search(pattern="^([a-z])[a-z0-9-]*$", string=name, flags=0):
            return True
        else:
            _logger.warning("invalid job name: " + name + ", use default name instead.")
            return False
    else:
        _logger.warning("no job name, use default name instead.")
        return False


def _verify_cpu(name=None):
    """
    verify right cpu unit for k8s
    :param name:
    :return:
    """
    if name:
        if re.search(pattern="^[0-9]+\.{0,1}[0-9]{0,2}$", string=name, flags=0):
            return True
        else:
            _logger.error("invalid cpu unit: %s" % name)
            return False
    else:
        _logger.error("no cpu set.")
        return False


def _verify_gpu(name=None):
    """
    verify right gpu amount in single node
    :param name:
    :return:
    """
    if name:
        if re.search(pattern="^[1-8]", string=name, flags=0):
            return True
        else:
            _logger.error("invalid gpu amount: %s" % name)
            return False
    else:
        _logger.error("no gpu set.")
        return False


def _verify_mem(name=None):
    """
    verify right memory unit for k8s
    :param name:
    :return:
    """
    if name:
        if re.search(pattern="^[0-9]+(.[0-9]+)?(m|G|Gi|M|Mi)$", string=name, flags=0):
            return True
        else:
            _logger.error("invalid memory unit: %s" % name)
            return False
    else:
        _logger.error("no memory set.")
        return False


def _json2_dict(file=None):
    with open(file) as f:
        return json.load(f)


def _parse_namespace(username):
    return username.split("@")[0]


def _parse_fuse_sub_dir(path):
    prefix = "/alluxio/fuse/"
    if path.startswith(prefix):
        return path[len(prefix):]  # 截取子路径
    else:
        return path


class JobSpec(object):
    """build SubmitJobs' job spec"""

    def __init__(self, name=None, job_type="standalone"):
        """
        job obj
        :param name: give a job name
        :param job_type: standalone or pytorch-ddp
        """
        self.cmd = []
        # self.pvc_list = []
        # self.vol_list = []
        self.type = job_type
        self.name = name if _verify_name(name) else "job-" + str(uuid4())
        self.job_obj = {
            "jobType": self.type,
            "jobName": self.name,
            "gpus": "none",
            "affinityConfig": "none",
            "workerAmount": 1,
            "command": self.cmd,
            "ttl_time": 3,
        }

    def __repr__(self):
        return self.name

    def image(self, image: str = None):
        """
        set job image
        :param image: not None
        :return:
        """
        if image:
            self.job_obj["image"] = image
            _logger.info("set job image: %s" % image)
        else:
            _logger.error("no image set")

        return self

    def cpu(self, cpu: str = "1"):
        """
        set job cpu limit
        :param cpu: default 1
        :return:
        """
        if _verify_cpu(cpu):
            self.job_obj["cpu"] = cpu
            _logger.info("set job cpu limit: %s" % cpu)

        return self

    def mem(self, mem: str = "1Gi"):
        """
        set job memory limit
        :param mem: default 1Gi
        :return:
        """
        if _verify_mem(mem):
            self.job_obj["memory"] = mem
            _logger.info("set job memory limit: %s" % mem)
        return self

    def gpu(self, gpu: str = "none"):
        """
        set job gpus
        :param gpu: default none
        :return:
        """
        if _verify_gpu(gpu):
            self.job_obj["gpus"] = gpu
            _logger.info("set job gpu amount: %s" % gpu)

        return self

    def workers(self, number: int = 1):
        """
        set job's worker amount
        :param number: default 1
        :return:
        """
        self.job_obj["workerAmount"] = number
        _logger.info("set job worker amount: %s" % number)

        return self

    def command(self, cmd: str = None):
        """
        set run job command
        :param cmd: default None
        :return:
        """
        if cmd:
            for item in cmd.split(" "):
                if item:
                    self.cmd.append(item)

        return self

    def args(self, args: str = None):
        """
        set run job args
        :param args: default None
        :return:
        """
        if args:
            self.job_obj["args"] = [args]
        return self

    def affinity(self, config: str = "none"):
        """
        set node selector strategy
        :param config:
        :return:
        """
        self.job_obj["affinityConfig"] = config
        _logger.info("set job node selector: %s" % config)
        return self

    def datavols(self, name: str = None, mount_path: str = None):
        """
        add pvc
        :param name: pvc name
        :param mount_path: mount path
        :return:
        """
        pvc_list = [
            {
                "name": name,
                "path": mount_path
            }
        ]
        if self.job_obj.get("datavols"):
            self.job_obj["datavols"].extend(pvc_list)
        else:
            self.job_obj["datavols"] = pvc_list
        _logger.info("set job data vol: %s" % name)
        return self

    def fusevols(self, name: str = "alluxio-alluxio-csi-fuse-pvc", path: str = None, mount_path: str = None):
        """
        add alluxio fuse pvc
        :param name: pvc name: alluxio-alluxio-csi-fuse-pvc
        :param path: the same as old alluxio host path
        :param mount_path: mount path
        :return:
        """
        sub_path = _parse_fuse_sub_dir(path=path)
        pvc_list = [
            {
                "name": name,
                "subPath": sub_path,
                "mountPath": mount_path
            }
        ]
        if self.job_obj.get("fusevols"):
            self.job_obj["fusevols"].extend(pvc_list)
        else:
            self.job_obj["fusevols"] = pvc_list
        _logger.info("set job alluxio fuse vol path: %s" % path)
        return self

    def hostvols(self, host_path: str = None, mount_path: str = None):
        """
        add host path
        :param host_path: host path
        :param mount_path: mount path
        :return:
        """
        host_list = [
            {
                "hostPath": host_path,
                "mountPath": mount_path
            }
        ]
        if self.job_obj.get("hostvols"):
            self.job_obj["hostvols"].extend(host_list)
        else:
            self.job_obj["hostvols"] = host_list
        _logger.info("set job host vol: %s" % host_path)
        return self

    def sharedvols(self, server: str = None, path: str = None, mount_path: str = None):
        """
        add shared volumes
        :param server: nfs ip
        :param path: nfs path
        :param mount_path: mount path
        :return:
        """
        vol_list = [
            {
                "server": server,
                "path": path,
                "mountPath": mount_path
            }
        ]
        if self.job_obj.get("sharedvols"):
            self.job_obj["sharedvols"].extend(vol_list)
        else:
            self.job_obj["sharedvols"] = vol_list
        _logger.info("set job shared vol: %s" % path)
        return self

    def ttl(self, timeout: int = 3):
        """
        time to terminate completed job
        :param timeout: unit(day)
        :return:
        """
        self.job_obj["ttl_time"] = timeout
        _logger.info("set job ttl days: %s" % timeout)
        return self

    def retry(self, amount: int = 0):
        """
        job restart times
        :param amount: retry number
        :return:
        """
        if amount > 0:
            self.job_obj["restart_limit"] = amount
            _logger.info("set job retry time: %s" % amount)
        return self

    def dump(self, root: str = None):
        """
        save job spec to json
        :param root: saved path
        :return:
        """
        file_name = self.job_obj.get("jobName") + ".json"
        if root:
            os.makedirs(root, exist_ok=True)
            path = os.path.join(root, file_name)
        else:
            path = file_name
        with open(path, "w") as f:
            json.dump(self.job_obj, f)
        _logger.info("save job spec to {path}".format(path=path))


class ReuseJobSpec(object):
    def __init__(self, file: str = None):
        """
        build ReuseJobSpec from json like file
        :param file: file path
        """
        self.job_obj = _json2_dict(file)

    def __repr__(self):
        return self.job_obj.get("jobName")


class EasyJobs(object):
    """Simple way to create jobs in submit jobs"""

    def __init__(self, host: str = NODE_HOST,
                 port: int = 31380):
        self.host = host
        self.port = port
        self.token = ""
        self.namespace = NAMESPACE
        self.base_url = "http://{host}:{port}/jobs".format(host=self.host, port=self.port)
        _logger.warning("Verify kubeflow account by func<login(username, password)>")

    def login(self, username: str = "", password: str = "", cloud: str = "qzm"):
        """
        kubeflow account verify
        :param username: kubeflow username
        :param password: kubeflow password
        :param cloud: choose which cloud platform ("qzm" or "huawei")
        :return:
        """
        session = requests.Session()
        response = session.get(self.base_url)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {"login": username, "password": password}
        session.post(response.url, headers=headers, data=data)
        try:
            self.token = session.cookies.get_dict()["authservice_session"]
            if cloud == "huawei":
                # self.namespace = "kubeflow"
                # 为了临时区分往华为云提交任务的人，使用的方法
                self.namespace = _parse_namespace(username)
                self.base_url = "http://w-hw-bj4-k8s.stonewise.cn:31080"
            elif cloud == "tencent":
                self.namespace = _parse_namespace(username)
                self.base_url = "http://43.138.0.41:31080"
            else:
                self.namespace = _parse_namespace(username)
            _logger.info("Connected to submit jobs successfully, namespace: {namespace}, cloud: {cloud}".format(
                namespace=self.namespace,
                cloud=cloud
            ))
        except KeyError:
            _logger.error("Incorrect account or password, try again.")

    def create(self, spc: Optional[Union[JobSpec, ReuseJobSpec]] = None):
        """
        create job by job spec obj
        :param spc: union of JobSpec, ReuseJobSpec
        :return: True(ok) or False(not ok)
        """
        response = requests.post(
            url=self.base_url + "/api/v2/create/{namespace}/{job_type}".format(namespace=self.namespace,
                                                                               job_type=spc.job_obj.get("jobType")),
            headers={"client_type": "easy-kubeflow"},
            cookies={"authservice_session": self.token},
            json=spc.job_obj)
        try:
            if response.json().get("code") == 200:
                time.sleep(5)
                sync_time = 5
                # sync job status until job status changed
                while sync_time < 30:
                    get_rsp = requests.get(
                        url=self.base_url + "/api/v2/get-status/{namespace}/{job_type}/{job_name}".format(
                            namespace=self.namespace,
                            job_name=spc.job_obj.get("jobName"),
                            job_type=spc.job_obj.get("jobType")),
                        headers={"client_type": "easy-kubeflow"},
                        cookies={"authservice_session": self.token}
                    )
                    if get_rsp.json().get("data").get("Status") == "Failed":
                        time.sleep(5)
                        sync_time += 5
                    else:
                        break
                _logger.info(response.json())
                return True
            else:
                _logger.error(response.json())
                return False
        except JSONDecodeError:
            _logger.error("Incorrect account or password, login again.")
            return False

    def delete(self, name: Optional[Union[str, JobSpec, ReuseJobSpec]], job_type: str = "standalone",
               timeout: int = 600):
        """
        delete job
        :param name: job name, JobSpec, ReuseJobSpec
        :param job_type:
        :param timeout: delete timeout
        :return: True(ok) or False(not ok)
        """
        if isinstance(name, str):
            job_name = name
        else:
            job_name = name.job_obj.get("jobName")
            job_type = name.job_obj.get("jobType")
        response = requests.delete(
            url=self.base_url + "/api/delete/{namespace}/{job_name}/{job_type}".format(namespace=self.namespace,
                                                                                       job_name=job_name,
                                                                                       job_type=job_type),
            headers={"client_type": "easy-kubeflow"},
            cookies={"authservice_session": self.token}
        )
        try:
            if response.json().get("code") == 200:
                time.sleep(5)
                sync_time = 5
                # sync job status until job pod removed
                while sync_time < timeout:
                    get_rsp = requests.get(
                        url=self.base_url + "/api/v2/get-status/{namespace}/{job_type}/{job_name}".format(
                            namespace=self.namespace,
                            job_name=job_name,
                            job_type=job_type),
                        headers={"client_type": "easy-kubeflow"},
                        cookies={"authservice_session": self.token}
                    )
                    if get_rsp.json().get("code") == 200:
                        time.sleep(5)
                        sync_time += 5
                    else:
                        break
                if sync_time >= timeout:
                    _logger.warning("Delete job timeout.")
                    return False
                else:
                    _logger.info(response.json())
                    return True
            else:
                _logger.error(response.json())
                return False
        except JSONDecodeError:
            _logger.error("Incorrect account or password, login again.")
            return False

    def get(self, name: Optional[Union[str, JobSpec, ReuseJobSpec]], job_type: str = "standalone"):
        """
        get job status info
        :param name: job name, JobSpec, ReuseJobSpec
        :param job_type:
        :return: True(ok) or False(not ok)
        """
        if isinstance(name, str):
            job_name = name
        else:
            job_name = name.job_obj.get("jobName")
            job_type = name.job_obj.get("jobType")
        response = requests.get(
            url=self.base_url + "/api/v2/get-status/{namespace}/{job_type}/{job_name}".format(namespace=self.namespace,
                                                                                              job_name=job_name,
                                                                                              job_type=job_type),
            headers={"client_type": "easy-kubeflow"},
            cookies={"authservice_session": self.token}
        )
        try:
            if response.json().get("code") == 200:
                _logger.info(response.json())
                return True
            else:
                _logger.error(response.json())
                return False
        except JSONDecodeError:
            _logger.error("Incorrect account or password, login again.")
            return False

    def resources(self, cpu: float = 0, memory: str = "1Gi", gpu: int = 1):
        resource = {
            "cpu": cpu,
            "gpu": gpu,
            "memory": memory
        }
        response = requests.post(
            url=self.base_url + "/api/v2/get/resource/remaining",
            headers={"client_type": "easy-kubeflow"},
            json=resource,
            cookies={"authservice_session": self.token}
        )
        try:
            if response.json().get("code") == 200:
                _logger.info(response.json())
                return True
            else:
                _logger.error(response.json())
                return False
        except JSONDecodeError:
            _logger.error("Incorrect account or password, login again.")
            return False

    def run_tensorboard(self, log_dir: str = None, ttl: int = 360):
        tb_name = "tb-" + str(uuid4())[:16]
        tb = {
            "hostvols": [
                {
                    "hostPath": log_dir,
                    "mountPath": log_dir
                }
            ],
            "duration_hour": ttl,
            "log_path": log_dir,
            "name": tb_name,
            "namespace": self.namespace
        }
        response = requests.post(
            url=self.base_url + "/api/v2/create/tensorboard",
            headers={"client_type": "easy-kubeflow"},
            json=tb,
            cookies={"authservice_session": self.token}
        )
        try:
            if response.json().get("code") == 200:
                _logger.info(response.json())
                return True
            else:
                _logger.error(response.json())
                return False
        except JSONDecodeError:
            _logger.error("Incorrect account or password, login again.")
            return False
