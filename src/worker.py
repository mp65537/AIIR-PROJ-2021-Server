import os
import subprocess
import logging

from mpi4py import MPI

from logutils import ListLoggingHandler

node_comm = MPI.COMM_WORLD
node_rank = node_comm.Get_rank()

comm_tag = 25
shell_path = os.getenv("BUILDER_SH_PATH", "/bin/bash")
shell_switch = os.getenv("BUILDER_SH_SWITCH", "-c")
max_exec_time = int(os.getenv("BUILDER_MAX_EXEC_TIME", "600"))
build_directory = os.getenv("BUILDER_DIR", "/build")

worker_logger = logging.getLogger(__name__ + str(node_rank))

def start_worker():
    logging.info("Builder worker with id = {} has been started".format(node_rank))
    while True:
        task_data = node_comm.recv(source = 0, tag = comm_tag)
        if task_data["id"] == 0:
            node_comm.send({"success": True, "task_id": 0}, dest = 0, tag = comm_tag)
        else:
            node_comm.send(execute_task(task_data), dest = 0, tag = comm_tag)

def execute_task(task_data):
    task_result = {
        "success": False,
        "node_id": node_rank,
        "task_id": task_data["id"],
        "logs": []
    }
    task_target_name = task_data["name"]
    task_target_path = os.path.join(build_directory, task_target_name)
    task_cmd = task_data["command"]
    log_handler = ListLoggingHandler(task_result["logs"])
    worker_logger.addHandler(log_handler)
    try:
        exit_code = execute_task_cmd(task_cmd)
        worker_logger.info("Command '{}' exited with code = {}"
            .format(task_cmd, exit_code))
        if exit_code:
            worker_logger.error("Last command exited with non-zero code!")
            return task_result
        if task_data["check_exist"] and (not os.path.exists(task_target_path)):
            worker_logger.error("Target '{}' does not exists after last command")
            return task_result
        task_result["success"] = True
        return task_result
    finally:
        worker_logger.removeHandler(log_handler)

def execute_task_cmd(cmd_str):
    proc_obj = subprocess.Popen([shell_path, shell_switch, cmd_str], 
        cwd = build_directory)
    return proc_obj.wait(timeout = max_exec_time)
