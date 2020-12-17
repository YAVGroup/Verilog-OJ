import subprocess, datetime

from .base import BaseExecutor

class DockerExecutor(BaseExecutor):
    def __init__(self, detail, judger_config):
        self.mem_limit = detail['mem_limit']
        self.time_limit = detail['time_limit']

    # returns child_docker_id
    def create_docker(
            self,
            docker_image_name,
            id, 
            readonly=False,
            pids_limit=512,     # enough for average user, not enough for great harm
            mem_limit="512M",
            cpus=1
        ):

        cmd = (
            f"docker create --init --rm -i --network none "
            f"--pids-limit {pids_limit} -m {mem_limit} --memory-swap -1 --cpus {cpus} "
        )

        if readonly:
            cmd += "--read-only "

        timestr = datetime.datetime.now().strftime("%m%d_%H%M%S_%f")[:-3]
        child_docker_name = f"{docker_image_name}_u{id}_{timestr}"
        cmd += f'--name "{child_docker_name}" '

        cmd += docker_image_name

        return subprocess.check_output(cmd, shell=True).decode().strip()

    def start_docker(self, child_docker_id, timeout):
        cmd = f"timeout -s 9 {timeout} docker start -i {child_docker_id}"
        subprocess.run(cmd, shell=True)
