import io
import os
import zipfile
import logging

from server import BinaryWebServer
from buildconf import BuildConfReader, BuildConfError
from tasks import TaskManager
from logutils import ListLoggingHandler

listen_address = "0.0.0.0"
listen_port = 8080
build_directory = "/build"

head_logger = logging.getLogger(__name__)
buildconf_path = os.path.join(build_directory, "buildconf.yaml")

def start_head():
    logging.info("Application main node has been started")
    external_server = BinaryWebServer(
        listen_address, listen_port, handle_build_request)
    try:
        external_server.start_server()
    except KeyboardInterrupt:
        logging.info("Received Ctrl+C. Closing..")
    external_server.stop_server()

def handle_build_request(request_data):
    response_data = {"success": False, "logs": []}
    if not (("zip" in request_data) 
        or ("target" in request_data)):
        return response_data
    log_list = response_data["logs"]
    log_handler = ListLoggingHandler(log_list)
    head_logger.addHandler(log_handler)
    try:
        try:
            extract_source_zip(request_data["zip"])
        except (zipfile.BadZipFile, zipfile.LargeZipFile) as error:
            logging.error("Error extracting source: " + str(error))
            return response_data
        try:
            build_reader = BuildConfReader.from_path(
                buildconf_path)
        except BuildConfError as error:
            logging.error("Error reading buildconf.yaml: " + str(error))
            return response_data
        build_tasks = TaskManager(
            request_data["target"],
            build_reader.targets_func)
        assign_build_tasks(build_tasks, log_list)
        try:
            artifact_data = package_artifact_zip(build_directory, build_reader.artifact)
        except (zipfile.BadZipFile, zipfile.LargeZipFile, ForbiddenPath) as error:
            logging.error("Error packaging artifact: " + str(error))
            return response_data
        response_data["artifact"] = artifact_data
        response_data["success"] = False
        return response_data
    finally:
        head_logger.removeHandler(log_handler)

def extract_source_zip(zip_data, out_dir):
    with io.BytesIO(zip_data) as mem_file:
        with zipfile.ZipFile(mem_file, mode = "r") as mem_zip:
            mem_zip.extractall(out_dir)

def assign_build_tasks(build_tasks, log_list):
    while not build_tasks.all_done:
        pass

def package_artifact_zip(in_dir, artifact_entries):
    with io.BytesIO() as mem_file:
        with zipfile.ZipFile(mem_file, mode = "x", 
                compression = zipfile.ZIP_DEFLATED, 
                compresslevel= 9) as mem_zip:
            if "directories" in artifact_entries:
                for dir_entry in artifact_entries["directories"]:
                    if ".." in dir_entry:
                        raise ForbiddenPath("The '..' path is forbidden for security reasons")
                    dir_path = os.path.realpath(os.path.join(in_dir, dir_entry))
                    for root, _, file_names in os.walk(dir_path):
                        for file_name in file_names:
                            file_path = os.path.join(root, file_name)
                            file_relpath = os.path.relpath(file_path, start = in_dir)
                            mem_zip.write(file_path, arcname = file_relpath)  
            if "files" in artifact_entries:
                for file_entry in artifact_entries["files"]:
                    if ".." in file_entry:
                        raise ForbiddenPath("The '..' path is forbidden for security reasons")
                    file_path = os.path.realpath(os.path.join(in_dir, file_entry))
                    file_relpath = os.path.relpath(file_path, start = in_dir)
                    mem_zip.write(file_path, arcname = file_relpath)
        mem_file.seek(0)
        return mem_file.read()

class ForbiddenPath(Exception):
    pass
