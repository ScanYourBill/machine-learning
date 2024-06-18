import cv2
import json
import pytesseract
import pickle
import numpy as np
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences


def process_receipt(image_path, model_path, tokenizer_path, output_json_path):
    """
    Process a receipt image, predict item categories using a pre-trained NLP model, and save the results to a JSON file.

    Args:
        image_path (str): Path to the receipt image file.
        model_path (str): Path to the pre-trained Keras model file.
        tokenizer_path (str): Path to the tokenizer pickle file.
        output_json_path (str): Path to the output JSON file to save the results.

    Raises:
        ValueError: If no suitable Region of Interest (ROI) is found in the image.
    """

    # Custom config for pytesseract
    myconfig = r"--psm 6 oem 3"

    # Load the pre-trained model
    loaded_model = load_model(model_path)

    # Load the tokenizer
    with open(tokenizer_path, "rb") as handle:
        loaded_tokenizer = pickle.load(handle)

    # Define the unique labels for classification
    unique_labels = [
        "Clothing",
        "Food",
        "Stationery",
        "Others",
        "Toiletries",
        "Medical and Health Care",
        "Entertainment",
    ]

    # Load the receipt image
    img = cv2.imread(image_path)
    base_image = img.copy()

    def predict_text(text):
        """
        Predict the category of the given text using the pre-trained NLP model.

        Args:
            text (str): The text to classify.

        Returns:
            str: The predicted category label.
        """
        # Tokenize the input text
        sequence = loaded_tokenizer.texts_to_sequences([text])
        # Pad the sequence to the required length
        data = pad_sequences(sequence, maxlen=100)
        # Perform prediction
        prediction = loaded_model.predict(data)
        # Get the predicted label
        predicted_label = unique_labels[np.argmax(prediction)]

        return predicted_label

    # Preprocess the image for OCR
    blur = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (7, 7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 22))
    dilate = cv2.dilate(thresh, kernal, iterations=1)

    # Find contours in the dilated image
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])

    # Extract the Region of Interest (ROI) containing the receipt text
    roi = None
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if y > 15 and w > 500:
            roi = base_image[y : y + h, x : x + w]
            cv2.rectangle(img, (x, y), (x + w, y + h), (36, 255, 12), 2)

    if roi is None:
        raise ValueError("No suitable ROI found in the image.")

    # Perform OCR on the ROI to extract text
    ocr_result = pytesseract.image_to_string(roi, config=myconfig)

    # Split the OCR result into lines
    lines = ocr_result.split("\n")

    # Parse each line to extract item details
    items = []
    totals = 0
    for line in lines:
        # Remove leading and trailing whitespace
        line = line.strip()
        # Ignore empty lines
        if line:
            parts = line.split()
            # Check if this is a total line
            if parts[0] == "Total:":
                totals = int(parts[1].replace(",", ""))
            else:
                # Extract item details
                name = " ".join(parts[:-3])
                category = predict_text(name)
                quantity = int(parts[-3])
                price = int(parts[-2].replace(",", ""))
                total = int(parts[-1].replace(",", ""))
                items.append(
                    {
                        "name": name,
                        "category": category,
                        "quantity": quantity,
                        "price": price,
                        "total": total,
                    }
                )

    # Prepare the data to be written to JSON
    data = {"items": items, "totals": totals}

    # Write the data to a JSON file
    with open(output_json_path, "w") as f:
        json.dump(data, f)

    print("Data has been written to", output_json_path)


# Usage example:
process_receipt(
    "data/receipt_09.jpg",
    "model/model.h5",
    "model/tokenizer.pickle",
    "data/ocr_result.json",
)
