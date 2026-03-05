# 游戏项目文档指南（Godot）

## 概述

本指南适用于 Godot 游戏开发项目，提供游戏开发的文档建议。

### 最小文档集（必备）

1. **README.md** - 项目说明
2. **GDD 摘要** - 游戏设计
3. **场景/脚本结构** - 技术架构
4. **导出配置** - 发布说明

---

## 完整文档集

### 1. 游戏设计文档（GDD）摘要

**核心内容**：

```markdown
## 游戏概述

### 核心玩法
- 游戏类型：平台跳跃/解谜/RPG
- 游戏目标：到达终点/击败 BOSS
- 核心机制：跳跃/攻击/解谜

### 角色设计
- 主角：能力、属性
- 敌人：类型、行为模式
- NPC：功能、对话

### 关卡设计
- 关卡列表
- 难度曲线
- 机关设计

### 经济系统
- 货币类型
- 商店系统
- 道具系统
```

### 2. 场景与节点结构

**核心内容**：

```markdown
## 场景树

### 主场景
```
Main (Node2D)
├── Player
├── Enemies
├── Level
└── UI
```

### Player 场景
```
Player (CharacterBody2D)
├── Sprite2D
├── CollisionShape2D
├── Camera2D
└── AnimationPlayer
```
```

### 3. 信号与通信机制

**核心内容**：

```markdown
## 信号系统

### 自定义信号
```gdscript
# 玩家信号
signal player_died
signal player_scored(points)

# 游戏信号
signal game_over
signal level_completed
```

### 信号命名规范
- 动词过去式：`player_died`, `enemy_defeated`
- 名词 + 动词：`score_changed`, `level_loaded`
```

### 4. 资源管理策略

**核心内容**：

```markdown
## 资源管理

### 加载方式
- 预加载：`@onready var texture = preload("res://...")`
- 动态加载：`load("res://...")`

### 内存释放
- 使用 `queue_free()` 释放节点
- 及时断开信号连接
- 使用资源池管理频繁创建的对象
```

### 5. 导出与发布配置

**核心内容**：

```markdown
## 导出配置

### Windows
- 导出预设：Windows Desktop
- 格式：EXE
- 图标配置

### Android
- 导出预设：Android
- 格式：APK/AAB
- 签名配置
- 最低 SDK 版本

### Web
- 导出预设：Web
- 格式：HTML5
- PCK 加密
```

### 6. 脚本架构

**核心内容**：

```markdown
## 脚本组织

### 类结构
- 玩家脚本：Player.gd
- 敌人脚本：Enemy.gd, Slime.gd, Boss.gd
- 管理器：GameManager.gd, AudioManager.gd

### Autoload 单例
- GameManager: 全局游戏状态
- AudioManager: 音频管理
- SceneManager: 场景管理

### C# 插件交互（如使用）
- C# 脚本位置
- GDScript 与 C# 通信
```

---

## 推荐工具

| 工具 | 用途 |
|------|------|
| **Godot Editor** | 游戏开发 |
| **Aseprite** | 像素画制作 |
| **BFXR** | 音效生成 |
| **Tiled** | 地图编辑 |

---

## 检查清单

- [ ] GDD 摘要完整（核心玩法、角色、关卡）
- [ ] 场景树结构清晰
- [ ] 信号通信机制说明
- [ ] 资源管理策略合理
- [ ] 导出配置完整
- [ ] 脚本架构清晰

---

## 参考资料

- [Godot 官方文档](https://godotengine.org/)
- [游戏设计文档指南](https://gamedev.net/)
- [项目类型总览](README.md)
