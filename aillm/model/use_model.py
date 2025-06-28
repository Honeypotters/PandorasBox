from transformers import pipeline

from transformers import AutoModel

model_name = "model/trained_models"
model = AutoModel.from_pretrained(model_name)

generator = pipeline("text-generation", model)
generator(
    ""
)