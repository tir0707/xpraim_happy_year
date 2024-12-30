import time
import threading
from datetime import datetime, timedelta
import telebot
from config import API_TOKEN, CHANNEL_ID, TIMER_DURATION, FINAL_MESSAGE, TIMER_DESCRIPTION

class TimerBot:
    def __init__(self, api_token, channel_id, timer_duration, final_message, timer_description):
        self.bot = telebot.TeleBot(api_token)
        self.channel_id = channel_id
        self.timer_duration = self.parse_duration(timer_duration)
        self.final_message = final_message
        self.timer_description = timer_description
        self.message_id = None

    def parse_duration(self, duration_str):
        """Парсинг строки времени в timedelta."""
        hours, minutes, seconds = map(int, duration_str.split(':'))
        return timedelta(hours=hours, minutes=minutes, seconds=seconds)

    def start_timer(self):
        """Запуск таймера и отправка сообщений в канал."""
        end_time = datetime.now() + self.timer_duration
        remaining_time = self.timer_duration

        # Первоначальная отправка сообщения
        sent_message = self.bot.send_message(
            self.channel_id,
            f'{self.timer_description}\n                                 Осталось: {str(remaining_time).split()[0]}'
        )
        self.message_id = sent_message.message_id

        while remaining_time.total_seconds() > 0:
            time.sleep(5)  # Задержка в 5 секунд
            remaining_time = end_time - datetime.now()
            time_str = str(remaining_time).split('.')[0]  # Убираем миллисекунды

            try:
                # Обновление сообщения
                self.bot.edit_message_text(
                    chat_id=self.channel_id,
                    message_id=self.message_id,
                    text=f'{self.timer_description}\n                          Осталось: {time_str}'
                )
            except Exception as e:
                print(f'Ошибка обновления сообщения: {e}')

        # Отправляем финальное сообщение
        self.bot.send_message(self.channel_id, self.final_message)

    def run(self):
        """Метод для запуска таймера в отдельном потоке."""
        thread = threading.Thread(target=self.start_timer)
        thread.start()

if __name__ == '__main__':
    timer_bot = TimerBot(
        API_TOKEN, CHANNEL_ID, TIMER_DURATION, FINAL_MESSAGE, TIMER_DESCRIPTION
    )
    timer_bot.run()
