# 羽毛球场地预约系统

基于 FastAPI + React 的羽毛球场地预约系统，包含场地时段管理、在线预约、费用结算和会员折扣。项目采用前后端分离和模块化目录结构，便于继续扩展数据库、登录权限和管理端能力。

## 功能

- 场地管理：查看场地、场地材质和每日时段。
- 时段管理：按日期查看时段，可停用或恢复时段。
- 在线预约：选择可预约时段、填写预约人、选择会员折扣后提交订单。
- 费用结算：根据会员等级自动计算折扣价，订单支持结算和取消。
- 会员折扣：内置普通、银卡、金卡、教练等折扣示例。

## 项目结构

```text
.
├── backend
│   ├── app
│   │   ├── data          # 内存数据与初始化种子
│   │   ├── models        # 领域模型
│   │   ├── routes        # API 路由
│   │   ├── services      # 业务逻辑
│   │   ├── main.py       # FastAPI 入口
│   │   └── schemas.py    # 请求模型
│   ├── Dockerfile
│   └── requirements.txt
├── frontend
│   ├── src
│   │   ├── api           # API 客户端
│   │   ├── components    # 可复用组件
│   │   ├── pages         # 页面组合
│   │   ├── utils         # 工具函数
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

## Docker 启动

```bash
docker compose up --build
```

启动后访问：

- 前端：http://localhost:5173
- 后端 API：http://localhost:8000/api/health
- API 文档：http://localhost:8000/docs

## 本地开发

后端：

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

前端：

```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

如需指定 API 地址：

```bash
VITE_API_BASE_URL=http://localhost:8000/api npm run dev
```

## 主要接口

- `GET /api/courts`：场地列表
- `GET /api/time-slots?date=YYYY-MM-DD`：时段列表
- `PATCH /api/time-slots/{slot_id}`：更新时段价格或状态
- `GET /api/members`：会员列表
- `POST /api/bookings`：提交预约
- `POST /api/bookings/{booking_id}/settle`：结算订单
- `POST /api/bookings/{booking_id}/cancel`：取消订单

## 说明

当前版本使用内存数据，适合演示和评测；重启后预约数据会恢复到初始状态。生产化可将 `backend/app/data/store.py` 替换为数据库仓储层，并继续复用现有路由和服务层。
