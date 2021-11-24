import torch
import numpy as np


def get_prediction(sentence, tokenizer, model):
    """
    Predicts a label based on a sentence
    ---------
    Input
    sentence: sentence to evaluate (string)
    -------
    Output
    out: label (string)
    """

    # Class names
    class_names = [
        "positive",
        "negative",
        "neutral",
    ]

    # Processing sentence
    encoded_dict = tokenizer.encode_plus(
        sentence,
        add_special_tokens=True,
        max_length=95,
        pad_to_max_length=True,
        return_attention_mask=True,
        return_tensors="pt",
    )
    input_ids = torch.cat([encoded_dict["input_ids"]], dim=0)
    attention_mask = torch.cat([encoded_dict["attention_mask"]], dim=0)

    # Predicting
    model.eval()
    with torch.no_grad():
        outputs = model(
            input_ids, token_type_ids=None, attention_mask=attention_mask
        )
    preds = outputs.logits.numpy()
    index = np.argmax(preds[0])
    out = class_names[index]

    return out
