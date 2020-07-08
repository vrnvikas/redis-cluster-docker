import os
import subprocess
import docker


def get_env_variable(var_name, default=None):
    """Get the environment variable or raise exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = "The environment variable {} was missing, abort...".format(
                var_name
            )
            raise EnvironmentError(error_msg)


def get_container_ip(container, network_name):
    """Get container IP for given container."""
    return container['NetworkSettings']['Networks'][network_name]['IPAddress']


def create_cluster(docker_client, compose_project_name,node_names, node_ports, network_name):
    """Initialize redis cluster."""
    command_prefix = "echo yes | redis-cli -p 6379 --cluster create "
    command_suffix = "--cluster-replicas 1 --cluster-yes"
    nodes = ""
    for node, port in zip(node_names, node_ports):
        node_ip = get_container_ip(docker_client.inspect_container(compose_project_name + "_" + node + "_1"),
                                   compose_project_name + "_" + network_name)
        nodes += node_ip + ":" + port + " "

    create_cluster_cmd_final = command_prefix + nodes + command_suffix
    print(create_cluster_cmd_final)
    return subprocess.run(create_cluster_cmd_final, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          universal_newlines=True, text=True, shell=True)


client = docker.APIClient(base_url='unix://var/run/docker.sock')

COMPOSE_PROJECT_NAME = get_env_variable('COMPOSE_PROJECT_NAME')
REDIS_NODES = get_env_variable('REDIS_NODES').split(',')
REDIS_NODE_PORTS = get_env_variable('REDIS_NODE_PORTS').split(',')
REDIS_NETWORK = get_env_variable('REDIS_NETWORK')

print("Initiating Cluster Creating")

result = create_cluster(client, COMPOSE_PROJECT_NAME, REDIS_NODES, REDIS_NODE_PORTS, REDIS_NETWORK)

print("Exit Code : ")
print(result.returncode)

if result.returncode == 0:
    print("Cluster Created")
    print(result.stdout)
else:
    print("Error in Creating cluster")
    print(result.stderr)
