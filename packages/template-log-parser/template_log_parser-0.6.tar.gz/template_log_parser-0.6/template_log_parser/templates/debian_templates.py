id_process = "{time} {server_name} {process}[{id}]: {message}"
id_process_2 = "{time} {server_name} {process}[{id}] {message}"
non_id_process = "{time} {server_name} {process}: {message}"
org_desktop = "{time} {server_name} org.{process} {message}"
pycharm = "{time} {server_name} pycharm-{process} {message}"
rsync = "{time} {server_name} rsync-{id} {message}"
stream_controller = "{time} {server_name} com.core447.StreamController.des {message}"
ubuntu = "{time} {server_name} ubuntu-{process} {message}"


debian_template_dict = {
    "]:": [id_process, 5, "id_process"],
    ":": [non_id_process, 4, "non_id_process"],
    "rsync": [rsync, 4, "rsync"],
    "StreamController": [stream_controller, 3, "stream_controller"],
    "org": [org_desktop, 4, "org_desktop"],
    "pycharm": [pycharm, 4, "pycharm"],
    "ubuntu": [ubuntu, 4, "ubuntu"],
    "] ": [id_process_2, 5, "id_process"],  # Run very last
}
