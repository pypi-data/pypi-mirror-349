
# ytb2audiobot

![Build Status](https://img.shields.io/github/actions/workflow/status/andrewalevin/ytb2audiobot/python-publish.yml)
![PyPI - Version](https://img.shields.io/pypi/v/ytb2audiobot)
![Docker Image Version](https://img.shields.io/docker/v/andrewlevin/ytb2audiobot)


🦜 YouTube to Audio by Andrew A Levin


# Installation

## 🐳 Docker

#### Minimal Docker compose file

```yaml
services:
  ytb2audiobot:
    image: andrewlevin/ytb2audiobot
    environment:
      - Y2A_TG_TOKEN=YOUR_TG_TOKEN
      - Y2A_HASH_SALT=YOUR_HASH_SALT
    restart: on-failure:3
```


#### Full Docker compose file with all options in default.

See detailed description about all options below.

```yaml
services:
  ytb2audiobot:
    image: andrewlevin/ytb2audiobot
    environment:
      - Y2A_TG_TOKEN=YOUR_TG_TOKEN
      - Y2A_HASH_SALT=YOUR_HASH_SALT
    restart: on-failure:3
```


## 🐍 Python run

Direct install


#### Reqirments install

TODO -> add full description

```bash
apt install ffmpeg

# and  

npm install -g vot-cli
```


You can nativly install and run as Python package 

Write all you enviroments in .env file

```bash
Y2A_TG_TOKEN='751*******TOEKEN********omPmnE'
Y2A_HASH_SALT='j298hf********YOU-HASH***********34f2'
Y2A_OWNER_BOT_ID_TO_SAY_HELLOW='4****YOU-OWNER-ID******3'
Y2A_SEGMENT_REBALANCE_TO_FIT_TIMECODES='true'
Y2A_SEGMENT_AUDIO_DURATION_SEC=2404
Y2A_DEBUG_MODE='true'
```

And after that run 

```bash
export $(grep -v '^#' .env | xargs)
ytb2audiobot
```


## Environment Options

**Y2A_TG_TOKEN**

- No Default


**Y2A_HASH_SALT**

- No Default


**Y2A_OWNER_BOT_ID_TO_SAY_HELLOW**

- No Default

Отправить сообщение при запуске вледельцу бота, что он включился и начал работу.


**Y2A_BUTTON_CHANNEL_WAITING_DOWNLOADING_TIMEOUT_SEC**

- Default: 8

Время ожидания нажатия кнопки скачивания аудио для работы бота в канале.




**Y2A_KILL_JOB_DOWNLOAD_TIMEOUT_SEC**

- Default: 2520 (seconds or 43 minutes)

Максимальная продолжительность попытки скачивания аудио.

После 

# todo Add to info text about timeout


**Y2A_SEGMENT_AUDIO_DURATION_SPLIT_THRESHOLD_SEC**

- Default: 6060 (seconds or 101 minutes)

После какой продолжительности аудио будет проихсоходить разделение на части.

101 секунда по-умолчанию выбрана так, что это чуть больше 1 часа и 40 минут, что должно соответсовать одной лекции,
а также умещатьсь в максимальные размеры посылаемого файла через Telegram bot в 50 mb.


**Y2A_SEGMENT_AUDIO_DURATION_SEC**

- Default: 2340 (seconds  or 39 minutes)

Разделение по частям размера сегмента.
Последняя часть присодиняется к предпоследней, если она меньше отношения Золотого сечения.

Значение по-умоляанию выбрано из оптимального, как половина времени стандартной лекции.

**Y2A_SEGMENT_DURATION_PADDING_SEC**

- Default: 6 (seconds)

При нарезки на сегменты итогового аудио файла количество секунд наложения соседних сегментов.
От места разделения добавляется к текущему n секунд в конце,
и также в начале следующего.

**Y2A_SEGMENT_REBALANCE_TO_FIT_TIMECODES** 

- Default: true

Перенарезка аудио итогового аудио файла так, чтобы в текст описание в Telegram 
входили все timecodes.

**Y2A_TRANSLATION_OVERLAY_ORIGIN_AUDIO_TRANSPARENCY**

- Default: 0.3 

Устанавливает громкость фоновой оригинальной дорожки.
- 0.1 - Тихо
- 0.9 - Оригинальная громкость непереведенного аудио


**Y2A_AUDIO_QUALITY_BITRATE**

- Default: 48k

- Available Values: 48k, 64k, 96k, 128k, 196k, 256k, 320k

- 48k - Меньше размер файла
- 

**Y2A_DEBUG_MODE** 

- Default: false

В этом режиме выводятся дорполнительные сообщения в log.
А также Y2A_KEEP_DATA_FILES в состоянии true.

**Y2A_KEEP_DATA_FILES**

- Default: false

Не удалять скаченные аудио файлы с сервера.

**Y2A_REMOVE_AGED_DATA_FILES_SEC**

- Default: 3600 (seconds)

Сколько времени хранить кэш скаченных аудио файлов на сервере.

**Y2A_AUTO_DOWNLOAD_CHAT_IDS_STORAGE_FILENAME**

- Default: autodownload-hashed-chat-ids.yaml

??


**Y2A_REPLY_TO_ORIGINAL**

- Default: true

В исходещем аудио делать или нет ссылку на оригинальное сообщение.


TODO -> Add Images





# 🚴‍♂️ Usage and Features

Only send me YouTube URL and I'll make all



## Commands
```
/help
/extra
/autodownload
```


## /autodownload - Command

By default it shows lit this

![](images/autodownload-just-download.jpg)

Works only in Channels.
Please add this bot to the list of admins and try again.

#todo

Let you to autodownload in your channels


![](images/autodownload-add.jpg)

![](images/autodownload-remove.jpg)


## 🔮 Advanced Options

You can call by any command

- \advanced, \adv, \ad, \extra, \ext, \ex, \options, \opt, \op 

![](images/menu-extra.jpg)

### 


## 📟 CLI options

### Subtitles in CLI

```bash
youtu.be/TUJmSgViGoM subtitles 

# OR

youtu.be/TUJmSgViGoM subs

# OR

youtu.be/TUJmSgViGoM sub
```


Search word directly

```bash
youtu.be/TUJmSgViGoM subs beatles

youtu.be/TUJmSgViGoM subs sting
```


### Set Bitrate in CLI

```bash
youtu.be/TUJmSgViGoM bitrate

# OR

youtu.be/TUJmSgViGoM bitr

# OR

youtu.be/TUJmSgViGoM bit
```

### Call Music in CLI


```bash
youtu.be/TUJmSgViGoM music

# OR

youtu.be/TUJmSgViGoM song
```



### 🌍 Translation

Get Translation

```bash
youtu.be/TUJmSgViGoM translation

# OR

youtu.be/TUJmSgViGoM translate

# OR

youtu.be/TUJmSgViGoM transl

# OR

youtu.be/TUJmSgViGoM trans

# OR

youtu.be/TUJmSgViGoM tran

# OR

youtu.be/TUJmSgViGoM tra

# OR

youtu.be/TUJmSgViGoM tr
```

### Set overlay background original audio volume

Default is 0.3

```bash

youtu.be/TUJmSgViGoM trans 0.6

# OR

youtu.be/TUJmSgViGoM trans 0.4

# OR

youtu.be/TUJmSgViGoM trans 0.1
```


**Set translation without background original audio**

```bash

youtu.be/TUJmSgViGoM trans 0.0

# OR

youtu.be/TUJmSgViGoM trans 0
```



### Force Re Download audio avoiding file keepd in cache.


```bash

youtu.be/TUJmSgViGoM force

# OR

youtu.be/TUJmSgViGoM forc

# OR

youtu.be/TUJmSgViGoM for

# OR

youtu.be/TUJmSgViGoM f
```



=====


=====


### Install as service unit in OS

```bash
curl -sL https://andrewalevin.github.io/ytb2audiobot/install-manual.sh | bash
```




### Install as Docker Compose

```bash
curl -sL https://andrewalevin.github.io/ytb2audiobot/install-docker-compose.sh | bash
```


# ytb2audiobot-view
ytb2audiobot-view

  - 🔐 Privace
  - 🚴‍♂️ Usage and Features
    - 🎏 Split
    - 🎶 Bitrate
    - 📝 Subtitles
    - 📣 Channel
  - 🚀 Install your own bot server


## 🔐 Защита персональных данных: Рекомендации по обеспечению конфиденциальности

Ваши персональные данные – это ценность, которая заслуживает надежной защиты. Если вы разделяете мои опасения по поводу сохранности личной информации и стремитесь обеспечить максимальную конфиденциальность, следуйте этим рекомендациям:

  - **Оцените свои риски:** Если у вас есть сомнения в безопасности ваших данных, лучше не пользоваться этим ботом.
  - **Установите бота на свой сервер:** Чтобы контролировать все процессы и быть уверенным в безопасности, установите бота самостоятельно на свой сервер.
  - **Открытый код:** Весь код бота публично доступен для просмотра. Можете изучить его, чтобы убедиться в отсутствии эксплойтов, скрытых сохранений данных и любых других возможных утечек ваших персональных данных.

Эти шаги помогут вам защитить свои персональные данные и обеспечить максимальную безопасность при использовании данного бота.


## 🚴‍♂️ Usage and Features

Send any youtube link to movie. Видео станет загружаться сразу автоматически.

В диалоговом окне покажется примерное время загрузки. 

После успешной обрботки и загрузки в телеграм диалоговое окно будет удалено

#### 🕰 Таймкоды для удобства прослушивания

Для вашего удобства и экономии времени к описанию ролика добавляются таймкоды, если они указаны в описании ролика на youtube.

В Телеграме при прослушивании вы можете легко перемещаться по файлу, нажимая на соответствующий таймкод. Это позволяет быстро находить нужные моменты и делать прослушивание еще более комфортным.

![photo-1-640](https://github.com/andrewalevin/ytb2audiobot-view/assets/155118488/989f29e7-03d9-46fe-a85d-764b4599d641)




### 🎏 Split param 

Вы всегда можете разделить аудиофайл для более удобного прослушивания.

Как это работает:

  - **По умолчанию:** Все аудиофайлы, длиннее 1 часа 39 минут (как университетская лекция), автоматически разбиваются на части по 39 минут.
  - **Плавный переход:** При разделении к предыдущей части добавляется 5 секунд из следующей, а к началу следующей части - 5 секунд из предыдущей. Это помогает понять, на каком месте вы остановились, и избежать потери информации при разделении.
  - **Магия золотого сечения:** Если последняя часть файла меньше пропорции золотого сечения, она присоединяется к предпоследней части.

**Аудиокниги:** Длинная аудиокнига будет разбита на части, что облегчает загрузку файлов меньшего размера, их передачу и работу с ними.

**Философские тексты:** Например, "Этика" Канта. Слушать такой текст даже по 39 минут сложно, поэтому гораздо удобнее разбивать его на небольшие фрагменты по 20 минут.

Наслаждайтесь удобным прослушиванием!


Параметр 

```
youtu.be/TUJmSgViGoM split 25
```

Алиасами команды для удобства использования и вспоминания добавлены

{split,spl,sp,разделить,раздел,разд,раз}


### 🎶 Настройка битрейта аудиофайлов

По умолчанию, загружаемые аудиофайлы конвертируются в минимальный размер с оптимальным качеством, что обеспечивает битрейт 48k.

Музыкальные файлы могут звучать лучше с более высоким качеством звука.

**Как задать битрейт:**

Вы можете самостоятельно задать выходной битрейт аудиофайла в диапазоне от 48k до 320k. 
Для этого добавьте к отправляемой ссылке через пробел ключевое слово {bit, bitrate} и значение битрейта в тысячных.

**Пример:**

```
youtu.be/TUJmSgViGoM bit 320
```

Алиасами команды для удобства использования и вспоминания добавлены

{bitrate,bitr,bit,битрейт,битр,бит}


<img width="400" alt="img-bitrate-800" src="https://github.com/andrewalevin/ytb2audiobot-view/assets/155118488/b6e98d12-c172-4254-9c12-be341a49c58a">


Для файла из примера получаются следюущие примеры 4 минутный клип:

  - 48k bitrate - 2.1 mb file size (по-умолчанию)
  - 96k bitrate - 3.5 mb file size 
  - 320k bitrate - 9.6 mb file size


### 📝 Subtitles param 

Для скачивания субтитров и поиска по ним воспользуйтесь командой или ее алиасами (для удобства незапомниания :)

{subtitles,subtitle,subt,subs,sub,su,саб,сабы,субтитры,субт,суб,сб}

**Без параметров:** Просто введите команду, и бот скачает субтитры для текущего видео. В субтитрах будут таймкоды и ссылки на соответствующие моменты видео на YouTube.

**С параметрами:** Если после команды ввести слово для поиска, бот выдаст фрагменты субтитров, в которых встречается это слово.


### 📣 Использование бота в канале

У меня есть несколько тематических личных каналов, куда я добавляю ролики для просмотра. Теперь бот может работать и в каналах, что делает его использование еще удобнее.

**Как это работает:**

  - Отправьте ссылку или текст, в котором присутсвтует YouTube ссылка на видео ролик.
    
  - После этого появится кнопка callback. Нажмите на неё, чтобы начать скачивание аудиофайла.

    Кнопка скачивания исчезнет через 8 секунд и ничего не будет происходить.
    
  - Вы также можете использовать команду для скачивания аудиофайла:

    {download, down, dow, d, bot, скачать, скач, ск}

Все другие команды также работают в канале, обеспечивая полный функционал бота.


## 🚀 Install and Launche on your server

**Как установить бот у себя на сервере?**


Inside running directory 

```bash

mkdir ytb2audiobot

cd ytb2audiobot

python3 -m venv venv

source venv/bin/activate

```


Telegram token paste

nano .env

```bash

TG_TOKEN_p='*** YOUR TELEGRAM TOKEN FROM BOT FATHER ***'
```

Run in production mode 

Redirects all outputs to void 
(stderr to stdout and stdout to /dev/null)

```bash

ytb2audiobot > /dev/null 2>&1

```

Run with in dev mode with log

Show all std in terminal and save it to stdout.log file.

```bash

ytb2audiobot | tee -a stdout.log

```

### 🤿 Техническая информация

- Файлы скачиваются в папку datadir. Она создается в tempdir оперционной системы, а в текущей папке создается symlink для macos.

   data-ytb2audiobot -> /var/folders/vd/_ygl4klj7cq01t8crn22rw7c0000gn/T/pip-ytb2audiobot-data




## 🏂 Todo

- Очереди для избежания flood youtube
- 































