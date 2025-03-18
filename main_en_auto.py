import json
import cv2
from skimage.metrics import structural_similarity as ssim
import shutil
import pandas as pd

from core.process_img_script import process_img
from core.command_operator import *
from core.LLm_history import Global_LLm_history, language, gpt_choice
from core.screenshot_translator import ScreenshotTranslator
from core.LLM_api import use_LLM
from core.help_seq_getter import help_get_flag, help_seq_get
from core.Config import *
import logging
logging.disable(logging.DEBUG)
logging.disable(logging.WARNING)

taskdf = pd.read_excel(TaskTable_PATH, keep_default_na=False)
input_ProcessImgModel = True
if input_ProcessImgModel:
    # Import models, only once at startup
    import core.import_models as import_models
    model_ver, model_det, model_cls, preprocess, ocr = import_models.import_all_models \
        (alg,
            # model_path_yolo='pt_model/yolo_s_best.pt',
            accurate_ocr = accurate_ocr,
            model_path_yolo='pt_model/yolo_mdl.pt',
            model_path_vins_dir='pt_model/yolo_vins_',
            model_ver='14',
            model_path_vins_file='_mdl.pt',
            model_path_cls='pt_model/clip_mdl.pth'
            )


def are_images_similar(save_path_old, save_path_new, threshold=0.90, threshold_roi=0.97, roi=None): # Image similarity threshold 
    
    img1 = cv2.imread(save_path_old) # Read image
    img2 = cv2.imread(save_path_new)

    # Check if dimensions are different
    if img1.shape != img2.shape:
        shutil.copy(save_path_new, save_path_old)
        return False  # Indicates the image has been updated
    
    if roi is not None:
        x, y, w, h = roi
        img1_roi = img1[y:y + h, x:x + w]
        img2_roi = img2[y:y + h, x:x + w]
        gray_img1_roi = cv2.cvtColor(img1_roi, cv2.COLOR_BGR2GRAY)
        gray_img2_roi = cv2.cvtColor(img2_roi, cv2.COLOR_BGR2GRAY)
        similarity_index_roi, _ = ssim(gray_img1_roi, gray_img2_roi, full=True)
    else:
        similarity_index_roi = 1

    gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
  
    similarity_index, _ = ssim(gray_img1, gray_img2, full=True)
    shutil.copy(save_path_new, save_path_old)
    return similarity_index > threshold and similarity_index_roi > threshold_roi

def eleLoc_2_roi(element_location): # element_location = {'left': 42, 'right': 838, 'top': 2036, 'bottom': 2185}
    roi = (
        element_location['left'] - 10,
        element_location['top'] - 10 ,
        element_location['right'] - element_location['left'] + 30,
        element_location['bottom'] - element_location['top'] + 30
    )
    return roi

def client_main():
    
    # Initialization
    global task_str
    global tapped_button_str
    global invalid_button_str
    global taped_element_content
    global taped_element_roi
    global default_reason
    
    shutil.copy(save_path_default, save_path_old)
    first_flag = True
    task_str = ""
    default_reason = ""
    invalid_button_str = [""]
    taped_element_content = ""
    taped_element_roi = None
    tapped_button_str = ["，now the operations performed are"]


    print("\n*--------------------------------- START --------------------------------------*")

    message = "Q：" + input("🥰: Hi, I'm VisionTasker. What can I do for you~")  # Go to Alipay to analyze my spending in annual

    # message = "Q：" + message
    if message.startswith("Q"):  # Process messages starting with "Q"
        task_str = str(message)
        task_str = task_str.split('Q：')[-1]
        print("👂 User:", task_str)
        response = "🧐: OK, let me help you 👌"
        print(response)

        # If you enter m again, reset all information for this task
        if len(tapped_button_str) > 1:
            print("Enter the task content again, and the operation record is available, reset the task, please return to the initial interface")
            shutil.copy(save_path_default, save_path_old)
            default_reason = ""
            invalid_button_str = [""]
            taped_element_content = ""
            taped_element_roi = None
            tapped_button_str = ["，now the operations performed are"]
            Global_LLm_history.__init__(language, gpt_choice)
            # Get help document information based on task content
        if not help_get_flag:
            help_str = ''
        else:
            help_question, help_content = help_seq_get(task_str)
            help_str = f"Help document information for this task: {help_question} {help_content}" if help_question and help_content else ''
            print(help_str)

    else:
        # Process other messages
        print("Received a different message")

    
    try:
        while True:
            time.sleep(5)
            if not first_flag:
                print('🧐: Move on!')
            first_flag = False
            print("\n*---------------------- SCREEN UNDERSTANDING ---------------------------*")
            # Screenshot or long screenshot
            if longscreenshot_flag:
                capture_longscreenshot(save_path_new)
            else:
                capture_screenshot(save_path_new)

            print('🧐: Hmmm, I can watch your screen now...')
            # Determine the clickability of the last clicked control based on whether the image is updated (not updated means not clickable)
            screenshot_update_flag = not(are_images_similar(save_path_old, save_path_new, roi = taped_element_roi))
            if (not screenshot_update_flag) and taped_element_content != '' and not default_reason: # Image not updated + not after sending m + not during the process where the element does not exist or the response format is incorrect
                tapped_button_str.pop()  # Remove the last clicked control information
                # Remove the last input and output information from llm
                Global_LLm_history.clear_previous_one_record()
                Global_LLm_history.clear_previous_one_record()

                invalid_button_str.append(f"['{taped_element_content}']")  # Record this invalid button
            else:
                invalid_button_str = ['']  # Reset invalid control list
            print('🧐: OK, let me take a closer look......')
            result_js = process_img(label_path_dir, save_path_old, output_root, layout_json_dir, high_conf_flag,
                        alg, clean_save, plot_show, ocr_save_flag, model_ver, model_det, 
                        model_cls, preprocess, pd_free_ocr=ocr, ocr_only=ocr_output_only, lang=language, accurate_ocr=accurate_ocr)


            # Save json file
            json.dump(result_js, open(SCREEN_jSON_PATH, 'w', encoding='utf-8'), indent=4, ensure_ascii=False)

            # Convert screen information json file to readable string
            print('🧐: Haha, time for LLM!')
            print("\n*--------------------------- TASK PLANNING -----------------------------*")

            ScreenshotTranslatorTest = ScreenshotTranslator(SCREEN_jSON_PATH)
            humanword = ScreenshotTranslatorTest.json2humanword()

            # Tips for llm
            if len(invalid_button_str) == 1:  # =1 means initial, no invalid controls
                invalid_button_string = '。'
                if default_reason.startswith("The interface does not exist"):
                    invalid_button_string = f"。Note {default_reason}。"
                    default_reason = ""
            else: # There are invalid controls, i.e., non-clickable controls
                invalid_button_string = ''.join(map(str, invalid_button_str)) # Invalid control reminder
                invalid_button_string = f"。Note that control {invalid_button_string} is not clickable。"
                if default_reason.startswith("The interface does not exist"):
                    invalid_button_string = f"。Note that control {invalid_button_string} is not clickable, {default_reason}。"
                    default_reason = ""

            # Integrate the information to be sent to llm
            if len(tapped_button_str) == 1: # =1 means initial, no controls clicked
                object_message_humanword = f'Q：{task_str}，{help_str}The current interface has the following buttons: {humanword}{invalid_button_string}'
            else:
                tapped_button_string = ''.join(map(str, tapped_button_str))
                object_message_humanword = f'Q：{task_str}{tapped_button_string}，{help_str}The current interface has the following buttons: {humanword}{invalid_button_string}'
            print(object_message_humanword)

            object_message_humanword = json.dumps(object_message_humanword)
            order_list = use_LLM(gpt_choice, object_message_humanword)


            for order in order_list:
                if order['action'] != 'default':  # llm returns a valid command
                    # If the control clicked this time is different from the last time, this time is valid
                    if taped_element_content != order['button_content']:
                        taped_element_content = order['button_content'] # Clicked control content
                        taped_element_roi = eleLoc_2_roi(order['element_location']) # Clicked location

                        # Record operation history
                        if order['action'] == 'keyboard_input':
                            input_text_content = order['data']['input_text']
                            tapped_button_str.append(f'(Entered {repr(input_text_content)} in the input box: [{repr(taped_element_content)}] and pressed Enter)')
                        elif order['action'] == 'tap':
                            tapped_button_str.append(f'(Clicked [{repr(taped_element_content)}])')
                else:
                    default_reason = order['reason']
                    print("Please send the screenshot again and GPT will regenerate the operation command")

            response = json.dumps(order_list, ensure_ascii=False)  # Convert order_list to JSON format

            print(f"Execute: {response}")  # Process the message and generate a reply
            response = eval(response)


            if isinstance(response, str):
                # print("response is a string type")
                pass
            elif isinstance(response, list):
                order_list = response
                operator(order_list)  # Pass each operation in the order_list returned by the server
                print("\n*---------------------------- √ ONE STEP COMPLETED ----------------------------*\n\n\n")

            else:
                print("response is another type")
                
        
    finally:
        print(f"client_main encountered an exception")


if __name__ == "__main__":

    client_main()
