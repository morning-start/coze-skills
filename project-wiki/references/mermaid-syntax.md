# Mermaid 图表语法指南

## 1. 流程图 (Flowchart)

### 基础语法

```mermaid
graph LR
    A[开始] --> B{判断}
    B -->|是| C[处理1]
    B -->|否| D[处理2]
    C --> E[结束]
    D --> E
```

### 方向控制

- `LR`: Left to Right (从左到右)
- `TD`: Top to Down (从上到下)
- `RL`: Right to Left (从右到左)
- `BT`: Bottom to Top (从下到上)

### 节点样式

```mermaid
graph LR
    A[圆角矩形]
    B[方形]
    C[(圆形)]
    D[(圆柱形)]
    E{菱形}
    F[/平行四边形/]
```

### 样式设置

```mermaid
graph LR
    A[开始] --> B[处理]
    B --> C[结束]
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333
    style C fill:#bfb,stroke:#333
```

## 2. 类图 (Class Diagram)

### 基础语法

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +eat()
        +sleep()
    }
    class Dog {
        +String breed
        +bark()
    }
    Animal <|-- Dog
```

### 关系类型

- `-->`: 关联 (Association)
- `--|>`: 继承 (Inheritance)
- `..|>`: 实现 (Implementation)
- `-->o`: 聚合 (Aggregation)
- `-->*`: 组合 (Composition)
- `--`: 依赖 (Dependency)

### 复杂示例

```mermaid
classDiagram
    class User {
        +String id
        +String name
        +String email
        +login()
        +logout()
    }
    class Order {
        +String orderId
        +Date created
        +float amount
        +create()
        +cancel()
    }
    class Product {
        +String productId
        +String name
        +float price
    }
    
    User "1" --> "*" Order : 下单
    Order "1" --> "*" Product : 包含
```

## 3. 序列图 (Sequence Diagram)

### 基础语法

```mermaid
sequenceDiagram
    participant Alice
    participant Bob
    Alice->>Bob: 你好
    Bob-->>Alice: 你好！
```

### 循环与条件

```mermaid
sequenceDiagram
    participant Client
    participant Server
    participant Database
    
    Client->>Server: 请求数据
    loop 轮询检查
        Server->>Database: 查询状态
        Database-->>Server: 返回状态
        alt 数据就绪
            Database-->>Server: 返回数据
            Server-->>Client: 返回结果
        else 数据未就绪
            Server->>Server: 等待100ms
        end
    end
```

## 4. 状态图 (State Diagram)

### 基础语法

```mermaid
stateDiagram-v2
    [*] --> 待处理
    待处理 --> 处理中: 开始处理
    处理中 --> 已完成: 处理完成
    处理中 --> 失败: 处理失败
    失败 --> 待处理: 重试
    已完成 --> [*]
```

## 5. 实体关系图 (ER Diagram)

### 基础语法

```mermaid
erDiagram
    USER ||--o{ ORDER : 下单
    USER {
        string id PK
        string name
        string email
    }
    ORDER {
        string id PK
        date created
        float amount
    }
```

### 关系符号

- `||--||`: 一对一
- `||--o{`: 一对多
- `}o--||`: 多对一
- `}o--o{`: 多对多

## 6. 甘特图 (Gantt Chart)

### 基础语法

```mermaid
gantt
    title 项目开发计划
    dateFormat  YYYY-MM-DD
    section 需求阶段
    需求分析       :a1, 2024-01-01, 10d
    原型设计       :after a1, 5d
    section 开发阶段
    后端开发       :2024-01-16, 20d
    前端开发       :2024-01-21, 15d
    section 测试阶段
    集成测试       :2024-02-10, 7d
    上线发布       :2024-02-17, 3d
```

## 7. 饼图 (Pie Chart)

### 基础语法

```mermaid
pie title 技术栈分布
    "JavaScript" : 40
    "Python" : 30
    "Java" : 20
    "Go" : 10
```

## 8. 依赖关系图 (Graph)

### 模块依赖图

```mermaid
graph TD
    A[前端应用] --> B[API网关]
    B --> C[用户服务]
    B --> D[订单服务]
    B --> E[支付服务]
    C --> F[(MySQL)]
    D --> F
    E --> G[(Redis)]
    
    style A fill:#e1f5ff
    style B fill:#fff3e0
    style C fill:#e8f5e9
    style D fill:#e8f5e9
    style E fill:#e8f5e9
    style F fill:#fce4ec
    style G fill:#f3e5f5
```

### 类层级图

```mermaid
graph LR
    A[BaseClass] --> B[DerivedClass1]
    A --> C[DerivedClass2]
    B --> D[SubClass1]
    B --> E[SubClass2]
    
    style A fill:#f9f,stroke:#333
    style B fill:#bbf,stroke:#333
    style C fill:#bbf,stroke:#333
    style D fill:#bfb,stroke:#333
    style E fill:#bfb,stroke:#333
```

## 9. 最佳实践

### 9.1 命名规范

- 使用清晰、有意义的名称
- 避免特殊字符
- 保持命名一致性

### 9.2 布局优化

- 选择合适的方向（LR/TD）
- 合理分组（使用 subgraph）
- 控制节点数量（避免过于复杂）

### 9.3 样式建议

- 使用不同的颜色区分模块
- 保持视觉层次清晰
- 添加必要的标签和说明

### 9.4 可维护性

- 将复杂图表拆分成多个小图
- 添加图例和注释
- 定期更新保持与代码同步

## 10. 在 Markdown 中使用

### 直接嵌入

```markdown
\`\`\`mermaid
graph LR
    A --> B
\`\`\`
```

### 使用代码块

```markdown
# 架构图

\`\`\`mermaid
graph TD
    subgraph "应用层"
        A[服务A]
        B[服务B]
    end
    subgraph "数据层"
        C[(数据库)]
    end
    A --> C
    B --> C
\`\`\`
```

---

**注意**: Mermaid 图表在 GitHub、GitLab、Typora 等平台可直接渲染，其他平台可能需要插件支持
