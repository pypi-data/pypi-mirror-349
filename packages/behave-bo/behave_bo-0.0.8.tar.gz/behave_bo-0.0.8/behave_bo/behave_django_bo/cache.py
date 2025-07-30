import re
import time

from django.core.cache.backends.locmem import (
    LocMemCache,
)

from behave_bo.loggers import (
    tests_logger,
)


class BehaveLocMemCache(LocMemCache):
    """Cache для использования в тестах. Дополнен методом keys,
    аналогичным методу keys в RedisCache"""

    def keys(self, pattern):
        """
        Метод для получения списка ключей по шаблону из кеша приложения.
        Возвращает ключи без служебного префикса, который добавляется по-умолчанию в методах LocMemCache.

        Args:
            pattern: Регулярное выражение для поиска ключей в кэше
        """
        pattern = pattern.replace('*', '.*')
        res = list()

        with self._lock:
            cache_keys = self._cache.copy()

        for key in cache_keys:
            # получим изначальный ключ удалив из него префикс key_prefix:version:
            pure_key = key.replace(f'{self.key_prefix}:{self.version}:', '', 1)

            if re.match(pattern, pure_key) and not self._has_expired(key):
                res.append(pure_key)

        return res

    def ttl(self, key, version=None):
        """Получение значение ttl для ключа.

        Эмулирует метод django_redis.client.default.DefaultClient.ttl.

        Args:
            key: Значение ключа в кэше;
            version: Версия ключа в кэше.

        Returns:
            ttl ключа или None, если ключ не существует.
        """
        time_to_live = 0

        if self.has_key(key, version=version):
            key = self.make_key(key, version=version)

            if expire_time := self._expire_info.get(key, None):
                time_to_live = int(expire_time - time.time())
            else:
                time_to_live = None

        return time_to_live

    def _cull(self):
        """Удаляет ключи при превышении их количества, задаваемого в настройке MAX_ENTRIES.

        Здесь просто выведем в лог сообщение для отслеживания вызова метода.
        """
        tests_logger.warn(
            f'Превышен лимит количества хранимых ключей, равный {self._max_entries}. '
            f'{len(self._cache) // self._cull_frequency} ключей будет удалено.'
        )
        super()._cull()
