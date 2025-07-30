# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-01-29 13:26:17
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-06 23:58:52
# @Description: A plugin suite contains multiple plugins. A PluginSuite
# object stores every information about a suite, including the dependencies between
# each plugins, suite metadata , suite documentation path, suite format markdown path.
# When itself is called, it execute procedure to run the suite.
import sys
import os
from collections import defaultdict
from typing import Dict, List, Any, Tuple, Optional
import subprocess
import os.path
import yaml   
import shutil
import xml.etree.ElementTree as ET

from gailbot.shared.exception.serviceException import FailPluginSuiteRegister
from gailbot.pluginSuiteManager.error.errorMessage import SUITE_REGISTER_MSG
from gailbot.pluginSuiteManager.suite.gbPluginMethod import GBPluginMethods
from gailbot.configs import PLUGIN_CONFIG
from gailbot.pluginSuiteManager.suite.pluginData import Suite, ConfModel, Requirements, Dependencies
from gailbot.shared.pipeline import (
    Pipeline,
)
from gailbot.shared.utils.general import get_name
from pathlib import Path
import importlib
import platform
from gailbot.pluginSuiteManager.suite.pluginComponent import PluginComponent
from gailbot.shared.utils.logger import makelogger
from gailbot.shared.utils.general import read_toml
from gailbot.workspace.manager import WorkspaceManager
from gailbot.workspace.directory_structure import OutputFolder

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gailbot.pluginSuiteManager.APIConsumer import APIConsumer
from S3BucketManager import S3BucketManager
from userpaths import get_profile
from gailbot.shared.utils.download import download_single_url
import platform
import threading, signal

USER = get_profile()

logger = makelogger("plugin suite")

import uuid

def get_real_username():
    try:
        return subprocess.check_output(["stat", "-f%Su", "/dev/console"], text=True).strip()
    except Exception:
        return os.environ.get("USER") or os.environ.get("LOGNAME") or os.getlogin()

def get_gailbot_root_path() -> str:
    username = get_real_username()
    system = platform.system()

    if system == "Darwin":  # macOS
        base_path = os.path.join("/Users", username)
    elif system == "Linux":
        base_path = os.path.join("/home", username)
    else:
        raise EnvironmentError(f"Unsupported OS: {system}")

    if os.path.isdir(base_path):
        return base_path

    # Fall back to full scan if not found
    for root, dirs, files in os.walk("/", topdown=True):
        dirs[:] = [d for d in dirs if not d.startswith(".") and "Volumes" not in root and "private" not in root]
        if os.path.basename(root) == username:
            if os.path.isdir(root):
                return root

    raise FileNotFoundError(f"GailBot directory not found under expected paths for {username}")

class PluginSuite:
    """
    Manages a suite of plugins and responsible for loading, queries, and
    execution.
    Needs to store the details of each plugin (source file etc.)
    """

    def __init__(self, conf_model: ConfModel, root: str):
        """a dictionary of the dependency map  -> transcriptionPipeline argument"""
        self.suite_name = conf_model.suite.name
        self.conf_model = conf_model
        self.source_path = root
        self.optional_plugins: List[str] = []
        self.required_plugins: List[str] = []
        self.workspace = WorkspaceManager()
        self.workspace.init_workspace()
        # suite and document_path will be loaded in _load_from_config
        self.suite = conf_model.suite
        self.formatmd_path = os.path.join(root, self.suite_name, PLUGIN_CONFIG.FORMAT)
        self.dependency_map, self.plugins = self._load_from_config(conf_model, root)

        # self.download_plugins(plugin_ids= self.plugins)

        # Add vars here from conf.
        self._is_ready = True
        self.is_official = False

    @property
    def name(self) -> str:
        return self.suite_name

    @property
    def is_ready(self):
        return self._is_ready

    def set_to_official_suite(self):
        """set the plugin to official plugin"""
        self.is_official = True

    def __repr__(self):
        return (
            f"Plugin Suite: {self.name}\n" f"Dependency map: {self.dependency_graph()}"
        )

    def mountable_or_root(self, candidate: str, root: str) -> str:
 
        test_cmd = [
            "docker", "run", "--rm",
            "-v", f"{candidate}:/mnt:rw",
            "alpine", "true"                 # tiny base image always present
        ]
        ok = subprocess.run(
            test_cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode == 0

        if ok:
            return candidate

        fallback = Path(root, "gailbot_work")
        fallback.mkdir(parents=True, exist_ok=True)
        return str(fallback)

    def __call__(self, base_input: Any, methods: GBPluginMethods, selected_plugins=None) -> Dict:
        selected_plugins = self.plugins
        output_path = OutputFolder(methods.out_path)

        adj_list = {k: v for k, v in self.dependency_map.items() if k in selected_plugins}
        dag = self._topological_sort(adj_list)

        host_id = next(pid for pid, deps in self.dependency_map.items() if not deps)
        host_base_path = selected_plugins[host_id]

        host_path = os.path.join(self.workspace.plugins, host_base_path)
        os.makedirs(os.path.join(host_path, "transcript"), exist_ok=True)
        with open(os.path.join(host_path, "transcript", "dag.txt"), "w") as f:
            f.write(" ".join(dag))
        xml = self._convert_to_xml(methods.utterances)
        with open(os.path.join(host_path, "transcript", "original_data.txt"), "w") as f:
            f.write(ET.tostring(xml, encoding="unicode", method="xml"))
        os.makedirs(output_path.transcribe, exist_ok=True)
        with open(os.path.join(output_path.transcribe, "original_trancript.xml"), "w") as f:
            f.write(ET.tostring(xml, encoding="unicode", method="xml"))

        root_path = get_gailbot_root_path()
        project_name = uuid.uuid4().hex[:128]

        methods.work_path = self.mountable_or_root(methods.work_path, root_path)
        os.makedirs(methods.work_path, exist_ok=True)
        with open(os.path.join(methods.work_path, ".write_test"), "w") as f:
            f.write("ok")

        env = os.environ.copy()
        env["WORK_PATH"] = methods.work_path
        env["OUTPUT"]    = str(output_path.root)
        env["NAME"]      = project_name
        env["ROOT"]      = root_path

        system = platform.system()
        if system == "Linux":
            pagesize   = os.sysconf("SC_PAGESIZE")
            phys_pages = os.sysconf("SC_PHYS_PAGES")
            total_bytes = pagesize * phys_pages
        elif system == "Darwin":
            total_bytes = int(subprocess.check_output(["sysctl","-n","hw.memsize"]))
        else:
            total_bytes = 1 << 30
        shm_mb  = total_bytes // (2 * 1024 * 1024)
        threads = os.cpu_count() or 1

        compose_file = os.path.join(self.source_path, self.suite_name, "plugin_suite_composed.yaml")
        cfg = yaml.safe_load(open(compose_file))
        for svc in cfg["services"].values():
            svc["shm_size"] = f"{shm_mb}m"
            svc.setdefault("environment", {})["OMP_NUM_THREADS"] = str(threads)
        yaml.safe_dump(cfg, open(compose_file, "w"), sort_keys=False)

        subprocess.run(
            ["docker","compose","-f",compose_file,"-p",project_name,
            "up","--build","-d"],
            env=env, check=True
        )
        log_proc = subprocess.Popen(
            ["docker", "compose", "-f", compose_file, "-p", project_name,
            "logs", "--no-color", "--timestamps", "-f"],
            env=env,
            stdout=subprocess.PIPE,      # capture stdout
            stderr=subprocess.STDOUT,    # merge stderr in
            text=True,
        )

        def _forward_logs():
            for line in log_proc.stdout:
                logger.info(line.rstrip())

        t = threading.Thread(target=_forward_logs, daemon=True)
        t.start()

        service_names = list(cfg["services"].keys())
        subprocess.run(
            ["docker","compose","-f",compose_file,"-p",project_name,
            "wait"] + service_names,
            env=env, check=True,
            text=True
        )
        log_proc.send_signal(signal.SIGINT)
        log_proc.wait()

        subprocess.run(
            ["docker","compose","-f",compose_file,"-p",project_name,
            "down","--rmi","all","--volumes","--remove-orphans"],
            env=env, check=True,
            
        )


        os.makedirs(output_path.analysis, exist_ok=True)

        # 1) Collect all plugin result files into results dict
        results: Dict[str, Dict[str, str]] = defaultdict(dict)
        for item in os.listdir(methods.work_path):
            src_path = os.path.join(methods.work_path, item)
            if os.path.isfile(src_path) and item.startswith("plugin_") and "_result." in item:
                # parse plugin_id and extension
                base_name = os.path.basename(item)               # plugin_{id}_result.ext
                parts = base_name[:43].split("_")
                plugin_id = parts[1]
                ext = os.path.splitext(item)[1].lstrip(".")
                # read content
                with open(src_path, "r", encoding="utf-8") as f:
                    results[plugin_id][ext] = f.read()

        # 2) Write each plugin’s results into its own folder
        for plugin_id, files in results.items():
            plugin_dir = os.path.join(output_path.analysis, f"plugin_{plugin_id}")
            os.makedirs(plugin_dir, exist_ok=True)
            for ext, content in files.items():
                fname = f"plugin_{plugin_id}_result.{ext}"
                dst_path = os.path.join(plugin_dir, fname)
                with open(dst_path, "w", encoding="utf-8") as dst:
                    dst.write(content)
                logger.info(f"Wrote {dst_path}")

        # 3) Also collect the final plugin’s files into a separate folder
        final_plugin_id = dag[-1]
        final_dir = os.path.join(output_path.analysis, "final_plugin")
        os.makedirs(final_dir, exist_ok=True)
        for ext, content in results.get(final_plugin_id, {}).items():
            fname = f"plugin_{final_plugin_id}_result.{ext}"
            dst_path = os.path.join(final_dir, fname)
            with open(dst_path, "w", encoding="utf-8") as dst:
                dst.write(content)
            logger.info(f"Wrote final plugin file {dst_path}")



    def check_required_files(self, directory):
        required_files = {"app.py", "client.py", "utils.py"}
        existing_files = set(os.listdir(directory))

        return required_files.issubset(existing_files)

    def is_plugin(self, plugin_name: str) -> bool:
        """given a name , return true if the plugin is in the plugin suite"""
        return plugin_name in self.plugins

    def plugin_names(self) -> List[str]:
        """Get names of all plugins"""
        return list(self.plugins.keys())

    def dependency_graph(self) -> Dict:
        """Return the entire dependency graph as a dictionary"""
        return self.dependency_map

    def get_meta_data(self) -> Suite:
        """get the metadata about this plugin"""
        return self.suite



    ##########
    # PRIVATE
    ##########
    def _load_from_config(
        self, conf_model: ConfModel, root: str
    ) -> Tuple[Dict[str, List[str]], Dict[str, str]] | None:
        """
        load the plugin suite, the information about each plugin name,
        and its path is stored in the dict_config, all path information
        is relative to the abs_path

        Parameters
        ----------
        conf_model: stores the plugin suite data for suite registration
        root: the path to the root folder of the plugin suite source code

        """
        plugins: Dict[str, str] = dict()

        plugin_entries = conf_model.suite.plugins.split(' ')

        for plugin_id in plugin_entries:
            plugin_path = os.path.join(self.workspace.plugins, plugin_id)
            plugins[plugin_id] = plugin_path
            
        self.download_plugins(plugin_ids = plugin_entries)
        
        dependency_map: Dict[str, List[str]] = self._create_adjacency_list(plugins)


        return (
            dependency_map,
            plugins,
        )  
    

    def _create_adjacency_list(self, plugins_data: Dict[str, str]) -> Dict[str, List[str]]:
        """
        Create an adjacency list from the list of plugin data.

        Args:
        - plugins_data: List of dictionaries containing plugin information.

        Returns:
        - Dict: An adjacency list where keys are plugin names and values are lists of dependencies.
        """
        adjacency_list = {}
        for plugin_id, plugin_path in plugins_data.items():
            toml_file_path = os.path.join(plugin_path, "plugin_info.toml")
            

            plugin_info = read_toml(toml_file_path)

            adjacency_list[plugin_id] = list(plugin_info.get('requirements', {}).values())

                    

        return adjacency_list
    

    def _convert_to_xml(self, data):
        root = ET.Element("transcript")
        
        current_speaker = None
        current_u = None
        
        for data in data.values():
            for item in data:
                #logger.info(item)
                if item['speaker'] != current_speaker:
                    current_speaker = item['speaker']
                    current_u = ET.SubElement(root, "u", speaker=current_speaker)
                
                word = ET.SubElement(current_u, "w", start=str(item['start']), end=str(item['end']))
                word.text = item['text']

        return root



    
    def _topological_sort(self, adj_list):
        # Initialize the graph and in-degree dictionary
        graph = {}
        in_degree = {}

        # Build the graph and compute in-degrees of each node
        for node in adj_list:
            if node not in graph:
                graph[node] = []
            if node not in in_degree:
                in_degree[node] = 0
            for dep in adj_list[node]:
                if dep not in graph:
                    graph[dep] = []
                graph[dep].append(node)
                if node not in in_degree:
                    in_degree[node] = 0
                in_degree[node] += 1

        # Find all nodes with in-degree 0
        queue = []
        for node in in_degree:
            if in_degree[node] == 0:
                queue.append(node)
        
        order = []

        # Process nodes with in-degree 0 and update the in-degrees of their neighbors
        while queue:
            current = queue.pop(0)
            order.append(current)
            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Check if there was a cycle
        if len(order) == len(in_degree):
            return order
        else:
            raise ValueError("A cycle was detected in the dependencies")



    
    def _separate_plugins(self, adj_list):
        # Create dictionaries to store the counts of incoming and outgoing edges
        outgoing_edges = defaultdict(set)
        incoming_edges = defaultdict(set)
        
        # Populate the dictionaries with the adjacency list information
        for plugin, dependencies in adj_list.items():
            outgoing_edges[plugin].update(dependencies)
            for dep in dependencies:
                incoming_edges[dep].add(plugin)
        
        # Find independent and required plugins
        self.optional_plugins = [plugin for plugin in outgoing_edges if plugin not in incoming_edges]
        self.required_plugins = [plugin for plugin in incoming_edges]
        


    def sub_dependency_graph(
        self, selected: List[str]
    ) -> Optional[Dict[str, List[str]]]:
        """
        given a selected list of plugins, return a subgraph of the dependency graph that
        include only the required plugin and the list of selected plugin

        Parameters
        ----------
        selected

        Returns
        -------

        """
        selected.extend(self.required_plugins)
        selected = set(selected)
        new_dependency = dict()
        for key, dependency in self.dependency_map.items():
            if key in selected:
                new_dependency[key] = list(
                    filter(lambda elt: elt in selected, dependency)
                )
        if not self.__check_dependency(new_dependency):
            logger.error(f"cannot resolve dependency for graph {new_dependency}")
        return new_dependency

    def __check_dependency(self, graph: Dict[Any, List[Any]]):
        """

        Parameters
        ----------
        graph

        Returns None
        -------

        Raises
        -------
        FailPluginSuiteRegister

        """
        visited = {k: 0 for k in graph.keys()}

        def check_circle(node: Any):
            visited[node] = -1
            for dependency in graph[node]:
                if visited[dependency] == -1:
                    raise FailPluginSuiteRegister(
                        self.suite_name,
                        SUITE_REGISTER_MSG.FAIL_LOAD_PLUGIN.format(
                            plugin=node,
                            cause=f" cannot resolve dependency {dependency} for plugin {node}",
                        ),
                    )
                elif visited[dependency] == 0:
                    if check_circle(dependency):
                        raise FailPluginSuiteRegister(
                            self.suite_name,
                            SUITE_REGISTER_MSG.FAIL_LOAD_PLUGIN.format(
                                plugin=node,
                                cause=f" cannot resolve dependency {dependency} for plugin {node}",
                            ),
                        )
            visited[node] = 1

        for node in graph.keys():
            check_circle(node)

        return True
    
    def download_plugins(self, plugin_ids: List[str]):
        s3 = S3BucketManager.get_instance()
        api = APIConsumer.get_instance()
        for plugin in plugin_ids:
            plugin_info = api.fetch_plugin_info(plugin_id= plugin)
            
            s3_url = plugin_info['s3_url']
            local_dir = os.path.join(self.workspace.plugins, plugin)
            if not os.path.isdir(local_dir):
                os.makedirs(local_dir)
            download_single_url(url= s3_url, download_path= local_dir, extract_root= local_dir, s3_client=s3.get_s3(), unzip= True, true_extract=True)