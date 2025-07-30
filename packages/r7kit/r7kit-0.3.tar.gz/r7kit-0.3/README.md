
**r7kit** — лёгкая обёртка над Temporal + Redis для организации workflow-задач с хранением состояния (payload) в Redis и автоматической сериализацией.

---


1. [Установка](#установка)  
2. [Конфигурация](#конфигурация)  
3. [Базовые понятия](#базовые-понятия)  
4. [Определение Workflow](#определение-workflow)  
5. [Запуск worker-процесса](#запуск-worker-процесса)  
6. [Запуск workflow из клиента](#запуск-workflow-из-клиента)  
7. [CRUD операций над задачей](#crud-операций-над-задачей)  
8. [Вложенный payload и child-workflow](#вложенный-payload-и-child-workflow)  
9. [Логирование и сериализация](#логирование-и-сериализация)  
10. [TTL-удаление задач](#ttl-удаление-задач)  

---


```bash
pip install r7kit
```

> Библиотека не поднимает ни Temporal-сервис, ни Redis — предполагается, что они уже есть.

---


Можно настроить r7kit через переменные окружения или программно до первого импорта:

```python
from r7kit.config import configure

configure(
    redis_url="redis://localhost:6379",
    temporal_address="localhost:7233",
    stream_default="task_events",
    deleted_ttl=60,  # TTL после delete (в секундах)
)
```

Переменные окружения:

- `REDIS_URL`
- `TEMPORAL_ADDRESS`
- `R7KIT_STREAM`
- `R7KIT_DELETED_TTL`

---


Каждому workflow соответствует **Redis-задача**, которая хранится в `HSET task:{uuid}` и имеет:

- статус (status)
- временные метки (created_at, updated_at)
- payload (вложенный словарь)
- поток событий (Redis Stream)

Библиотека сериализует payload в orjson + префикс, автоматически декодируя при чтении.

---


```python
from r7kit.decorators import taskflow
from r7kit.base_task_workflow import BaseTaskWorkflow

@taskflow(queue="producer-queue")
class MyFlow(BaseTaskWorkflow):
    async def handle(self) -> int:
        await self.load_task()
        x = self.payload["input"]
        await self.patch_task({"status": "processing"})
        await self.patch_task({"status": "done", "payload": {"result": x * 2}})
        await self.delete_task(ttl=60)
        return x * 2
```

> Наследуй `BaseTaskWorkflow`, используй `load_task`, `patch_task`, `delete_task` и `self.payload`.

---


```python
from r7kit.worker import R7Worker

if __name__ == "__main__":
    R7Worker("myapp", queue="producer-queue").start()
```

> Указывается имя пакета, где лежат ваши воркфлоу, и очередь.

---


```python
from myapp.flows import MyFlow

handle, uuid = await MyFlow.start(payload={"input": 42})
await handle.result()
```

Или:

```python
from r7kit.workflow_utils import submit_workflow

await submit_workflow(MyFlow, payload={"input": 42})
```

---


После `await self.load_task()` доступны:

- `self.task`: объект `TaskModel`
- `self.payload`: словарь

Поддерживаются:

```python
await self.patch_task({"status": "in_progress"})
await self.delete_task(ttl=60)
await self.get_task()
await self.exists()  # логическое удаление
```

Асинхронный контекст для сохранения payload:

```python
async with self.state():
    self.payload["x"] = 1
```

---


Можно запускать дочерние воркфлоу:

```python
result = await self.child("OtherFlow", queue="q").run()
```

Или:

```python
handle, child_task_id = await self.child("OtherFlow", queue="q").start(payload={...})
```

---


Для логирования:

```python
from r7kit.logging import setup
setup("DEBUG")
```

Для ручной сериализации (например, вне воркфлоу):

```python
from r7kit.serializer import dumps, loads
```

---


Удаление:

```python
await self.delete_task(ttl=10)
```

Это:

- Ставит `deleted_at = now`
- Устанавливает `PEXPIRE` на Redis-ключ задачи
- Логируется в Redis Stream

TTL можно задать через `R7KIT_DELETED_TTL` или явно в методе.

---


```python
@taskflow(queue="producer-queue")
class ProducerWorkflow(BaseTaskWorkflow):
    async def handle(self) -> int:
        await self.load_task()
        x = int(self.payload["mathematic"]["input"])
        await self.patch_task({"status": "sent"})
        res = await self.child("ProcessorWorkflow", queue="processor-queue").run()
        await self.patch_task({"status": "done", "payload": {"mathematic": {"input": x, "result": res}}})
        await self.delete_task(ttl=10)
        return res
```

---


- [temporalio](https://github.com/temporalio/sdk-python)
- redis.asyncio
- orjson
- pydantic

---


MIT
