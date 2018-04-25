## colorlog

This is the demo to use the color log.

### Log Format
实际上, 只有Console是支持颜色的，之前我提到过终端中颜色的原理[Text Color Of Console](https://bearfly1990.github.io/2018/04/21/ColorfulConsole/)。
这个库就是在输出到终端的时候，前后加了转义序列ESC(e.g.`"\033[1;35;40m 高亮洋红背景黑 \033[0m"`)
我在这个demo中顺便加入了输出log到文件的简单用法。
```python
LOG_FORMAT_CONSOLE = "%(log_color)s%(asctime)s [%(levelname)-5.5s] %(message)s"
LOG_FORMAT_FILE = "%(asctime)s [%(levelname)-5.5s] %(message)s"
```
从上面的代码可以看出来，为了使用自定义颜色，需要在format string中加入`%(log_color)s`。

### ColoredFormatter
这个是关键的一个类，从`colorlog`[源码](https://github.com/borntyping/python-colorlog/blob/master/colorlog/colorlog.py)
中可以看到，它是继承自`logging.Formatter`，封装了自己的实现。
```python
class ColoredFormatter(logging.Formatter):
   # 略...
   def format(self, record):
        # 略...
        # Add a reset code to the end of the message
        # (if it wasn't explicitly added in format str)
        if self.reset and not message.endswith(escape_codes['reset']):
            message += escape_codes['reset']
```
如果要使用默认的颜色等设置，直接`formatter = ColoredFormatter(LOG_FORMAT_CONSOLE)`就可以。
而如果要更多地设置，可以使用如下的方式，从下面的[源码](https://github.com/borntyping/python-colorlog/blob/master/colorlog/escape_codes.py)里
可以看到，它支持8种颜色，挑个自己喜欢的，觉得不好的当然也可以改源码，加入自己的颜色。

当然，它也支持改变背景色，只要加上`bg_`,而如果想要高亮的话，可以加前缀`bold_`，尽情试一下。
```python
# The color names
COLORS = [
    'black',
    'red',
    'green',
    'yellow',
    'blue',
    'purple',
    'cyan',
    'white'
]

PREFIXES = [
    # Foreground without prefix
    ('3', ''), ('01;3', 'bold_'), ('02;3', 'thin_'),

    # Foreground with fg_ prefix
    ('3', 'fg_'), ('01;3', 'fg_bold_'), ('02;3', 'fg_thin_'),

    # Background with bg_ prefix - bold/light works differently
    ('4', 'bg_'), ('10', 'bg_bold_'),
]
```
这个是我目前使用的配色，参考下：
```python
formatter_console = ColoredFormatter(
	LOG_FORMAT_CONSOLE,
	datefmt=None,
	reset=True,
	log_colors={
		'DEBUG':    'cyan',
		'INFO':     'green',
		'WARNING':  'bold_yellow',
		'ERROR':    'bold_red',
		'CRITICAL': 'bold_red,bg_white',
	},
	secondary_log_colors={},
	style='%'
)
```
### 其他设置
其实上边讲完，剩下的就是使用logging的常规方式，可以在demo里看到：
```python
formatter_file = logging.Formatter(LOG_FORMAT_FILE)

handler_stream = logging.StreamHandler()
handler_stream.setLevel(LOG_LEVEL)
handler_stream.setFormatter(formatter_console)

handler_file = logging.FileHandler("colorlog.log")
handler_file.setLevel(LOG_LEVEL)
handler_file.setFormatter(formatter_file)

log = logging.getLogger(__name__)
log.setLevel(LOG_LEVEL)
# set file and console hander to log
log.addHandler(handler_stream)
log.addHandler(handler_file)

log.debug("A quirky message only developers care about")
log.info("Curious users might want to know this")
log.warn("Something is wrong and any user should be informed")
log.error("Serious stuff, this is red for a reason")
log.critical("OH NO everything is on fire")
```

源码地址:[colorlog](https://github.com/borntyping/python-colorlog)






