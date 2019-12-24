import time

import boto3 as boto3
import cv2
import re

access_key = 'AKIASKQ2RR3OEGEJUSMO'
secrete_key = '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'

client = boto3.client('textract', aws_access_key_id=access_key, aws_secret_access_key=secrete_key)

previous_text = ''

while True:
    for i in range(1, 13):
        image = 'images/{}.jpeg'.format(str(i))
        with open(image, 'rb') as f:  # open the file in read binary mode
            data = f.read()

        response = client.detect_document_text(
            Document={
                'Bytes': data
            }
        )
        for block in response.get('Blocks'):
            if 'Text' in block:
                text = block.get('Text')
                if '-' in text:
                    if (re.match(r'\d{2,3}\-\d{2,3}\-\d{2,3}', text) is None\
                            and re.match(r'\d{2,3}:\d{2,3}\-\d{2,3}', text) is None)\
                            or previous_text == text:
                        continue
                    previous_text = text
                    img = cv2.imread(image)
                    width = block.get('Geometry').get('BoundingBox').get('Width')
                    height = block.get('Geometry').get('BoundingBox').get('Height')
                    left = block.get('Geometry').get('BoundingBox').get('Left')
                    top = block.get('Geometry').get('BoundingBox').get('Top')

                    im_height, im_width, channels = img.shape

                    face_width = int(width * im_width)
                    face_height = int(height * im_height)
                    face_left_position = int(left * im_width)
                    face_top_position = int(top * im_height)

                    img = cv2.rectangle(img, (face_left_position, face_top_position),
                                        (face_left_position + face_width, face_height + face_top_position),
                                        (147, 112, 219), 5)

                    font = cv2.FONT_HERSHEY_SIMPLEX
                    bottomLeftCornerOfText = (10, 100)
                    fontScale = 2
                    fontColor = (255, 0, 0)
                    lineType = 2

                    cv2.putText(img, text.replace(':', '-'),
                                bottomLeftCornerOfText,
                                font,
                                fontScale,
                                fontColor,
                                lineType)

                    cv2.namedWindow('window', cv2.WINDOW_NORMAL)
                    cv2.imshow("window", img)
                    cv2.resizeWindow('window', 2000, 1000)
                    cv2.moveWindow('window', 200, 200)
                    cv2.waitKey(1)
                    print(i)
                    print(text)
    time.sleep(10)

