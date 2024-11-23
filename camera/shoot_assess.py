import tensorflow as tf
from keras.preprocessing import image
import numpy as np
import subprocess

subprocess.Popen(['fswebcam', 'testimg.jpg'] ,stdout=subprocess.PIPE)


model = tf.keras.models.load_model('model/plant_disease_model.h5')

def preprocess_image(img_path, target_size=(150, 150)):

    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  
    img_array /= 255.0  
    return img_array

def predict_image_class(model, img_path):
    img_array = preprocess_image(img_path)
    predictions = model.predict(img_array)
    return predictions

# to be updated when the new model is ready; just for example and testing
def get_class_labels():

    return ['Alternaria Leaf Spot (Alternaria helianthi)',
'Anthracnose (Colletotrichum spp.)',
'Anthracnose (Elsinoe ampelina)',
'Anthracnose Leaf Blight (Colletotrichum graminicola)',
'apple scab',
'Bacterial Spot (Xanthomonas campestris pv. vesicatoria)',
'Bacterial Spot (Xanthomonas spp.)',
'Barley Yellow Dwarf Virus',
'Black Rot (Guignardia bidwellii)',
'Cercospora Leaf Spot (Cercospora capsici)',
'Charcoal Rot (Macrophomina phaseolina)',
'Common Rust (Puccinia sorghi)',
'Corn Smut (Ustilago maydis)',
'Crown Gall (Agrobacterium tumefaciens)',
'Downy Mildew (Plasmopara halstedii)',
'Downy Mildew (Plasmopara viticola)',
'Early Blight (Alternaria solani)',
'Fusarium Head Blight (Fusarium spp.)',
'Fusarium Wilt (Fusarium oxysporum f.sp. lycopersici)',
'Goss’s Wilt (Clavibacter michiganensis subsp. nebraskensis)',
'Grapevine Leafroll Disease',
'Gray Leaf Spot (Cercospora zeae-maydis)',
'Gray Mold (Botrytis cinerea)',
'Late Blight (Phytophthora infestans)',
'Leaf Rust (Puccinia hordei)',
'Leaf Rust (Puccinia triticina)',
'Leaf Scorch (Diplocarpon earlianum)',
'Leaf Spot (Mycosphaerella fragariae)',
'Loose Smut (Ustilago nuda)',
'Maize Dwarf Mosaic Virus',
'Net Blotch (Pyrenophora teres)',
'Northern Corn Leaf Blight (Exserohilum turcicum)',
'Pepper Mild Mottle Virus',
'Phomopsis Stem Canker (Phomopsis helianthi)',
'Phytophthora Blight (Phytophthora capsici)',
'Pierce\'s Disease (Xylella fastidiosa)',
'Powdery Mildew (Blumeria graminis f.sp. hordei)',
'Powdery Mildew (Blumeria graminis f.sp. tritici)',
'Powdery Mildew (Erysiphe necator)',
'Powdery Mildew (Leveillula taurica)',
'Powdery Mildew (Podosphaera aphanis)',
'Red Stele (Phytophthora fragariae)',
'Rust (Puccinia helianthi)',
'Scald (Rhynchosporium secalis)',
'Sclerotinia Stem Rot (Sclerotinia sclerotiorum)',
'Septoria Leaf Blotch (Zymoseptoria tritici)',
'Septoria Leaf Spot (Septoria lycopersici)',
'Southern Corn Leaf Blight (Bipolaris maydis)',
'Spot Blotch (Cochliobolus sativus)',
'Stem Rust (Puccinia graminis)',
'Strawberry Black Root Rot (Complex of various pathogens including Rhizoctonia spp. and Pythium spp.)',
'Stripe Rust (Puccinia striiformis)',
'Sunflower Mosaic Virus',
'Tan Spot (Pyrenophora tritici-repentis)',
'Tomato Mosaic Virus',
'Tomato Spotted Wilt Virus',
'Verticillium Wilt (Verticillium dahliae)',
'Wheat Streak Mosaic Virus',
]

def print_prediction(predictions, class_labels):
    predicted_class = np.argmax(predictions, axis=1)[0]
    print(f"Predicted Class: {class_labels[predicted_class]}")
    print(f"Prediction Probabilities: {predictions}")


img_path = 'testimg.jpg'
predictions = predict_image_class(model, img_path)
class_labels = get_class_labels()
print_prediction(predictions, class_labels)
