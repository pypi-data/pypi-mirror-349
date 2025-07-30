
# 📦 TikTokRocket-core

**TikTokRocket-core** — вспомогательный Python-модуль для автоматизации взаимодействия с TikTok, включающая в себя модули для работы с браузером, обхода антибот-защиты, API-клиент TikTokRocket, систему управления аккаунтами, и интеграцию с SMS-активациями. Разрабатывается как часть внутренней инфраструктуры автоматизации и предоставляет универсальный доступ к основному функционалу автоматизации TikTok.
## 🏷 Badges

[![Status: Private](https://img.shields.io/badge/status-private-critical.svg)](https://eugconrad.com)
[![License: Custom](https://img.shields.io/badge/license-restricted-red.svg)](https://eugconrad.com/license)
[![Platform: TikTok](https://img.shields.io/badge/platform-tiktok-black.svg?logo=tiktok)](https://tiktok.eugconrad.com)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Maintainer](https://img.shields.io/badge/maintainer-@eugconrad-blueviolet.svg)](https://t.me/eugconrad)
## 🚀 Основной функционал

- **Интегрированный API-клиент** для взаимодействия с платформой [TikTokRocket](https://tiktok.eugconrad.com): управление аккаунтами, автоматизированный доступ к ботам и авторизация
- **Автоматическая установка и обновление Chrome и ChromeDriver** до требуемой ревизии, обеспечивая стабильную совместимость с Selenium
- **Антидетект-браузер на базе Selenium** с встроенными механизмами обхода защит TikTok и эмуляцией поведения реального пользователя
- **Поддержка SMS-активаций** через подключаемые адаптеры (например, Grizzly), включая получение временных номеров и кода подтверждения
- **Графический интерфейс на PySimpleGUI** для авторизации и получения API-токена
- **Централизованное хранилище установленных компонентов** (браузер, драйвер, токены) с доступом из любых приложений, использующих библиотеку
- **Лёгкая интеграция в сторонние решения**, включая CLI-утилиты, десктопные приложения и серверные скрипты
## ⚠️ Лицензия и ограничения

Данный проект распространяется **на условиях ограниченного некоммерческого использования**.

- Разрешается использовать библиотеку **только в личных или учебных целях**.
- **Коммерческое использование запрещено**, включая:
    - перепродажу, аренду, передачу третьим лицам
    - использование в SaaS-продуктах или сервисах
    - модификацию с целью извлечения прибыли

Каждый файл содержит уведомление об авторстве и условиях использования.  
Нарушение условий лицензии повлечёт юридические последствия.

Для получения коммерческой лицензии — свяжитесь с автором:

- 📧 Email: [me@eugconrad.com](mailto:me@eugconrad.com)
- 💬 Telegram: [@eugconrad](https://t.me/eugconrad)
- 🌐 Website: [eugconrad.com](https://eugconrad.com)
## 🧰 Tech Stack

**Язык:** Python 3.11+

**GUI:** PySimpleGUI

**Автоматизация браузера:**
- Selenium
- undetected-chromedriver
- selenium-wire
- selenium-stealth
- fake-useragent

**Сеть и API:**
- aiohttp
- requests
- python-dotenv
- blinker

**Системные и утилитные зависимости:**
- platformdirs
- loguru
- setuptools

**Инструменты сборки:**
- poetry-core

> Линтер: `pylint` с кастомной настройкой (`line-too-long`, `broad-exception-*`, `signature-differ` отключены)
## 🛟 Support

Если возникли вопросы или нужна помощь:

- 📧 Email: [me@eugconrad.com](mailto:me@eugconrad.com)
- 💬 Telegram: [@eugconrad](https://t.me/eugconrad)

Официальный сайт проекта: [tiktok.eugconrad.com](https://tiktok.eugconrad.com)

> Коммерческая поддержка доступна по договорённости.
