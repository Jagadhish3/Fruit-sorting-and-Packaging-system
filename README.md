# 🍎 Autonomous Fruit Sorting and Packaging System

This project presents a deep learning-based fruit classification system using **InceptionV3** for image recognition. The model identifies fruit types from images and provides predictions via a simple web interface. It is developed using **TensorFlow**, **Keras**, and **OpenCV**, and trained on a custom dataset derived from the Fruit 360 dataset.

---

## 🧠 Key Features

- Fruit classification using **CNN (Convolutional Neural Networks)**
- Uses **InceptionV3 with Transfer Learning** for high accuracy
- Achieves **90.14% validation accuracy**
- Simple and interactive **web interface** for prediction
- Trained on 10 fruit types including *apple, banana, cherry, chickoo, grapes, kiwi, mango, orange, strawberry, mixed*

---

## 🛠️ Tech Stack

- Python
- TensorFlow / Keras
- OpenCV
- Jupyter Notebook
- HTML / CSS (for web interface)
- Git LFS (for storing `.h5` model files over 100MB)

---

## 📁 Dataset

- Sourced from **Fruit 360 Dataset**
- Images include different backgrounds, lighting, angles
- Preprocessed with:
  - Normalization (0-1 pixel scaling)
  - Data augmentation (rotation, flipping, brightness)
  - Resizing to 224x224 px

---

## 🧪 Model Architecture

- **Input:** 224x224x3 RGB images
- **Base Model:** InceptionV3 (pre-trained on ImageNet)
- **Layers:**
  - Convolutional Layers
  - Inception Modules
  - Fully Connected Layers
  - Softmax Output (10 Classes)

---

## 📈 Performance

| Epoch | Train Acc | Valid Acc | Train Loss | Valid Loss |
|-------|-----------|-----------|------------|------------|
| 1     | 17.81%    | 73.24%    | 2.2461     | 1.2308     |
| 5     | 91.73%    | 87.32%    | 0.3996     | 0.3290     |
| 10    | 97.42%    | 90.14%    | 0.1328     | 0.2338     |

---

## 🌐 Web Deployment

A minimalistic web interface is created that allows users to:

- Upload an image of a fruit
- Get the predicted fruit type
- View results instantly

---

## 🚀 How to Run Locally

1. **Clone the Repo**
   ```bash
   git clone https://github.com/your-username/Fruit-Sorting_and-Packaging-System.git
   cd Fruit-Sorting_and-Packaging-System
