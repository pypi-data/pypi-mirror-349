import requests
from typing import *
from dataclasses import dataclass

@dataclass
class ClientConfig:
    base_url: str
    username: Optional[str] = None
    password: Optional[str] = None
    token: Optional[str] = None

@dataclass
class ResultData:
    data_header: List[str]
    data: List[List[Any]]
    error: Optional[str] = None

class VoxelClient:
    def __init__(self, config: ClientConfig):
        self.config = config

    def _get_default_config(self)-> Dict[str, Any]:
        return {
            "username": self.config.username,
            "password": self.config.password,
            "token": self.config.token
        }

    def get_available_versions(self) -> List[str]:
        url = f"{self.config.base_url}/select_voxel_version/"
        data = self._get_default_config()
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"获取版本列表失败: {str(e)}")
            return []


    def execute_sql(self, version: str, sql: str) -> ResultData:
        url = f"{self.config.base_url}/execute_sql/"
        data = self._get_default_config()
        data["version"] = version
        data["sql"] = sql
        
        try:
            # 发送POST请求
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            # 返回响应数据
            json_data = response.json()
            return ResultData(
                data_header=json_data["data_header"],
                data=json_data["data"],
                error=json_data["error"]
            )
            
        except requests.exceptions.RequestException as e:
            return ResultData(
                data_header=[],
                data=[],
                error=f"请求失败: {str(e)}"
            )

    def get_table_data(self, version: str, table_name: str, name_list: List[str] = None) -> ResultData:
        if name_list is None:
            select_str = "*"
        else:
            select_str = ", ".join(name_list)
        return self.execute_sql(version, f"SELECT {select_str} FROM {table_name} ")

    def get_table_define(self, version: str) -> ResultData:
        result = self.get_table_data(version, "TableDefine", name_list=["Name", "Type", "Path"])
        return result

    def get_table_link(self, version: str) -> ResultData:
        result = self.get_table_data(version, "TableLink", name_list=["TableNameA", "LinkNameA", "TableNameB", "LinkNameB"])
        return result