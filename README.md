# 视觉小说剧情调试工具

专注于剧情创作阶段的调试与分析工具，帮助编剧和开发者快速验证剧情结构的合理性。

## 核心功能（按重要性排序）

### 1. 调试分析系统
- **数值平衡分析**
  - 自动检测属性和好感度的合理范围
  - 识别潜在的数值瓶颈
  - 提供具体的平衡性改进建议
- **剧情一致性验证**
  - 检查场景引用完整性
  - 验证角色关联正确性
  - 分析选项可用性分布

### 2. 条件系统
- **复合条件支持**
  - AND/OR逻辑组合
  - 支持属性条件和关系条件
  - 灵活的比较运算符
- **多维度条件检查**
  - 时间条件（时段/星期）
  - 标记条件
  - 属性阈值

### 3. 分支管理
- **分支结构分析**
  - 自动探索所有可能路径
  - 检测死路和循环
  - 计算分支覆盖率
- **分支状态追踪**
  - 记录分支点信息
  - 管理分支状态
  - 支持分支合并

### 4. 事件系统
- **事件调度**
  - 延迟事件处理
  - 条件触发
  - 全局事件监听
- **场景转换**
  - 多种转换类型
  - 条件式跳转
  - 转换效果管理

### 5. 时间系统
- 时间段划分（早中晚夜）
- 日期和星期管理
- 事件时间安排

### 6. 标记系统
- 永久/临时标记
- 标记过期机制
- 条件标记

## 实现重点

1. **调试友好**
   - 详细的分析报告
   - 具体的改进建议
   - 可视化分析结果

2. **创作辅助**
   - 快速验证剧情结构
   - 及时发现潜在问题
   - 平衡性指导

3. **灵活扩展**
   - 模块化设计
   - 清晰的接口定义
   - 便于功能扩展

## 使用场景

- 剧情编写初期的快速验证
- 数值平衡的反复调整
- 分支结构的完整性检查
- 游戏流程的可达性分析

## 开发计划

1. [ ] 增强分析工具的可视化功能
2. [ ] 添加更多平衡性指标
3. [ ] 支持更复杂的条件组合
4. [ ] 改进建议系统的智能性