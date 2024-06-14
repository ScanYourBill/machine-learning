import cv2
import json
import pytesseract
import pickle
import numpy as np
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences


# Custom config
myconfig = r"--psm 6 oem 3"

# Load the model
loaded_model = load_model('nlp_model\model_ave.h5')

# Load the tokenizer
with open('nlp_model\tokenizer_ave.pickle', 'rb') as handle:
    loaded_tokenizer = pickle.load(handle)

# Define the unique labels
unique_labels = ['Clothing', 'Food', 'Stationery', 'Others', 'Toiletries', 'Medical and Health Care', 'Entertainment']

# Load image
img = cv2.imread("data/receipt_47.jpg")
base_image = img.copy()

def predict_text(text):
    # Tokenize text
    sequence = loaded_tokenizer.texts_to_sequences([text])
    # Pad the sequence
    data = pad_sequences(sequence, maxlen=100)

    # Perform prediction
    prediction = loaded_model.predict(data)
    predicted_label = unique_labels[np.argmax(prediction)]

    return predicted_label


blur = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (7,7), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 22))
dilate = cv2.dilate(thresh, kernal, iterations=1)

cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])

for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    if y > 15 and w > 500:
        roi = base_image[y:y+h, x:x+w]
        cv2.rectangle(img, (x, y), (x+w, y+h), (36, 255, 12), 2)

ocr_result = pytesseract.image_to_string(roi, config=myconfig)
# cv2.imwrite("bbox.png", img) # check bounding box
# print(ocr_result) # check the ocr result

# Split the text into lines
lines = ocr_result.split('\n')

# Parse each line
items = []
for line in lines:
    # Remove leading and trailing whitespace
    line = line.strip()
    # Ignore empty lines
    if line:
        parts = line.split()
        # Check if this is a total line
        if parts[0] == 'Total:':
            totals = int(parts[1].replace(',', ''))
        else:
            name = ' '.join(parts[:-3])
            category = predict_text(name)
            quantity = int(parts[-3])
            price = int(parts[-2].replace(',', ''))
            total = int(parts[-1].replace(',', ''))
            items.append({"name": name, "category": category, "quantity": quantity, "price": price, "total": total})

# Prepare the data
data = {"items": items, "totals": totals}

# Write the data to a JSON file
with open('result.json', 'w') as f:
    json.dump(data, f)

print("Data has been written to result.json")