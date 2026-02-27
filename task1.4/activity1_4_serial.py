'''
To install face_recognition, simply use 'pip install face_recognition' in a terminal
However, often you may meet an error about the 'dlib' library with cmake.
The easy solution is to visit https://github.com/z-mahmud22/Dlib_Windows_Python3.x and download the 
compiled wheels locally with the python version, and install it from local

if you want to show the found image with the known face, you need opencv and also uncomment the related code.
'''

import cv2  
import time
import face_recognition  
import os
import concurrent.futures

def show_found_image(image_path, face_location):
    """
    Loads the image via OpenCV and draws the bounding box.
    This MUST be run in the main process, not the background workers.
    """
    # cv2 reads in BGR format automatically
    img = cv2.imread(image_path)
    if img is None:
        print(f"Warning: could not load image for display: {image_path}")
        return

    top, right, bottom, left = face_location
    cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)

    cv2.imshow(f"Match Found: {os.path.basename(image_path)}", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def process_single_image(args):
    """
    The background worker function. Each CPU core runs this independently.
    Returns: (filename, is_match, full_path, matched_location)
    """
    filename, folder_path, known_encoding = args
    full_path = os.path.join(folder_path, filename)
    
    try:
        # Load the unknown face image
        unknown_image = face_recognition.load_image_file(full_path)

        # OPTIMIZATION: Get locations first, then pass them into encodings.
        # This prevents the library from running the heavy detection math twice!
        # upsample_num_times=0 skips image upscaling for significantly faster detection.
        face_locations = face_recognition.face_locations(unknown_image, upsample_num_times=0)
        # model="small" uses a faster 5-point landmark model vs the default 68-point model.
        unknown_encodings = face_recognition.face_encodings(unknown_image, known_face_locations=face_locations, model="small")

        for i, unknown_encoding in enumerate(unknown_encodings):
            # Compare the unknown face encoding with the known encoding
            matches = face_recognition.compare_faces([known_encoding], unknown_encoding)

            if matches[0]:  # If a match is found
                # Return True and the specific coordinates of the matching face
                return (filename, True, full_path, face_locations[i])
                
        return (filename, False, full_path, None)
    except Exception as e:
        # Failsafe for corrupted images
        return (filename, False, full_path, None)


def main():
    start = time.time()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load the known face image and get the features of the face
    known_path = os.path.join(script_dir, "known_man.jpg")
    known_image = face_recognition.load_image_file(known_path)
    known_encoding = face_recognition.face_encodings(known_image)[0]

    folder_path = os.path.join(script_dir, "imageset")
    
    # Only grab actual image files to prevent crashing on hidden OS files (like .DS_Store)
    filenames = [file.name for file in os.scandir(folder_path) 
                 if file.is_file() and file.name.lower().endswith('.jpg')]

    # Package the arguments for the workers
    tasks = [(filename, folder_path, known_encoding) for filename in filenames]

    print(f"Starting parallel scan of {len(tasks)} images...")

    # THE PARALLEL PROCESS POOL
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # as_completed yields results exactly as they finish, rather than waiting for all of them
        futures = {executor.submit(process_single_image, task): task for task in tasks}
        
        for future in concurrent.futures.as_completed(futures):
            filename, is_match, full_path, matched_location = future.result()
            
            if is_match:
                print("Match found! in " + filename)
                # Cancel all pending futures — no need to keep scanning
                for pending in futures:
                    pending.cancel()
                # Display the image in the main thread
                show_found_image(full_path, matched_location)
                break

    print(f"Total time: {time.time()-start:.2f} seconds")


if __name__ == '__main__':
    main()