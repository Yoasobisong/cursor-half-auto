#!/bin/bash

# 设置错误处理
set -eo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日志函数
log() {
  local level=$1; shift
  local color
  case "$level" in
    "INFO") color="$GREEN" ;;
    "WARN") color="$YELLOW" ;;
    "ERROR") color="$RED" ;;
    "DEBUG") color="$BLUE" ;;
    *) color="$NC" ;;
  esac
  echo -e "${color}[$level]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $*"
}

# 检查访问权限
check_permissions() {
  if [ "$(id -u)" -ne 0 ]; then
    log "ERROR" "所需许可证 root. 用 sudo 运行:"
    echo "  sudo $0"
    exit 1
  fi
}

# 查找 Cursor 安装文件夹
find_cursor_dir() {
  local possible_dirs=(
    "/opt/Cursor"
    "/opt/cursor-bin"
    "/usr/lib/cursor"
    "$HOME/.cursor"
  )

  for dir in "${possible_dirs[@]}"; do
    if [ -d "$dir" ]; then
      echo "$dir"
      return 0
    fi
  done

  log "ERROR" "无法找到文件夹 Cursor"
  exit 1
}

# 获取准确的流程清单
get_cursor_pids() {
  local cursor_dir=$(find_cursor_dir)
  ps aux | grep -iE "$cursor_dir/[cC]ursor" | grep -v -E 'grep|--type=renderer' | awk '{print $2}'
}

# 安全终止进程
terminate_cursor() {
  log "INFO" "光标进程搜索..."
  local pids=$(get_cursor_pids)

  if [ -z "$pids" ]; then
    log "INFO" "未发现任何 Cursor 进程"
    return 0
  fi

  log "WARN" "发现的过程 Cursor (PID): $pids"
  echo "过程详情:"
  ps -fp $pids

  read -r -p "您确定要终止这些进程吗？ [y/N] " response </dev/tty
  if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    log "INFO" "完成流程..."
    kill -TERM $pids 2>/dev/null || true

    for i in {1..10}; do
      sleep 0.5
      local remaining=$(get_cursor_pids)
      [ -z "$remaining" ] && break
    done

    local remaining=$(get_cursor_pids)
    if [ -n "$remaining" ]; then
      log "WARN" "强制完成..."
      kill -KILL $remaining 2>/dev/null || true
    fi

    log "INFO" "成功完成的流程"
  else
    log "ERROR" "用户取消"
    exit 1
  fi
}

# 备份
backup_files() {
  local user_home=$1
  local cursor_dir_name=$(basename $(find_cursor_dir))
  local config_dir="$user_home/.config/$cursor_dir_name/User/globalStorage"
  local storage_file="$config_dir/storage.json"
  local backup_dir="$config_dir/backups"

  mkdir -p "$backup_dir"
  local timestamp=$(date +%Y%m%d_%H%M%S)

  # 确保目录权限正确
  chown -R $(logname):$(logname) "$config_dir"
  chmod -R 755 "$config_dir"

  if [ -f "$storage_file" ]; then
    cp "$storage_file" "$backup_dir/storage.json.bak_$timestamp"
    chmod 644 "$backup_dir/storage.json.bak_$timestamp"
    log "INFO" "配置已备份： $backup_dir/storage.json.bak_$timestamp"
  fi

  local machine_id="/etc/machine-id"
  if [ -f "$machine_id" ]; then
    cp "$machine_id" "$backup_dir/machine-id.bak_$timestamp"
    chmod 644 "$backup_dir/machine-id.bak_$timestamp"
    log "INFO" "创建了备份机器 ID"
  fi
}

# 生成新的 ID
generate_ids() {
  local user_home=$1
  local cursor_dir_name=$(basename $(find_cursor_dir))
  local config_dir="$user_home/.config/$cursor_dir_name/User/globalStorage"
  local config_file="$config_dir/storage.json"

  local new_machine_id=$(uuidgen | tr -d '-')
  local new_device_id=$(uuidgen)
  local new_sqm_id="$(uuidgen | tr '[:lower:]' '[:upper:]')"

  log "DEBUG" "生成新的 ID:"
  log "DEBUG" "Machine ID: $new_machine_id"
  log "DEBUG" "Device ID: $new_device_id"
  log "DEBUG" "SQM ID: $new_sqm_id"

  # 确保目录存在并具有正确的权限
  if [ ! -d "$config_dir" ]; then
    mkdir -p "$config_dir"
  fi
  
  # 移除任何现有的不可修改属性
  if [ -f "$config_file" ]; then
    chattr -i "$config_file" 2>/dev/null || true
  fi

  # 设置正确的所有权和权限
  chown -R $(logname):$(logname) "$config_dir"
  chmod -R 755 "$config_dir"

  if [ ! -f "$config_file" ]; then
    echo '{}' > "$config_file"
  fi

  echo "$new_machine_id" | tr -d '-' | cut -c1-32 > "/etc/machine-id"

  tmp_file=$(mktemp)
  jq --arg machine "$new_machine_id" \
     --arg device "$new_device_id" \
     --arg sqm "{$new_sqm_id}" \
     '.telemetry.machineId = $machine |
      .telemetry.devDeviceId = $device |
      .telemetry.sqmId = $sqm' "$config_file" > "$tmp_file"

  mv "$tmp_file" "$config_file"
  chmod 644 "$config_file"
  chown $(logname):$(logname) "$config_file"
  
  # 确保文件可写
  chattr -i "$config_file" 2>/dev/null || true
}

# 主要功能
main() {
  check_permissions
  clear

  echo -e "${BLUE}================================${NC}"
  echo -e "${GREEN}   Cursor 设备ID 修改工具 (Linux版)  ${NC}"
  echo -e "${BLUE}================================${NC}"
  echo -e "${YELLOW}   Cursor 安装路径以下之一:${NC}"
  echo -e "${YELLOW}       /opt/Cursor"
  echo -e "${YELLOW}       /opt/cursor-bin"
  echo

  local current_user=$(logname 2>/dev/null || echo "$SUDO_USER")
  local user_home=$(getent passwd "$current_user" | cut -d: -f6)

  terminate_cursor
  backup_files "$user_home"
  generate_ids "$user_home"

  log "INFO" "操作完成! 请重新启动Cursor"
}

main "$@"
