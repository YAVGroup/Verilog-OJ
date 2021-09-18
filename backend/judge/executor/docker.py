import subprocess, datetime, json
import tempfile, os, shutil, logging, traceback
import judge.executor.annotated_subprocess as asubprocess

from .base import BaseExecutor

logger = logging.getLogger(__name__)

class DockerExecutor(BaseExecutor):
    """Run in docker, host docker socket provided by bind mount

    Docker spawned doesn't have network connected.
    /judge/{testcase, problem, submit} is created in /host_dir and then
    bind mounted in target docker.

    Notice the files created in isolated container is root/root, so
    there might be trouble read/write then as non-root user.
    """
    def __init__(self, detail, judger_config):
        self.detail = detail
        self.judger_config = judger_config

    # returns child_docker_id
    def create_docker(
            self,
            docker_image_name,
            id,
            bind_mount_hostside,      # Shell escape by yourself
            bind_mount_containerside,
            container_cmd,            # add at last
            readonly=False,
            pids_limit=512,     # enough for average user, not enough for great harm
            mem_limit=512,      # size limit in MB
            cpus=1
        ):

        cmd = (
            f"docker create --init --rm -i --network none "
            f"--pids-limit {pids_limit} -m {mem_limit}M --memory-swap -1 --cpus {cpus} "
        )

        if readonly:
            cmd += "--read-only "

        timestr = datetime.datetime.now().strftime("%m%d_%H%M%S_%f")[:-3]
        child_docker_name = f"judge_container_u{id}_{timestr}"
        cmd += f'--name "{child_docker_name}" '

        # Bind mount related stuff
        cmd += f'-v "{bind_mount_hostside}:{bind_mount_containerside}" '

        cmd += docker_image_name + " "

        cmd += container_cmd
        logger.info(f"Called with {cmd}")
        return subprocess.check_output(cmd, shell=True).decode().strip()

    def check_alive(self, child_docker_id):
        cmd = f"docker inspect {child_docker_id}"
        logger.info(f"Check alive with {cmd}")
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        out_cmd, _ = process.communicate()

        json_obj = json.loads(out_cmd)
        if len(json_obj) == 0:
            logger.info(f"{child_docker_id} is no longer alive")
            return False
        else:
            logger.info(f"{child_docker_id} is still alive")
            return True
        

    def start_docker(self, child_docker_id, timeout):
        """Returns the timestamped aggregate log"""
        cmd = f"timeout -s 9 {timeout} docker start -i {child_docker_id}"
        logger.info(f"Called with {cmd}")
        process = asubprocess.Popen(cmd, shell=True)
        annotated_log = process.communicate()
        
        is_alive = self.check_alive(child_docker_id)
        if is_alive:
            cmd = f"docker kill {child_docker_id}"
            logger.info(f"Kill running docker with {cmd}")
            process = subprocess.Popen(cmd, shell=True)
            process.communicate()
        
        return annotated_log

    def prepare(self):
        self.move_status("JUDGING")

    def run(self):
        base_dir = None
        comp_dir = None
        try:
            idx = 0
            while True:
                comp_dir = str(self.detail['submission_result']['id']) + f"_{idx}/"
                base_dir = os.path.join(
                    self.judger_config['docker_host_dir'],
                    comp_dir
                )
                if not os.path.exists(base_dir):
                    break
                else:
                    idx += 1
            
            os.mkdir(base_dir)
            self.place_tree(base_dir)
            os.chdir(base_dir)

            possible_errors = []
            #print(self.judger_config)
            child_docker_id = self.create_docker(
                self.judger_config['docker_image'],
                self.detail['submission_result']['id'],
                os.path.join(self.judger_config['docker_judger_host_path'], comp_dir),
                self.judger_config['docker_inside_dir'],
                f'/bin/bash -c "cd {self.judger_config["docker_inside_dir"]};/bin/bash {self.judger_config["docker_inside_dir"]}/testcase/{self.judger_config["entry_file"]}"',
                readonly=False,
                mem_limit=self.detail['testcase']['mem_limit']
            )

            # assign a default time limit
            time_limit = self.judger_config['max_time_limit']
            if self.detail['testcase']['time_limit'] > 0 and self.detail['testcase']['time_limit'] < time_limit:
                time_limit = self.detail['testcase']['time_limit']

            logger.info(f"Run with mem_limit={self.detail['testcase']['mem_limit']} and time_limit={time_limit}")

            buf_log = self.start_docker(child_docker_id, timeout=time_limit)
            log = None
            if self.judger_config['submit_logs']:
                log = buf_log.decode("utf8")

            # Fetch score, waveform & possible error - root required
            score_file_path = os.path.join(base_dir, self.judger_config['final_score'])
            score = None
            if os.path.exists(score_file_path):
                with open(score_file_path, "r") as f:
                    score = int(f.read())
            logger.info("Final score: {}".format(score))

            if score is None:
                score = 0

            appdata = ""
            appdata_file_path = os.path.join(base_dir, self.judger_config['appdata_path'])
            try:
                with open(appdata_file_path, "r") as f:
                    appdata = f.read()
            except:
                appdata = "Error reading appdata ({}), traceback below\n{}".format(
                    appdata_file_path, traceback.format_exc())
            
            possible_error_file_path = os.path.join(base_dir, self.judger_config['possible_error_path'])
            try:
                with open(possible_error_file_path, "r") as f:
                    possible_errors.append(f.read().strip())
            except:
                possible_errors.append("NA")
            
            self.patch_result({
                'grade': str(score),
                'log': log if log is not None else "Suppressed due to judger configuration",
                'status': 'DONE',
                'app_data': appdata if self.judger_config['submit_appdata'] else 'N/A',
                'possible_failure': possible_errors[0] if len(possible_errors) > 0 else "NONE"
            })

        finally:
            if not shutil.rmtree.avoids_symlink_attacks:
                logger.warning("shutil.rmtree.avoids_symlink_attacks evaluates to false, symlink attack possible!")
            
            shutil.rmtree(base_dir)