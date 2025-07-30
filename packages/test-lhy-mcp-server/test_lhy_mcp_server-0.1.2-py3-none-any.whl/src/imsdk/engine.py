"""
IM SDK Python封装模块

用于加载和封装Rust Universal IM SDK动态库
"""
import os
import ctypes
import sys
import threading
from typing import Dict, Any, List



from src.imsdk import LIB_DIR

USER_ID = ""

class IMSDK:
    """IM SDK的Python封装类"""
    
    def __init__(self) -> None:
        """初始化IM SDK"""
        # 初始化属性
        self.engine = None
        self.builder = None
    
    def engine_build(self, app_key: str, navi_host: str, device_id: str) -> Dict[str, Any]:
        """
        初始化IM SDK并返回状态
        
        Args:
            app_key: 应用的AppKey
            device_id: 设备ID
            
        Returns:
            失败：包含code和message的字典
            成功：包含code、app_key、device_id和message的字典
        """
        
        return {
            "code": 0,
            "app_key": app_key,
            "device_id": device_id,
            "message": "IM SDK初始化成功"
        }
       

    def engine_connect(self, token: str, timeout_sec: int = 10) -> Dict[str, Any]:
        """
        连接融云服务
        
        Args:
            token: 用户连接token
            timeout_sec: 连接超时时间，单位为秒
            
        Returns:
            失败：包含code和message的字典
            成功：包含code、user_id和message的字典
        """
        
        return {
                    "code": "0",
                    "user_id": "123",
                    "message": "连接成功" 
                }
    
    def send_message(self, receiver: str, content: str, conversation_type) -> Dict[str, Any]:
        """
        发送消息
        
        Args:
            receiver: 接收者ID
            content: 消息内容
            conversation_type: 会话类型，默认为单聊
            
        Returns:
            失败：包含code和message的字典
            成功：包含code、message_id和message的字典
        """
        
        return {"code": -2, "message": "发送消息超时，未收到回调"}
            
    
    def get_history_messages(self, target_id: str, conversation_type: int, count: int = 10, timestamp: int = 0, order: int = 0) -> List[Dict[str, Any]]:
        
        return [{"code": 0, "messages": [{"code": 0, "message_id": "123", "content": "测试消息"}]}]
        
    def engine_disconnect(self) -> Dict[str, Any]:
        """
        断开与IM服务器的连接
        
        Returns:
            包含code和message的字典
        """
        
        return {"code": 0, "message": "断开连接成功"}


    def destroy(self):
        """
        销毁IM SDK
        """
        if self.engine:
            self.engine_disconnect()
        self.engine = None
        self.builder = None

# 创建默认SDK实例，使用默认参数
default_sdk = IMSDK() 