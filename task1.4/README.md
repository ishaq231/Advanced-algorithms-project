# Task 1.4 – Parallel Face Recognition

## Setup

### 1. Install dlib (required before face_recognition)

`face_recognition` depends on `dlib`, which needs to be compiled. On Windows this often fails.
Use the pre-compiled wheels instead:

1. Download the `.whl` for your Python version from [z-mahmud22/Dlib_Windows_Python3.x](https://github.com/z-mahmud22/Dlib_Windows_Python3.x)
2. Install it:
   ```
   pip install dlib-<version>-cpXX-cpXX-win_amd64.whl
   ```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

```bash
python activity1_4_serial.py
```

The script scans all images in the `imageset/` folder and prints the filename when a match is found.
