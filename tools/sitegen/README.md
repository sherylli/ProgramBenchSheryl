# tools/sitegen

ProgramBench 站点生成器（初级版）。

## 用法

```bash
python3 tools/sitegen/generate.py
# 可选参数
python3 tools/sitegen/generate.py --tasks-dir src/programbench/data/tasks --out dist/index.html
```

## 当前能力

- 扫描 `src/programbench/data/tasks/` 下每个 task 的 `task.yaml`
- 提取 `repository` / `commit` / `language` / `difficulty`
- 生成一个平铺的 `index.html` 总览表

## 尚未实现

- 领域分类
- 单个 task 的详情页
- 领域分布与分领域明细页
- 搜索 / 筛选 / 排序
- 增删 task 后的增量更新与断链清理
