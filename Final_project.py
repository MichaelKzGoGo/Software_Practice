import cv2
import telebot
import time


class Detector():
    def __init__(self):
        pass
    def is_cloud_exist(self, input_video):
        _, frame = input_video.read()
        cv2.imshow('Video_input', frame)
        cv2.waitKey(1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        threshold_value = 150
        _, binary = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

        num_white_pixels = cv2.countNonZero(binary)
        total_pixels = binary.shape[0] * binary.shape[1]
        white_pixel_percentage = num_white_pixels / total_pixels

        return white_pixel_percentage

class Sender():
    def __init__(self, bot, chat_id):
        self.bot = bot
        self.chat_id = chat_id

    def send_message(self, message):
        self.bot.send_message(chat_id=self.chat_id, text=message)


class Application():
    def __init__(self, input_video, bot_token, chat_id):
        self.input_video = input_video
        self.bot = telebot.TeleBot(bot_token)
        self.sender = Sender(self.bot, chat_id)
        self.detector = Detector()

    def run(self):
        while True:
            white_pixel_percentage = self.detector.is_cloud_exist(self.input_video)

            if white_pixel_percentage > 0.2:
                message = "There are clouds in the sky!"
            else:
                message = "There are no clouds in the sky!"

            self.sender.send_message(message)


if __name__ == "__main__":
    bot_token = "Insert Your Token Here"
    chat_id = "Insert Your Chat ID here"
    input_video = cv2.VideoCapture(0)

    app = Application(input_video, bot_token, chat_id)
    app.run()