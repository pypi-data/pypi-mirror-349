import random
import time
from enum import Enum
from DrissionPage._pages.mix_tab import MixTab
from DrissionPage.common import Keys
from .utils import clipboard as cb
from typing import List
import loguru

class ActionsConfig:
    def __init__(self, action_speed_ratio = 1, get_need_wait = None):
        self.action_speed_ratio = action_speed_ratio
        self.get_need_wait = get_need_wait

default_config = ActionsConfig()

# 最后的bool表示是否应用action_speed_ratio
class SleepTime(Enum):
    MOUSE_RELEASE = (0.1, 0.2, False)
    KEY_RELEASE = (0.1, 0.15, False)
    KEY_DOWN = (0.15, 0.25, False)
    HUMAN_THINK = (0.2, 2, True)
    WAIT_PAGE = (1, 1.5, True)
    NONE_OPERATION = (1, 5, True)
    DELETE_TEXT = (5, 10, True)

def sleep(sleep_time: SleepTime, config: ActionsConfig):
    if sleep_time.value[2]:
        time.sleep(random.uniform(sleep_time.value[0], sleep_time.value[1]) * config.action_speed_ratio)
    else:
        time.sleep(random.uniform(sleep_time.value[0], sleep_time.value[1]))
        
def move_to(tab: MixTab, ele_or_loc, timeout=3, offset_x: float = 0, offset_y: float = 0, config: ActionsConfig = default_config):
    if config.get_need_wait and config.get_need_wait():
        while config.get_need_wait and config.get_need_wait():
            time.sleep(0.1)
    if not isinstance(ele_or_loc, (tuple, list)):
        ele_or_loc = tab.ele(ele_or_loc, timeout=timeout)
    act = tab.actions
    return act.move_to(ele_or_loc, offset_x=offset_x+random.randint(5, 7), offset_y=offset_y+random.randint(5, 7))

def click(tab: MixTab, ele_or_loc, more_real=True, act_click=False, timeout=3, offset_x: float = 0, offset_y: float = 0, config: ActionsConfig = default_config):
    if not isinstance(ele_or_loc, (tuple, list)):
        ele_or_loc = tab.ele(ele_or_loc, timeout=timeout)
    act = tab.actions
    if more_real:
        sleep(SleepTime.HUMAN_THINK, config=config)
    if more_real:
        if act_click:
            act.click(ele_or_loc, timeout=timeout)
        else:
            move_to(tab, ele_or_loc, offset_x=offset_x, offset_y=offset_y, config=config).hold()
            sleep(SleepTime.MOUSE_RELEASE, config=config)
            act.release()
    else:
        tab.ele(ele_or_loc, timeout=timeout).click()
        
    sleep(SleepTime.WAIT_PAGE, config=config)
    
def hold(tab: MixTab, ele_or_loc, more_real=True, act_click=False, timeout=3, offset_x: float = 0, offset_y: float = 0, config: ActionsConfig = default_config):
    if not isinstance(ele_or_loc, (tuple, list)):
        ele_or_loc = tab.ele(ele_or_loc, timeout=timeout)
    act = tab.actions
    if more_real:
        sleep(SleepTime.HUMAN_THINK, config=config)
    if act_click:
        act.hold(ele_or_loc)
    else:
        move_to(tab, ele_or_loc, offset_x=offset_x, offset_y=offset_y, config=config).hold()
        
    sleep(SleepTime.WAIT_PAGE, config=config)
    
def release(tab: MixTab, config: ActionsConfig = default_config):
    act = tab.actions
    act.release()
    sleep(SleepTime.WAIT_PAGE, config=config)

def type_message_to_shift_and_enter(message: str):
    tem_messages = message.split('\n')
    messages = []
    shift_and_enter = (Keys.SHIFT, Keys.ENTER)
    for message in tem_messages:
        messages.append(message)
        messages.append(shift_and_enter)
    return messages

def _get_ele_text(tab: MixTab, ele_or_loc, timeout=3):
    text = tab.ele(ele_or_loc, timeout=timeout).text
    if not text:
        text = tab.ele(ele_or_loc, timeout=timeout).value
    return text

def type(tab: MixTab, ele_or_loc, message: str, more_real=True, timeout=3, config=default_config, assist_ele=None):
    act = tab.actions
    sleep(SleepTime.HUMAN_THINK, config=config)
    if not message:
        return
    
    if ele_or_loc and not isinstance(ele_or_loc, (tuple, list)):
        ele_or_loc = tab.ele(ele_or_loc, timeout=timeout)
    if more_real:
        if ele_or_loc:
            click(tab, ele_or_loc, timeout=timeout, config=config, more_real=more_real)
        _paste(tab, message, config=config)
        if not assist_ele:
            assist_ele = ele_or_loc
        if assist_ele and not isinstance(assist_ele, (tuple, list)):
            text = _get_ele_text(tab, assist_ele, timeout=timeout)
            if len(text) == 0:
                _paste(tab, message, config=config)
                text = _get_ele_text(tab, assist_ele, timeout=timeout)
                if len(text) == 0:
                    raise ValueError(f"输入框内容不一致，输入内容：{message}，实际内容：{text}")
        else:
            # 避免末尾回车触发发送
            if not ele_or_loc:
                act.type(message.rstrip())
            else:
                tab.ele(ele_or_loc, timeout=timeout).input(message.rstrip())
        
    sleep(SleepTime.WAIT_PAGE, config=config)
    
def _paste(tab: MixTab, message, config=default_config):
    act = tab.actions
    for i in range(3):
        try:
            tab.actions.key_down(Keys.CTRL)
            sleep(SleepTime.KEY_DOWN, config=config)
            tab.actions.key_down('a')
            sleep(SleepTime.KEY_RELEASE, config=config)
            tab.actions.key_up('a')
            sleep(SleepTime.KEY_RELEASE, config=config)
            tab.actions.key_up(Keys.CTRL)
            data = cb.save_clipboard()
            # 避免末尾回车触发发送
            cb.set_clipboard(message.rstrip())
            tab.actions.key_down(Keys.CTRL)
            sleep(SleepTime.KEY_DOWN, config=config)
            tab.actions.key_down('v')
            sleep(SleepTime.KEY_RELEASE, config=config)
            tab.actions.key_up('v')
            sleep(SleepTime.KEY_RELEASE, config=config)
            tab.actions.key_up(Keys.CTRL)
            cb.restore_clipboard(data)
            break
        except Exception as e:
            loguru.logger.exception(e)
            
    
def type_and_send(tab: MixTab, ele_or_loc, messages: List[str], more_real=True, timeout=3, config=default_config, assist_ele=None):
    act = tab.actions
    sleep(SleepTime.HUMAN_THINK, config=config)
    first=False
    # 没有指定元素，则直接模拟键盘输入
    if ele_or_loc and not isinstance(ele_or_loc, (tuple, list)):
        ele_or_loc = tab.ele(ele_or_loc, timeout=timeout)
    if more_real:
        if ele_or_loc:
            click(tab, ele_or_loc, timeout=timeout, config=config, more_real=more_real)
    for message in messages:
        if not message:
            continue
        if more_real:
            if not first:
                first=True
            _paste(tab, message, config=config)
        else:
            # 避免末尾回车触发发送
            if not ele_or_loc:
                act.type(message.rstrip())
            else:
                tab.ele(ele_or_loc, timeout=timeout).input(message.rstrip())

        sleep(SleepTime.WAIT_PAGE, config=config)
        if not assist_ele:
            assist_ele = ele_or_loc
        if assist_ele and not isinstance(assist_ele, (tuple, list)):
            text = _get_ele_text(tab, assist_ele, timeout=timeout)
            if len(text) == 0:
                _paste(tab, message, config=config)
                text = _get_ele_text(tab, assist_ele, timeout=timeout)
                if len(text) == 0:
                    raise ValueError(f"输入框内容不一致，输入内容：{message}，实际内容：{text}")
        send_key(tab, Keys.ENTER, config=config)

def send_key(tab: MixTab, key: Keys, config: ActionsConfig = default_config):
    act = tab.actions
    act.key_down(key)
    sleep(SleepTime.KEY_RELEASE, config=config)
    act.key_up(key)
    sleep(SleepTime.WAIT_PAGE, config=config)

def scroll(tab: MixTab, ele_or_loc, delta_y, delta_x, timeout=3, config: ActionsConfig = default_config):
    if not isinstance(ele_or_loc, (tuple, list)):
        ele_or_loc = tab.ele(ele_or_loc, timeout=timeout)
    act = tab.actions
    move_to(tab,ele_or_loc, config=config)
    act.scroll(delta_y, delta_x)

def simulated_human(tab: MixTab, config: ActionsConfig = default_config):
    try:
        act = tab.actions
        # 1. 随机移动鼠标
        width, height = tab.rect.size
        x = random.randint(0, width)
        y = random.randint(0, height)
        act.move_to((x, y))
        
        # 模拟人类在移动完鼠标后略作停顿
        sleep(SleepTime.HUMAN_THINK, config=config)

        # 2. 随机决定是否进行滚轮滚动
        if random.random() < 0.6:  # 60% 的概率进行滚动操作
            # 滚动距离可以是向上或向下
            # delta_y 向下滚动为正，向上滚动为负
            delta_y = random.randint(-300, 300)  
            # 如果需要横向滚动，可设置 delta_x
            delta_x = 0  

            act.scroll(delta_y=delta_y, delta_x=delta_x)

            # 停顿一小段时间，模拟卷动后的停顿或浏览
            sleep(SleepTime.HUMAN_THINK, config=config)

        # 3. 随机等待，模拟人与人差异
        sleep(SleepTime.NONE_OPERATION, config=config)
    except Exception:
        pass
