# Chunk Metadata Adapter

Библиотека для создания, управления и преобразования метаданных для чанков контента в различных системах, включая RAG-пайплайны, обработку документов и наборы данных для машинного обучения.

## Возможности

- Создание структурированных метаданных для чанков контента
- Поддержка разных форматов метаданных (плоский и структурированный)
- Отслеживание происхождения и жизненного цикла данных
- Сохранение информации о качестве и использовании чанков
- Поддержка расширенных метрик качества: coverage, cohesion, boundary_prev, boundary_next

## Жизненный цикл данных

Библиотека поддерживает следующие этапы жизненного цикла данных:

1. **RAW (Сырые данные)** - данные в исходном виде, сразу после загрузки в систему
2. **CLEANED (Очищенные)** - данные прошли предварительную очистку от шума, ошибок и опечаток
3. **VERIFIED (Проверенные)** - данные проверены на соответствие правилам и стандартам
4. **VALIDATED (Валидированные)** - данные прошли валидацию с учетом контекста и перекрестных ссылок
5. **RELIABLE (Надежные)** - данные признаны надежными и готовы к использованию в критических системах

![Жизненный цикл данных](https://example.com/data_lifecycle.png)

### Преимущества учета жизненного цикла

- **Прозрачность происхождения** - отслеживание всех этапов обработки данных
- **Контроль качества** - возможность отфильтровать данные, не достигшие требуемых этапов обработки
- **Аудит процессов** - возможность анализировать и улучшать процессы очистки и валидации
- **Управление надежностью** - возможность использовать только проверенные данные для критических задач

## Установка

```bash
pip install chunk-metadata-adapter
```

## Использование

### Создание метаданных для чанка в процессе жизненного цикла

```python
from chunk_metadata_adapter import ChunkMetadataBuilder, ChunkType, ChunkStatus
import uuid

# Создаем builder для проекта
builder = ChunkMetadataBuilder(project="MyProject")
source_id = str(uuid.uuid4())

# Шаг 1: Создание чанка с сырыми данными (RAW)
raw_chunk = builder.build_semantic_chunk(
    text="Данные пользователя: Иван Иванов, ivan@eample.com, Москва",
    language="text",
    type=ChunkType.DOC_BLOCK,
    source_id=source_id,
    status=ChunkStatus.RAW  # Указываем статус RAW
)

# Шаг 2: Очистка данных (исправление ошибок, опечаток)
cleaned_chunk = builder.build_semantic_chunk(
    text="Данные пользователя: Иван Иванов, ivan@example.com, Москва",  # Исправлена опечатка в email
    language="text",
    type=ChunkType.DOC_BLOCK,
    source_id=source_id,
    status=ChunkStatus.CLEANED  # Данные очищены
)

# Шаг 3: Верификация данных (проверка по правилам)
verified_chunk = builder.build_semantic_chunk(
    text="Данные пользователя: Иван Иванов, ivan@example.com, Москва",
    language="text",
    type=ChunkType.DOC_BLOCK,
    source_id=source_id,
    status=ChunkStatus.VERIFIED,  # Данные проверены
    tags=["verified_email"]  # Метки верификации
)

# Шаг 4: Валидация данных (проверка относительно других данных)
validated_chunk = builder.build_semantic_chunk(
    text="Данные пользователя: Иван Иванов, ivan@example.com, Москва",
    language="text",
    type=ChunkType.DOC_BLOCK,
    source_id=source_id,
    status=ChunkStatus.VALIDATED,  # Данные валидированы
    links=[f"reference:{str(uuid.uuid4())}"]  # Связь с проверочным источником
)

# Шаг 5: Надежные данные (готовы к использованию)
reliable_chunk = builder.build_semantic_chunk(
    text="Данные пользователя: Иван Иванов, ivan@example.com, Москва",
    language="text",
    type=ChunkType.DOC_BLOCK,
    source_id=source_id,
    status=ChunkStatus.RELIABLE,  # Данные признаны надежными
    coverage=0.95,
    cohesion=0.8,
    boundary_prev=0.7,
    boundary_next=0.9
)
```

### Фильтрация чанков по статусу жизненного цикла

```python
# Пример функции для фильтрации чанков по статусу
def filter_chunks_by_status(chunks, min_status):
    """
    Фильтрует чанки, оставляя только те, которые достигли определенного статуса
    или выше в жизненном цикле данных.
    
    Порядок статусов: 
    RAW < CLEANED < VERIFIED < VALIDATED < RELIABLE
    
    Args:
        chunks: список чанков для фильтрации
        min_status: минимальный требуемый статус (ChunkStatus)
        
    Returns:
        отфильтрованный список чанков
    """
    status_order = {
        ChunkStatus.RAW.value: 1,
        ChunkStatus.CLEANED.value: 2,
        ChunkStatus.VERIFIED.value: 3,
        ChunkStatus.VALIDATED.value: 4, 
        ChunkStatus.RELIABLE.value: 5
    }
    
    min_level = status_order.get(min_status.value, 0)
    
    return [
        chunk for chunk in chunks 
        if status_order.get(chunk.status.value, 0) >= min_level
    ]

# Пример использования
reliable_only = filter_chunks_by_status(all_chunks, ChunkStatus.RELIABLE)
```

## Документация

Более подробную документацию можно найти в [директории docs](./docs).

## Лицензия

MIT 