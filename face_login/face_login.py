# -*- coding: utf-8 -*-
# 摄像头头像识别
import face_recognition
import cv2
from tqdm import tqdm
import time

video_capture = cv2.VideoCapture(1)
# 本地图像
print("正在读取人脸数据...")
zwz_image = face_recognition.load_image_file("zwz.jpg")
zwz_face_encoding = face_recognition.face_encodings(zwz_image)[0]
known_face_encodings = [zwz_face_encoding]
known_face_names = ["Zhouwenzhang"]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


def login_username():
    print("请输入用户名：")
    username = input()
    if username == 'zwz':
        print("正在启动识别组件...")
    else:
        print("用户未注册")


def recognition():
    while True:
        # 读取摄像头画面
        ret, frame = video_capture.read()
        # 改变摄像头图像的大小，图像小，所做的计算就少
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # opencv的图像是BGR格式的，而我们需要是的RGB格式的，因此需要进行一个转换。
        rgb_small_frame = small_frame[:, :, ::-1]
        if process_this_frame:
            # 根据encoding来判断是不是同一个人，是就输出true，不是为flase
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # 默认为unknown
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                face_names.append(name)
    # 将捕捉到的人脸显示出来
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # 矩形框
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # 加上标签
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            if face_names[0] == "Zhouwenzhang":
                for i in tqdm(range(0, 100)):
                    time.sleep(0.01)
                print('')
                print("Zhouwenzhang")
                time.sleep(1)
                video_capture.release()
                cv2.destroyAllWindows()
                return "Log in"
        # Display
        cv2.imshow('Recognition', frame)

        # 按Q退出
        if cv2.waitKey(1) & 0xFF == ord('Q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    login_username()
    print(recognition())