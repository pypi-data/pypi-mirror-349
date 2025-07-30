import os
import platform
import socket
import getpass
import datetime
import psutil
import json
import subprocess
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# 初始化MCP服务器
mcp = FastMCP(name="utils-toolkit", host="0.0.0.0", port=8000)

def main():
    """主函数，启动MCP服务器"""
    mcp.run()

@mcp.tool(name="get_system_info", description="获取系统信息，包括操作系统版本、网络IP、登录用户和当前时间")
def get_system_info() -> dict:
    """
    获取系统信息，包括操作系统版本、网络IP、登录用户和当前时间
    
    Returns:
        包含系统信息的字典
    """
    # 获取操作系统信息
    os_info = {
        "system": platform.system(),
        "version": platform.version(),
        "release": platform.release(),
        "architecture": platform.machine()
    }
    
    # 获取网络IP
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
    except Exception:
        ip_address = "无法获取IP地址"
    
    # 获取当前登录用户
    try:
        current_user = getpass.getuser()
    except Exception:
        current_user = "无法获取用户信息"
    
    # 获取当前时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        "os_info": os_info,
        "network": {
            "hostname": hostname,
            "ip_address": ip_address
        },
        "user": current_user,
        "current_time": current_time
    }

@mcp.tool(name="get_hardware_info", description="获取硬件配置信息，包括CPU、内存和GPU")
def get_hardware_info() -> dict:
    """
    获取硬件配置信息，包括CPU、内存和GPU
    
    Returns:
        包含硬件信息的字典
    """
    # CPU信息
    cpu_info = {
        "physical_cores": psutil.cpu_count(logical=False),
        "total_cores": psutil.cpu_count(logical=True),
        "cpu_usage_percent": psutil.cpu_percent(),
        "cpu_freq": {
            "current": psutil.cpu_freq().current if psutil.cpu_freq() else "未知",
            "min": psutil.cpu_freq().min if psutil.cpu_freq() and psutil.cpu_freq().min else "未知",
            "max": psutil.cpu_freq().max if psutil.cpu_freq() and psutil.cpu_freq().max else "未知"
        }
    }
    
    # 内存信息
    memory = psutil.virtual_memory()
    memory_info = {
        "total": f"{memory.total / (1024**3):.2f} GB",
        "available": f"{memory.available / (1024**3):.2f} GB",
        "used": f"{memory.used / (1024**3):.2f} GB",
        "percent": f"{memory.percent}%"
    }
    
    # GPU信息（尝试使用nvidia-smi获取）
    gpu_info = {}
    try:
        nvidia_smi = subprocess.check_output("nvidia-smi --query-gpu=name,memory.total,memory.used,memory.free,temperature.gpu --format=csv,noheader", shell=True)
        nvidia_smi = nvidia_smi.decode("utf-8").strip().split("\n")
        gpu_info["available"] = True
        gpu_info["devices"] = []
        
        for i, line in enumerate(nvidia_smi):
            values = [x.strip() for x in line.split(",")]
            if len(values) >= 5:
                gpu_info["devices"].append({
                    "id": i,
                    "name": values[0],
                    "memory_total": values[1],
                    "memory_used": values[2],
                    "memory_free": values[3],
                    "temperature": values[4]
                })
    except Exception:
        gpu_info["available"] = False
        gpu_info["message"] = "无法获取GPU信息或没有NVIDIA GPU"
    
    return {
        "cpu": cpu_info,
        "memory": memory_info,
        "gpu": gpu_info
    }

@mcp.tool(name="export_chat_history", description="将聊天记录导出到文件")
def export_chat_history(chat_content: str, filename: str = "chat_history.txt") -> str:
    """
    将聊天记录导出到文件
    
    Args:
        chat_content: 聊天内容
        filename: 导出的文件名，默认为chat_history.txt
    
    Returns:
        导出结果信息
    """
    # 创建output目录（如果不存在）
    output_dir = Path("./output")
    output_dir.mkdir(exist_ok=True)
    
    # 构建完整的文件路径
    file_path = output_dir / filename
    
    # 写入聊天内容
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(chat_content)
        return f"聊天记录已成功导出到 {file_path}"
    except Exception as e:
        return f"导出聊天记录失败: {str(e)}"

@mcp.tool(name="process_monitor", description="获取当前运行的进程信息")
def process_monitor(top_n: int = 10) -> list:
    """
    获取当前运行的进程信息
    
    Args:
        top_n: 返回的进程数量，默认为前10个占用CPU最多的进程
    
    Returns:
        进程信息列表
    """
    processes = []
    for proc in sorted(psutil.process_iter(['pid', 'name', 'username', 'memory_percent', 'cpu_percent']), 
                      key=lambda p: p.info['cpu_percent'], 
                      reverse=True)[:top_n]:
        try:
            proc.cpu_percent()  # 首次调用总是返回0，需要先调用一次
        except:
            continue
            
    # 等待一小段时间以获取准确的CPU使用率
    import time
    time.sleep(0.5)
    
    for proc in sorted(psutil.process_iter(['pid', 'name', 'username', 'memory_percent']), 
                      key=lambda p: p.cpu_percent(), 
                      reverse=True)[:top_n]:
        try:
            process_info = {
                "pid": proc.pid,
                "name": proc.info['name'],
                "username": proc.info['username'],
                "memory_percent": f"{proc.info['memory_percent']:.2f}%",
                "cpu_percent": f"{proc.cpu_percent():.2f}%",
                "status": proc.status()
            }
            processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return processes

@mcp.tool(name="disk_usage", description="获取磁盘使用情况")
def disk_usage() -> dict:
    """
    获取磁盘使用情况
    
    Returns:
        包含磁盘使用情况的字典
    """
    disk_info = {}
    for partition in psutil.disk_partitions():
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            disk_info[partition.device] = {
                "mountpoint": partition.mountpoint,
                "filesystem": partition.fstype,
                "total": f"{partition_usage.total / (1024**3):.2f} GB",
                "used": f"{partition_usage.used / (1024**3):.2f} GB",
                "free": f"{partition_usage.free / (1024**3):.2f} GB",
                "percent": f"{partition_usage.percent}%"
            }
        except Exception:
            # 某些磁盘可能无法访问
            continue
    
    return disk_info

@mcp.tool(name="network_stats", description="获取网络统计信息")
def network_stats() -> dict:
    """
    获取网络统计信息
    
    Returns:
        包含网络统计信息的字典
    """
    net_io = psutil.net_io_counters()
    net_stats = {
        "bytes_sent": f"{net_io.bytes_sent / (1024**2):.2f} MB",
        "bytes_recv": f"{net_io.bytes_recv / (1024**2):.2f} MB",
        "packets_sent": net_io.packets_sent,
        "packets_recv": net_io.packets_recv,
        "connections": len(psutil.net_connections())
    }
    
    # 获取网络接口信息
    interfaces = {}
    for interface_name, interface_addresses in psutil.net_if_addrs().items():
        interfaces[interface_name] = [addr.address for addr in interface_addresses if addr.family == socket.AF_INET]
    
    net_stats["interfaces"] = interfaces
    return net_stats

@mcp.tool(name="system_uptime", description="获取系统运行时间")
def system_uptime() -> str:
    """
    获取系统运行时间
    
    Returns:
        系统运行时间的字符串表示
    """
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot_time
    
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return f"系统已运行: {days}天 {hours}小时 {minutes}分钟 {seconds}秒 (启动于 {boot_time.strftime('%Y-%m-%d %H:%M:%S')})"

if __name__ == "__main__":
    print("启动万能工具服务...")
    main()